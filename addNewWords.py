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

    json_updated = False

    for word in words:
        if word in data:
            continue

        print(f"\nWord '{word}' is not in the JSON dictionary.")
        choice = input("Do you want to add it? ([a]dd / [s]kip): ").strip().lower()

        if choice in ("a", "add"):
            pronunciation = input(f"Enter pronunciation for '{word}': ").strip()
            data[word] = pronunciation
            json_updated = True
            print(f"Added '{word}': '{pronunciation}'")
        else:
            print(f"Skipped '{word}'.")

    if json_updated:
        # Sort dictionary alphabetically by key
        data = dict(sorted(data.items(), key=lambda item: item[0]))
        
        # Save back to JSON file
        with open(args.json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("\nJSON file successfully updated and saved alphabetically.")
    else:
        print("\nNo changes were made to the JSON file.")

if __name__ == "__main__":
    main()