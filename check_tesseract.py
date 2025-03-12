import pytesseract
from PIL import Image
import os

# List of common Tesseract installation paths
possible_paths = [
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    r'C:\Users\DELL\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
]

print("Checking for Tesseract installation...")
print("\nChecking common installation paths:")
for path in possible_paths:
    if os.path.exists(path):
        print(f"Found Tesseract at: {path}")
        pytesseract.tesseract_cmd = path
        break
    else:
        print(f"Not found at: {path}")

try:
    # Try to get Tesseract version
    version = pytesseract.get_tesseract_version()
    print(f"\nSuccess! Tesseract is installed!")
    print(f"Version: {version}")
    print(f"Path: {pytesseract.tesseract_cmd}")
except Exception as e:
    print("\nTesseract is not installed or not properly configured.")
    print(f"Error: {str(e)}")
    print("\nTo install Tesseract OCR:")
    print("1. Download the installer from: https://github.com/UB-Mannheim/tesseract/wiki")
    print("2. Run the installer as administrator")
    print("3. Make sure to:")
    print("   - Use the default installation path (C:\\Program Files\\Tesseract-OCR)")
    print("   - Check 'Add to PATH' during installation")
    print("   - Install the English language package")
