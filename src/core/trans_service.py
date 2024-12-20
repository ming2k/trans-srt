import requests
import uuid
import json
import os
import time
from typing import Optional
from requests.exceptions import RequestException

class TranslationService:
    def __init__(self, key: str = None, location: str = None, max_retries: int = 3, retry_delay: int = 1):
        self.key = key or os.getenv('AZURE_TRANSLATOR_KEY')
        self.location = location or os.getenv('AZURE_TRANSLATOR_LOCATION')
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        if not self.key or not self.location:
            raise ValueError("Azure credentials not found. Set AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_LOCATION environment variables or pass them directly.")
            
        self.endpoint = "https://api.cognitive.microsofttranslator.com"
        self.path = '/translate'
        self.constructed_url = self.endpoint + self.path

    def translate_text(self, text: str, target_lang: str = 'zh-Hans') -> Optional[str]:
        retries = 0
        while retries < self.max_retries:
            try:
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

                response = requests.post(
                    self.constructed_url, 
                    params=params, 
                    headers=headers, 
                    json=body,
                    timeout=10  # Add timeout
                )
                response.raise_for_status()
                result = response.json()
                return result[0]['translations'][0]['text']
                
            except RequestException as e:
                retries += 1
                if retries < self.max_retries:
                    print(f"Translation attempt {retries} failed: {str(e)}. Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    print(f"Translation failed after {self.max_retries} attempts: {str(e)}")
                    return None 