"""
Creates a new CMU from api.dictionaryapi.dev. Is able to stop and pick up again.
Checks the most recent entry in the JSON and then starts up again from that point
in the frequency list, adding the next <number> words.

Pulls from frequency list general_english_100k.txt.
Adds spellings to new_cmu.json.

Usage:
python generate_new_cmu.py <number>
<number> is the number of words to add.
"""
import requests
import re
import json
import sys
import os
import time
from phonecodes import phonecodes

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ARPABET_PHONEMES = sorted([
    'AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'EH', 'ER', 'EY', 'IH', 'IY', 'OW', 'OY', 'UH', 'UW',
    'B', 'CH', 'D', 'DH', 'F', 'G', 'HH', 'JH', 'K', 'L', 'M', 'N', 'NG', 'P', 'R', 'S', 'SH', 
    'T', 'TH', 'V', 'W', 'Y', 'Z', 'ZH'
], key=len, reverse=True)

PHONEME_PATTERN = re.compile(fr"({'|'.join(ARPABET_PHONEMES)})(\d)?")

def get_all_ipa(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    ipa_variants = set()
    try:
        # Added a 0.3 second delay before the request to prevent 429 errors
        time.sleep(0.5)
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            for entry in data:
                if 'phonetic' in entry:
                    ipa_variants.add(entry['phonetic'].strip('/'))
                for p in entry.get('phonetics', []):
                    if 'text' in p and p['text']:
                        ipa_variants.add(p['text'].strip('/'))
        elif response.status_code == 404:
            return []
        elif response.status_code == 429:
            print(f"\n[!] Rate Limited (429). Cooling down for 5 seconds...")
            time.sleep(5)
            return get_all_ipa(word) # Retry
        else:
            raise Exception(f"API Error {response.status_code}")
    except Exception as e:
        print(f"\n[!] Error for '{word}': {e}")
        input("Press Enter to retry...")
        return get_all_ipa(word)
    return sorted(list(ipa_variants))

def force_split_and_clean(raw_arpa):
    raw_arpa = raw_arpa.upper().replace(" ", "")
    matches = PHONEME_PATTERN.findall(raw_arpa)
    return " ".join([m[0] for m in matches])

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_new_cmu.py [number_of_words]")
        return
    
    num_to_process = int(sys.argv[1])
    input_path = os.path.join(BASE_DIR, "general_english_100k.txt")
    output_path = os.path.join(BASE_DIR, "new_cmu.json")

    data_store = {}
    if os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            try:
                data_store = json.load(f)
            except:
                data_store = {}

    last_word = None
    if data_store:
        last_key = list(data_store.keys())[-1]
        last_word = re.sub(r'\d+$', '', last_key)

    with open(input_path, 'r', encoding='utf-8') as f:
        all_words = [line.strip().lower() for line in f if line.strip()]

    start_idx = all_words.index(last_word) + 1 if last_word in all_words else 0
    words_to_do = all_words[start_idx : start_idx + num_to_process]

    print(f"Processing {len(words_to_do)} words starting from index {start_idx}...")

    for word in words_to_do:
        print(f"Current: {word:20}", end="\r")
        ipa_list = get_all_ipa(word)
        
        if ipa_list:
            # DEDUPLICATION: Use a set to store unique ARPAbet strings for this word
            unique_arpa_for_word = set()
            
            for ipa in ipa_list:
                try:
                    raw_arpa = phonecodes.convert(ipa, "ipa", "arpabet", "eng")
                    clean_arpa = force_split_and_clean(raw_arpa)
                    unique_arpa_for_word.add(clean_arpa)
                except:
                    continue # Skip invalid IPA strings
            
            # Add unique results to the data_store
            for i, arpa in enumerate(sorted(list(unique_arpa_for_word)), 1):
                data_store[f"{word}{i}"] = arpa

        # Frequent auto-save
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data_store, f, indent=4)

    print(f"\nBatch complete. Total entries: {len(data_store)}")

if __name__ == "__main__":
    main()