import pytest
from src.models.enums import ReportType
from src.parsing.classifier import ReportClassifier

def test_classifier_type_a():
    text = "דוח נוכחות סוג A - מזהה עובד: E1001"
    assert ReportClassifier.classify(text) == ReportType.TYPE_A

def test_classifier_type_b():
    text = "TYPE B Attendance Summary Report"
    assert ReportClassifier.classify(text) == ReportType.TYPE_B

def test_classifier_invalid():
    with pytest.raises(ValueError):
        ReportClassifier.classify("טקסט סתמי לחלוטין ללא הקשר")