import re
import os
from pdf2image import convert_from_path
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 
#pytesseract.pytesseract.tesseract_cmd = r"C:\Users\thm-psr\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

# Version 7: Lösung des Speicherproblems bei zu großen PDF-Dateien (Achtung bei Dieter ist nicht sauber gespeichert)
def pdf_to_text(pdf_path, output_text_path, lang='deu', poppler_path=r'C:\Users\thm-efg\Downloads\Poppler\poppler-24.08.0\Library\bin'):
    # Convert the PDF to images (reduce DPI for lower memory usage)
    pages = convert_from_path(pdf_path, 150, poppler_path=poppler_path)  # Set DPI to 150 to reduce memory consumption
    
    # Open the output file for writing
    with open(output_text_path, 'w', encoding='utf-8') as f:
        # Process each page image with OCR and write the results immediately to the output file
        for i, page in enumerate(pages):
            # Perform OCR on the page with the specified language
            page_text = pytesseract.image_to_string(page, lang=lang)
            
            # Write OCR result of the current page to the file
            f.write(page_text + "\n")
            
    print(f"Textextraktion abgeschlossen für {pdf_path}. Gespeichert unter: {output_text_path}")

def extract_list_from_text(text):
    # Define the start and end markers for the list extraction
    start_marker = "Wir bitten deshalb um Übersendung folgender Unterlagen in Kopie:"
    end_marker = "Bezüglich unserer Anfrage"

    # Use regular expression to extract the list part from the full text
    extracted_text = re.search(f"{re.escape(start_marker)}(.*?){re.escape(end_marker)}", text, re.DOTALL)

    if extracted_text:
        list_text = extracted_text.group(1).strip()
    else:
        list_text = "Keine Liste gefunden."
    
    return list_text

# Root folder containing PDFs and subfolders
root_pdf_folder = r"I:\Projekte\2024_07_MD_Anfragen\2023\Phase B\Positiv"  # Change this to your root folder path

# Folder to store the result text files
output_folder = r"I:\Projekte\2024_07_MD_Anfragen\Analyse\23\positiv"  # Change this to your output folder path

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Recursively iterate over all files in the root_pdf_folder and its subdirectories
for dirpath, dirnames, filenames in os.walk(root_pdf_folder):
    for filename in filenames:
        # Check if the file is a .pdf
        if filename.lower().endswith(".pdf"):
            # Full path of the current PDF file
            pdf_path = os.path.join(dirpath, filename)
            
            # Create the output text file path based on the PDF filename (e.g., abc.pdf -> abc.txt)
            output_text_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
            
            # Call the pdf_to_text function to process the PDF and save the text
            pdf_to_text(pdf_path, output_text_path)
            
            # Read the extracted text from the output file to extract the list part
            with open(output_text_path, 'r', encoding='utf-8') as file:
                full_text = file.read()
                list_text = extract_list_from_text(full_text)
            
            # Overwrite the output text file with the extracted list text
            with open(output_text_path, 'w', encoding='utf-8') as file:
                file.write(list_text)

            print(f"Textextraktion abgeschlossen für {pdf_path}. Gespeichert unter: {output_text_path}")


# # Version 6: Iteration durch Unterverzeichnisse (bei großen Dateien nicht möglich)
# def pdf_to_text(pdf_path, output_text_path, lang='deu', poppler_path=r'C:\Users\thm-efg\Downloads\Poppler\poppler-24.08.0\Library\bin'):
# # def pdf_to_text(pdf_path, output_text_path, lang='deu', poppler_path = r"C:\Users\thm-psr\Documents\poppler-24.08.0\Library\bin"):

#     # Umwandlung der Seite von PDF in ein Bild
#     pages = convert_from_path(pdf_path, 300, poppler_path=poppler_path)
    
#     # Liste zum Speichern des Textes jeder Seite
#     text = []

#     # Jede Seitenbild mit OCR verarbeiten
#     for i, page in enumerate(pages):
#         # OCR auf der Seite mit der angegebenen Sprache ausführen
#         page_text = pytesseract.image_to_string(page, lang=lang)
#         text.append(page_text)
        
#     # Alle Texte zu einer einzigen Zeichenkette kombinieren
#     full_text = "\n".join(text)
    
#     # Definieren der Start- und Endmarkierungen für die Listenauswertung
#     start_marker = "Wir bitten deshalb um Übersendung folgender Unterlagen in Kopie:"
#     end_marker = "Bezüglich unserer Anfrage"

#     # Reguläre Ausdruck verwenden, um den Listenteil aus dem gesamten Text zu extrahieren
#     extracted_text = re.search(f"{re.escape(start_marker)}(.*?){re.escape(end_marker)}", full_text, re.DOTALL)

#     if extracted_text:
#         list_text = extracted_text.group(1).strip()
#     else:
#         list_text = "Keine Liste gefunden."

#     # Den extrahierten Listentext in eine neue Textdatei mit dem gleichen Namen wie das PDF speichern
#     with open(output_text_path, 'w', encoding='utf-8') as f:
#         f.write(list_text)

#     print(f"Textextraktion abgeschlossen für {pdf_path}. Gespeichert unter: {output_text_path}")

# # Root-Ordner, der PDFs und Unterordner enthält
# root_pdf_folder = r"I:\Projekte\2024_07_MD_Anfragen\2023\Phase B"  # Ersetze dies durch den Pfad deines Root-Ordners

# # Ordner, in dem du die Ergebnis-Textdateien speichern möchtest
# output_folder = r"I:\Projekte\2024_07_MD_Anfragen\Analyse\23"  # Ersetze dies durch den Pfad deines Ausgabeverzeichnisses

# # Erstelle den Ausgabeverzeichnis, falls er noch nicht existiert
# os.makedirs(output_folder, exist_ok=True)

# # Rekursiv über alle Dateien im root_pdf_folder und seinen Unterverzeichnissen iterieren
# for dirpath, dirnames, filenames in os.walk(root_pdf_folder):
#     for filename in filenames:
#         # Überprüfen, ob die Datei eine .pdf-Erweiterung hat
#         if filename.lower().endswith(".pdf"):
#             # Vollständiger Pfad der aktuellen PDF-Datei
#             pdf_path = os.path.join(dirpath, filename)
            
#             # Erstelle den Ausgabepfad für die Textdatei basierend auf dem PDF-Dateinamen (z.B. abc.pdf -> abc.txt)
#             output_text_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
            
#             # Rufe die pdf_to_text-Funktion auf, um das PDF zu verarbeiten
#             pdf_to_text(pdf_path, output_text_path)

## Version 5
# def pdf_to_text(pdf_path, output_text_path, lang='deu', poppler_path=r'C:\Users\thm-efg\Downloads\Poppler\poppler-24.08.0\Library\bin'):
#     # Convert each page of the PDF to an image
#     pages = convert_from_path(pdf_path, 300, poppler_path=poppler_path)
    
#     # List to hold the text from each page
#     text = []

#     # Process each page image with OCR
#     for i, page in enumerate(pages):
#         # Perform OCR on the page with the specified language
#         page_text = pytesseract.image_to_string(page, lang=lang)
#         text.append(page_text)
        
#     # Combine all the text into a single string
#     full_text = "\n".join(text)
    
#     # Define the start and end markers for the list extraction
#     start_marker = "Wir bitten deshalb um Übersendung folgender Unterlagen in Kopie:"
#     end_marker = "Bezüglich unserer Anfrage"

#     # Use regular expression to extract the list part from the full text
#     extracted_text = re.search(f"{re.escape(start_marker)}(.*?){re.escape(end_marker)}", full_text, re.DOTALL)

#     if extracted_text:
#         list_text = extracted_text.group(1).strip()
#     else:
#         list_text = "No list found."

#     # Write the extracted list text to a new text file with the same name as the PDF
#     with open(output_text_path, 'w', encoding='utf-8') as f:
#         f.write(list_text)

#     print(f"Text extraction complete for {pdf_path}. Saved to: {output_text_path}")

# # Folder containing PDF files
# pdf_folder = r"I:\Projekte\2024_07_MD_Anfragen\2023\Phase A\Erörterungsverfahren"  # Replace this with the path to your folder containing PDFs

# # Folder where you want to save the result text files
# output_folder = r"C:\Users\thm-efg\Documents\Ergebnis\2023\Test"  # Replace this with the path to your desired output folder

# # Create the output folder if it doesn't exist
# os.makedirs(output_folder, exist_ok=True)

# # Iterate over all files in the PDF folder
# for filename in os.listdir(pdf_folder):
#     # Check if the file has a .pdf extension
#     if filename.lower().endswith(".pdf"):
#         # Full path of the current PDF file
#         pdf_path = os.path.join(pdf_folder, filename)
        
#         # Create the output text file path based on the PDF filename (e.g., abc.pdf -> abc.txt)
#         output_text_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
        
#         # Call the pdf_to_text function to process the PDF
#         pdf_to_text(pdf_path, output_text_path)
