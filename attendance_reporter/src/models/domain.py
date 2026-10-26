from dataclasses import dataclass, field
from datetime import date, time
from typing import List, Optional
from src.models.enums import ReportType, AttendanceStatus

@dataclass(frozen=True)
class AttendanceRow:
    employee_id: str
    employee_name: str
    date: date
    status: AttendanceStatus
    check_in: Optional[time] = None
    check_out: Optional[time] = None
    notes: Optional[str] = None

@dataclass(frozen=True)
class AttendanceReport:
    report_id: str
    report_type: ReportType
    rows: List[AttendanceRow] = field(default_factory=list)
    generated_at: Optional[str] = None