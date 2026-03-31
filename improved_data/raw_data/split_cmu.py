import os

def split_json_by_lines(input_file, output_folder, lines_per_file=200):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created directory: {output_folder}")

    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            file_count = 1
            line_count = 0
            current_out_file = None
            
            for line in infile:
                # Open a new file if we've reached the limit or it's the first run
                if line_count % lines_per_file == 0:
                    if current_out_file:
                        current_out_file.close()
                    
                    new_filename = f"cmu_split_{file_count}.json"
                    current_out_file = open(os.path.join(output_folder, new_filename), 'w', encoding='utf-8')
                    file_count += 1
                
                current_out_file.write(line)
                line_count += 1

            # Clean up
            if current_out_file:
                current_out_file.close()
                
        print(f"Success! Processed {line_count} lines into {file_count - 1} files.")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Configuration
INPUT_FILE = 'cmu_dict_full_NEW.json'
OUTPUT_DIR = './split_cmu/'

split_json_by_lines(INPUT_FILE, OUTPUT_DIR)