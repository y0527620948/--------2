from src.models.enums import ReportType
from src.parsing.base_parser import BaseParser
from src.parsing.type_a_parser import TypeAParser
from src.parsing.type_b_parser import TypeBParser
from src.transformation.base_strategy import BaseTransformationStrategy
from src.transformation.type_a_strategy import TypeATransformationStrategy
from src.transformation.type_b_strategy import TypeBTransformationStrategy

class ReportPipelineFactory:
    """
    מחלקת Factory לניתוב דינמי של הפארסר ואסטרטגיית הטרנספורמציה לפי סוג הדוח.
    """
    @staticmethod
    def get_parser(report_type: ReportType) -> BaseParser:
        if report_type == ReportType.TYPE_A:
            return TypeAParser()
        elif report_type == ReportType.TYPE_B:
            return TypeBParser()
        raise ValueError(f"סוג דוח לא נתמך בפארסר: {report_type}")

    @staticmethod
    def get_strategy(report_type: ReportType) -> BaseTransformationStrategy:
        if report_type == ReportType.TYPE_A:
            return TypeATransformationStrategy()
        elif report_type == ReportType.TYPE_B:
            return TypeBTransformationStrategy()
        raise ValueError(f"סוג דוח לא נתמך באסטרטגיה: {report_type}")