from enum import Enum, unique

@unique
class ReportType(Enum):
    TYPE_A = "TYPE_A"
    TYPE_B = "TYPE_B"

@unique
class AttendanceStatus(Enum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    LATE = "LATE"
    EXCUSED = "EXCUSED"