from pathlib import Path

import pandas as pd


def load_csv(path: Path) -> pd.DataFrame:
    """Load a CSV while preserving blank fields for validation and cleaning."""
    try:
        return pd.read_csv(path, dtype=str, keep_default_na=True)
    except FileNotFoundError as error:
        raise ValueError(f"Input file was not found: {path}") from error
    except (pd.errors.ParserError, UnicodeDecodeError) as error:
        raise ValueError(f"Could not read CSV file: {error}") from error
