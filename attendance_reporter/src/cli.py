import argparse
from pathlib import Path

from src.generation.report_generator import ReportGenerator
from src.parsing.classifier import ReportClassifier
from src.parsing.ocr import OCRService
from src.parsing.parser_factory import ReportPipelineFactory



def process_file(input_file: Path, output_file: Path | None = None) -> Path:
    input_path = Path(input_file)
    if not input_path.is_file():
        raise FileNotFoundError(f"קובץ הקלט לא נמצא: {input_path}")

    output_path = Path(output_file) if output_file else input_path.with_name(
        f"{input_path.stem}_processed.txt"
    )
    if input_path.resolve() == output_path.resolve():
        raise ValueError("קובץ הפלט חייב להיות שונה מקובץ הקלט.")

    cleaned_text = OCRService().extract_and_clean(str(input_path))
    report_type = ReportClassifier.classify(cleaned_text)
    report = ReportPipelineFactory.get_parser(report_type).parse(cleaned_text)
    if not report.rows:
        raise ValueError("לא נמצאו שורות נוכחות תקינות בקובץ.")

    transformed_report = ReportPipelineFactory.get_strategy(report_type).transform(report)
    ReportGenerator.generate_output(transformed_report, str(output_path))
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="מעבד קובץ טקסט של דוח נוכחות ויוצר קובץ דוח חדש."
    )
    parser.add_argument("input", type=Path, help="נתיב לקובץ הקלט")
    parser.add_argument("-o", "--output", type=Path, help="נתיב לקובץ הפלט")
    args = parser.parse_args()

    try:
        output_path = process_file(args.input, args.output)
    except (OSError, ValueError) as error:
        parser.exit(1, f"שגיאה: {error}\n")

    print(f"נוצר קובץ פלט: {output_path}")
    return 0