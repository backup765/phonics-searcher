import sys
import os

def clean_plurals(file_path):
    # Setup absolute path for global execution
    abs_path = os.path.abspath(file_path)
    
    if not os.path.exists(abs_path):
        print(f"Error: File '{file_path}' not found.")
        return

    # 1. Read the original file
    with open(abs_path, 'r') as f:
        original_lines = [line.strip() for line in f if line.strip()]

    # 2. Lookup set for fast comparison
    word_lookup = set(original_lines)
    cleaned_words = []

    for word in original_lines:
        is_redundant_plural = False
        
        # Only process words 6 characters or longer (e.g., 'pockets' is 7, 'pocket' is 6)
        if len(word) >= 7:
            
            # Rule 1: Ends in 's' but not 'ss' (e.g., 'pockets' -> 'pocket')
            if word.endswith('s') and not word.endswith('ss'):
                singular = word[:-1]
                if singular in word_lookup:
                    is_redundant_plural = True
            
            # Rule 2: Ends in 'es' (e.g., 'watches' -> 'watch')
            if word.endswith('es') and not is_redundant_plural:
                singular = word[:-2]
                if singular in word_lookup:
                    is_redundant_plural = True

        # Keep the word if it's short OR not a redundant plural
        if not is_redundant_plural:
            cleaned_words.append(word)

    # 3. Write back to the same file, preserving order
    with open(abs_path, 'w') as f:
        for word in cleaned_words:
            f.write(word + '\n')
    
    removed = len(original_lines) - len(cleaned_words)
    print(f"Success! Removed {removed} plurals (6+ chars). Order preserved in {file_path}.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python remove_plurals.py a.txt")
    else:
        clean_plurals(sys.argv[1])