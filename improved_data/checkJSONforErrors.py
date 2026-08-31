import argparse
import json
import re

# Allowed phonetic units (longest first to ensure greedy matching during parsing)
ALLOWED_PHONETICS = [
    "YUW", "AOR", "AAR",
    "AE", "IH", "EH", "HH", "AA", "AH", "EY", "JH", "OW", "AY", "IY", 
    "UH", "UW", "KS", "CH", "SH", "DH", "TH", "KW", "AW", "OY", "ER",
    "S", "T", "P", "N", "K", "R", "M", "D", "G", "L", "F", "B", 
    "Z", "W", "NG", "V", "Y"
]

def check_duplicates(data):
    """Find and return dictionary entries with duplicate base word keys."""
    normalized_map = {}
    duplicates = []

    for original_key in data.keys():
        base_key = original_key.rstrip('+')
        if base_key in normalized_map:
            duplicates.append((original_key, normalized_map[base_key]))
        else:
            normalized_map[base_key] = original_key

    return duplicates

def validate_pronunciation(pronunciation):
    """Check if the pronunciation consists exclusively of allowed phonetic units and spaces."""
    # Build regex pattern matching allowed phonetics separated by whitespace
    tokens = re.split(r'\s+', pronunciation.strip())
    invalid_tokens = []

    for token in tokens:
        if not token:
            continue
        if token not in ALLOWED_PHONETICS:
            invalid_tokens.append(token)

    return invalid_tokens

def main():
    parser = argparse.ArgumentParser(
        description="Check dictionary JSON for duplicate keys and invalid phonetic components."
    )
    parser.add_argument("json_file", help="Path to the JSON dictionary file.")
    args = parser.parse_args()

    try:
        with open(args.json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find JSON file '{args.json_file}'.")
        return
    except json.JSONDecodeError:
        print(f"Error: File '{args.json_file}' is not valid JSON.")
        return

    print("--- Checking for Duplicates ---")
    duplicates = check_duplicates(data)
    if duplicates:
        print(f"Found {len(duplicates)} duplicate entry/entries:")
        for key1, key2 in duplicates:
            print(f" - Duplicate match: '{key1}' conflicts with '{key2}'")
    else:
        print("No duplicate words found.")

    print("\n--- Checking Phonetic Pronunciations ---")
    abnormal_count = 0
    for word, pronunciation in data.items():
        if not isinstance(pronunciation, str):
            print(f" - Word '{word}': Pronunciation is not a string ({type(pronunciation).__name__})")
            abnormal_count += 1
            continue

        invalid = validate_pronunciation(pronunciation)
        if invalid:
            abnormal_count += 1
            print(f" - Word '{word}' ('{pronunciation}'): Invalid token(s) found -> {invalid}")

    if abnormal_count == 0:
        print("No abnormal pronunciations found.")

if __name__ == "__main__":
    main()