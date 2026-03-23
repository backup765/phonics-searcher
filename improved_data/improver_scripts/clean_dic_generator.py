"""
Takes a json dictionary and 'cleans' it by removing words that are not spelled phonetically,
according to the phonetics taught in Jolly Phonics. Double consonants are allowed.
All non-alphabet characters are stripped from the input before checking if its spelling is good.

Usage:
python clean_dic_generator.py <your_file.json>

Creates:
your_file_clean.json

Examples:
  "kick": "K IH K" -> OK. k and ck both go to K
  "kicked": "K IH K T" -> NOT OK. T does not correspond to 'ed'
  "letter": "L EH T ER" -> OK. T can match to multiple 't's. 


The following conversion table is used between Jolly Phonics and ARPAbet

JP | CMU
--------
S | S
A | AE
T | T
I | IH
P | P
N | N
C | K
K | K
CK | K
E | EH
H | HH
R | R
M | M
D | D
G | G
O | AA
U | AH
L | L
F | F
B | B
AI | EY
J | JH
OA | OW
IE | AY
EE | IY
OR | AOR
Z | Z
W | W
NG | NG
V | V
OO | UH
OO | UW
Y | Y
X | KS
CH | CH
SH | SH
TH | DH
TH | TH
QU | KW
OU | AW
OI | OY
UE | YUW
ER | ER
AR | AAR


"""

import json
import os
import sys
import re

# Mapping of Spelling (JP) to ARPAbet (CMU)
# Note: longer spellings (QU, CK) are checked first to prevent partial matches
JP_TO_CMU = [
    ("CK", "K"), ("AI", "EY"), ("OA", "OW"), ("IE", "AY"), ("EE", "IY"),
    ("OR", "AOR"), ("NG", "NG"), ("OO", "UH"), ("OO", "UW"), ("CH", "CH"),
    ("SH", "SH"), ("TH", "DH"), ("TH", "TH"), ("QU", "KW"), ("OU", "AW"),
    ("OI", "OY"), ("UE", "YUW"), ("ER", "ER"), ("AR", "AAR"), ("S", "S"),
    ("A", "AE"), ("T", "T"), ("I", "IH"), ("P", "P"), ("N", "N"),
    ("C", "K"), ("K", "K"), ("E", "EH"), ("H", "HH"), ("R", "R"),
    ("M", "M"), ("D", "D"), ("G", "G"), ("O", "AA"), ("U", "AH"),
    ("L", "L"), ("F", "F"), ("B", "B"), ("J", "JH"), ("Z", "Z"),
    ("W", "W"), ("V", "V"), ("Y", "Y"), ("X", "KS")
]

def is_phonetic(word, phonemes):
    """
    Checks if a word's spelling matches its phonemes using Jolly Phonics rules.
    Uses recursion to handle branching paths (like TH or multiple OO sounds).
    """
    if not word and not phonemes:
        return True
    if not word or not phonemes:
        return False

    current_phoneme = phonemes[0]
    
    # Try matching every rule that results in the current phoneme
    for spelling, cmu in JP_TO_CMU:
        if cmu == current_phoneme:
            # 1. Standard match (e.g., "S" matches "S")
            if word.startswith(spelling):
                if is_phonetic(word[len(spelling):], phonemes[1:]):
                    return True
            
            # 2. Double consonant rule (e.g., "TT" matches "T")
            # Only applies if the spelling is a single consonant letter
            if len(spelling) == 1 and spelling not in "AEIOU":
                double = spelling + spelling
                if word.startswith(double):
                    if is_phonetic(word[2:], phonemes[1:]):
                        return True
                        
    return False

def clean_dictionary(input_path):
    if not input_path.endswith('.json'):
        print("Error: Input must be a .json file.")
        return

    base_name = os.path.splitext(input_path)[0]
    output_path = f"{base_name}_clean.json"

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    clean_data = {}
    
    for word, pron_str in data.items():
        # Clean input word: remove everything except A-Z
        clean_word = re.sub(r'[^A-Z]', '', word.upper())
        phonemes = pron_str.split()

        if is_phonetic(clean_word, phonemes):
            clean_data[word] = pron_str

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(clean_data, f, indent=2)

    print(f"Cleaned {len(data)} entries down to {len(clean_data)}.")
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clean_dic_generator.py <your_file.json>")
    else:
        clean_dictionary(sys.argv[1])