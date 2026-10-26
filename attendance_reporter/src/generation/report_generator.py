from src.models.domain import AttendanceReport

class ReportGenerator:
    """
    מחולל דוחות אחראי על יצירת קובץ פלט חדש מתוך נתוני הדוח המעובדים.
    """
    @staticmethod
    def generate_output(report: AttendanceReport, output_file_path: str) -> None:
        content = f"=== Attendance Report Output ({report.report_type.value}) ===\n"
        content += f"Report ID: {report.report_id}\n"
        content += f"Generated At: {report.generated_at}\n"
        content += f"Total Rows: {len(report.rows)}\n"
        content += "----------------------------------------\n"
        
        for row in report.rows:
            content += f"ID: {row.employee_id} | Name: {row.employee_name} | Date: {row.date} | Status: {row.status.value} | Notes: {row.notes}\n"
            
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(content)