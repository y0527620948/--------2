import re

from src.models.enums import ReportType


class ReportClassifier:
    TYPE_A_FEATURES = {
        "100%": 1,
        "125%": 1,
        "150%": 1,
        "הפסקה": 1,
    }

    TYPE_B_FEATURES = {
        "מחיר לשעה": 1,
        "סה כ לתשלום": 1,
        "סה כ ימי עבודה לחודש": 1,
        "סה כ שעות חודשיות": 1,
    }

    MINIMUM_SCORE = 3
    MINIMUM_SCORE_GAP = 2

    @staticmethod
    def _normalize(text: str) -> str:
        text = text.upper().replace("_", " ")
        return re.sub(r"[^\w%]+", " ", text).strip()

    @staticmethod
    def _contains_phrase(text: str, phrase: str) -> bool:
        normalized_phrase = ReportClassifier._normalize(phrase)
        return f" {normalized_phrase} " in f" {text} "

    @staticmethod
    def _calculate_score(text: str, features: dict[str, int]) -> int:
        return sum(
            points
            for phrase, points in features.items()
            if ReportClassifier._contains_phrase(text, phrase)
        )

    @staticmethod
    def classify(cleaned_text: str) -> ReportType:
        if not cleaned_text or not cleaned_text.strip():
            raise ValueError("הטקסט ריק, לא ניתן לבצע סיווג.")

        text = ReportClassifier._normalize(cleaned_text)

        is_type_a = any(
            ReportClassifier._contains_phrase(text, marker)
            for marker in ("TYPE A", "סוג A", "REPORT A")
        )
        is_type_b = any(
            ReportClassifier._contains_phrase(text, marker)
            for marker in ("TYPE B", "סוג B", "REPORT B")
        )

        if is_type_a and is_type_b:
            raise ValueError("נמצאו בטקסט סימנים גם ל-Type A וגם ל-Type B.")

        if is_type_a:
            return ReportType.TYPE_A

        if is_type_b:
            return ReportType.TYPE_B

        score_a = ReportClassifier._calculate_score(
            text,
            ReportClassifier.TYPE_A_FEATURES,
        )
        score_b = ReportClassifier._calculate_score(
            text,
            ReportClassifier.TYPE_B_FEATURES,
        )

        if (
            max(score_a, score_b) < ReportClassifier.MINIMUM_SCORE
            or abs(score_a - score_b) < ReportClassifier.MINIMUM_SCORE_GAP
        ):
            raise ValueError(
                "לא ניתן לזהות את סוג הדוח באופן חד-משמעי "
                f"(Type A: {score_a}, Type B: {score_b})."
            )

        if score_a > score_b:
            return ReportType.TYPE_A

        return ReportType.TYPE_B