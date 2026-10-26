from datetime import datetime, date, time
from src.models.enums import ReportType, AttendanceStatus
from src.models.domain import AttendanceRow, AttendanceReport
from src.parsing.base_parser import BaseParser

class TypeBParser(BaseParser):
    """
    פארסר ייעודי לפענוח דוחות מסוג B (כולל נתוני הפסקות, הערות ומבנה מורחב).
    """

    def _parse_rows(self, raw_lines: list[str]) -> list[AttendanceRow]:
        rows = []
        for line in raw_lines:
            if "TYPE_B" in line.upper() or "סוג B" in line or "EMP-B" in line or "מזהה עובד B" in line:
                try:
                    parts = [p.strip() for p in line.split('|')]
                    emp_id, emp_name, rep_date, status, check_in, check_out, notes = "", "", date.today(), AttendanceStatus.PRESENT, None, None, ""
                    
                    for part in parts:
                        if "מזהה" in part or part.startswith("B") or part.startswith("EMP"):
                            emp_id = part.split(':')[-1].strip() if ':' in part else part
                        elif "שם" in part:
                            emp_name = part.split(':')[-1].strip()
                        elif "תאריך" in part:
                            date_str = part.split(':')[-1].strip()
                            rep_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                        elif "סטטוס" in part:
                            status_str = part.split(':')[-1].strip().upper()
                            status = AttendanceStatus[status_str] if status_str in AttendanceStatus.__members__ else AttendanceStatus.PRESENT
                        elif "כניסה" in part:
                            time_str = part.split(':')[-1].strip()
                            if len(time_str) >= 5:
                                check_in = datetime.strptime(time_str[:5], "%H:%M").time()
                        elif "יציאה" in part:
                            time_str = part.split(':')[-1].strip()
                            if len(time_str) >= 5:
                                check_out = datetime.strptime(time_str[:5], "%H:%M").time()
                        elif "הערות" in part or "REMARK" in part.upper():
                            notes = part.split(':')[-1].strip()
                                
                    if emp_id:
                        row = AttendanceRow(
                            employee_id=emp_id,
                            employee_name=emp_name or "עובד B",
                            date=rep_date,
                            status=status,
                            check_in=check_in,
                            check_out=check_out,
                            notes=notes
                        )
                        rows.append(row)
                except Exception:
                    continue
        return rows

    def _build_report(self, rows: list, cleaned_text: str) -> AttendanceReport:
        return AttendanceReport(
            report_id="REPORT-B-001",
            report_type=ReportType.TYPE_B,
            rows=rows,
            generated_at=datetime.now().isoformat()
        )