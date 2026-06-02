
# Demand Forecast (Daily → Quarterly → 6Q Ahead)

Forecast per-part demand **6 calendar quarters ahead** based on **daily sales** input (`YYYY-MM-DD`).
The forecast **starts at the quarter immediately after** the last observed date.

## Input
Excel `.xlsx` (or `.csv`) with columns:
- `Part_number` (string)
- `Value` (numeric)
- `Date` (`YYYY-MM-DD`)

## Quick Start (CLI)
```bash
pip install -r requirements.txt

# CSV
python -m src.app --input data/sales_daily.csv --date-format %Y-%m-%d --agg sum --horizon 6 --outdir outputs

# Excel (single sheet)
python -m src.app --input data/sales_daily.xlsx --date-format %Y-%m-%d --agg sum --horizon 6 --outdir outputs

# Excel (specific sheet)
python -m src.app --input data/sales_daily.xlsx --sheet-name Sheet1 --date-format %Y-%m-%d --agg sum --horizon 6 --outdir outputs

