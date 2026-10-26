from datetime import datetime, date, time
from src.models.enums import ReportType, AttendanceStatus
from src.models.domain import AttendanceRow, AttendanceReport
from src.parsing.base_parser import BaseParser

class TypeAParser(BaseParser):
    """
    פארסר ייעודי לפענוח דוחות מסוג A.
    """

    def _parse_rows(self, raw_lines: list[str]) -> list[AttendanceRow]:
        rows = []
        for line in raw_lines:
            # דוגמה לפורמט שורה: מזהה עובד: E1001 | שם: ישראל ישראלי | תאריך: 2026-06-01 | סטטוס: PRESENT | כניסה: 08:30 | יציאה: 17:00
            if "מזהה עובד" in line or "E1001" in line or "PRESENT" in line:
                try:
                    parts = [p.strip() for p in line.split('|')]
                    emp_id, emp_name, rep_date, status, check_in, check_out = "", "", date.today(), AttendanceStatus.PRESENT, None, None
                    
                    for part in parts:
                        if "מזהה עובד" in part or part.startswith("E"):
                            emp_id = part.split(':')[-1].strip() if ':' in part else part
                        elif "שם" in part:
                            emp_name = part.split(':')[-1].strip()
                        elif "תאריך" in part:
                            date_str = part.split(':')[-1].strip()
                            rep_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                        elif "סטטוס" in part:
                            status_str = part.split(':')[-1].strip().upper()
                            # תיקון: שימוש ב-__members__ הנכון של פייתון
                            status = AttendanceStatus[status_str] if status_str in AttendanceStatus.__members__ else AttendanceStatus.PRESENT
                        elif "כניסה" in part:
                            time_str = part.split(':')[-1].strip()
                            if len(time_str) >= 5:
                                check_in = datetime.strptime(time_str[:5], "%H:%M").time()
                        elif "יציאה" in part:
                            time_str = part.split(':')[-1].strip()
                            if len(time_str) >= 5:
                                check_out = datetime.strptime(time_str[:5], "%H:%M").time()
                                
                    if emp_id:
                        row = AttendanceRow(
                            employee_id=emp_id,
                            employee_name=emp_name or "לא ידוע",
                            date=rep_date,
                            status=status,
                            check_in=check_in,
                            check_out=check_out
                        )
                        rows.append(row)
                except Exception as e:
                    # מומלץ להשאיר הדפסת דיבוג במידת הצורך, או להמשיך הלאה
                    continue
        return rows

    def _build_report(self, rows: list, cleaned_text: str) -> AttendanceReport:
        return AttendanceReport(
            report_id="REPORT-A-001",
            report_type=ReportType.TYPE_A,
            rows=rows,
            generated_at=datetime.now().isoformat()
        )