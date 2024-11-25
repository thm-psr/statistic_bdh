import os
import re
from PyPDF2 import PdfReader
import pandas as pd

def extract_requested_documents(root_dir, target_filename="Prüfauftrag.pdf"):
    document_stats = {}
    total_files = 0  # Zählt die Gesamtzahl der Prüfauftrag.pdf
    no_structure_count = 0  # Zählt Dateien ohne relevante Struktur
    
    # Muster für den interessierenden Abschnitt
    start_pattern = r"Wir bitten deshalb um Übersendung folgender Unterlagen in Kopie:"
    end_pattern = r"Bezüglich unserer Anfrage"
    
    # Regulärer Ausdruck für Dokumente im Format "Text (ID)"
    document_pattern = r"([^\n]+?\s*\([A-Z]{2}\d{6}\))"
    
    # Durchlaufe alle Verzeichnisse und Dateien
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for file in filenames:
            if file.lower() == target_filename.lower():
                total_files += 1  # Zähle die Datei
                pdf_path = os.path.join(dirpath, file)
                try:
                    # PDF lesen
                    reader = PdfReader(pdf_path)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text()

                    # Überprüfen, ob Text gefunden wurde
                    if not text.strip():
                        no_structure_count += 1
                        continue
                    
                    # Abschnitt extrahieren
                    match = re.search(f"{start_pattern}(.*?){end_pattern}", text, re.DOTALL | re.IGNORECASE)
                    if match:
                        document_text = match.group(1).strip()
                        
                        # Dokumente extrahieren basierend auf dem Muster
                        documents = re.findall(document_pattern, document_text)
                        
                        if not documents:  # Falls kein Dokument gefunden wurde
                            no_structure_count += 1
                        
                        for doc in documents:
                            doc_name = doc.strip()
                            if doc_name:
                                document_stats[doc_name] = document_stats.get(doc_name, 0) + 1
                    else:
                        no_structure_count += 1  # Abschnitt nicht gefunden
                except Exception as e:
                    print(f"Fehler beim Lesen der Datei {pdf_path}: {e}")
    
    return document_stats, total_files, no_structure_count

def save_to_excel(document_stats, total_files, no_structure_count, output_path):
    # Daten in ein DataFrame umwandeln
    df = pd.DataFrame(list(document_stats.items()), columns=["Angefragte Dokumente", "Häufigkeit"])
    df = df.sort_values(by="Häufigkeit", ascending=False)
    
    # Zusätzliche Informationen hinzufügen
    summary = pd.DataFrame([
        {"Angefragte Dokumente": "Total Prüfauftrag.pdf gelesen", "Häufigkeit": total_files},
        {"Angefragte Dokumente": "Prüfauftrag.pdf ohne Struktur/Pattern", "Häufigkeit": no_structure_count},
        {"Angefragte Dokumente": "", "Häufigkeit": ""}
    ])
    
    # Zusammenführen
    df = pd.concat([summary, df], ignore_index=True)
    
    # Excel-Datei speichern
    df.to_excel(output_path, index=False)
    print(f"Statistiken wurden in '{output_path}' gespeichert.")

# Hauptverzeichnis angeben
root_directory = r"I:\Projekte\MD Anfragen 23_24\Anforderungen MD 2023"

# Zielpfad für die Excel-Datei
output_excel_path = r"I:\Projekte\MD Anfragen 23_24\Analyse\md_statistik2023.xlsx"

# Extraktion starten
document_statistics, total_files, no_structure_count = extract_requested_documents(root_directory)

# Ergebnisse in Excel speichern
save_to_excel(document_statistics, total_files, no_structure_count, output_excel_path)
