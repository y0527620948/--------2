import re
from typing import Optional

class OCRService:
    """
    שירות אחראי על חילוץ טקסט גולמי (OCR) וניקוי טקסטים מקבצים סרוקים או מסמכים.
    """
    
    @staticmethod
    def clean_text(raw_text: str) -> str:
        """
        מנקה טקסט גולמי שהופק מ-OCR או ממקור חיצוני מרעשים, רווחים כפולים ותווים מיותרים.
        """
        if not raw_text:
            return ""
        
        # המרת שורות חדשות וניקוי רווחים מיותרים מרובים
        cleaned = re.sub(r'[ \t]+', ' ', raw_text)
        cleaned = re.sub(r'\r\n', '\n', cleaned)
        cleaned = re.sub(r'\n\s*\n+', '\n', cleaned)
        
        return cleaned.strip()

    def extract_and_clean(self, file_path: str) -> str:
        """
        מתאם בין קריאת הקובץ (או הפעלת מנוע OCR כגון Tesseract) לבין ניקוי הטקסט.
        """
        # כאן תצורף אינטגרציה עתידית עם ספריות כגון pytesseract / pdf2image במידת הצורך.
        # לעת עתה, נסמלץ קריאת קובץ טקסט גולמי או מעטפת בסיסית.
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.clean_text(content)
        except FileNotFoundError:
            raise FileNotFoundError(f"הקובץ לא נמצא בנתיב: {file_path}")