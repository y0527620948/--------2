import tempfile
import os
from datetime import date
from src.models.enums import ReportType, AttendanceStatus
from src.models.domain import AttendanceReport, AttendanceRow
from src.transformation.type_a_strategy import TypeATransformationStrategy
from src.generation.report_generator import ReportGenerator

def test_transformation_and_generation():
    row = AttendanceRow(
        employee_id="E1001",
        employee_name="ישראל ישראלי",
        date=date(2026, 6, 1),
        status=AttendanceStatus.PRESENT
    )
    report = AttendanceReport(
        report_id="REP-01",
        report_type=ReportType.TYPE_A,
        rows=[row]
    )
    
    # טרנספורמציה
    strategy = TypeATransformationStrategy()
    transformed_report = strategy.transform(report)
    
    assert "[Processed by TypeA Strategy]" in transformed_report.rows[0].notes
    
    # הפקת פלט
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as tmp:
        tmp_path = tmp.name
        
    try:
        ReportGenerator.generate_output(transformed_report, tmp_path)
        assert os.path.exists(tmp_path)
        with open(tmp_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "E1001" in content
            assert "Processed by TypeA Strategy" in content
    finally:
        os.unlink(tmp_path)