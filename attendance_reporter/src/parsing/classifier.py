import re
from src.models.enums import ReportType

class ReportClassifier:
    """
    רכיב סיווג דוחות המזהה את סוג הדוח מתוך הטקסט הנקי באמצעות סימנים מבניים וביטויים רגולריים.
    """
    
    @staticmethod
    def classify(cleaned_text: str) -> ReportType:
        if not cleaned_text:
            raise ValueError("הטקסט ריק, לא ניתן לבצע סיווג.")
            
        text_upper = cleaned_text.upper()
        
        # זיהוי דוח מסוג A על בסיס מבנה או מילות מפתח מותאמות
        if "TYPE A" in text_upper or "סוג A" in text_upper or "REPORT_A" in text_upper:
            return ReportType.TYPE_A
        elif "TYPE B" in text_upper or "סוג B" in text_upper or "REPORT_B" in text_upper:
            return ReportType.TYPE_B
            
        # ברירת מחדל או זיהוי heuristical במידה ואין התאמה מובהקת
        if "E1001" in text_upper or "PRESENT" in text_upper:
            return ReportType.TYPE_A
            
        raise ValueError("לא ניתן לזהות את סוג הדוח מתוך הטקסט המסופק.")