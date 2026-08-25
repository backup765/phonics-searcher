"""
Takes an input JSON dictionary and generates a filtered version with profane keys removed
using better-profanity, with specific whitelisted words permitted.

Usage:
python remove_profanity.py <input.json>

input.json - Original dictionary to be filtered

Creates:
input_clean.json
"""
import json
import os
import sys
from better_profanity import profanity


def remove_profanity():
    # 1. Validate arguments
    if len(sys.argv) < 2:
        print("Usage: python remove_profanity.py <input.json>")
        return

    input_json = os.path.abspath(sys.argv[1])

    if not os.path.exists(input_json):
        print(f"Error: {input_json} not found.")
        return

    # 2. Whitelist specified words by converting VaryingString items to standard str
    whitelist = {"pot", "god", "fat", "kill", "weed", "naked", "nude", "paddy", "slope", "womb", "fart"}
    censor_words_str = {str(word) for word in profanity.CENSOR_WORDSET}
    custom_bad_words = censor_words_str - whitelist
    profanity.load_censor_words(custom_words=custom_bad_words)

    # 3. Load the source JSON dictionary
    with open(input_json, "r", encoding="utf-8") as f:
        dictionary_data = json.load(f)

    # 4. Filter out keys that contain profanity
    filtered_data = {
        word: value
        for word, value in dictionary_data.items()
        if not profanity.contains_profanity(word)
    }

    # 5. Save with an updated name in the same directory as input_json
    input_dir = os.path.dirname(input_json)
    base_name = os.path.splitext(os.path.basename(input_json))[0]

    output_filename = f"{base_name}_clean.json"
    output_path = os.path.join(input_dir, output_filename)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, indent=2)

    # 6. Report summary
    removed_count = len(dictionary_data) - len(filtered_data)
    print("--- Process Complete ---")
    print(f"Source items: {len(dictionary_data)}")
    print(f"Filtered items: {len(filtered_data)}")
    print(f"Profane items removed: {removed_count}")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    remove_profanity()