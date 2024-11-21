from collections import defaultdict
import re
import os
import matplotlib.pyplot as plt

# VERSION 5: Schnitstelle zum Zählen bzw. zur Darstellung als Balkendiagramm

# Folder containing the text files
folder_input = r"C:\Users\acer\Downloads\Testdata\testdaten"

# Initialize a dictionary to keep track of counts across all files
word_counts = defaultdict(int)

# Pattern to detect a code in parentheses (e.g., "(A12345)")
code_pattern = re.compile(r"\(.*?\)")

# Loop through all text files in the folder
for file_name in os.listdir(folder_input):
    if file_name.endswith(".txt"):  # Only process .txt files
        file_path = os.path.join(folder_input, file_name)
        
        with open(file_path, "r", encoding="utf-8") as file:
            current_entry = ""  # To accumulate lines until a full entry is formed
            
            for line in file:
                line = line.strip()  # Remove extra whitespace or newlines
                if not line:  # Skip empty lines
                    continue
                
                # Add the current line to the accumulating entry
                current_entry += (" " + line).strip()
                
                # Check if the accumulated entry contains a code
                if code_pattern.search(current_entry):
                    # Check for a dash and include everything after it in the entry
                    if " - " in current_entry:
                        # Split on the dash and keep the part after the dash
                        parts = current_entry.split(" - ", 1)
                        full_entry = parts[0] + " - " + parts[1]
                    else:
                        full_entry = current_entry

                    # Count the full entry as one word
                    word_counts[full_entry.strip()] += 1
                    current_entry = ""  # Reset for the next entry

# Display results in the CMD
print("Results:")
for entry, count in word_counts.items():
    print(f"'{entry}': {count}")

# Plot the results using matplotlib
# Extract labels (names of Unterlagen) and their counts
labels = list(word_counts.keys())
counts = list(word_counts.values())

# Create the bar chart
plt.figure(figsize=(12, 8))
bars = plt.bar(labels, counts, color='skyblue', edgecolor='black')

# Add count labels on top of each bar
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height + 0.1, str(height), ha='center', va='bottom', fontsize=10)

# Add labels and title
plt.xlabel("Unterlagen", fontsize=14)
plt.ylabel("Anfragehäufigkeit", fontsize=14)
plt.title("Prüfauftraganfrage Statistik 2024", fontsize=16)
plt.xticks(rotation=45, ha="right", fontsize=10)  # Rotate the x-axis labels for readability

# Adjust layout to avoid clipping
plt.tight_layout()

# Show the plot
plt.show()

# # VERSION 4: Ein- und mehrzeilige Zählungen sowie Zählungen mit dem zusätzlichen Befehl "-" werden jetzt unterstützt
# # Folder containing the text files
# folder_input = r"C:\Users\acer\Downloads\Testdata\testdaten"

# # Initialize a dictionary to keep track of counts across all files
# word_counts = defaultdict(int)

# # Pattern to detect a code in parentheses (e.g., "(A12345)")
# code_pattern = re.compile(r"\(.*?\)")

# # Loop through all text files in the folder
# for file_name in os.listdir(folder_input):
#     if file_name.endswith(".txt"):  # Only process .txt files
#         file_path = os.path.join(folder_input, file_name)
        
#         with open(file_path, "r", encoding="utf-8") as file:
#             current_entry = ""  # To accumulate lines until a full entry is formed
            
#             for line in file:
#                 line = line.strip()  # Remove extra whitespace or newlines
#                 if not line:  # Skip empty lines
#                     continue
                
#                 # Add the current line to the accumulating entry
#                 current_entry += (" " + line).strip()
                
#                 # Check if the accumulated entry contains a code
#                 if code_pattern.search(current_entry):
#                     # Check for a dash and include everything after it in the entry
#                     if " - " in current_entry:
#                         # Split on the dash and keep the part after the dash
#                         parts = current_entry.split(" - ", 1)
#                         full_entry = parts[0] + " - " + parts[1]
#                     else:
#                         full_entry = current_entry

#                     # Count the full entry as one word
#                     word_counts[full_entry.strip()] += 1
#                     current_entry = ""  # Reset for the next entry

# # Display results in the CMD
# print("Results:")
# for entry, count in word_counts.items():
#     print(f"'{entry}': {count}")


# # VERSION 3: 

# from collections import defaultdict
# import re
# import os

# # Folder containing the text files
# folder_input = r"C:\Users\acer\Downloads\Testdata\testdaten"

# # Initialize a dictionary to keep track of counts across all files
# word_counts = defaultdict(int)

# # Pattern to detect lines containing a code in parentheses (e.g., "(LB120199)")
# code_pattern = re.compile(r"\(.*?\)")  # Matches (A123456)
# # Pattern to split concatenated entries
# split_pattern = re.compile(r"(.*?\(.*?\)\s*[-:])")

# # Loop through all text files in the folder
# for file_name in os.listdir(folder_input):
#     if file_name.endswith(".txt"):  # Only process .txt files
#         file_path = os.path.join(folder_input, file_name)
        
#         # Variable to accumulate lines until a full entry is formed
#         current_entry = ""
        
#         with open(file_path, "r", encoding="utf-8") as file:
#             for line in file:
#                 line = line.strip()  # Remove extra whitespace or newlines
#                 if line:  # Skip empty lines
#                     current_entry += (" " + line).strip()  # Append line to current entry
                    
#                     # Check if the current entry contains multiple concatenated entries
#                     if code_pattern.search(current_entry):
#                         # Split the current entry into individual parts based on patterns
#                         parts = split_pattern.findall(current_entry)
#                         if not parts:  # If no parts matched, treat as one entry
#                             word_counts[current_entry] += 1
#                         else:
#                             for part in parts:
#                                 word_counts[part.strip()] += 1
#                         current_entry = ""  # Reset for the next entry

# # Display results in the CMD
# print("Results:")
# for entry, count in word_counts.items():
#     print(f"'{entry}': {count}")


# # VERSION 2: Für den Fall, dass die Unterlagennamen in der txt-Datei mehrzeilig sind
# # Folder containing the text files
# folder_path = r"C:\Users\acer\Downloads\Testdata\testdaten"

# # Initialize a dictionary to keep track of counts across all files
# word_counts = defaultdict(int)

# # Pattern to detect lines that end with a code in parentheses (e.g., "(SD110104)")
# pattern = re.compile(r"\(.*?\)$")

# # Loop through all text files in the folder
# for file_name in os.listdir(folder_path):
#     if file_name.endswith(".txt"):  # Only process .txt files
#         file_path = os.path.join(folder_path, file_name)
        
#         # Variable to accumulate lines until a full entry is formed
#         current_entry = ""
        
#         with open(file_path, "r", encoding="utf-8") as file:
#             for line in file:
#                 line = line.strip()  # Remove extra whitespace or newlines
#                 if line:  # Skip empty lines
#                     current_entry += (" " + line).strip()  # Append line to current entry
                    
#                     # Check if the current entry ends with a code
#                     if pattern.search(current_entry):
#                         word_counts[current_entry] += 1  # Count the completed entry
#                         current_entry = ""  # Reset for the next entry

# # Print each entry on a new line
# for word, count in word_counts.items():
#     print(f"'{word}': {count}")

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
