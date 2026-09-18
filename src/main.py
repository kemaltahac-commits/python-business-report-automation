import logging
import sys
from pathlib import Path

from analyzer import analyze_data
from cleaner import clean_data
from excel_reporter import generate_excel_report
from loader import load_csv
from pdf_reporter import generate_pdf_report
from validator import DataValidationError, validate_data


ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = ROOT / "input" / "mainsales.csv"
OUTPUT_DIR = ROOT / "output"
LOG_PATH = ROOT / "logs" / "app.log"


def configure_logging() -> logging.Logger:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename=LOG_PATH, level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s", force=True)
    return logging.getLogger("business_report")


def main() -> int:
    logger = configure_logging()
    try:
        print("Loading data...")
        data = load_csv(INPUT_PATH)
        print("Validating data...")
        validate_data(data)
        print("Cleaning data...")
        cleaned = clean_data(data, logger)
        print("Analyzing data...")
        analysis = analyze_data(cleaned)
        print("Generating Excel report...")
        generate_excel_report(analysis, OUTPUT_DIR / "business_report.xlsx")
        print("Generating PDF report...")
        generate_pdf_report(analysis, OUTPUT_DIR / "business_report.pdf")
        logger.info("Report completed successfully with %s rows.", len(cleaned))
        print("Report completed successfully.")
        return 0
    except (DataValidationError, ValueError, OSError) as error:
        logger.exception("Report generation failed: %s", error)
        print(f"Report generation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
