import random
from datetime import date, datetime, time, timedelta

from src.models.domain import AttendanceReport, AttendanceRow
from src.transformation.base_strategy import BaseTransformationStrategy
from src.transformation.invariants import InvariantValidator
from src.transformation.invariants import (
    InvariantValidator,
    MAX_TIME_SHIFT_MINUTES,
)


class TypeBTransformationStrategy(BaseTransformationStrategy):
    @staticmethod
    def shift_time(value: time | None, offset_minutes: int) -> time | None:
        if value is None:
            return None
        return (
            datetime.combine(date.min, value) + timedelta(minutes=offset_minutes)
        ).time()

    def transform(self, report: AttendanceReport) -> AttendanceReport:
        transformed_rows = []

        for row in report.rows:
            InvariantValidator.validate_row(row)

            if row.check_in is not None and row.check_out is not None:
                check_in_minutes = row.check_in.hour * 60 + row.check_in.minute
                check_out_minutes = row.check_out.hour * 60 + row.check_out.minute

                min_offset = max(-MAX_TIME_SHIFT_MINUTES, -check_in_minutes)
                max_offset = min(MAX_TIME_SHIFT_MINUTES, 1439 - check_out_minutes)
                offset_minutes = random.randint(min_offset, max_offset)
            else:
                offset_minutes = 0

            new_check_in = self.shift_time(row.check_in, offset_minutes)
            new_check_out = self.shift_time(row.check_out, offset_minutes)

            worked_hours = InvariantValidator.calculate_worked_hours(
                new_check_in,
                new_check_out,
                break_minutes=30,
            )

            h_100 = min(worked_hours, 8.0)
            h_125 = max(0.0, min(worked_hours - 8.0, 2.0))
            h_150 = max(0.0, worked_hours - 10.0)

            summary_note = (
                f"שעות: {worked_hours}h "
                f"(100%:{h_100}, 125%:{h_125}, 150%:{h_150}) "
                "[TypeB Strategy]"
            )

            new_row = AttendanceRow(
                employee_id=row.employee_id,
                employee_name=row.employee_name,
                date=row.date,
                status=row.status,
                check_in=new_check_in,
                check_out=new_check_out,
                notes=summary_note,
            )
            transformed_rows.append(new_row)

        return AttendanceReport(
            report_id=report.report_id,
            report_type=report.report_type,
            rows=transformed_rows,
            generated_at=report.generated_at,
        )