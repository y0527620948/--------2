from datetime import datetime, time, date
from src.models.domain import AttendanceRow
MAX_TIME_SHIFT_MINUTES = 30

class InvariantValidator:
    """
    מחלקה לאכיפת חוקי דומיין ואינווריאנטים (Invariants) על שורות נוכחות.
    """
    @staticmethod
    def validate_row(row: AttendanceRow) -> None:
        # אינווריאנט 1: שעת יציאה חייבת להיות אחרי שעת כניסה (אם קיימות שתיהן)
        if row.check_in and row.check_out:
            in_datetime = datetime.combine(date.min, row.check_in)
            out_datetime = datetime.combine(date.min, row.check_out)
            if out_datetime <= in_datetime:
                raise ValueError(f"אינווריאנט שגוי: שעת היציאה ({row.check_out}) חייבת להיות מאוחרת משעת הכניסה ({row.check_in}).")

    @staticmethod
    def calculate_worked_hours(check_in: time, check_out: time, break_minutes: int = 0) -> float:
        if not check_in or not check_out:
            return 0.0
        in_dt = datetime.combine(date.min, check_in)
        out_dt = datetime.combine(date.min, check_out)
        diff_seconds = (out_dt - in_dt).total_seconds()
        total_minutes = (diff_seconds / 60.0) - break_minutes
        return max(0.0, round(total_minutes / 60.0, 2))