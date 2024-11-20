import re
import os
from pdf2image import convert_from_path
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 

#Version 6
def pdf_to_text(pdf_path, output_text_path, lang='deu', poppler_path=r'C:\Users\thm-efg\Downloads\Poppler\poppler-24.08.0\Library\bin'):
    # Umwandlung der Seite von PDF in ein Bild
    pages = convert_from_path(pdf_path, 300, poppler_path=poppler_path)
    
    # Liste zum Speichern des Textes jeder Seite
    text = []

    # Jede Seitenbild mit OCR verarbeiten
    for i, page in enumerate(pages):
        # OCR auf der Seite mit der angegebenen Sprache ausführen
        page_text = pytesseract.image_to_string(page, lang=lang)
        text.append(page_text)
        
    # Alle Texte zu einer einzigen Zeichenkette kombinieren
    full_text = "\n".join(text)
    
    # Definieren der Start- und Endmarkierungen für die Listenauswertung
    start_marker = "Wir bitten deshalb um Übersendung folgender Unterlagen in Kopie:"
    end_marker = "Bezüglich unserer Anfrage"

    # Reguläre Ausdruck verwenden, um den Listenteil aus dem gesamten Text zu extrahieren
    extracted_text = re.search(f"{re.escape(start_marker)}(.*?){re.escape(end_marker)}", full_text, re.DOTALL)

    if extracted_text:
        list_text = extracted_text.group(1).strip()
    else:
        list_text = "Keine Liste gefunden."

    # Den extrahierten Listentext in eine neue Textdatei mit dem gleichen Namen wie das PDF speichern
    with open(output_text_path, 'w', encoding='utf-8') as f:
        f.write(list_text)

    print(f"Textextraktion abgeschlossen für {pdf_path}. Gespeichert unter: {output_text_path}")

# Root-Ordner, der PDFs und Unterordner enthält
root_pdf_folder = r"I:\Projekte\2024_07_MD_Anfragen\2023\Phase B"  # Ersetze dies durch den Pfad deines Root-Ordners

# Ordner, in dem du die Ergebnis-Textdateien speichern möchtest
output_folder = r"I:\Projekte\2024_07_MD_Anfragen\Analyse\23"  # Ersetze dies durch den Pfad deines Ausgabeverzeichnisses

# Erstelle den Ausgabeverzeichnis, falls er noch nicht existiert
os.makedirs(output_folder, exist_ok=True)

# Rekursiv über alle Dateien im root_pdf_folder und seinen Unterverzeichnissen iterieren
for dirpath, dirnames, filenames in os.walk(root_pdf_folder):
    for filename in filenames:
        # Überprüfen, ob die Datei eine .pdf-Erweiterung hat
        if filename.lower().endswith(".pdf"):
            # Vollständiger Pfad der aktuellen PDF-Datei
            pdf_path = os.path.join(dirpath, filename)
            
            # Erstelle den Ausgabepfad für die Textdatei basierend auf dem PDF-Dateinamen (z.B. abc.pdf -> abc.txt)
            output_text_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
            
            # Rufe die pdf_to_text-Funktion auf, um das PDF zu verarbeiten
            pdf_to_text(pdf_path, output_text_path)

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

# from pdf2image import convert_from_path
# import pytesseract
# from PIL import Image
# import os

## Version 1
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust this path if necessary

# def pdf_to_text(pdf_path, output_text_path, lang='deu', poppler_path=r'C:\Users\thm-efg\Downloads\Poppler\poppler-24.08.0\Library\bin'):
#     # Convert each page of the PDF to an image
#     pages = convert_from_path(pdf_path, 300, poppler_path=poppler_path)
    
#     # Flag to track if we have found the start and end markers
#     found_text = False
#     full_text = ""

#     # Process each page image with OCR
#     for i, page in enumerate(pages):
#         # Perform OCR on the page with the specified language
#         page_text = pytesseract.image_to_string(page, lang=lang)
        
#         # Check if the page contains the start and end phrases
#         if "Zu prüfende Prozeduren" in page_text or "Wir bitten deshalb um Übersendung folgender Unterlagen in Kopie:" in page_text:
#             # Start accumulating text from here
#             found_text = True
#             full_text += page_text
        
#         if found_text:
#             full_text += page_text
#             # Check if the text contains the ending phrase
#             if "Bezüglich unserer Anfrage beziehen wir uns auf" in page_text:
#                 break  # Stop processing further pages as we've found the relevant text

#     if found_text:
#         # Write the extracted text to a file
#         with open(output_text_path, 'w', encoding='utf-8') as f:
#             f.write(full_text.strip())  # Remove any extra whitespace around the text

#         print("Text extraction complete. Saved to:", output_text_path)
#     else:
#         print("Relevant text not found in the PDF.")

# # Specify your PDF path and output text file path
# pdf_path = r'I:\Projekte\2024_07_MD_Anfragen\2023\Phase A\Erörterungsverfahren\2231416 Haupt, Helmut.pdf'
# output_text_path = 'result.txt'

# # Run the OCR extraction
# pdf_to_text(pdf_path, output_text_path)

# Version 2
# Specify the path to Tesseract-OCR executable
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust this path if necessary

# def pdf_to_text(pdf_path, lang='deu', poppler_path=r'C:\Users\thm-efg\Downloads\Poppler\poppler-24.08.0\Library\bin'):
#     # Get the file name (without extension) from the pdf_path
#     base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
#     # Create the output text file path with the same name as the PDF but with .txt extension
#     output_text_path = f'{base_name}.txt'
    
#     # Convert each page of the PDF to an image
#     pages = convert_from_path(pdf_path, 300, poppler_path=poppler_path)
    
#     # Flag to track if we have found the start and end markers
#     found_text = False
#     full_text = ""

#     # Process each page image with OCR
#     for i, page in enumerate(pages):
#         # Perform OCR on the page with the specified language
#         page_text = pytesseract.image_to_string(page, lang=lang)
        
#         # Check if the page contains the start and end phrases
#         if "Zu prüfende Prozeduren" in page_text or "Wir bitten deshalb um Übersendung folgender Unterlagen in Kopie:" in page_text:
#             # Start accumulating text from here
#             found_text = True
#             full_text += page_text
        
#         if found_text:
#             full_text += page_text
#             # Check if the text contains the ending phrase
#             if "Bezüglich unserer Anfrage beziehen wir uns auf" in page_text:
#                 break  # Stop processing further pages as we've found the relevant text

#     if found_text:
#         # Write the extracted text to the file with the same name as the PDF
#         with open(output_text_path, 'w', encoding='utf-8') as f:
#             f.write(full_text.strip())  # Remove any extra whitespace around the text

#         print(f"Text extraction complete. Saved to: {output_text_path}")
#     else:
#         print("Relevant text not found in the PDF.")

# # Specify your PDF path
# pdf_path = r'I:\Projekte\2024_07_MD_Anfragen\2023\Phase A\Erörterungsverfahren\2231416 Haupt, Helmut.pdf'

# # Run the OCR extraction
# pdf_to_text(pdf_path)

#Version 3

# Specify the path to Tesseract-OCR executable
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust this path if necessary

# def pdf_to_text(pdf_path, lang='deu', poppler_path=r'C:\Users\thm-efg\Downloads\Poppler\poppler-24.08.0\Library\bin'):
#     # Get the file name (without extension) from the pdf_path
#     base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
#     # Create the output text file path with the same name as the PDF but with .txt extension
#     output_text_path = f'{base_name}.txt'
    
#     # Convert each page of the PDF to an image
#     pages = convert_from_path(pdf_path, 300, poppler_path=poppler_path)
    
#     # Flag to track if we have found the start and end markers
#     found_text = False
#     full_text = ""
    
#     start_marker = "Wir bitten deshalb um Übersendung folgender Unterlagen in Kopie:"
#     end_marker = "Bezüglich unserer Anfrage beziehen wir uns auf"
    
#     # Process each page image with OCR
#     for i, page in enumerate(pages):
#         # Perform OCR on the page with the specified language
#         page_text = pytesseract.image_to_string(page, lang=lang)

#         # If we haven't found the start marker yet, skip pages until we do
#         if start_marker in page_text:
#             found_text = True
#             # Add the text from the start marker
#             full_text += page_text

#         if found_text:
#             full_text += page_text
#             # Once we reach the end marker, stop accumulating text
#             if end_marker in page_text:
#                 break  # Stop processing further pages as we've found the relevant text

#     # Extract the text between the start and end markers using regex
#     if found_text:
#         # Extract the text between the start and end markers
#         extracted_text = re.search(f"{re.escape(start_marker)}(.*?){re.escape(end_marker)}", full_text, re.DOTALL)
        
#         if extracted_text:
#             # Extract the relevant part of the text (the list between the start and end markers)
#             list_text = extracted_text.group(1).strip()
            
#             # Write the extracted list to the output text file
#             with open(output_text_path, 'w', encoding='utf-8') as f:
#                 f.write(list_text)

#             print(f"Text extraction complete. Saved to: {output_text_path}")
#         else:
#             print("Relevant text not found between the markers.")
#     else:
#         print("Start marker not found in the PDF.")

# # Specify your PDF path
# pdf_path = r'I:\Projekte\2024_07_MD_Anfragen\2023\Phase A\Negativ\Fehlbelegung\Primäre Fehlbelegung\2230200 Walter, Werner.pdf'

# # Run the OCR extraction
# pdf_to_text(pdf_path)

#Version 4

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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
# pdf_folder = r"I:\Projekte\2024_07_MD_Anfragen\2023\Phase A\Negativ\Kodierfehler\ICD Kodierfehler\HD"

# # Iterate over all files in the folder
# for filename in os.listdir(pdf_folder):
#     # Check if the file has a .pdf extension
#     if filename.lower().endswith(".pdf"):
#         # Full path of the current PDF file
#         pdf_path = os.path.join(pdf_folder, filename)
        
#         # Create the output text file path based on the PDF filename (e.g., abc.pdf -> abc.txt)
#         output_text_path = os.path.join(pdf_folder, f"{os.path.splitext(filename)[0]}.txt")
        
#         # Call the pdf_to_text function to process the PDF
#         pdf_to_text(pdf_path, output_text_path)