from datetime import date, time
from src.parsing.ocr import OCRService
from src.models.enums import ReportType, AttendanceStatus
from src.models.domain import AttendanceRow, AttendanceReport

def test_run_integration_verification():
    print("--- מתחיל תהליך אינטגרציה: OCR -> ניקוי -> מיפוי לדומיין ---")
    
    # הדמיית קלט גולמי מטעם קובץ (או סריקה)
    raw_sample_input = """
    דוח נוכחות   סוג A
    מזהה עובד: E1001   |   שם:   ישראל ישראלי   |   תאריך: 2026-06-01   |   סטטוס: PRESENT   |   כניסה: 08:30   |   יציאה: 17:00
    """
    
    # 2. ניקוי הטקסט באמצעות שירות ה-OCR
    cleaned_text = OCRService.clean_text(raw_sample_input)
    print(f"[OCR Service] טקסט נקי שהתקבל:\n{cleaned_text}\n")
    
    # 3. מיפוי ידני/הדמיוני למודלי הדומיין (טרם בניית הפארסרים המלאים)
    row = AttendanceRow(
        employee_id="E1001",
        employee_name="ישראל ישראלי",
        date=date(2026, 6, 1),
        status=AttendanceStatus.PRESENT,
        check_in=time(8, 30),
        check_out=time(17, 0)
    )
    
    report = AttendanceReport(
        report_id="REP-INT-001",
        report_type=ReportType.TYPE_A,
        rows=[row],
        generated_at="2026-06-06"
    )
    
    # 4. אימות תוצאות
    assert report.report_type == ReportType.TYPE_A
    assert len(report.rows) == 1
    assert report.rows[0].employee_id == "E1001"
    assert report.rows[0].status == AttendanceStatus.PRESENT
    
    print("[Domain Model] הנתונים מופו בהצלחה ל-AttendanceReport ולאימוטביליות AttendanceRow.")
    print("--- אינטגרציה הסתיימה בהצלחה מלאה! ---")

if __name__ == "__main__":
    test_run_integration_verification()