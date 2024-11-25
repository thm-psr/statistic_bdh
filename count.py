from collections import defaultdict
import re
import os
import matplotlib.pyplot as plt

# VERSION 5: Schnitstelle zum Zählen bzw. zur Darstellung als Balkendiagramm

folder_input = r"I:\Projekte\2024_07_MD_Anfragen\Analyse\2023_alle"
#folder_input = r"I:\Projekte\2024_07_MD_Anfragen\Analyse\2024_alle"

word_counts = defaultdict(int)

code_pattern = re.compile(r"\(.*?\)")

for file_name in os.listdir(folder_input):
    if file_name.endswith(".txt"): 
        file_path = os.path.join(folder_input, file_name)
        
        with open(file_path, "r", encoding="utf-8") as file:
            current_entry = ""  
            
            for line in file:
                line = line.strip() 
                if not line:
                    continue
                
                current_entry += (" " + line).strip()
               
                if code_pattern.search(current_entry):
                    if " - " in current_entry:
                        parts = current_entry.split(" - ", 1)
                        full_entry = parts[0] + " - " + parts[1]
                    else:
                        full_entry = current_entry

                    word_counts[full_entry.strip()] += 1
                    current_entry = ""  

# Ergebnis in cmd angezeigt
print("Results:")
for entry, count in word_counts.items():
    print(f"'{entry}': {count}")

# Darstellung auf Balkendiagramm
labels = list(word_counts.keys())
counts = list(word_counts.values())

plt.figure(figsize=(12, 8))
bars = plt.bar(labels, counts, color='skyblue', edgecolor='black')

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height + 0.1, str(height), ha='center', va='bottom', fontsize=10)

plt.xlabel("Unterlagen", fontsize=10)
plt.ylabel("Anfragehäufigkeit", fontsize=10)
plt.title("Prüfauftraganfrage Statistik 2023", fontsize=13)
#plt.title("Prüfauftraganfrage Statistik 2024", fontsize=13)
plt.xticks(rotation=90, ha="right", fontsize=10)  
plt.tight_layout()
plt.show()
