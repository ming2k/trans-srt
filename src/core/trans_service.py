import requests
import uuid
import json
import os
from typing import Optional

class TranslationService:
    def __init__(self, key: str = None, location: str = None):
        self.key = key or os.getenv('AZURE_TRANSLATOR_KEY')
        self.location = location or os.getenv('AZURE_TRANSLATOR_LOCATION')
        
        if not self.key or not self.location:
            raise ValueError("Azure credentials not found. Set AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_LOCATION environment variables or pass them directly.")
            
        self.endpoint = "https://api.cognitive.microsofttranslator.com"
        self.path = '/translate'
        self.constructed_url = self.endpoint + self.path

    def translate_text(self, text: str, target_lang: str = 'zh-Hans') -> Optional[str]:
        params = {
            'api-version': '3.0',
            'from': 'en',
            'to': target_lang
        }

        headers = {
            'Ocp-Apim-Subscription-Key': self.key,
            'Ocp-Apim-Subscription-Region': self.location,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        body = [{
            'text': text
        }]

        try:
            response = requests.post(
                self.constructed_url, 
                params=params, 
                headers=headers, 
                json=body
            )
            response.raise_for_status()
            result = response.json()
            return result[0]['translations'][0]['text']
        except Exception as e:
            print(f"Translation error: {str(e)}")
            return None 