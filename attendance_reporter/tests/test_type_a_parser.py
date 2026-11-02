from src.models.enums import ReportType, AttendanceStatus
from src.parsing.type_a_parser import TypeAParser


def test_type_a_parser():
    sample_content = (
        "מזהה עובד: E1001 | שם: ישראל ישראלי | תאריך: 2026-06-01 | "
        "סטטוס: PRESENT | כניסה: 08:30 | יציאה: 17:00"
    )

    parser = TypeAParser()
    report = parser.parse(sample_content)

    assert report.report_type == ReportType.TYPE_A
    assert len(report.rows) == 1
    assert report.rows[0].employee_id == "E1001"
    assert report.rows[0].employee_name == "ישראל ישראלי"
    assert report.rows[0].status == AttendanceStatus.PRESENT