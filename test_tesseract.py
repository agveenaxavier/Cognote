import subprocess
import os

def run_tesseract_version():
    try:
        # Try running tesseract directly
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, 
                              text=True)
        print("Direct command output:")
        print(result.stdout)
        return True
    except FileNotFoundError:
        print("Tesseract not found in PATH")
        return False

def check_tesseract_path():
    tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    if os.path.exists(tesseract_path):
        print(f"\nTesseract executable found at: {tesseract_path}")
        try:
            result = subprocess.run([tesseract_path, '--version'], 
                                  capture_output=True, 
                                  text=True)
            print("\nFull path command output:")
            print(result.stdout)
            return True
        except Exception as e:
            print(f"Error running Tesseract: {e}")
            return False
    else:
        print(f"\nTesseract not found at: {tesseract_path}")
        return False

print("=== Testing Tesseract Installation ===")
print("\nTrying direct command...")
direct_success = run_tesseract_version()

print("\nChecking specific path...")
path_success = check_tesseract_path()

if not (direct_success or path_success):
    print("\nTesseract installation issues detected!")
    print("Please ensure:")
    print("1. Tesseract is installed properly")
    print("2. The installation path is correct")
    print("3. The PATH environment variable includes Tesseract")
    print("\nTry these steps:")
    print("1. Uninstall Tesseract")
    print("2. Restart your computer")
    print("3. Install Tesseract again as administrator")
    print("4. Make sure to check 'Add to PATH' during installation")
