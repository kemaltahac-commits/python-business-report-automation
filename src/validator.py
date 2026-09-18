from dataclasses import dataclass

import pandas as pd


REQUIRED_COLUMNS = ("OrderID", "Customer", "Product", "Region", "OrderDate", "Quantity", "Sales")


class DataValidationError(ValueError):
    """Raised when input cannot produce a trustworthy report."""


@dataclass(frozen=True)
class ValidationResult:
    duplicate_order_ids: list[str]


def _non_empty(series: pd.Series) -> pd.Series:
    return series.notna() & series.astype(str).str.strip().ne("")


def validate_data(data: pd.DataFrame) -> ValidationResult:
    """Validate source structure and values without modifying source data."""
    missing = sorted(set(REQUIRED_COLUMNS) - set(data.columns))
    if missing:
        raise DataValidationError(f"Missing required columns: {', '.join(missing)}")
    if data.empty:
        raise DataValidationError("The input CSV contains no data rows.")

    errors: list[str] = []
    for column in ("Quantity", "Sales"):
        source = data[column]
        converted = pd.to_numeric(source, errors="coerce")
        invalid = _non_empty(source) & converted.isna()
        if invalid.any():
            errors.append(f"{column} has non-numeric values at rows: {', '.join(map(str, (data.index[invalid] + 2).tolist()))}")

    source_dates = data["OrderDate"]
    converted_dates = pd.to_datetime(source_dates, errors="coerce")
    invalid_dates = _non_empty(source_dates) & converted_dates.isna()
    if invalid_dates.any():
        errors.append(f"OrderDate has invalid values at rows: {', '.join(map(str, (data.index[invalid_dates] + 2).tolist()))}")

    ids = data["OrderID"].fillna("").astype(str).str.strip()
    duplicates = ids[ids.ne("") & ids.duplicated(keep=False)].unique().tolist()
    if duplicates:
        errors.append(f"Duplicate OrderIDs detected: {', '.join(duplicates)}")
    if errors:
        raise DataValidationError("; ".join(errors))
    return ValidationResult(duplicate_order_ids=duplicates)
