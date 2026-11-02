from src.models.enums import ReportType, AttendanceStatus
from src.parsing.type_b_parser import TypeBParser


def test_type_b_parser():
    sample_content = (
        "דוח נוכחות סוג B | מזהה עובד B: EMP-B001 | שם: שמעון צדיק | "
        "תאריך: 2026-06-01 | סטטוס: PRESENT | כניסה: 09:00 | "
        "יציאה: 18:00 | הערות: REMARK_TEST"
    )

    parser = TypeBParser()
    report = parser.parse(sample_content)

    assert report.report_type == ReportType.TYPE_B
    assert len(report.rows) == 1
    assert report.rows[0].employee_id == "EMP-B001"
    assert report.rows[0].employee_name == "שמעון צדיק"
    assert report.rows[0].status == AttendanceStatus.PRESENT
    assert "REMARK_TEST" in report.rows[0].notes