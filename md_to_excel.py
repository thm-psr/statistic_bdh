import os
import re
from PyPDF2 import PdfReader
import pandas as pd

def extract_requested_documents(root_dir, target_filename="Prüfauftrag.pdf"):
    document_stats = {}
    
    # Muster für den interessierenden Abschnitt
    start_pattern = "Wir bitten deshalb um Übersendung folgender Unterlagen in Kopie:"
    end_pattern = "Bezüglich unserer Anfrage"
    
    # Durchlaufe alle Verzeichnisse und Dateien
    for dirpath, dirnames, filenames in os.walk(root_dir):
        print(f"Verarbeite Verzeichnis: {dirpath}")  # Debugging-Ausgabe
        for file in filenames:
            # Dateinamen in Kleinbuchstaben umwandeln für Vergleich
            if file.lower() == target_filename.lower():
                pdf_path = os.path.join(dirpath, file)
                print(f"Verarbeite Datei: {pdf_path}")  # Debugging-Ausgabe
                try:
                    # PDF lesen
                    reader = PdfReader(pdf_path)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text()

                    # Überprüfen, ob Text gefunden wurde
                    if not text.strip():
                        print(f"Keine Inhalte gefunden in {pdf_path}")
                        continue
                    
                    # Abschnitt extrahieren
                    match = re.search(f"{start_pattern}(.*?){end_pattern}", text, re.DOTALL | re.IGNORECASE)
                    if match:
                        document_list = match.group(1).strip().split("\n")
                        for doc in document_list:
                            doc_name = doc.strip()
                            if doc_name:
                                document_stats[doc_name] = document_stats.get(doc_name, 0) + 1
                    else:
                        print(f"Kein passender Abschnitt gefunden in {pdf_path}")
                except Exception as e:
                    print(f"Fehler beim Lesen der Datei {pdf_path}: {e}")
    
    return document_stats

def save_to_excel(document_stats, output_path):
    # Daten in ein DataFrame umwandeln
    df = pd.DataFrame(list(document_stats.items()), columns=["Dokument", "Anzahl"])
    df = df.sort_values(by="Anzahl", ascending=False)
    
    # Excel-Datei speichern
    df.to_excel(output_path, index=False)
    print(f"Statistiken wurden in '{output_path}' gespeichert.")

# Hauptverzeichnis angeben
root_directory = r"I:\Projekte\MD Anfragen 23_24\Anforderungen MD 2023\Anforderungen April 2023"

# Zielpfad für die Excel-Datei
output_excel_path = r"I:\Projekte\MD Anfragen 23_24\Analyse\document_statistics.xlsx"

# Extraktion starten
document_statistics = extract_requested_documents(root_directory)

# Ergebnisse in Excel speichern
if document_statistics:
    save_to_excel(document_statistics, output_excel_path)
else:
    print("Keine Daten gefunden, Excel-Datei wurde nicht erstellt.")
