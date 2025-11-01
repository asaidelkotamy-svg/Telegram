import requests
from googletrans import Translator
import time

translator = Translator()

def get_random_fact(api_key):
    """يجلب معلومة عشوائية من API Ninjas"""
    url = "https://api.api-ninjas.com/v1/facts"
    headers = {"X-Api-Key": api_key}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]["fact"]
    return None


def translate_text(text):
    """يترجم النص إلى العربية"""
    try:
        translated = translator.translate(text, dest='ar')
        return translated.text
    except Exception as e:
        print("خطأ في الترجمة:", e)
        return text


def wait_hours(hours):
    """انتظار بعدد الساعات المحدد"""
    time.sleep(hours * 3600)
