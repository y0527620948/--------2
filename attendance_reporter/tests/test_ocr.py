import pytest
from src.parsing.ocr import OCRService

def test_clean_text():
    dirty_text = "  שם  העובד:   ישראל   ישראלי \r\n\r\n סטטוס: נוכח  "
    cleaned = OCRService.clean_text(dirty_text)
    
    # ווידוא שרווחים כפולים וירידות שורע מיותרות נוקו כהלכה
    assert "שם העובד: ישראל ישראלי" in cleaned
    assert "סטטוס: נוכח" in cleaned
    assert "\r" not in cleaned