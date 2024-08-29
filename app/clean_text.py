import os
import re

def clean_text(text):
    
    lines = text.splitlines()
    
    # Assume the first line might contain URLs and handle it separately
    if lines:
    
        first_line = lines[0]
        rest_of_text = ' '.join(lines[1:])
        
        # Remove extra whitespace, convert to lowercase, and remove non-ASCII characters
        rest_of_text = re.sub(r'\s+', ' ', rest_of_text)
        rest_of_text = re.sub(r'[^\x00-\x7F]+', '', rest_of_text)
        rest_of_text = rest_of_text.lower()
        rest_of_text = re.sub(r'[^a-zA-Z0-9\s]', '', rest_of_text)
        
        cleaned_text = first_line + '\n' + rest_of_text
    else:
        cleaned_text = text  
    
    return cleaned_text

def clean_data_directory(input_dir, output_dir):
    
    os.makedirs(output_dir, exist_ok=True)
    
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    raw_text = f.read()
                
                cleaned_text = clean_text(raw_text)
                
                relative_path = os.path.relpath(root, input_dir)
                output_file_dir = os.path.join(output_dir, relative_path)
                os.makedirs(output_file_dir, exist_ok=True)
                output_file_path = os.path.join(output_file_dir, file)
                
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned_text)
    
    print(f"Data cleaned and saved to {output_dir}")

input_directory = 'data'  
output_directory = 'cleaned_data'  

clean_data_directory(input_directory, output_directory)    