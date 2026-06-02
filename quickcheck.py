import argparse
from pathlib import Path
import pandas as pd

from src.io_loader import load_sales_daily
from src.validator import validate_daily
from src.aggregator import daily_to_quarterly
from src.forecaster import select_and_forecast

def main():
    ap = argparse.ArgumentParser("Quick forecast smoke test (no plotting)")
    ap.add_argument("--input", required=True)
    ap.add_argument("--sheet-name", default=None)
    ap.add_argument("--date-format", default="%Y-%m-%d")
    ap.add_argument("--horizon", type=int, default=6)
    ap.add_argument("--outdir", default="outputs")
    ap.add_argument("--max-parts", type=int, default=25, help="limit number of parts to test")
    args = ap.parse_args()

    df = load_sales_daily(args.input, date_format=args.date_format, sheet_name=args.sheet_name)
    df = df.sort_values("Date").reset_index(drop=True)
    validate_daily(df)

    print(f"[QC] Loaded {len(df)} rows, columns={list(df.columns)}")
    qdf = daily_to_quarterly(df, agg="sum", quarter_alias="QE-DEC")
    if qdf.empty:
        print("[QC] No quarterly data produced.")
        return

    parts = qdf["Part_number"].unique().tolist()
    print(f"[QC] Quarterly rows: {len(qdf)}, unique parts: {len(parts)}")

    forecasts, debug = [], []
    count = 0
    for part in parts:
        g = qdf[qdf["Part_number"] == part]
        series_q = pd.Series(g["Value_Q"].values,
                             index=pd.PeriodIndex(g["Quarter"], freq="Q-DEC"))
        try:
            fc = select_and_forecast(series_q, horizon=args.horizon, seasonal_periods=4)
            row = {"Part_number": part, "Method": fc["method"]}
            for i, (idx, val) in enumerate(zip(fc["index"], fc["values"]), start=1):
                row[f"q+i_label_{i}"] = str(idx)
                row[f"t+{i}"] = float(val)
            forecasts.append(row)
        except Exception as e:
            debug.append({"Part_number": part, "reason": str(e)})

        count += 1
        if count >= args.max_parts:
            break

    out_dir = Path(args.outdir)
    (out_dir / "forecasts").mkdir(parents=True, exist_ok=True)
    (out_dir / "debug").mkdir(parents=True, exist_ok=True)

    f_path = out_dir / "forecasts" / "quickcheck_forecasts.csv"
    d_path = out_dir / "debug" / "quickcheck_debug.csv"
    pd.DataFrame(forecasts).to_csv(f_path, index=False)
    pd.DataFrame(debug).to_csv(d_path, index=False)

    print(f"[QC] Wrote {len(forecasts)} forecasts ? {f_path}")
    print(f"[QC] Wrote {len(debug)} debug rows ? {d_path}")

if __name__ == "__main__":
    main()
