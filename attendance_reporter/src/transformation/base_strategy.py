from abc import ABC, abstractmethod
from src.models.domain import AttendanceReport

class BaseTransformationStrategy(ABC):
    """
    אסטרטגיית בסיס אבסטרקטית לטרנספורמציית נתוני דוחות (Strategy Pattern).
    """
    @abstractmethod
    def transform(self, report: AttendanceReport) -> AttendanceReport:
        pass