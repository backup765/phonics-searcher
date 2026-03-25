import sys
import os

def clean_plurals(file_path):
    # Get absolute path to ensure it works regardless of where you call it from
    abs_path = os.path.abspath(file_path)
    
    if not os.path.exists(abs_path):
        print(f"Error: File '{file_path}' not found.")
        return

    # Read words into a set for O(1) lookup speed
    with open(abs_path, 'r') as f:
        words = set(line.strip() for line in f if line.strip())

    cleaned_words = []

    for word in words:
        is_redundant_plural = False
        
        # Rule 1: Ends in 's' but not 'ss' (e.g., pockets -> pocket)
        if word.endswith('s') and not word.endswith('ss') and len(word) > 2:
            singular = word[:-1]
            if singular in words:
                is_redundant_plural = True
        
        # Rule 2: Ends in 'es' (e.g., taxes -> tax)
        # We only check this if Rule 1 didn't already flag it
        if word.endswith('es') and not is_redundant_plural and len(word) > 3:
            singular = word[:-2]
            if singular in words:
                is_redundant_plural = True

        if not is_redundant_plural:
            cleaned_words.append(word)

    # Overwrite the original file with the cleaned, sorted list
    with open(abs_path, 'w') as f:
        for word in sorted(cleaned_words):
            f.write(word + '\n')
    
    print(f"Success! Cleaned {len(words) - len(cleaned_words)} plurals from {file_path}.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python remove_plurals.py <filename.txt>")
    else:
        clean_plurals(sys.argv[1])