import logging

import pandas as pd


TEXT_COLUMNS = ("OrderID", "Customer", "Product", "Region")
CORE_COLUMNS = ("OrderID", "Customer", "Product", "Region", "OrderDate", "Quantity", "Sales")


def clean_data(data: pd.DataFrame, logger: logging.Logger | None = None) -> pd.DataFrame:
    """Normalize formatting and remove rows that are incomplete, with an audit log."""
    cleaned = data.copy()
    for column in TEXT_COLUMNS:
        cleaned[column] = cleaned[column].astype("string").str.strip()
        cleaned.loc[cleaned[column].eq(""), column] = pd.NA
    cleaned["OrderDate"] = pd.to_datetime(cleaned["OrderDate"], errors="coerce")
    cleaned["Quantity"] = pd.to_numeric(cleaned["Quantity"], errors="coerce")
    cleaned["Sales"] = pd.to_numeric(cleaned["Sales"], errors="coerce")

    incomplete = cleaned[list(CORE_COLUMNS)].isna().any(axis=1)
    if incomplete.any() and logger:
        logger.warning("Excluded %s incomplete row(s) during cleaning.", int(incomplete.sum()))
    cleaned = cleaned.loc[~incomplete].copy()
    if cleaned.empty:
        raise ValueError("No complete rows remain after cleaning.")
    return cleaned
