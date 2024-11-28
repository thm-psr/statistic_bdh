import os
import re
from PyPDF2 import PdfReader

# Auskommentieren wenn nicht benutzt

# Für sekundäre Fehlbelegung
# keywords = [
#     "Bestand die Notwendigkeit der stationären KH – Behandlung nach § 39 SGB V für die gesamte Dauer vom ... bis ...?",
#     "War die Überschreitung der oberen Grenzverweildauer in vollem Umfang medizinisch begründet?",
#     "War die Überschreitung der unteren Grenzverweildauer bzw. das Erreichen der UGVD medizinisch begründet?",
#     "Ist die Anzahl der Beatmungsstunden korrekt?",
#     "Sind die abgerechneten Zusatzentgelte korrekt?"
# ]

# Für primäre Fehlbelegung
keywords = [
    "Bestand die Notwendigkeit der stationären KH – Behandlung nach § 39 SGB V für die gesamte Dauer vom ... bis ...?",
    "Bestand die medizinische Notwendigkeit der Aufnahme in ein Krankenhaus zur vollstationären Behandlung?",
    "War die Überschreitung der unteren Grenzverweildauer bzw. das Erreichen der UGVD medizinisch begründet?"
]

# Für Kodierprüfung
# keywords = [
#     "Ist / sind die Prozedur(en) korrekt?",
#     "Ist / sind die Nebendiagnose(n) (ND) korrekt?",
#     "Ist die Hauptdiagnose (HD) korrekt?",
#     "Ist die Anzahl der Beatmungsstunden korrekt?",
#     "Sind die abgerechneten Zusatzentgelte korrekt?",
#     "Sonstige Fragen DRG: 8-981.22 neurol. Komplexbehandlung - war die Maßnahme über 72 Std. medizinisch indiziert?",
#     "Sonstige Fragen DRG: War der Verlauf zum Zeitpunkt der Aufnahme oder innerhalb der ersten 72 Stunden fluktuierend oder progredient und ergab sich im Anschluss an den Zeitraum nach 72 Stunden weiterhin die Indikation für die Behandlung auf der Stroke unit?"
# ]


document_list = [
    "(KH-) Entlassungsbericht (AD010103)", "Verlegungsbericht (intern) (AD010106)", "Pflegebericht (VL160105)",
    "Befunde Radiologie (ggf. MRT, CT) (DG020110)", "Befunde Sonographie (DG020111)", "Laborbefund extern (LB120102)",
    "Laborbefunde kumulativ (LB120103)", "Fieberkurve/Tageskurve (VL160106)", "Arztdokumentation (Visite) (AD060105)",
    "Ärztliche Anordnungen (AD060108)", "Ärztliche Verlaufsdokumentation (AD010110)", "Konsiliarbefund extern (AD060104)",
    "Konsiliarbefund intern (AD060103)", "Anamnese/Krankengeschichte (AU010101)", "Aufnahmebefund (AU010103)",
    "Narkoseprotokoll (OP010101)", "Befunde Histologie (ggf. Zytologie) (PT080102)",
    "Interventionsbericht (diagnostisch, therapeutisch) (AD010114)", "(Postoperativer) Überwachungsbogen (OP010102)",
    "Befund extern (AD020208)", "Vorbefunde (E-OP-Arzt-Berichte) (AD020208)", "Einsatzprotokoll (AU190101)",
    "Notaufnahmebericht (AU190102)", "Prämedikationsbogen (AM010301)", "Checkliste Entlassung (AM030102)",
    "Entlassungsplan (AM030103)", "Einweisung (AU050101)", "Blutgasanalyse (LB020101)", "Intensivkurven (VL090102)",
    "Beatmungsprotokolle und Berechnung der Beatmungsstunden (VL090101)", "Medikamentenbogen (TH130107)",
    "Chargendokumentation (OP150101)", "Intensivmedizinische Verlaufsdokumentation (ggf. TISS/SAPS-Einzelaufstellung) (VL090105)",
    "Therapieeinheiten/-nachweise Ergotherapie (TH060101)", "Therapieeinheiten/-nachweise Physiotherapie (TH060103)",
    "Therapieeinheiten/-nachweise Logopädie (TH060102)", "Teambesprechungsprotokoll (AD060107)",
    "Verlaufsdokumentation Sozialdienst (AM190201)", "Komplexbehandlungsunterlagen inkl. Mindestmerkmale (u. a. Assessments, Teambesprechungen, Therapieprotokolle, Verlaufsberichte) (SD110199)",
    "Barthel-Index (SD070201)", "(Zusatz-) Entgelte Nachweise (UB999996)", "Befunde Endoskopie (DG020105)",
    "Neurologische Komplexbehandlung: Unterlagen inkl. Mindestmerkmale (u. a. Überwachung, Therapieprotokolle, Verlaufsberichte) (SD110104)",
    "Operationsbericht(e) (OP150103)", "Wunddokumentation (VL230101)", "Laborbefunde Mikrobiologie (LB130101)",
    "Beurlaubung (AD020102)", "Entlassung gegen ärztlichen Rat (AM050108)", "Hämatransfusionsprotokolle (TH200103)",
    "Bestrahlungsprotokoll (TH020102)", "Chemotherapieprotokolle (TH130103)",
    "MRE/Nicht-MRE Komplexbehandlung: Unterlagen inkl. Mindestmerkmale (u.a. Isolierung, Schutzmaßnahmen, Therapieprotokolle, Verlaufsberichte) (SD110103)",
    "Strahlentherapieprotokolle (TH020102)", "Therapieprotokoll mit Radionukliden (TH020105)",
    "Funktionsdiagnostik Ergometrie (DG060119)", "Herzkatheterprotokoll (DG020106)",
    "Sonstiges KHB (AD010199) - Tumorkonferenzprotokoll", "Sonstiges TLB (LB120199) - Befund evozierter Potentiale",
    "Sonstiges TLB (LB120199) - Blutdruckprotokoll", "Sonstiges TLB (LB120199) - Echokardiographiebefund",
    "Sonstiges TLB (LB120199) - EEG-Auswertung", "Sonstiges TLB (LB120199) - EKG-Auswertung",
    "Sonstiges TLB (LB120199) - EMG-Befund", "Sonstiges TLB (LB120199) - Neurographiebefund"
]

def normalize_text(text):
    """
    Normalize the text by removing line breaks, extra spaces, and handling hyphenated words.
    """
    text = re.sub(r'\s+', ' ', text).strip()  # Replace line breaks and extra spaces
    text = re.sub(r'-\s', '', text)  # Fix hyphenated line breaks
    return text

def process_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = "\n".join([page.extract_text() for page in reader.pages])
        normalized_text = normalize_text(text)  # Normalize the extracted text

        # Check for the presence of the required term
        if pruefgegenstand not in normalized_text:
            print(f"Prüfgegenstand in {file_path} nicht gefunden.")
            return None, None

        # Check for the presence of at least one keyword
        keyword_matches = {keyword: normalized_text.count(keyword) for keyword in keywords}
        if not any(keyword_matches.values()):  # Skip if no keywords are found
            return None, None

        # Count document occurrences
        document_count = {doc: normalized_text.count(doc) for doc in document_list}

        return keyword_matches, document_count
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    return None, None

def traverse_and_process(input_directory, output_file):
    pdf_results = {}
    total_document_count_by_keyword = {keyword: {doc: 0 for doc in document_list} for keyword in keywords}

    for dirpath, _, filenames in os.walk(input_directory):
        for file in filenames:
            if file.startswith("Prüfauftrag") and file.endswith(".pdf"):
                file_path = os.path.join(dirpath, file)
                keyword_matches, document_count = process_pdf(file_path)
                if keyword_matches:
                    pdf_results[file_path] = {
                        "keyword_matches": keyword_matches,
                        "document_count": document_count
                    }

                    # Update total document count by keyword
                    for keyword, count in keyword_matches.items():
                        if count > 0:  # If keyword is matched, update the document count for each document
                            for doc, doc_count in document_count.items():
                                total_document_count_by_keyword[keyword][doc] += doc_count

    # Write results to output file
    with open(output_file, "w", encoding="utf-8") as f:
        for pdf, data in pdf_results.items():
            f.write(f"\nFile: {pdf}\n")
            f.write("Keyword Match Count:\n")
            for keyword, count in data["keyword_matches"].items():
                f.write(f"{keyword}: {count}\n")

            f.write("\nDocument Count:\n")
            for doc, count in data["document_count"].items():
                f.write(f"{doc}: {count}\n")

        f.write("\nTotal Document Count Across All PDFs (divided by Fragen):\n")
        for keyword, doc_count in total_document_count_by_keyword.items():
            f.write(f"\nFor Keyword: {keyword}\n")
            for doc, count in doc_count.items():
                f.write(f"{doc}: {count}\n")

    print(f"Results have been written to {output_file}")

# Define input and output paths

# Sekundäre Fehlbelegung | Kodierprüfung | Fragen zur Voraussetzung bestimmter Maßnahmen | Andere / weitere Prüfgegenstände
pruefgegenstand = "Kodierprüfung" 
input_directory = r"I:\Projekte\MD Anfragen 23_24\Anforderungen MD 2024"
output_directory = r"I:\Projekte\MD Anfragen 23_24\Analyse\Test"
output_file = os.path.join(output_directory, "result_primaere_fehlbelegung_2024.txt")

# Process PDFs and save results
traverse_and_process(input_directory, output_file)

# # # Version 3

# # Define keywords and document list
# keywords = [
#     "Bestand die Notwendigkeit der stationären KH – Behandlung nach § 39 SGB V für die gesamte Dauer vom ... bis ...?",
#     "War die Überschreitung der oberen Grenzverweildauer in vollem Umfang medizinisch begründet?",
#     "War die Überschreitung der unteren Grenzverweildauer bzw. das Erreichen der UGVD medizinisch begründet?"
# ]

# document_list = [
#     "(KH-) Entlassungsbericht (AD010103)", "Verlegungsbericht (intern) (AD010106)", "Pflegebericht (VL160105)",
#     "Befunde Radiologie (ggf. MRT, CT) (DG020110)", "Befunde Sonographie (DG020111)", "Laborbefund extern (LB120102)",
#     "Laborbefunde kumulativ (LB120103)", "Fieberkurve/Tageskurve (VL160106)", "Arztdokumentation (Visite) (AD060105)",
#     "Ärztliche Anordnungen (AD060108)", "Ärztliche Verlaufsdokumentation (AD010110)", "Konsiliarbefund extern (AD060104)",
#     "Konsiliarbefund intern (AD060103)", "Anamnese/Krankengeschichte (AU010101)", "Aufnahmebefund (AU010103)",
#     "Narkoseprotokoll (OP010101)", "Befunde Histologie (ggf. Zytologie) (PT080102)",
#     "Interventionsbericht (diagnostisch, therapeutisch) (AD010114)", "(Postoperativer) Überwachungsbogen (OP010102)",
#     "Befund extern (AD020208)", "Vorbefunde (E-OP-Arzt-Berichte) (AD020208)", "Einsatzprotokoll (AU190101)",
#     "Notaufnahmebericht (AU190102)", "Prämedikationsbogen (AM010301)", "Checkliste Entlassung (AM030102)",
#     "Entlassungsplan (AM030103)", "Einweisung (AU050101)", "Blutgasanalyse (LB020101)", "Intensivkurven (VL090102)",
#     "Beatmungsprotokolle und Berechnung der Beatmungsstunden (VL090101)", "Medikamentenbogen (TH130107)",
#     "Chargendokumentation (OP150101)", "Intensivmedizinische Verlaufsdokumentation (ggf. TISS/SAPS-Einzelaufstellung) (VL090105)",
#     "Therapieeinheiten/-nachweise Ergotherapie (TH060101)", "Therapieeinheiten/-nachweise Physiotherapie (TH060103)",
#     "Therapieeinheiten/-nachweise Logopädie (TH060102)", "Teambesprechungsprotokoll (AD060107)",
#     "Verlaufsdokumentation Sozialdienst (AM190201)", "Komplexbehandlungsunterlagen inkl. Mindestmerkmale (u. a. Assessments, Teambesprechungen, Therapieprotokolle, Verlaufsberichte) (SD110199)",
#     "Barthel-Index (SD070201)", "(Zusatz-) Entgelte Nachweise (UB999996)", "Befunde Endoskopie (DG020105)",
#     "Neurologische Komplexbehandlung: Unterlagen inkl. Mindestmerkmale (u. a. Überwachung, Therapieprotokolle, Verlaufsberichte) (SD110104)",
#     "Operationsbericht(e) (OP150103)", "Wunddokumentation (VL230101)", "Laborbefunde Mikrobiologie (LB130101)",
#     "Beurlaubung (AD020102)", "Entlassung gegen ärztlichen Rat (AM050108)", "Hämatransfusionsprotokolle (TH200103)",
#     "Bestrahlungsprotokoll (TH020102)", "Chemotherapieprotokolle (TH130103)",
#     "MRE/Nicht-MRE Komplexbehandlung: Unterlagen inkl. Mindestmerkmale (u.a. Isolierung, Schutzmaßnahmen, Therapieprotokolle, Verlaufsberichte) (SD110103)",
#     "Strahlentherapieprotokolle (TH020102)", "Therapieprotokoll mit Radionukliden (TH020105)",
#     "Funktionsdiagnostik Ergometrie (DG060119)", "Herzkatheterprotokoll (DG020106)",
#     "Sonstiges KHB (AD010199) - Tumorkonferenzprotokoll", "Sonstiges TLB (LB120199) - Befund evozierter Potentiale",
#     "Sonstiges TLB (LB120199) - Blutdruckprotokoll", "Sonstiges TLB (LB120199) - Echokardiographiebefund",
#     "Sonstiges TLB (LB120199) - EEG-Auswertung", "Sonstiges TLB (LB120199) - EKG-Auswertung",
#     "Sonstiges TLB (LB120199) - EMG-Befund", "Sonstiges TLB (LB120199) - Neurographiebefund"
# ]

# def normalize_text(text):
#     """
#     Normalize the text by removing line breaks, extra spaces, and handling hyphenated words.
#     """
#     # Replace line breaks and extra spaces
#     text = re.sub(r'\s+', ' ', text).strip()
#     # Fix hyphenated line breaks (e.g., "docu-\nment" -> "document")
#     text = re.sub(r'-\s', '', text)
#     return text

# def process_pdf(file_path):
#     try:
#         reader = PdfReader(file_path)
#         text = "\n".join([page.extract_text() for page in reader.pages])
#         normalized_text = normalize_text(text)  # Normalize the extracted text

#         # Check for the presence of at least one keyword
#         keyword_matches = {keyword: normalized_text.count(keyword) for keyword in keywords}
#         if not any(keyword_matches.values()):  # Skip if no keywords are found
#             return None, None, None

#         # Extract text between specific phrases
#         start_phrase = "Wir bitten deshalb um Übersendung folgender Unterlagen in Kopie:"
#         end_phrase = "Bezüglich unserer Anfrage beziehen wir uns auf"
#         extracted_section = re.search(f"{start_phrase}(.*?){end_phrase}", normalized_text, re.DOTALL)

#         unterfrage_section = None
#         if extracted_section:
#             extracted_text = extracted_section.group(1).strip()

#             # Find and extract the "Unterfrage" part
#             unterfrage_index = extracted_text.find("Unterfrage")
#             if unterfrage_index != -1:
#                 unterfrage_section = extracted_text[unterfrage_index:]

#             # Count document occurrences
#             document_count = {doc: normalized_text.count(doc) for doc in document_list}

#             return keyword_matches, unterfrage_section, document_count
#     except Exception as e:
#         print(f"Error processing {file_path}: {e}")
#     return None, None, None

# # Traverse directories and process PDFs
# def traverse_and_process(input_directory, output_file):
#     pdf_results = {}
#     total_document_count_by_keyword = {keyword: {doc: 0 for doc in document_list} for keyword in keywords}

#     for dirpath, _, filenames in os.walk(input_directory):
#         for file in filenames:
#             if file.startswith("Prüfauftrag") and file.endswith(".pdf"):
#                 file_path = os.path.join(dirpath, file)
#                 keyword_matches, unterfrage_section, document_count = process_pdf(file_path)
#                 if keyword_matches:
#                     pdf_results[file_path] = {
#                         "keyword_matches": keyword_matches,
#                         "unterfrage_section": unterfrage_section,
#                         "document_count": document_count
#                     }

#                     # Update total document count by keyword
#                     for keyword, count in keyword_matches.items():
#                         if count > 0:  # If keyword is matched, update the document count for each document
#                             for doc, doc_count in document_count.items():
#                                 total_document_count_by_keyword[keyword][doc] += doc_count

#     # Write results to output file
#     with open(output_file, "w", encoding="utf-8") as f:
#         for pdf, data in pdf_results.items():
#             f.write(f"\nFile: {pdf}\n")
#             f.write("Keyword Match Count:\n")
#             for keyword, count in data["keyword_matches"].items():
#                 f.write(f"{keyword}: {count}\n")

#             if data['unterfrage_section']:
#                 f.write("Unterfrage Section:\n")
#                 f.write(f"{data['unterfrage_section']}\n")

#             f.write("\nDocument Count:\n")
#             for doc, count in data["document_count"].items():
#                 f.write(f"{doc}: {count}\n")

#         # Write total document count across all PDFs, divided by each keyword
#         f.write("\nTotal Document Count Across All PDFs (divided by Fragen):\n")
#         for keyword, doc_count in total_document_count_by_keyword.items():
#             f.write(f"\nFor Keyword: {keyword}\n")
#             for doc, count in doc_count.items():
#                 f.write(f"{doc}: {count}\n")

#     print(f"Results have been written to {output_file}")

# # Define input and output paths
# input_directory = r"I:\Projekte\MD Anfragen 23_24\Anforderungen MD 2024\08 Anforderungen August 2024"
# output_directory = r"I:\Projekte\MD Anfragen 23_24\Analyse\Test"
# output_file = os.path.join(output_directory, "result_august_2024.txt")

# # Process PDFs and save results
# traverse_and_process(input_directory, output_file)



# # # Version 2: Ohne Filter für Unterfrage

# # Define keywords and document list
# keywords = [
#     "Bestand die Notwendigkeit der stationären KH – Behandlung nach § 39 SGB V für die gesamte Dauer vom ... bis ...?",
#     "War die Überschreitung der oberen Grenzverweildauer in vollem Umfang medizinisch begründet?",
#     "War die Überschreitung der unteren Grenzverweildauer bzw. das Erreichen der UGVD medizinisch begründet?"
# ]

# document_list = [
#     "(KH-) Entlassungsbericht (AD010103)", "Verlegungsbericht (intern) (AD010106)", "Pflegebericht (VL160105)",
#     "Befunde Radiologie (ggf. MRT, CT) (DG020110)", "Befunde Sonographie (DG020111)", "Laborbefund extern (LB120102)",
#     "Laborbefunde kumulativ (LB120103)", "Fieberkurve/Tageskurve (VL160106)", "Arztdokumentation (Visite) (AD060105)",
#     "Ärztliche Anordnungen (AD060108)", "Ärztliche Verlaufsdokumentation (AD010110)", "Konsiliarbefund extern (AD060104)",
#     "Konsiliarbefund intern (AD060103)", "Anamnese/Krankengeschichte (AU010101)", "Aufnahmebefund (AU010103)",
#     "Narkoseprotokoll (OP010101)", "Befunde Histologie (ggf. Zytologie) (PT080102)",
#     "Interventionsbericht (diagnostisch, therapeutisch) (AD010114)", "(Postoperativer) Überwachungsbogen (OP010102)",
#     "Befund extern (AD020208)", "Vorbefunde (E-OP-Arzt-Berichte) (AD020208)", "Einsatzprotokoll (AU190101)",
#     "Notaufnahmebericht (AU190102)", "Prämedikationsbogen (AM010301)", "Checkliste Entlassung (AM030102)",
#     "Entlassungsplan (AM030103)", "Einweisung (AU050101)", "Blutgasanalyse (LB020101)", "Intensivkurven (VL090102)",
#     "Beatmungsprotokolle und Berechnung der Beatmungsstunden (VL090101)", "Medikamentenbogen (TH130107)",
#     "Chargendokumentation (OP150101)", "Intensivmedizinische Verlaufsdokumentation (ggf. TISS/SAPS-Einzelaufstellung) (VL090105)",
#     "Therapieeinheiten/-nachweise Ergotherapie (TH060101)", "Therapieeinheiten/-nachweise Physiotherapie (TH060103)",
#     "Therapieeinheiten/-nachweise Logopädie (TH060102)", "Teambesprechungsprotokoll (AD060107)",
#     "Verlaufsdokumentation Sozialdienst (AM190201)", "Komplexbehandlungsunterlagen inkl. Mindestmerkmale (u. a. Assessments, Teambesprechungen, Therapieprotokolle, Verlaufsberichte) (SD110199)",
#     "Barthel-Index (SD070201)", "(Zusatz-) Entgelte Nachweise (UB999996)", "Befunde Endoskopie (DG020105)",
#     "Neurologische Komplexbehandlung: Unterlagen inkl. Mindestmerkmale (u. a. Überwachung, Therapieprotokolle, Verlaufsberichte) (SD110104)",
#     "Operationsbericht(e) (OP150103)", "Wunddokumentation (VL230101)", "Laborbefunde Mikrobiologie (LB130101)",
#     "Beurlaubung (AD020102)", "Entlassung gegen ärztlichen Rat (AM050108)", "Hämatransfusionsprotokolle (TH200103)",
#     "Bestrahlungsprotokoll (TH020102)", "Chemotherapieprotokolle (TH130103)",
#     "MRE/Nicht-MRE Komplexbehandlung: Unterlagen inkl. Mindestmerkmale (u.a. Isolierung, Schutzmaßnahmen, Therapieprotokolle, Verlaufsberichte) (SD110103)",
#     "Strahlentherapieprotokolle (TH020102)", "Therapieprotokoll mit Radionukliden (TH020105)",
#     "Funktionsdiagnostik Ergometrie (DG060119)", "Herzkatheterprotokoll (DG020106)",
#     "Sonstiges KHB (AD010199) - Tumorkonferenzprotokoll", "Sonstiges TLB (LB120199) - Befund evozierter Potentiale",
#     "Sonstiges TLB (LB120199) - Blutdruckprotokoll", "Sonstiges TLB (LB120199) - Echokardiographiebefund",
#     "Sonstiges TLB (LB120199) - EEG-Auswertung", "Sonstiges TLB (LB120199) - EKG-Auswertung",
#     "Sonstiges TLB (LB120199) - EMG-Befund", "Sonstiges TLB (LB120199) - Neurographiebefund"
# ]

# def process_pdf(file_path):
#     try:
#         reader = PdfReader(file_path)
#         text = "\n".join([page.extract_text() for page in reader.pages])

#         # Check for the presence of at least one keyword
#         keyword_matches = {keyword: text.count(keyword) for keyword in keywords}
#         if not any(keyword_matches.values()):  # Skip if no keywords are found
#             return None, None, None

#         # Extract text between specific phrases
#         start_phrase = "Wir bitten deshalb um Übersendung folgender Unterlagen in Kopie:"
#         end_phrase = "Bezüglich unserer Anfrage beziehen wir uns auf"
#         extracted_section = re.search(f"{start_phrase}(.*?){end_phrase}", text, re.DOTALL)

#         unterfrage_section = None
#         if extracted_section:
#             extracted_text = extracted_section.group(1).strip()

#             # Find and extract the "Unterfrage" part
#             unterfrage_index = extracted_text.find("Unterfrage")
#             if unterfrage_index != -1:
#                 unterfrage_section = extracted_text[unterfrage_index:]

#             # Count document occurrences
#             document_count = {doc: extracted_text.count(doc) for doc in document_list}

#             return keyword_matches, unterfrage_section, document_count
#     except Exception as e:
#         print(f"Error processing {file_path}: {e}")
#     return None, None, None

# # Traverse directories and process PDFs
# def traverse_and_process(input_directory, output_file):
#     pdf_results = {}
#     total_document_count = {doc: 0 for doc in document_list}  # Initialize total document count dictionary

#     for dirpath, _, filenames in os.walk(input_directory):
#         for file in filenames:
#             if file.startswith("Prüfauftrag") and file.endswith(".pdf"):
#                 file_path = os.path.join(dirpath, file)
#                 keyword_matches, unterfrage_section, document_count = process_pdf(file_path)
#                 if keyword_matches:
#                     pdf_results[file_path] = {
#                         "keyword_matches": keyword_matches,
#                         "unterfrage_section": unterfrage_section,
#                         "document_count": document_count
#                     }

#                     # Update total document count
#                     for doc, count in document_count.items():
#                         total_document_count[doc] += count

#     # Write results to output file
#     with open(output_file, "w", encoding="utf-8") as f:
#         for pdf, data in pdf_results.items():
#             f.write(f"\nFile: {pdf}\n")
#             f.write("Keyword Match Count:\n")
#             for keyword, count in data["keyword_matches"].items():
#                 f.write(f"{keyword}: {count}\n")

#             if data['unterfrage_section']:
#                 f.write("Unterfrage Section:\n")
#                 f.write(f"{data['unterfrage_section']}\n")

#             f.write("\nDocument Count:\n")
#             for doc, count in data["document_count"].items():
#                 f.write(f"{doc}: {count}\n")

#         # Write total document count across all PDFs
#         f.write("\nTotal Document Count Across All PDFs:\n")
#         for doc, total_count in total_document_count.items():
#             f.write(f"{doc}: {total_count}\n")

#     print(f"Results have been written to {output_file}")

# # Define input and output paths
# input_directory = r"I:\Projekte\MD Anfragen 23_24\Anforderungen MD 2024\08 Anforderungen August 2024"
# output_directory = r"I:\Projekte\MD Anfragen 23_24\Analyse\Test"
# output_file = os.path.join(output_directory, "result_august_2024.txt")

# # Process PDFs and save results
# traverse_and_process(input_directory, output_file)


# # # Version 1
# # Ergebnis als txt Datei

# # Define keywords and document list
# keywords = [
#     "Bestand die Notwendigkeit der stationären KH – Behandlung nach § 39 SGB V für die gesamte Dauer vom ... bis ...?",
#     "Ist die Anzahl der Beatmungsstunden korrekt?",
#     "War die Überschreitung der oberen Grenzverweildauer in vollem Umfang medizinisch begründet?",
#     "War die Überschreitung der unteren Grenzverweildauer bzw. das Erreichen der UGVD medizinisch begründet?"
# ]

# document_list = [
#     "(KH-) Entlassungsbericht (AD010103)", "Verlegungsbericht (intern) (AD010106)", "Pflegebericht (VL160105)",
#     "Befunde Radiologie (ggf. MRT, CT) (DG020110)", "Befunde Sonographie (DG020111)", "Laborbefund extern (LB120102)",
#     "Laborbefunde kumulativ (LB120103)", "Fieberkurve/Tageskurve (VL160106)", "Arztdokumentation (Visite) (AD060105)",
#     "Ärztliche Anordnungen (AD060108)", "Ärztliche Verlaufsdokumentation (AD010110)", "Konsiliarbefund extern (AD060104)",
#     "Konsiliarbefund intern (AD060103)", "Anamnese/Krankengeschichte (AU010101)", "Aufnahmebefund (AU010103)",
#     "Narkoseprotokoll (OP010101)", "Befunde Histologie (ggf. Zytologie) (PT080102)",
#     "Interventionsbericht (diagnostisch, therapeutisch) (AD010114)", "(Postoperativer) Überwachungsbogen (OP010102)",
#     "Befund extern (AD020208)", "Vorbefunde (E-OP-Arzt-Berichte) (AD020208)", "Einsatzprotokoll (AU190101)",
#     "Notaufnahmebericht (AU190102)", "Prämedikationsbogen (AM010301)", "Checkliste Entlassung (AM030102)",
#     "Entlassungsplan (AM030103)", "Einweisung (AU050101)", "Blutgasanalyse (LB020101)", "Intensivkurven (VL090102)",
#     "Beatmungsprotokolle und Berechnung der Beatmungsstunden (VL090101)", "Medikamentenbogen (TH130107)",
#     "Chargendokumentation (OP150101)", "Intensivmedizinische Verlaufsdokumentation (ggf. TISS/SAPS-Einzelaufstellung) (VL090105)",
#     "Therapieeinheiten/-nachweise Ergotherapie (TH060101)", "Therapieeinheiten/-nachweise Physiotherapie (TH060103)",
#     "Therapieeinheiten/-nachweise Logopädie (TH060102)", "Teambesprechungsprotokoll (AD060107)",
#     "Verlaufsdokumentation Sozialdienst (AM190201)", "Komplexbehandlungsunterlagen inkl. Mindestmerkmale (u. a. Assessments, Teambesprechungen, Therapieprotokolle, Verlaufsberichte) (SD110199)",
#     "Barthel-Index (SD070201)", "(Zusatz-) Entgelte Nachweise (UB999996)", "Befunde Endoskopie (DG020105)",
#     "Neurologische Komplexbehandlung: Unterlagen inkl. Mindestmerkmale (u. a. Überwachung, Therapieprotokolle, Verlaufsberichte) (SD110104)",
#     "Operationsbericht(e) (OP150103)", "Wunddokumentation (VL230101)", "Laborbefunde Mikrobiologie (LB130101)",
#     "Beurlaubung (AD020102)", "Entlassung gegen ärztlichen Rat (AM050108)", "Hämatransfusionsprotokolle (TH200103)",
#     "Bestrahlungsprotokoll (TH020102)", "Chemotherapieprotokolle (TH130103)",
#     "MRE/Nicht-MRE Komplexbehandlung: Unterlagen inkl. Mindestmerkmale (u.a. Isolierung, Schutzmaßnahmen, Therapieprotokolle, Verlaufsberichte) (SD110103)",
#     "Strahlentherapieprotokolle (TH020102)", "Therapieprotokoll mit Radionukliden (TH020105)",
#     "Funktionsdiagnostik Ergometrie (DG060119)", "Herzkatheterprotokoll (DG020106)",
#     "Sonstiges KHB (AD010199) - Tumorkonferenzprotokoll", "Sonstiges TLB (LB120199) - Befund evozierter Potentiale",
#     "Sonstiges TLB (LB120199) - Blutdruckprotokoll", "Sonstiges TLB (LB120199) - Echokardiographiebefund",
#     "Sonstiges TLB (LB120199) - EEG-Auswertung", "Sonstiges TLB (LB120199) - EKG-Auswertung",
#     "Sonstiges TLB (LB120199) - EMG-Befund", "Sonstiges TLB (LB120199) - Neurographiebefund"
# ]

# def process_pdf(file_path):
#     try:
#         reader = PdfReader(file_path)
#         text = "\n".join([page.extract_text() for page in reader.pages])

#         # Check for the presence of at least one keyword
#         keyword_matches = {keyword: text.count(keyword) for keyword in keywords}
#         if not any(keyword_matches.values()):  # Skip if no keywords are found
#             return None, None

#         # Ensure "Unterfrage" does not appear after any matched keyword
#         for keyword, count in keyword_matches.items():
#             if count > 0:  # Only consider matched keywords
#                 keyword_index = text.find(keyword)
#                 if keyword_index != -1:
#                     unterfrage_index = text.find("Unterfrage", keyword_index)
#                     if unterfrage_index != -1:  # Skip this PDF if "Unterfrage" follows the keyword
#                         return None, None

#         # Extract text between specific phrases
#         start_phrase = "Wir bitten deshalb um Übersendung folgender Unterlagen in Kopie:"
#         end_phrase = "Bezüglich unserer Anfrage beziehen wir uns auf"
#         extracted_section = re.search(f"{start_phrase}(.*?){end_phrase}", text, re.DOTALL)

#         if extracted_section:
#             extracted_text = extracted_section.group(1).strip()

#             # Count document occurrences
#             document_count = {doc: extracted_text.count(doc) for doc in document_list}

#             return keyword_matches, document_count
#     except Exception as e:
#         print(f"Error processing {file_path}: {e}")
#     return None, None

# # Traverse directories and process PDFs
# def traverse_and_process(input_directory, output_file):
#     pdf_results = {}
#     total_document_count = {doc: 0 for doc in document_list}  # Initialize total document count dictionary

#     for dirpath, _, filenames in os.walk(input_directory):
#         for file in filenames:
#             if file.startswith("Prüfauftrag") and file.endswith(".pdf"):
#                 file_path = os.path.join(dirpath, file)
#                 extracted_text, document_count = process_pdf(file_path)
#                 if extracted_text:
#                     pdf_results[file_path] = {
#                         "extracted_text": extracted_text,
#                         "document_count": document_count
#                     }

#                     # Update total document count
#                     for doc, count in document_count.items():
#                         total_document_count[doc] += count

#     # Write results to output file
#     with open(output_file, "w", encoding="utf-8") as f:
#         for pdf, data in pdf_results.items():
#             f.write(f"\nFile: {pdf}\n")
#             f.write("Extracted Section:\n")
#             f.write(f"{data['extracted_text']}\n")
#             f.write("\nDocument Count:\n")
#             for doc, count in data["document_count"].items():
#                 f.write(f"{doc}: {count}\n")

#         # Write total document count across all PDFs
#         f.write("\nTotal Document Count Across All PDFs:\n")
#         for doc, total_count in total_document_count.items():
#             f.write(f"{doc}: {total_count}\n")

#     print(f"Results have been written to {output_file}")

# # Define input and output paths
# input_directory = r"I:\Projekte\MD Anfragen 23_24\Anforderungen MD 2024\08 Anforderungen August 2024"
# output_directory = r"I:\Projekte\MD Anfragen 23_24\Analyse\Test"
# output_file = os.path.join(output_directory, "result_august_2024.txt")

# # Process PDFs and save results
# traverse_and_process(input_directory, output_file)
