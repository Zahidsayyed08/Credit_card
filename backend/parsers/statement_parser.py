import pdfplumber
import re
from datetime import datetime
from typing import Dict, Any, Optional
# from parsers.statement_parser import StatementParser
from utils.ocr_handler import OCRHandler
from utils.gemini_extractor import GeminiExtractor

class StatementParser:
    """Parser for credit card statements using OCR and Gemini API"""
    
    def __init__(self, issuer: str):
        self.issuer = issuer
        self.ocr_handler = OCRHandler()
        self.gemini_extractor = GeminiExtractor()
    
    def parse(self, filepath: str) -> Dict[str, Any]:
        """
        Main parsing method - extracts text using OCR and uses Gemini to extract data
        
        Args:
            filepath: Path to the uploaded file (PDF, JPG, JPEG, or PNG)
            
        Returns:
            Dictionary with extracted data points
        """
        try:
            # Step 1: Extract text from file using OCR
            extracted_text = self.ocr_handler.extract_text(filepath)
            
            if not extracted_text or extracted_text.strip() == '':
                return {'error': 'No text could be extracted from the document'}
            
            # Step 2: Use Gemini to extract structured data
            result = self.gemini_extractor.extract_data(extracted_text, self.issuer)
            
            return result
        except Exception as e:
            return {'error': f'Failed to parse statement: {str(e)}'}
