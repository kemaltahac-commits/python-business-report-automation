# Python Business Report Automation Tool

Turns a sales CSV into a cleaned, repeatable business report in Excel and PDF formats, with AI-generated business insights.

## What it does

The application loads a CSV, validates its structure and values, cleans safe formatting issues, calculates business KPIs, generates an Excel workbook, generates a PDF executive report, and records the run in `logs/app.log`.

The PDF report also includes AI-generated business insights powered by the Gemini API. Python/Pandas performs the calculations and provides the structured analysis data, while the AI interprets those results into business trends, risks, opportunities, and an executive summary.

## Project structure

```text
input/mainsales.csv       Input sales data

output/                   Generated reports

logs/app.log              Application log

src/
├── loader.py             CSV loading
├── validator.py          Data validation
├── cleaner.py            Data cleaning
├── analyzer.py           Business analysis
├── excel_reporter.py     Excel report generation
├── pdf_reporter.py       PDF report generation
├── ai_client.py          Gemini AI integration
└── main.py               Application entry point

tests/                    Business-logic tests