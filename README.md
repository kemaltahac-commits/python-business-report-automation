# Python Business Report Automation Tool

Turns a sales CSV into a cleaned, repeatable business report in Excel and PDF formats, with AI-generated business insights.

## What it does

The application loads a CSV, validates its structure and values, cleans safe formatting issues, calculates business KPIs, generates an Excel workbook, generates a PDF executive report, and records the run in `logs/app.log`.

The PDF report also includes AI-generated business insights powered by the Gemini API.

Python/Pandas performs the calculations and provides the structured analysis data, while the AI interprets those results into business trends, risks, opportunities, and an executive summary.

## Pipeline

```text
CSV
 ↓
Load
 ↓
Validation
 ↓
Cleaning
 ↓
Business Analysis
 ↓
 ├── Excel Report
 │
 └── PDF Report
        ↓
   AI Business Insights
```

## Project Structure

```text
Python Business Report Automation Tool/
│
├── input/
│   └── mainsales.csv
│
├── output/
│   ├── business_report.xlsx
│   └── business_report.pdf
│
├── logs/
│   └── app.log
│
├── src/
│   ├── loader.py
│   ├── validator.py
│   ├── cleaner.py
│   ├── analyzer.py
│   ├── excel_reporter.py
│   ├── pdf_reporter.py
│   ├── ai_client.py
│   └── main.py
│
├── tests/
│
├── README.md
└── requirements.txt
```

## Technologies

- Python
- Pandas
- OpenPyXL
- ReportLab
- Google Gemini API
- Pytest

## Data Validation

Before analysis, the application validates:

- Required columns
- Empty input data
- Numeric `Quantity` values
- Numeric `Sales` values
- Valid `OrderDate` values
- Duplicate `OrderID` values

Invalid input raises a validation error instead of producing an unreliable report.

## Data Cleaning

The cleaning pipeline:

- Strips unnecessary whitespace from text fields
- Converts empty text values to missing values
- Converts dates to datetime values
- Converts `Quantity` to numeric values
- Converts `Sales` to numeric values
- Removes incomplete rows
- Records excluded rows in the application log

## Business Analysis

The Python/Pandas analysis calculates:

- Total Sales
- Total Orders
- Total Quantity
- Average Order Value
- Sales by Product
- Sales by Region
- Sales by Customer
- Quantity by Product
- Monthly Sales
- Top 5 Products
- Top 5 Customers
- Best-Performing Region
- Reporting Period

## Excel Report

The Excel report is generated as:

```text
output/business_report.xlsx
```

It contains the following worksheets:

- Summary
- Sales by Product
- Sales by Region
- Sales by Customer
- Product Quantity
- Monthly Sales

The workbook includes:

- Formatted headers
- Automatic column width adjustment
- Currency formatting
- KPI summary
- Reporting period
- Best-performing region

## PDF Report

The executive PDF report is generated as:

```text
output/business_report.pdf
```

The report includes:

- Reporting period
- Total Sales
- Total Orders
- Total Quantity
- Average Order Value
- Top Products
- Top Customers
- Regional Performance
- Monthly Sales
- Automated observations
- AI Business Insights

## AI Business Insights

The Gemini API does not perform the core business calculations.

Python/Pandas calculates the metrics first and passes the structured results to the AI.

The AI is then asked to interpret the calculated data and provide:

1. Key Trend
2. Strongest Product
3. Strongest Region
4. Business Risk
5. Business Opportunities
6. Executive Summary

The AI prompt explicitly instructs the model to use only the provided data and not invent numbers, customers, products, trends, or facts.

## Installation

Clone the repository:

```bash
git clone <YOUR_REPOSITORY_URL>
cd "Python Business Report Automation Tool"
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Gemini API Setup

The application expects the Gemini API key to be available through the `GEMINI_API_KEY` environment variable.

Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

The application will raise an error if the environment variable is not available.

## Usage

Run the application from the project root:

```bash
python src/main.py
```

The application will:

1. Load the sales CSV
2. Validate the data
3. Clean the data
4. Calculate business metrics
5. Generate the Excel report
6. Generate the PDF report
7. Generate AI business insights
8. Record the run in `logs/app.log`

## Example Run

```text
Loading data...
Validating data...
Cleaning data...
Analyzing data...
Generating Excel report...
Generating PDF report...
Gemini analiz yapıyor...
Report completed successfully.
```

## Output

After a successful run:

```text
output/
├── business_report.xlsx
└── business_report.pdf
```

The application log is stored at:

```text
logs/app.log
```

## Example Business Results

The project was tested with a 150-row sales dataset.

The resulting report contained:

- 150 orders
- $71,383.79 total sales
- Excel business report
- PDF executive report
- AI-generated business insights

Example analysis identified sales concentration in products such as Monitors and Webcams and highlighted regional sales performance.

## Testing

The project includes automated tests for the business pipeline.

Run the tests with:

```bash
pytest
```

The current test suite passes successfully.

## Design Principle

The project separates deterministic calculations from AI interpretation.

```text
Python / Pandas
      ↓
Reliable calculations
      ↓
Structured AnalysisResult
      ↓
Gemini AI
      ↓
Business interpretation
```

This allows Python to remain the source of truth for numerical calculations while AI is used for interpretation and business-oriented summaries.

## Purpose

This project demonstrates how Python, Pandas, automated reporting, and generative AI can be combined into a repeatable business reporting workflow.

It focuses on turning raw sales data into structured business information that can be delivered through Excel and PDF reports.