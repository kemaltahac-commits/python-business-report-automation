import os

from google import genai

from analyzer import AnalysisResult


def analyze_sales_with_ai(analysis: AnalysisResult) -> str:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY bulunamadı.")

    # Python/Pandas tarafından hesaplanan gerçek veriler
    sales_by_product = (
        analysis.sales_by_product
        .to_dict(orient="records")
    )

    sales_by_region = (
        analysis.sales_by_region
        .to_dict(orient="records")
    )

    sales_by_customer = (
        analysis.sales_by_customer
        .to_dict(orient="records")
    )

    monthly_sales = (
        analysis.monthly_sales
        .to_dict(orient="records")
    )

    prompt = f"""
You are a professional business analyst.

Analyze the following sales report.

IMPORTANT RULES:
- Use ONLY the data provided below.
- Do NOT invent numbers, trends, customers, products, or facts.
- Python has already calculated the metrics.
- Your job is to interpret the data and provide useful business insights.
- Keep the language concise, professional, and suitable for a business report.

GENERAL METRICS:
Total Sales: {analysis.total_sales:.2f}
Total Orders: {analysis.total_orders}
Total Quantity: {analysis.total_quantity:.0f}
Average Order Value: {analysis.average_order_value:.2f}

REPORTING PERIOD:
Start: {analysis.reporting_start}
End: {analysis.reporting_end}

BEST REGION:
{analysis.best_region}

SALES BY PRODUCT:
{sales_by_product}

SALES BY REGION:
{sales_by_region}

SALES BY CUSTOMER:
{sales_by_customer}

MONTHLY SALES:
{monthly_sales}

TOP PRODUCTS:
{analysis.top_products.to_dict(orient="records")}

TOP CUSTOMERS:
{analysis.top_customers.to_dict(orient="records")}

Provide the following sections:

1. KEY TREND
Explain the most important trend visible in the data.

2. STRONGEST PRODUCT
Identify the strongest product and explain its importance.

3. STRONGEST REGION
Identify the strongest region and explain its importance.

4. BUSINESS RISK
Identify one realistic business risk supported by the data.

5. OPPORTUNITIES
Identify two practical business opportunities supported by the data.

6. EXECUTIVE SUMMARY
Write a short 2-3 sentence summary suitable for a manager.

Do not repeat the raw tables.
Do not invent information.
Focus on actionable business interpretation.
"""

    print("Gemini analiz yapıyor...")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    if not response.text:
        raise RuntimeError("Gemini boş bir cevap döndürdü.")

    return response.text


if __name__ == "__main__":
    print("Bu modül doğrudan çalıştırılmak yerine main.py tarafından kullanılmalıdır.")