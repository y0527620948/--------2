import tempfile
import os
from src.models.enums import ReportType, AttendanceStatus
from src.parsing.type_a_parser import TypeAParser

def test_type_a_parser():
    sample_content = "מזהה עובד: E1001 | שם: ישראל ישראלי | תאריך: 2026-06-01 | סטטוס: PRESENT | כניסה: 08:30 | יציאה: 17:00"
    
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as tmp:
        tmp.write(sample_content)
        tmp_path = tmp.name
        
    try:
        parser = TypeAParser()
        report = parser.parse(tmp_path)
        
        assert report.report_type == ReportType.TYPE_A
        assert len(report.rows) == 1
        assert report.rows[0].employee_id == "E1001"
        assert report.rows[0].employee_name == "ישראל ישראלי"
        assert report.rows[0].status == AttendanceStatus.PRESENT
    finally:
        os.unlink(tmp_path)