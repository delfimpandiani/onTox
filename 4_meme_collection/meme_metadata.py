import os
import re

# Define the path to your input .txt file and the output directory
input_file = 'symbols.txt'
output_dir = 'memedata'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Helper function to create OS-compliant folder names
def clean_folder_name(symbol):
    # Remove any characters that are not allowed in folder names
    return re.sub(r'[<>:"/\\|?*]', '_', symbol.strip())

# Dictionary to keep track of original symbol names and their folder names
symbol_map = {}

# Read the file and create folders
with open(input_file, 'r') as file:
    for line in file:
        # Clean up the symbol name to make it safe for folder creation
        symbol = line.strip()
        folder_name = clean_folder_name(symbol)

        # Ensure unique folder names in case of duplicates
        if folder_name in symbol_map.values():
            folder_name += f"_{len(symbol_map) + 1}"

        # Store the mapping of original symbol to folder name
        symbol_map[symbol] = folder_name

        # Create the directory for the symbol
        os.makedirs(os.path.join(output_dir, folder_name), exist_ok=True)

# Save the symbol map as a reference file
with open(os.path.join(output_dir, 'symbol_index.txt'), 'w') as index_file:
    for original_symbol, folder_name in symbol_map.items():
        index_file.write(f"{original_symbol} -> {folder_name}\n")

print("Folders created and symbol index saved.")
