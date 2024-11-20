from collections import defaultdict
import re
import os

# VERSION 2: Für den Fall, dass die Unterlagennamen in der txt-Datei mehrzeilig sind
# Folder containing the text files
folder_path = r"C:\Users\acer\Downloads\Testdata\24"

# Initialize a dictionary to keep track of counts across all files
word_counts = defaultdict(int)

# Pattern to detect lines that end with a code in parentheses (e.g., "(SD110104)")
pattern = re.compile(r"\(.*?\)$")

# Loop through all text files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".txt"):  # Only process .txt files
        file_path = os.path.join(folder_path, file_name)
        
        # Variable to accumulate lines until a full entry is formed
        current_entry = ""
        
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()  # Remove extra whitespace or newlines
                if line:  # Skip empty lines
                    current_entry += (" " + line).strip()  # Append line to current entry
                    
                    # Check if the current entry ends with a code
                    if pattern.search(current_entry):
                        word_counts[current_entry] += 1  # Count the completed entry
                        current_entry = ""  # Reset for the next entry

# Print each entry on a new line
for word, count in word_counts.items():
    print(f"'{word}': {count}")


# VERSION 1
# from collections import defaultdict
# import re

# # Path to the input text file
# file_path = "testlist.txt"

# # Initialize a dictionary to keep track of counts
# word_counts = defaultdict(int)

# # Pattern to detect lines that end with a code in parentheses (e.g., "(SD110104)")
# pattern = re.compile(r"\(.*?\)$")

# # Variable to accumulate lines until a full entry is formed
# current_entry = ""

# # Read the file line by line and update counts
# with open(file_path, "r", encoding="utf-8") as file:
#     for line in file:
#         line = line.strip()  # Remove extra whitespace or newlines
#         if line:  # Skip empty lines
#             current_entry += (" " + line).strip()  # Append line to current entry
            
#             # Check if the current entry ends with a code
#             if pattern.search(current_entry):
#                 word_counts[current_entry] += 1  # Count the completed entry
#                 current_entry = ""  # Reset for the next entry

# # Print each entry on a new line
# for word, count in word_counts.items():
#     print(f"'{word}': {count}")
