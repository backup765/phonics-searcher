"""
Retrieves the pronunciations listed in the online dictionary in both IPA nad ARPAbet
"""
import requests
import re
from phonecodes import phonecodes

# Valid ARPAbet phonemes
ARPABET_PHONEMES = [
    'AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'EH', 'ER', 'EY', 'IH', 'IY', 'OW', 'OY', 'UH', 'UW',
    'B', 'CH', 'D', 'DH', 'F', 'G', 'HH', 'JH', 'K', 'L', 'M', 'N', 'NG', 'P', 'R', 'S', 'SH', 
    'T', 'TH', 'V', 'W', 'Y', 'Z', 'ZH'
]

# Sort by length descending to match 'SH' before 'S'
ARPABET_PHONEMES.sort(key=len, reverse=True)

# fr"" handles f-string interpolation and raw string backslashes
PHONEME_PATTERN = re.compile(fr"({'|'.join(ARPABET_PHONEMES)})(\d)?")

def get_all_ipa(word):
    """Fetches all unique IPA transcriptions from the API."""
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    ipa_variants = set()
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Iterate through all entries and all phonetics
            for entry in data:
                # Some entries have a top-level phonetic string
                if 'phonetic' in entry:
                    ipa_variants.add(entry['phonetic'].strip('/'))
                
                # Check the phonetics list
                for p in entry.get('phonetics', []):
                    if 'text' in p and p['text']:
                        ipa_variants.add(p['text'].strip('/'))
    except Exception:
        pass
        
    return sorted(list(ipa_variants))

def force_split_and_clean(raw_arpa):
    """Strips stress numbers and ensures single-space separation."""
    raw_arpa = raw_arpa.upper().replace(" ", "")
    matches = PHONEME_PATTERN.findall(raw_arpa)
    clean_tokens = [m[0] for m in matches]
    return " ".join(clean_tokens)

def main():
    word = input("Enter a word: ").strip().lower()
    if not word: return

    ipa_list = get_all_ipa(word)
    
    if ipa_list:
        print(f"\nWord: {word.upper()}")
        print("-" * 30)
        
        for i, ipa in enumerate(ipa_list, 1):
            try:
                # Convert this specific IPA variant
                raw_arpa = phonecodes.convert(ipa, "ipa", "arpabet", "eng")
                formatted_arpa = force_split_and_clean(raw_arpa)
                
                print(f"Option {i}:")
                print(f"  IPA:     /{ipa}/")
                print(f"  ARPAbet: {formatted_arpa}\n")
            except Exception:
                # If conversion fails for a specific variant, skip it
                print(f"Option {i}: Could not convert /{ipa}/")
    else:
        print(f"No pronunciations found for '{word}'.")

if __name__ == "__main__":
    main()