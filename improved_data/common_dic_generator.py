"""
Takes the full CMU json and generates a filtered version containing the top X most common words, based
on one of the lists.
"""
import json
import os

def filter_cmu_dict():
    # 1. List available frequency files
    files = [f for f in os.listdir('.') if f.endswith('.txt')]
    
    if not files:
        print("No .txt frequency lists found in this folder.")
        return

    print("--- Available Frequency Lists ---")
    for i, filename in enumerate(files):
        print(f"[{i}] {filename}")

    # 2. Get user choices
    choice_idx = int(input("\nSelect a list by number: "))
    selected_file = files[choice_idx]
    limit = int(input("How many top words to keep (e.g., 20000)? "))

    # 3. Read the frequency list and extract the top N words
    print(f"Reading {selected_file}...")
    top_words = set()
    with open(selected_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= limit:
                break
            # Split line and take the first part (the word)
            parts = line.split()
            if parts:
                top_words.add(parts[0].lower())

    # 4. Load the CMU dictionary
    input_json = 'cmu_dict_full.json'
    if not os.path.exists(input_json):
        print(f"Error: {input_json} not found.")
        return

    with open(input_json, 'r', encoding='utf-8') as f:
        cmu_data = json.load(f)

    # 5. Filter the data
    # We keep the word if its lowercase version is in our frequency set
    filtered_data = {
        word: pronunciation for word, pronunciation in cmu_data.items()
        if word.lower() in top_words
    }

    # 6. Save the output
    output_filename = f"filtered_{selected_file.replace('.txt', '')}_{limit}.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, indent=2)

    print(f"\nSuccess!")
    print(f"Original word count: {len(cmu_data)}")
    print(f"Filtered word count: {len(filtered_data)}")
    print(f"Saved to: {output_filename}")

if __name__ == "__main__":
    filter_cmu_dict()