import tempfile
import os
from src.models.enums import ReportType, AttendanceStatus
from src.parsing.type_b_parser import TypeBParser

def test_type_b_parser():
    sample_content = "דוח נוכחות סוג B | מזהה עובד B: EMP-B001 | שם: שמעון צדיק | תאריך: 2026-06-01 | סטטוס: PRESENT | כניסה: 09:00 | יציאה: 18:00 | הערות: REMARK_TEST"
    
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as tmp:
        tmp.write(sample_content)
        tmp_path = tmp.name
        
    try:
        parser = TypeBParser()
        report = parser.parse(tmp_path)
        
        assert report.report_type == ReportType.TYPE_B
        assert len(report.rows) == 1
        assert report.rows[0].employee_id == "EMP-B001"
        assert report.rows[0].employee_name == "שמעון צדיק"
        assert report.rows[0].status == AttendanceStatus.PRESENT
        assert "REMARK_TEST" in report.rows[0].notes
    finally:
        os.unlink(tmp_path)