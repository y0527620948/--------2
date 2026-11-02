from abc import ABC, abstractmethod
from src.models.domain import AttendanceReport

class BaseParser(ABC):
    """
    מחלקת בסיס אבסטרקטית לפענוח דוחות המיישמת את דפוס Template Method.
    """

    def parse(self, cleaned_text: str) -> AttendanceReport:

        # שלב 1: פירוק לשורות או מבנים גולמיים
        raw_lines = self._split_into_lines(cleaned_text)
        
        # שלב 2: פענוח ספציפי לסוג הדוח (ממומש על ידי תת-המחלקה)
        rows = self._parse_rows(raw_lines)
        
        # שלב 3: הרכבת דוח הדומיין המלא
        return self._build_report(rows, cleaned_text)

    def _split_into_lines(self, cleaned_text: str) -> list[str]:
        return [line.strip() for line in cleaned_text.split('\n') if line.strip()]

    @abstractmethod
    def _parse_rows(self, raw_lines: list[str]) -> list:
        pass

    @abstractmethod
    def _build_report(self, rows: list, cleaned_text: str) -> AttendanceReport:
        pass



