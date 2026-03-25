import json
import os
import sys

def compare_jsons(file1_path, file2_path):
    # Get absolute paths to ensure it runs from any base folder
    abs1 = os.path.abspath(file1_path)
    abs2 = os.path.abspath(file2_path)
    output_file = "COMPARE_RESULT.txt"

    try:
        with open(abs1, 'r') as f1, open(abs2, 'r') as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)
    except Exception as e:
        print(f"Error reading files: {e}")
        return

    # Convert to sets of items (key-value pairs) for easy comparison
    # This works for flat JSON like {"for": "F R ER"}
    set1 = set(data1.items())
    set2 = set(data2.items())

    only_in_a = set1 - set2
    only_in_b = set2 - set1

    with open(output_file, 'w') as out:
        out.write(f"--- ONLY IN {os.path.basename(abs1)} ---\n")
        for k, v in sorted(only_in_a):
            out.write(f'"{k}": "{v}"\n')
        
        out.write(f"\n--- ONLY IN {os.path.basename(abs2)} ---\n")
        for k, v in sorted(only_in_b):
            out.write(f'"{k}": "{v}"\n')

    print(f"Comparison complete. Results saved to {os.path.abspath(output_file)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_json.py a.json b.json")
    else:
        compare_jsons(sys.argv[1], sys.argv[2])