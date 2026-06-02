
import os
import pandas as pd

def load_sales_daily(path: str,
                     date_format: str = "%Y-%m-%d",
                     part_col: str = "Part_number",
                     value_col: str = "Value",
                     date_col: str = "Date",
                     sheet_name: str | None = None) -> pd.DataFrame:
    """
    Loads daily sales data from CSV or Excel.
    Ensures that Date is parsed into datetime.
    Drops rows with invalid dates.
    Always returns a DataFrame.
    """

    ext = os.path.splitext(path.lower())[1]

    # Read file
    if ext in [".xlsx", ".xls"]:
        read_kwargs = {}
        if sheet_name:
            read_kwargs["sheet_name"] = sheet_name
        df = pd.read_excel(path, **read_kwargs)
    elif ext == ".csv":
        df = pd.read_csv(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    # Check required columns
    expected = {part_col, value_col, date_col}
    missing = expected - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Trim whitespace
    df[date_col] = df[date_col].astype(str).str.strip()

    # Convert dates (safe conversion)
    df[date_col] = pd.to_datetime(df[date_col], format=date_format, errors="coerce")

    # Drop invalid dates
    invalid_count = df[date_col].isna().sum()
    if invalid_count > 0:
        print(f"[WARN] Dropping {invalid_count} rows with invalid dates")
        df = df.dropna(subset=[date_col])

    # Ensure numeric values
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")
    df = df.dropna(subset=[value_col])

    # ALWAYS return the DataFrame
    return df

