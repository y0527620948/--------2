import pytest
from datetime import date, time
from src.models.enums import AttendanceStatus
from src.models.domain import AttendanceRow
from src.transformation.invariants import InvariantValidator

def test_valid_invariant():
    row = AttendanceRow(
        employee_id="E1001",
        employee_name="ישראל",
        date=date(2026, 6, 1),
        status=AttendanceStatus.PRESENT,
        check_in=time(8, 0),
        check_out=time(17, 0)
    )
    # לא אמור לזרוק שגיאה
    InvariantValidator.validate_row(row)
    hours = InvariantValidator.calculate_worked_hours(row.check_in, row.check_out, break_minutes=60)
    assert hours == 8.0

def test_invalid_invariant_time():
    row = AttendanceRow(
        employee_id="E1001",
        employee_name="ישראל",
        date=date(2026, 6, 1),
        status=AttendanceStatus.PRESENT,
        check_in=time(17, 0),
        check_out=time(8, 0) # יציאה לפני כניסה
    )
    with pytest.raises(ValueError):
        InvariantValidator.validate_row(row)