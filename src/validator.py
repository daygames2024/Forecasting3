
def validate_daily(df,
                   part_col: str = "Part_number",
                   date_col: str = "Date",
                   value_col: str = "Value") -> None:
    """
    Validation WITHOUT rejecting multiple rows per day.
    Allows repeated (Part_number, Date) entries because
    each row represents independent sales that must be counted.
    """

    # Ensure no negative values
    if (df[value_col] < 0).any():
        raise ValueError("Negative sales detected; check input.")

    # Ensure dates and values are present (done earlier in io_loader)
    if df[[part_col, date_col, value_col]].isnull().any().any():
        raise ValueError("Null values detected in required columns.")

