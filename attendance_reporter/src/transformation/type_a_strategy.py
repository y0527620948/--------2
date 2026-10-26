from src.models.domain import AttendanceReport, AttendanceRow
from src.transformation.base_strategy import BaseTransformationStrategy

class TypeATransformationStrategy(BaseTransformationStrategy):
    """
    אסטרטגיית טרנספורמציה ייעודית לדוח מסוג A (אימוטביליות מלאה, יצירת מופעים חדשים).
    """
    def transform(self, report: AttendanceReport) -> AttendanceReport:
        transformed_rows = []
        for row in report.rows:
            # דוגמה לטרנספורמציה: יצירת אובייקט חדש עם הערה מעודכנת או התאמת נתונים
            new_notes = f"{row.notes or ''} [Processed by TypeA Strategy]".strip()
            
            new_row = AttendanceRow(
                employee_id=row.employee_id,
                employee_name=row.employee_name,
                date=row.date,
                status=row.status,
                check_in=row.check_in,
                check_out=row.check_out,
                notes=new_notes
            )
            transformed_rows.append(new_row)
            
        return AttendanceReport(
            report_id=report.report_id,
            report_type=report.report_type,
            rows=transformed_rows,
            generated_at=report.generated_at
        )