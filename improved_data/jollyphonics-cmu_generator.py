"""
Usage:
python jollyphonics-cmu_generator.py <your_file.json>

Creates:
your_file_JP-ARPAbet.json

Generates copies of words to make a dictionary in CMU format agree with Jolly Phonics rules.
New entries are the old entry, with a '+' at the end. 
Example:
"four": "F AO R"
    =>
"four": "F AO R"
"four+": "F AOR"

The disagreements between Jolly Phonics and ARPAbet which are changed are as follows. 

JP | CMU
--------
OR | AO R
X  | K S
QU | K W
UE | Y UW
AR | AA R
"""
import json
import os
import sys

def process_dictionary(input_path):
    # 1. Handle file paths and naming
    if not input_path.endswith('.json'):
        print("Error: Input file must be a .json file.")
        return

    # Generate output name: filename.json -> filename_JP-ARPAbet.json
    base_name = os.path.splitext(input_path)[0]
    output_path = f"{base_name}_JP-ARPAbet.json"

    # 2. Define the ARPAbet expansion rules
    rules = {
        "AO R": "AOR",
        "K S": "KS",
        "K W": "KW",
        "Y UW": "YUW",
        "AA R": "AAR"
    }

    # 3. Load the source data
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{input_path}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON in '{input_path}'.")
        return

    expanded_data = {}

    # 4. Apply rules and add "+" entries
    for word, pronunciation in data.items():
        # Add original
        expanded_data[word] = pronunciation

        new_pronunciation = pronunciation
        modified = False
        
        for sequence, replacement in rules.items():
            if sequence in new_pronunciation:
                # Use a specific replace to ensure we only catch space-separated phonemes
                new_pronunciation = new_pronunciation.replace(sequence, replacement)
                modified = True
        
        if modified:
            expanded_data[f"{word}+"] = new_pronunciation

    # 5. Sort alphabetically so "word" and "word+" stay together
    sorted_data = dict(sorted(expanded_data.items()))

    # 6. Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sorted_data, f, indent=2)

    print(f"Processing complete.")
    print(f"Input:  {len(data)} entries")
    print(f"Output: {len(expanded_data)} entries")
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    # Check if the user provided the filename argument
    if len(sys.argv) < 2:
        print("Usage: python jollyphonics-cmu_generator.py <your_file.json>")
    else:
        process_dictionary(sys.argv[1])