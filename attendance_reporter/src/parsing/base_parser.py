from abc import ABC, abstractmethod
from src.models.domain import AttendanceReport
from src.parsing.ocr import OCRService

class BaseParser(ABC):
    """
    מחלקת בסיס אבסטרקטית לפענוח דוחות המיישמת את דפוס Template Method.
    """
    
    def __init__(self, ocr_service: OCRService = None):
        self.ocr_service = ocr_service or OCRService()

    def parse(self, file_path: str) -> AttendanceReport:
        # שלב 1: חילוץ וניקוי טקסט גולמי
        cleaned_text = self.ocr_service.extract_and_clean(file_path)
        
        # שלב 2: פירוק לשורות או מבנים גולמיים
        raw_lines = self._split_into_lines(cleaned_text)
        
        # שלב 3: פענוח ספציפי לסוג הדוח (ממומש על ידי תת-המחלקה)
        rows = self._parse_rows(raw_lines)
        
        # שלב 4: הרכבת דוח הדומיין המלא
        return self._build_report(rows, cleaned_text)

    def _split_into_lines(self, cleaned_text: str) -> list[str]:
        return [line.strip() for line in cleaned_text.split('\n') if line.strip()]

    @abstractmethod
    def _parse_rows(self, raw_lines: list[str]) -> list:
        pass

    @abstractmethod
    def _build_report(self, rows: list, cleaned_text: str) -> AttendanceReport:
        pass