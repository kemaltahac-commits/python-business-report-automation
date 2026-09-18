import pandas as pd
import pytest

from src.analyzer import analyze_data
from src.cleaner import clean_data
from src.validator import DataValidationError, validate_data


def sample_data() -> pd.DataFrame:
    return pd.DataFrame({
        "OrderID": ["1", "2", "3"], "Customer": ["Alice", "Bob", "Alice"],
        "Product": ["Widget", "Gadget", "Widget"], "Region": ["North", "South", "North"],
        "OrderDate": ["2026-02-01", "2026-01-15", "2026-02-20"],
        "Quantity": ["2", "3", "1"], "Sales": ["100", "50", "150"],
    })


def test_missing_required_column_is_rejected():
    with pytest.raises(DataValidationError, match="Missing required columns"):
        validate_data(sample_data().drop(columns="Sales"))


def test_numeric_conversion_and_whitespace_cleaning():
    data = sample_data()
    data.loc[0, "Sales"] = " 100.5 "
    data.loc[0, "Customer"] = " Alice "
    validate_data(data)
    cleaned = clean_data(data)
    assert cleaned.loc[0, "Sales"] == 100.5
    assert cleaned.loc[0, "Customer"] == "Alice"


def test_duplicate_order_ids_are_rejected():
    data = sample_data()
    data.loc[1, "OrderID"] = "1"
    with pytest.raises(DataValidationError, match="Duplicate OrderIDs"):
        validate_data(data)


def test_calculated_metrics_top_product_region_and_month_order():
    data = clean_data(sample_data())
    result = analyze_data(data)
    assert result.total_sales == 300.0
    assert result.total_orders == 3
    assert result.average_order_value == 100.0
    assert result.top_products.iloc[0]["Product"] == "Widget"
    assert result.best_region == "North"
    assert result.monthly_sales["Month"].tolist() == ["2026-01", "2026-02"]
