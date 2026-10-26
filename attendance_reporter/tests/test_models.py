import pytest
from datetime import date, time
from dataclasses import FrozenInstanceError
from src.models.enums import ReportType, AttendanceStatus
from src.models.domain import AttendanceRow, AttendanceReport

def test_attendance_row_immutability():
    row = AttendanceRow(
        employee_id="E001",
        employee_name="ישראל ישראלי",
        date=date(2026, 6, 1),
        status=AttendanceStatus.PRESENT,
        check_in=time(8, 0),
        check_out=time(17, 0)
    )
    
    # ווידוא אימוטביליות (שינוי שדה אמור לזרוק שגיאה)
    with pytest.raises(FrozenInstanceError):
        row.employee_name = "שינוי אסור"

def test_attendance_report_creation():
    row = AttendanceRow(
        employee_id="E002",
        employee_name="שרה כהן",
        date=date(2026, 6, 1),
        status=AttendanceStatus.ABSENT
    )
    report = AttendanceReport(
        report_id="REP-001",
        report_type=ReportType.TYPE_A,
        rows=[row]
    )
    
    assert report.report_id == "REP-001"
    assert report.report_type == ReportType.TYPE_A
    assert len(report.rows) == 1
    assert report.rows[0].employee_id == "E002"