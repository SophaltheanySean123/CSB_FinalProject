import pytesseract
from PIL import Image
import os

# Optional: specify the Tesseract command path (needed on some systems)
# For macOS with Homebrew:
# pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
# For Windows:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Folder containing images
image_folder = "images"

# Loop through all images in the folder
for filename in os.listdir(image_folder):
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".tiff")):
        img_path = os.path.join(image_folder, filename)
        print(f"🔍 Processing: {filename}")
        
        # Open the image
        img = Image.open(img_path)
        
        # Extract text using pytesseract
        text = pytesseract.image_to_string(img)
        
        # Print or save the extracted text
        print(f"📝 Extracted text from {filename}:\n{text}\n{'-'*50}")
