from PyPDF2 import PdfReader
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

def extract_text_from_pdf(pdf_path):
    # First attempt with PyPDF2 for text-based PDFs
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text1 = page.extract_text()
        text += text1 
        # If no text found, use pytesseract for OCR on images
        if not text1.strip():
            images = convert_from_path(pdf_path)
            for img in images:
                text += pytesseract.image_to_string(img)
    
    return text