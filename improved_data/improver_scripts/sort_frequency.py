import json
import sys
import os
from collections import OrderedDict

def sort_json_by_frequency(json_path, txt_path):
    # Extract just the filename to create the output name
    base_name = os.path.basename(json_path)
    output_filename = f"freqSort_{base_name}"

    try:
        # Load the JSON data
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Load the frequency list
        with open(txt_path, 'r', encoding='utf-8') as f:
            freq_list = [line.strip() for line in f if line.strip()]

        sorted_data = OrderedDict()

        # Add items based on frequency list order
        for word in freq_list:
            if word in data:
                sorted_data[word] = data[word]

        # Append items found in JSON but missing from the frequency list
        for word in data:
            if word not in sorted_data:
                sorted_data[word] = data[word]

        # Write to the new JSON file in the current directory
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(sorted_data, f, indent=4)

        print(f"Success: Created {output_filename}")

    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e.filename}")
    except json.JSONDecodeError:
        print(f"Error: {json_path} is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python sort_frequency.py /path/to/a.json /path/to/b.txt")
    else:
        sort_json_by_frequency(sys.argv[1], sys.argv[2])