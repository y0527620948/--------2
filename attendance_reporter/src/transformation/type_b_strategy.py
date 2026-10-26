from src.models.domain import AttendanceReport, AttendanceRow
from src.transformation.base_strategy import BaseTransformationStrategy
from src.transformation.invariants import InvariantValidator

class TypeBTransformationStrategy(BaseTransformationStrategy):
    """
    אסטרטגיית טרנספורמציה לדוח מסוג B הכוללת חישוב וחלוקה של שעות (100%, 125%, 150%).
    """
    def transform(self, report: AttendanceReport) -> AttendanceReport:
        transformed_rows = []
        for row in report.rows:
            InvariantValidator.validate_row(row)
            
            # חישוב שעות כולל בהתחשב בהפסקה סטנדרטית של 30 דקות
            worked_hours = InvariantValidator.calculate_worked_hours(row.check_in, row.check_out, break_minutes=30)
            
            # חלוקה לרמות שכר: עד 8 שעות (100%), מעל 8 ועד 10 שעות (125%), מעל 10 שעות (150%)
            h_100 = min(worked_hours, 8.0)
            h_125 = max(0.0, min(worked_hours - 8.0, 2.0))
            h_150 = max(0.0, worked_hours - 10.0)
            
            summary_note = f"שעות: {worked_hours}h (100%:{h_100}, 125%:{h_125}, 150%:{h_150}) [TypeB Strategy]"
            
            new_row = AttendanceRow(
                employee_id=row.employee_id,
                employee_name=row.employee_name,
                date=row.date,
                status=row.status,
                check_in=row.check_in,
                check_out=row.check_out,
                notes=summary_note
            )
            transformed_rows.append(new_row)
            
        return AttendanceReport(
            report_id=report.report_id,
            report_type=report.report_type,
            rows=transformed_rows,
            generated_at=report.generated_at
        )