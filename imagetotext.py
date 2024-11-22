import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image = Image.open(r'C:\Users\thm-efg\Pictures\Screenshots\Screenshot 2024-11-21 142617.png')
text=pytesseract.image_to_string(image)

print(text)