import google.generativeai as genai
from config import Config
from typing import Dict, Any

class GeminiExtractor:
    """Use Gemini API to extract structured data from credit card statements"""
    
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def extract_data(self, text: str, issuer: str) -> Dict[str, Any]:
        """
        Use Gemini to extract key data points from statement text
        
        Args:
            text: Extracted text from the statement
            issuer: Credit card issuer name
            
        Returns:
            Dictionary with extracted data points
        """
        try:
            prompt = self._build_extraction_prompt(text, issuer)
            response = self.model.generate_content(prompt)
            
            # Parse the response
            result = self._parse_gemini_response(response.text, issuer)
            return result
        except Exception as e:
            raise Exception(f"Failed to extract data using Gemini: {str(e)}")
    
    def _build_extraction_prompt(self, text: str, issuer: str) -> str:
        """Build the prompt for Gemini to extract data"""
        prompt = f"""
        You are an expert at extracting information from credit card statements.
        
        Please extract the following 5 key data points from this {issuer} credit card statement:
        1. Card Last 4 Digits (the last 4 digits of the card number)
        2. Billing Cycle (the date range of the billing period)
        3. Payment Due Date (the date payment is due)
        4. Total Balance (the total amount owed)
        5. Card Variant/Type (the specific card product name/type)
        
        Statement Text:
        {text}
        
        Please respond in this exact JSON format:
        {{
            "card_last_4": "value or N/A",
            "billing_cycle": "value or N/A",
            "payment_due_date": "value or N/A",
            "total_balance": "value or N/A",
            "card_variant": "value or N/A"
        }}
        
        Only return the JSON, no other text.
        """
        return prompt
    
    def _parse_gemini_response(self, response_text: str, issuer: str) -> Dict[str, Any]:
        """Parse Gemini's response and format it"""
        import json
        
        try:
            # Extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response_text[json_start:json_end]
            data = json.loads(json_str)
            
            return {
                'issuer': issuer,
                'data_points': {
                    'card_last_4': data.get('card_last_4', 'N/A'),
                    'billing_cycle': data.get('billing_cycle', 'N/A'),
                    'payment_due_date': data.get('payment_due_date', 'N/A'),
                    'total_balance': data.get('total_balance', 'N/A'),
                    'card_variant': data.get('card_variant', 'N/A')
                }
            }
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse Gemini response: {str(e)}")
