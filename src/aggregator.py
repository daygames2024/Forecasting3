
import pandas as pd
from pathlib import Path

def daily_to_quarterly(df, agg="sum", quarter_alias="QE-DEC"):
    """
    Convert daily rows into per-part quarterly totals.

    Expects columns: Date (datetime-like), Part_number, Value (numeric)
    Returns columns: Part_number, Quarter (str 'YYYYQn'), Value_Q (float)
    """
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce").fillna(0.0)
    df = df.dropna(subset=["Date"]).sort_values("Date")

    out = []
    for part, g in df.groupby("Part_number", sort=False):
        if g.empty:
            continue

        s = g.set_index("Date")["Value"].sort_index()
        # Resample to quarter-end in December (no deprecation warning)
        q = getattr(s.resample("QE-DEC"), agg)()
        # Replace NaN with 0 (can happen with mean aggregation on empty quarters)
        q = q.fillna(0.0)
        # Ensure contiguous quarterly index to current end (fill missing with 0)
        q = q.asfreq("QE-DEC", fill_value=0.0)

        # Use PeriodIndex for quarter labels (Q-DEC) but store strings in output
        q_period = q.index.to_period("Q-DEC")
        part_df = pd.DataFrame(
            {
                "Part_number": part,
                "Quarter": q_period.astype(str),
                "Value_Q": q.values.astype(float),
            }
        )
        out.append(part_df)

    if not out:
        return pd.DataFrame(columns=["Part_number", "Quarter", "Value_Q"])

    return pd.concat(out, ignore_index=True)


def log_daily_totals(df,
                     part_col="Part_number",
                     value_col="Value",
                     date_col="Date",
                     outdir="outputs"):
    """
    Produces per-day summation logging into outputs/daily_logs/daily_summary.csv
    """
    daily = (
        df.groupby([part_col, date_col])[value_col]
        .sum()
        .reset_index()
        .sort_values([part_col, date_col])
    )

    log_dir = Path(outdir) / "daily_logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    out_path = log_dir / "daily_summary.csv"
    daily.to_csv(out_path, index=False)
    return out_path
