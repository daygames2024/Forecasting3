
# src/writer.py
from pathlib import Path
import pandas as pd

def write_outputs(forecasts, debug, outdir):
    """
    Writes:
      - outputs/forecasts/forecasts.csv  (aligned quarter headers)
      - outputs/debug/debug.csv
    Returns path to forecasts.csv
    """
    out_root = Path(outdir)
    f_dir = out_root / "forecasts"
    d_dir = out_root / "debug"
    f_dir.mkdir(parents=True, exist_ok=True)
    d_dir.mkdir(parents=True, exist_ok=True)

    # -----------------------------
    # Build aligned forecast table
    # -----------------------------
    if forecasts:
        # Extract globally aligned quarter labels (same for all rows)
        # Example: ["2025Q2", "2025Q3", "2025Q4", "2026Q1", "2026Q2", "2026Q3"]
        quarter_cols = forecasts[0].get("index", [])
        quarter_cols = list(quarter_cols)  # ensure list

        rows = []
        for row in forecasts:
            # Base fields
            base = {
                "Part_number": row.get("Part_number", ""),
                "Method": row.get("Method", ""),
                "Score": row.get("Score", ""),
                "Pattern": row.get("Pattern", ""),  # <-- Added Pattern column
                "last_1Q_total": row.get("last_1Q_total", ""),
                "last_2Q_total": row.get("last_2Q_total", ""),
                "last_4Q_total": row.get("last_4Q_total", ""),
                "Plot": row.get("Plot", ""),
            }
            # Quarter values under aligned header labels
            idx_list = row.get("index", [])
            val_list = row.get("values", [])
            for q_label, val in zip(idx_list, val_list):
                base[str(q_label)] = val
            rows.append(base)

        f_df = pd.DataFrame(rows)

        # Ensure all expected quarter columns exist even if some rows are missing
        for q in quarter_cols:
            if q not in f_df.columns:
                f_df[q] = ""

        # 🔁 Final column order: id/method/score → quarters → lag metrics → plot
        final_cols = [
            "Part_number", "Method", "Score", "Pattern"  # <-- Added Pattern here
        ] + quarter_cols + [
            "last_1Q_total", "last_2Q_total", "last_4Q_total", "Plot"
        ]
        # Create any missing columns with empty values before reordering
        for c in final_cols:
            if c not in f_df.columns:
                f_df[c] = ""
        f_df = f_df[final_cols]

    else:
        # Empty forecasts — still produce a well-formed file
        f_df = pd.DataFrame(columns=[
            "Part_number", "Method", "Score", "Pattern",  # <-- Added Pattern here
            # If you want to include header quarters even when empty, you could add them here
            "last_1Q_total", "last_2Q_total", "last_4Q_total", "Plot"
        ])

    # -----------------------------
    # Write forecast CSV
    # -----------------------------
    f_path = f_dir / "forecasts.csv"
    f_df.to_csv(f_path, index=False)

    # -----------------------------
    # Write debug CSV
    # -----------------------------
    d_df = pd.DataFrame(debug)
    if d_df.empty:
        d_df = pd.DataFrame(columns=["Part_number", "reason"])
    d_path = d_dir / "debug.csv"
    d_df.to_csv(d_path, index=False)

    return f_path
