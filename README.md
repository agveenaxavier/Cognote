# CogNote: Simplified Lecture Notes Organizer

A web application that helps students organize their lecture notes by converting images to searchable text using OCR technology.

## Features

- Image-to-text conversion using Tesseract OCR
- Upload and process lecture notes
- Search functionality for finding specific content
- Modern and responsive user interface

## Prerequisites

- Python 3.7 or higher
- Tesseract OCR installed on your system
- pip (Python package manager)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/eduvision.git
cd eduvision
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

3. Install Tesseract OCR:
   - Windows: Download and install from https://github.com/UB-Mannheim/tesseract/wiki
   - Make sure to add Tesseract to your system PATH

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

1. Click "Choose an image file" to select a lecture note image
2. Click "Upload & Process" to convert the image to text
3. Use the search bar to find specific content in your processed notes

## Technology Stack

- Backend: Python Flask
- OCR: Tesseract
- Frontend: HTML, CSS, JavaScript
- Image Processing: Pillow
