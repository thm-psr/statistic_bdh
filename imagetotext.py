import os
import pytesseract
from PIL import Image

# Tesseract ocr Pfad
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Pfad mit Bilddatei
image_folder = r''
output_folder = r''

image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')

for filename in os.listdir(image_folder):
    if filename.lower().endswith(image_extensions):  # Check if file is an image
        image_path = os.path.join(image_folder, filename)
        try:
            # Open the image
            image = Image.open(image_path)
            
            # Perform OCR to extract text
            text = pytesseract.image_to_string(image)
            
            # Save text to a corresponding .txt file
            text_filename = os.path.splitext(filename)[0] + '.txt'
            text_path = os.path.join(output_folder, text_filename)
            
            with open(text_path, 'w', encoding='utf-8') as text_file:
                text_file.write(text)
            
            print(f"Processed {filename} -> {text_filename}")
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

'''
# Version 1
image = Image.open(r'C:\Users\thm-efg\Pictures\Screenshots\Screenshot 2024-11-21 142617.png')
text=pytesseract.image_to_string(image)

print(text)
'''
