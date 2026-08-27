import argparse
import json
import re

def parse_words_from_text(file_path):
    """Read a text file and extract clean words separated by whitespace or commas."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Split by whitespace or commas
    raw_words = re.split(r"[\s,]+", content)
    # Strip whitespace and filter out empty strings
    words = [word.strip() for word in raw_words if word.strip()]
    return words

def save_json_sorted(file_path, data):
    """Sort dictionary alphabetically by key and write to file."""
    sorted_data = dict(sorted(data.items(), key=lambda item: item[0]))
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(sorted_data, f, indent=2, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(
        description="Check text file words against a dictionary JSON and optionally add missing ones."
    )
    parser.add_argument("text_file", help="Path to the input text file containing words.")
    parser.add_argument("json_file", help="Path to the JSON dictionary file.")
    args = parser.parse_args()

    # Load existing JSON data
    try:
        with open(args.json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find JSON file '{args.json_file}'.")
        return
    except json.JSONDecodeError:
        print(f"Error: File '{args.json_file}' is not valid JSON.")
        return

    # Extract words from text file
    try:
        words = parse_words_from_text(args.text_file)
    except FileNotFoundError:
        print(f"Error: Could not find text file '{args.text_file}'.")
        return

    # Build a lookup set of JSON keys stripped of trailing '+' characters
    normalized_keys = {key.rstrip('+') for key in data.keys()}

    for word in words:
        if word in data or word in normalized_keys:
            continue

        prompt_msg = f"\nWord '{word}' not found. Enter pronunciation (or press Enter to skip): "
        user_input = input(prompt_msg).strip()

        if user_input:
            data[word] = user_input
            # Update the local lookup set so duplicates within the same text file are handled
            normalized_keys.add(word)
            save_json_sorted(args.json_file, data)
            print(f"Added and saved '{word}': '{user_input}'")
        else:
            print(f"Skipped '{word}'.")

if __name__ == "__main__":
    main()