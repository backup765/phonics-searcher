import json
import sys
import os
from collections import OrderedDict

def sort_json_alphabetically(json_path):
    # Extract the filename to create the output name (e.g., alphaSort_a.json)
    base_name = os.path.basename(json_path)
    output_filename = f"alphaSort_{base_name}"

    try:
        # Load the JSON data
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not isinstance(data, dict):
            print(f"Error: {json_path} must contain a JSON object.")
            return

        # Sort keys alphabetically (Case-sensitive: A-Z then a-z)
        sorted_keys = sorted(data.keys())
        sorted_data = OrderedDict()
        
        for key in sorted_keys:
            sorted_data[key] = data[key]

        # Write to the new JSON file in the current directory
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(sorted_data, f, indent=4)

        print(f"Success: Alphabetically sorted JSON saved to {output_filename}")

    except FileNotFoundError:
        print(f"Error: Could not find file at {json_path}")
    except json.JSONDecodeError:
        print(f"Error: {json_path} is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sort_alphabet.py /path/to/your.json")
    else:
        sort_json_alphabetically(sys.argv[1])