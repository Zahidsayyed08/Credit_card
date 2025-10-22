import pytesseract
from PIL import Image
import pdfplumber
import os
from typing import Optional

class OCRHandler:
    """Handle OCR extraction from images and PDFs"""
    
    @staticmethod
    def extract_text_from_image(filepath: str) -> str:
        """Extract text from image using Tesseract OCR"""
        try:
            image = Image.open(filepath)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            raise Exception(f"Failed to extract text from image: {str(e)}")
    
    @staticmethod
    def extract_text_from_pdf(filepath: str) -> str:
        """Extract text from PDF using pdfplumber"""
        try:
            text = ""
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    @staticmethod
    def extract_text(filepath: str) -> str:
        """Extract text from any supported file format"""
        file_ext = os.path.splitext(filepath)[1].lower()
        
        if file_ext == '.pdf':
            return OCRHandler.extract_text_from_pdf(filepath)
        elif file_ext in ['.jpg', '.jpeg', '.png']:
            return OCRHandler.extract_text_from_image(filepath)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
