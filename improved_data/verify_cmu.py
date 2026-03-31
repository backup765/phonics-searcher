"""
Run it to work on creating revised_cmu.json, a new version of the CMU that hopefully has less errors.
Currently revised_cmu.json is working off of freqSort_cmu_dict_full_general_english_100k_common_21000.json
Usage:
python verify_cmu.py freqSort_cmu_dict_full_general_english_100k_common_21000.json <number>

<number> is number of entries from freq...json to go through.
ctrl-c at any time while running to end.
"""

import requests
import re
import json
import sys
import os
import time
from phonecodes import phonecodes

# Ensure absolute paths relative to the script's location
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
        time.sleep(0.3)
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for entry in data:
                if 'phonetic' in entry:
                    # Remove spaces from API IPA
                    ipa_variants.add(entry['phonetic'].strip('/').replace(" ", ""))
                for p in entry.get('phonetics', []):
                    if 'text' in p and p['text']:
                        # Remove spaces from API IPA
                        ipa_variants.add(p['text'].strip('/').replace(" ", ""))
        elif response.status_code == 429:
            print(f"\n[!] Rate Limited. Waiting 5s...")
            time.sleep(5)
            return get_all_ipa(word)
    except Exception:
        pass
    return sorted(list(ipa_variants))

def force_split_and_clean(raw_arpa):
    """Formats ARPAbet string: space-separated, no digits."""
    raw_arpa = raw_arpa.upper().replace(" ", "")
    matches = PHONEME_PATTERN.findall(raw_arpa)
    return " ".join([m[0] for m in matches])

def safe_arpa_to_ipa(arpa_string):
    """Converts ARPAbet back to IPA for display purposes."""
    try:
        ipa = phonecodes.convert(arpa_string, "arpabet", "ipa", "eng")
        # Remove spaces from converted IPA
        return ipa.replace(" ", "")
    except:
        return "???"

def main():
    if len(sys.argv) < 3:
        print("Usage: python verify_cmu.py [source_json_path] [num_to_process]")
        return

    source_relative_path = sys.argv[1]
    num_to_verify = int(sys.argv[2])
    
    source_path = os.path.join(BASE_DIR, source_relative_path)
    output_path = os.path.join(BASE_DIR, "revised_cmu.json")

    if not os.path.exists(source_path):
        print(f"Error: {source_path} not found.")
        return

    with open(source_path, 'r', encoding='utf-8') as f:
        source_data = json.load(f)

    revised_data = {}
    if os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            try:
                revised_data = json.load(f)
            except:
                revised_data = {}

    source_keys = list(source_data.keys())
    start_idx = 0
    if revised_data:
        last_revised_key = list(revised_data.keys())[-1]
        if last_revised_key in source_keys:
            start_idx = source_keys.index(last_revised_key) + 1

    keys_batch = source_keys[start_idx : start_idx + num_to_verify]

    for key in keys_batch:
        word = re.sub(r'\d+$', '', key)
        original_arpa = source_data[key]
        
        ipa_list = get_all_ipa(word)
        api_options = []
        
        unique_arpa = set()
        for ipa in ipa_list:
            try:
                clean_arpa = force_split_and_clean(phonecodes.convert(ipa, "ipa", "arpabet", "eng"))
                if clean_arpa not in unique_arpa:
                    api_options.append((clean_arpa, ipa))
                    unique_arpa.add(clean_arpa)
            except:
                continue

        if not api_options:
            print(f"[-] {word.upper()}: No API data. Auto-keeping original.")
            revised_data[key] = original_arpa
        
        elif any(opt[0] == original_arpa for opt in api_options):
            print(f"[+] {word.upper()}: Match confirmed.")
            revised_data[key] = original_arpa
            
        else:
            orig_ipa = safe_arpa_to_ipa(original_arpa)
            print(f"\n--- CONFLICT: {word.upper()} ---")
            print(f" [0] Keep Original: {original_arpa:20} /{orig_ipa}/")
            
            for i, (arpa, ipa) in enumerate(api_options, 1):
                print(f" [{i}] Use API:      {arpa:20} /{ipa}/")
            
            user_input = input("Select #, enter custom ARPAbet, or [Enter] to skip: ").strip()

            if user_input == "":
                print("Skipped.")
                continue 
            elif user_input == "0":
                revised_data[key] = original_arpa
            elif user_input.isdigit() and 0 < int(user_input) <= len(api_options):
                revised_data[key] = api_options[int(user_input) - 1][0]
            else:
                # Store custom input as uppercase
                revised_data[key] = user_input.upper()

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(revised_data, f, indent=4)

    print(f"\nBatch complete. Total entries in revised_cmu.json: {len(revised_data)}")

if __name__ == "__main__":
    main()