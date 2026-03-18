#!/usr/bin/env python3
"""
CMU Phoneme Subset Searcher
Searches for words using only selected phonemes

There are 4 dictionaries available. 
cmu_dict.json - the largest, full and complete catalogue - 125,752 entries
cmu_dict_common.json - most common 20k words from the full dict - 19987 entries
cmu_dict_clean.json - the full dict, 'cleaned' to only have words follwing the
    jolly phonics spelling rules. In theory students should be able to spell
    any of these words. Quality not guarenteed, needs manual adjustment to make
    sure rules are being followed - 11,160 entries
cmu_dict_clean_common.json - only the common words from the clean list. Again,
    quality not guarenteed - 2245 entries
"""

import json

# Define available phonemes
#S T P N M F L K D G B V Z R HH JH CH SH TH DH NG Y W AE IH EH AA UH AH EY AY OW AW OY UW ER AO IY

PHONEMES = [
    # Consonants
    'S', 'T', 'P', 'N', 'M', 'F', 'L', 'K', 'D', 'G', 'B', 'V', 'Z',
    'R', 'HH', 'JH', 'CH', 'SH', 'TH', 'DH', 'NG', 'Y', 'W',
    
    # Vowels
    'AE', 'IH', 'EH', 'AA', 'UH', 'AH', 'EY', 'AY', 'OW', 'AW',
    'OY', 'UW', 'ER', 'AO', 'IY'
]


""" 
Function to seach the given dictionary for the given phonemes
word_dict - the dict to search through
selected_phonemes - the phonemes allowed to be used
forced_phonemes - phonemes that MUST be used in the word
"""
def search_subset(word_dict, selected_phonemes, forced_phonemes=[]):
    target_set = set(selected_phonemes)
    forced_set = set(forced_phonemes)
    matches = []

    for word, pron in word_dict.items():
        word_set = set(pron.split())
        if word_set.issubset(target_set):
            if forced_set:
                # print(f"must have {forced_set}")
                if forced_set.issubset(word_set):
                    matches.append((word, pron))
            else:
                matches.append((word, pron))
    
    matches.sort(key=lambda x: (len(x[0]), x[0]))
    return matches


def main():
    # Open all the dicts. Probably don't need to do this
    with open('data/cmu_dict_common.json', 'r') as f:
        common_dict = json.load(f)
    with open('data/cmu_dict_full.json', 'r') as f:
        full_dict = json.load(f)
    with open('data/cmu_dict_clean.json', 'r') as f:
        clean_dict = json.load(f)    
    with open('data/cmu_dict_clean-common.json', 'r') as f:
        clean_common_dict = json.load(f)    
    
    print(f"Available phonemes: {', '.join(PHONEMES)}")
    print("\nEnter phonemes separated by spaces (e.g., S AE T), '!' to exit")
    
    #default to clean_common
    current_dict = clean_common_dict
    
    while True:
        query = input("\nSearch phonemes: ").strip().upper()
        #print(f"DEBUG: query = '{query}'") 
        if query == '!':
            break
        elif query == '!F':
            current_dict = full_dict
            print("\nswapped to full dict")
            continue
        elif query == '!CL':
            current_dict = clean_dict
            print("\nswapped to clean dict")
            continue
        elif query == '!CM':
            current_dict = common_dict
            print("\nswapped to common dict")
            continue
        elif query == '!CLM':
            current_dict = clean_common_dict
            print("\nswapped to clean common dict")
            continue
        elif not query:
            continue
        
        selected_phonemes = query.split()
        
        # Validate phonemes
        invalid = [p for p in selected_phonemes if p not in PHONEMES]
        if invalid:
            print(f"Invalid phonemes: {', '.join(invalid)}")
            print(f"Valid phonemes: {', '.join(PHONEMES)}")
            continue
        
        force_query = input("Force phonemes: ").strip().upper()
        forced_phonemes = force_query.split()

        print(f"Searching for words using only: {{{', '.join(selected_phonemes)}}}")
        
        results = search_subset(current_dict, selected_phonemes, forced_phonemes)
        
        if results:
            print(f"\nFound {len(results)} words:")
            for word, pron in results:
                print(f"{word:15} {pron}")
        else:
            print("No matches")

if __name__ == "__main__":
    main()