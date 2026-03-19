"""
Usage:
python common_dic_generator.py <input.json> <list.txt> <limit>

input.json - Original dictionary to be filtered
list.txt - A list, sorted by word frequency
limit - How many words in list.txt to look at


Creates:
input_list_common_limit.json

Takes the input json and generates a filtered version containing the top <limit> most common words, based
on a given list of words.
"""
import json
import os
import sys

def filter_cmu_dict():
    # 1. Validate arguments
    if len(sys.argv) < 4:
        print("Usage: python common_dic_generator.py <input.json> <list.txt> <limit>")
        return

    input_json = sys.argv[1]
    list_file = sys.argv[2]
    try:
        limit = int(sys.argv[3])
    except ValueError:
        print("Error: Limit must be an integer.")
        return

    # 2. Extract the top N words from the frequency list
    if not os.path.exists(list_file):
        print(f"Error: {list_file} not found.")
        return

    top_words = set()
    with open(list_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= limit: break
            parts = line.split()
            if parts: top_words.add(parts[0].lower())

    # 3. Load the source JSON dictionary
    if not os.path.exists(input_json):
        print(f"Error: {input_json} not found.")
        return

    with open(input_json, 'r', encoding='utf-8') as f:
        dictionary_data = json.load(f)

    # 4. Filter
    filtered_data = {
        word: prons for word, prons in dictionary_data.items()
        if word.lower() in top_words
    }

    # 5. Save with a combined name
    # Example: my_dict_google10k_5000.json
    base_name = os.path.splitext(input_json)[0]
    list_name = os.path.splitext(list_file)[0]
    output_name = f"{base_name}_{list_name}_common_{limit}.json"

    with open(output_name, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, indent=2)

    print(f"Filtered {len(dictionary_data)} down to {len(filtered_data)}.")
    print(f"Saved to: {output_name}")

if __name__ == "__main__":
    filter_cmu_dict()