from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from analyzer import AnalysisResult
from ai_client import analyze_sales_with_ai


def _money(value: float) -> str:
    return f"${value:,.2f}"


def _number(value: float) -> str:
    return f"{value:,.0f}"


def _safe_text(value) -> str:
    return escape(str(value))


def _format_table_value(column, value) -> str:
    """
    Format values for PDF tables.

    Sales -> currency
    Quantity / numeric counts -> whole numbers
    Everything else -> normal text
    """

    if column == "Sales":
        return _money(float(value))

    if column in {"Quantity", "Orders"}:
        return _number(float(value))

    return _safe_text(value)


def _build_styles():
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            fontSize=22,
            leading=26,
            alignment=TA_CENTER,
            spaceAfter=8,
        )
    )

    styles.add(
        ParagraphStyle(
            name="ReportSubtitle",
            parent=styles["Normal"],
            fontSize=10,
            leading=14,
            alignment=TA_CENTER,
            spaceAfter=18,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            parent=styles["Heading2"],
            fontSize=14,
            leading=18,
            spaceBefore=12,
            spaceAfter=8,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Observation",
            parent=styles["BodyText"],
            fontSize=9,
            leading=13,
            leftIndent=8,
            spaceAfter=5,
        )
    )

    styles.add(
        ParagraphStyle(
            name="AIHeading",
            parent=styles["Heading3"],
            fontSize=11,
            leading=14,
            spaceBefore=7,
            spaceAfter=4,
        )
    )

    styles.add(
        ParagraphStyle(
            name="AIText",
            parent=styles["BodyText"],
            fontSize=9,
            leading=13,
            spaceAfter=6,
        )
    )

    return styles


def _df_table(
    dataframe,
    headers,
    columns,
    widths=None,
    max_rows=None,
):
    rows = [headers]

    data = dataframe.copy()

    if max_rows is not None:
        data = data.head(max_rows)

    for _, row in data.iterrows():
        rows.append(
            [
                _format_table_value(
                    column,
                    row[column],
                )
                for column in columns
            ]
        )

    table = Table(
        rows,
        colWidths=widths,
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1f2937"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.grey,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "ALIGN",
                    (1, 1),
                    (-1, -1),
                    "RIGHT",
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#f3f4f6"),
                    ],
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
            ]
        )
    )

    return table


def _add_kpi_table(story, result: AnalysisResult):
    styles = getSampleStyleSheet()

    kpi_data = [
        [
            Paragraph("<b>Total Sales</b>", styles["BodyText"]),
            Paragraph("<b>Total Orders</b>", styles["BodyText"]),
            Paragraph("<b>Total Quantity</b>", styles["BodyText"]),
            Paragraph("<b>AOV</b>", styles["BodyText"]),
        ],
        [
            _money(result.total_sales),
            _number(result.total_orders),
            _number(result.total_quantity),
            _money(result.average_order_value),
        ],
    ]

    table = Table(
        kpi_data,
        colWidths=[
            43 * mm,
            43 * mm,
            43 * mm,
            43 * mm,
        ],
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#e5e7eb"),
                ),
                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, 1),
                    colors.white,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER",
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(table)
    story.append(Spacer(1, 8))


def build_observations(result: AnalysisResult):
    observations = []

    if not result.sales_by_product.empty:
        best_product = result.sales_by_product.iloc[0]

        observations.append(
            f"Top product: {best_product['Product']} "
            f"with {_money(float(best_product['Sales']))} in sales."
        )

    if not result.sales_by_region.empty:
        best_region = result.sales_by_region.iloc[0]

        observations.append(
            f"Top region: {best_region['Region']} "
            f"with {_money(float(best_region['Sales']))} in sales."
        )

    if not result.monthly_sales.empty:
        best_month = result.monthly_sales.loc[
            result.monthly_sales["Sales"].idxmax()
        ]

        observations.append(
            f"Best month: {best_month['Month']} "
            f"with {_money(float(best_month['Sales']))} in sales."
        )

    if result.average_order_value > 0:
        observations.append(
            f"Average order value is "
            f"{_money(result.average_order_value)}."
        )

    return observations


def _format_ai_line(line: str, styles):
    line = line.strip()

    if not line:
        return None

    if line.startswith("**") and line.endswith("**"):
        heading = line.strip("*").strip()

        return Paragraph(
            _safe_text(heading),
            styles["AIHeading"],
        )

    if len(line) > 3 and line[0].isdigit():
        dot_position = line.find(".")

        if dot_position != -1 and dot_position <= 3:
            heading = line[dot_position + 1:].strip()

            if heading and len(heading) < 80:
                return Paragraph(
                    f"<b>{_safe_text(line)}</b>",
                    styles["AIHeading"],
                )

    if line.startswith("- "):
        line = "• " + line[2:].strip()

    if line.startswith("* "):
        line = "• " + line[2:].strip()

    return Paragraph(
        _safe_text(line),
        styles["AIText"],
    )


def _add_ai_insights(
    story,
    result: AnalysisResult,
    styles,
):
    story.append(
        Paragraph(
            "AI Business Insights",
            styles["SectionTitle"],
        )
    )

    try:
        print("Generating AI business insights...")

        ai_insights = analyze_sales_with_ai(result)

        if not ai_insights:
            story.append(
                Paragraph(
                    "AI analysis returned no content.",
                    styles["AIText"],
                )
            )
            return

        for line in ai_insights.splitlines():
            element = _format_ai_line(
                line,
                styles,
            )

            if element is not None:
                story.append(element)

    except Exception as error:
        print(f"AI analysis failed: {error}")

        story.append(
            Paragraph(
                f"AI analysis unavailable: "
                f"{_safe_text(error)}",
                styles["AIText"],
            )
        )


def generate_pdf_report(
    result: AnalysisResult,
    output_path: Path,
):
    output_path = Path(output_path)
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    styles = _build_styles()

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        title="Business Sales Report",
        author="Python Business Report Automation",
    )

    story = []

    # ---------------------------------------------------------
    # TITLE
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Business Sales Report",
            styles["ReportTitle"],
        )
    )

    story.append(
        Paragraph(
            f"Reporting Period: "
            f"{result.reporting_start.strftime('%Y-%m-%d')} "
            f"to "
            f"{result.reporting_end.strftime('%Y-%m-%d')}",
            styles["ReportSubtitle"],
        )
    )

    # ---------------------------------------------------------
    # KPI
    # ---------------------------------------------------------

    _add_kpi_table(
        story,
        result,
    )

    # ---------------------------------------------------------
    # TOP PRODUCTS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Top Products",
            styles["SectionTitle"],
        )
    )

    story.append(
        _df_table(
            result.top_products,
            headers=["Product", "Sales"],
            columns=["Product", "Sales"],
            widths=[
                120 * mm,
                50 * mm,
            ],
        )
    )

    story.append(Spacer(1, 6))

    # ---------------------------------------------------------
    # TOP CUSTOMERS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Top Customers",
            styles["SectionTitle"],
        )
    )

    story.append(
        _df_table(
            result.top_customers,
            headers=["Customer", "Sales"],
            columns=["Customer", "Sales"],
            widths=[
                120 * mm,
                50 * mm,
            ],
        )
    )

    story.append(Spacer(1, 6))

    # ---------------------------------------------------------
    # REGIONAL PERFORMANCE
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Regional Performance",
            styles["SectionTitle"],
        )
    )

    story.append(
        _df_table(
            result.sales_by_region,
            headers=["Region", "Sales"],
            columns=["Region", "Sales"],
            widths=[
                120 * mm,
                50 * mm,
            ],
        )
    )

    story.append(Spacer(1, 6))

    # ---------------------------------------------------------
    # MONTHLY SALES
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Monthly Sales",
            styles["SectionTitle"],
        )
    )

    story.append(
        _df_table(
            result.monthly_sales,
            headers=["Month", "Sales"],
            columns=["Month", "Sales"],
            widths=[
                120 * mm,
                50 * mm,
            ],
        )
    )

    story.append(Spacer(1, 6))

    # ---------------------------------------------------------
    # AUTOMATED OBSERVATIONS
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "Automated Observations",
            styles["SectionTitle"],
        )
    )

    observations = build_observations(result)

    for observation in observations:
        story.append(
            Paragraph(
                f"• {_safe_text(observation)}",
                styles["Observation"],
            )
        )

    # ---------------------------------------------------------
    # AI BUSINESS INSIGHTS
    # ---------------------------------------------------------

    _add_ai_insights(
        story,
        result,
        styles,
    )

    # ---------------------------------------------------------
    # BUILD PDF
    # ---------------------------------------------------------

    document.build(story)

    print(
        f"PDF report created: {output_path}"
    )