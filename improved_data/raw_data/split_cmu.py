import os
import json
import argparse
from itertools import islice

def split_json_dict(input_file, output_folder, items_per_file=200):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created directory: {output_folder}")

    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            data = json.load(infile)

        if not isinstance(data, dict):
            print("Error: This script expects a JSON object {}. Your file appears to be a different format.")
            return

        # Convert dictionary items into a list of tuples to allow slicing
        items = list(data.items())
        total_items = len(items)
        file_count = 0

        for i in range(0, total_items, items_per_file):
            file_count += 1
            # Create a slice of the items
            chunk_slice = items[i : i + items_per_file]
            # Convert the slice back into a dictionary
            chunk_dict = dict(chunk_slice)
            
            new_filename = f"split_{file_count}.json"
            output_path = os.path.join(output_folder, new_filename)
            
            with open(output_path, 'w', encoding='utf-8') as outfile:
                # This writes the opening '{', the key-values, and the closing '}'
                json.dump(chunk_dict, outfile, indent=4)

        print(f"Success! Split {total_items} entries into {file_count} files in '{output_folder}'.")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: '{input_file}' is not a valid JSON file. Check for trailing commas or syntax errors.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split a large JSON dictionary into smaller valid JSON files.")
    parser.add_argument("input_file", help="Path to the source JSON file")
    parser.add_argument("--limit", type=int, default=200, help="Entries per file (default: 200)")
    
    args = parser.parse_args()
    
    OUTPUT_DIR = './split_cmu/'
    
    split_json_dict(args.input_file, OUTPUT_DIR, args.limit)