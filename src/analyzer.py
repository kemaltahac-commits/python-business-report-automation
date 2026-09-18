from dataclasses import dataclass

import pandas as pd


@dataclass
class AnalysisResult:
    total_sales: float
    total_orders: int
    total_quantity: float
    average_order_value: float
    sales_by_product: pd.DataFrame
    sales_by_region: pd.DataFrame
    sales_by_customer: pd.DataFrame
    quantity_by_product: pd.DataFrame
    monthly_sales: pd.DataFrame
    top_products: pd.DataFrame
    top_customers: pd.DataFrame
    best_region: str
    reporting_start: pd.Timestamp
    reporting_end: pd.Timestamp


def _sum_by(data: pd.DataFrame, group: str, value: str, label: str) -> pd.DataFrame:
    return (data.groupby(group, as_index=False)[value].sum()
            .rename(columns={value: label})
            .sort_values(label, ascending=False, ignore_index=True))


def analyze_data(data: pd.DataFrame) -> AnalysisResult:
    sales_by_product = _sum_by(data, "Product", "Sales", "Sales")
    sales_by_region = _sum_by(data, "Region", "Sales", "Sales")
    sales_by_customer = _sum_by(data, "Customer", "Sales", "Sales")
    quantity_by_product = _sum_by(data, "Product", "Quantity", "Quantity")
    monthly = data.assign(Month=data["OrderDate"].dt.to_period("M").astype(str))
    monthly_sales = (monthly.groupby("Month", as_index=False)["Sales"].sum()
                     .sort_values("Month", ignore_index=True))
    total_sales = float(data["Sales"].sum())
    total_orders = int(data["OrderID"].nunique())
    return AnalysisResult(
        total_sales=total_sales,
        total_orders=total_orders,
        total_quantity=float(data["Quantity"].sum()),
        average_order_value=total_sales / total_orders if total_orders else 0.0,
        sales_by_product=sales_by_product,
        sales_by_region=sales_by_region,
        sales_by_customer=sales_by_customer,
        quantity_by_product=quantity_by_product,
        monthly_sales=monthly_sales,
        top_products=sales_by_product.head(5).copy(),
        top_customers=sales_by_customer.head(5).copy(),
        best_region=str(sales_by_region.iloc[0]["Region"]),
        reporting_start=data["OrderDate"].min(),
        reporting_end=data["OrderDate"].max(),
    )
