# Monthly Bias Correction Update Guide

> **Quick Reference:** How to update your forecast accuracy report each month to keep bias corrections current

---

## What This Does

Updates the `forecast_accuracy_report.csv` file so your forecasts automatically get better over time by learning from past errors.

**Time Required:** 5 minutes  
**Frequency:** Monthly (after actual sales data is available)

---

## Monthly Update Steps

### Step 1: Gather Your Files 📁

You need **TWO files**:

| File | Description | Example |
|------|-------------|---------|
| **Old Forecast** | A forecast you made 1-3 months ago | `September_2024_forecast.csv` |
| **Current Sales** | Actual sales data covering the forecasted period | `November_2024_sales.xlsx` |

**Example Timeline:**
- September: You created a forecast predicting Q4 2024
- November: You now have actual Q4 2024 sales data
- **Action:** Compare September forecast vs November actuals

---

### Step 2: Run the Comparison Script 🔄

Open **PowerShell** in your project folder and run:

```powershell
python fix_forecast_comparison.py --old-forecast "path/to/old_forecast.csv" --actual-sales "path/to/current_sales.xlsx"
```

**Real-World Example:**

```powershell
python fix_forecast_comparison.py --old-forecast "output/September_2024_forecast.csv" --actual-sales "data/sales_Nov2024.xlsx"
```

---

### Step 3: Verify the Output ✅

The script creates **two files** in your `output` folder:

#### File 1: `forecast_accuracy_report.csv`
- Main bias correction file
- Used automatically by forecasting system
- Updated with latest accuracy data

#### File 2: `forecast_accuracy_report_analysis.xlsx`
- Detailed Excel report with 6 sheets
- Review this to understand forecast performance

**Console Output Example:**
```
✅ Loaded forecast data: 1,234 parts
✅ Loaded actual sales data: 45,678 rows
✅ Matched 5,432 forecast-actual pairs

Average error: +28.5%
⚠️ SYSTEMATIC OVER-FORECASTING DETECTED
   Suggested correction factor: 0.817x

✅ Full report saved to: output/forecast_accuracy_report.csv
✅ Detailed analysis report saved to: output/forecast_accuracy_report_analysis.xlsx
```

---

### Step 4: Next Forecast Automatically Uses Updates 🚀

**No additional steps needed!**

The next time you run a forecast, the system will:
- ✅ Automatically detect the updated `forecast_accuracy_report.csv`
- ✅ Apply the latest correction factors to each part
- ✅ Generate both corrected and uncorrected forecasts
- ✅ Create Excel summary sheets for BOTH files (with performance metrics)

Just run your normal forecast command:
```powershell
python -m src.app --input "sales_data.xlsx" --events-file "maintenance_events.csv"
```

**Output files created:**
1. `forecast_output.csv` - Uncorrected forecast (CSV)
2. `forecast_output.xlsx` - Uncorrected forecast with summary sheet
3. `forecast_output_Corrected.csv` - Bias-corrected forecast (CSV)
4. `forecast_output_Corrected.xlsx` - **Bias-corrected forecast with summary sheet** ⭐
5. `correction_factors.csv` - Part-specific correction factors applied

---

## Required File Formats

### Old Forecast File (CSV)

Must have columns for each quarter you forecasted:

```csv
Part_number,25Q1,25Q2,25Q3,25Q4,26Q1,26Q2
ABC-123,100,105,110,115,120,125
DEF-456,50,52,55,58,60,62
GHI-789,200,205,210,215,220,225
```

### Actual Sales File (Excel or CSV)

Must have three columns: `Date`, `Part_number`, `Value`

```csv
Date,Part_number,Value
2024-10-01,ABC-123,25
2024-10-08,ABC-123,18
2024-10-15,DEF-456,12
2024-10-22,ABC-123,22
```

**Note:** The script automatically aggregates daily sales to quarterly totals.

---

## Monthly Workflow Checklist

- [ ] **Week 1 of Month:** Download latest sales data from your system
- [ ] **Week 1 of Month:** Locate forecast file from 1-2 months ago
- [ ] **Week 1 of Month:** Run `fix_forecast_comparison.py` script
- [ ] **Week 1 of Month:** Review `forecast_accuracy_report_analysis.xlsx` for insights
- [ ] **Week 2+ of Month:** Run new forecasts (bias corrections apply automatically)

---

## What the Script Does Automatically

1. ✅ Loads your old forecast and actual sales data
2. ✅ Aggregates daily sales to quarterly totals
3. ✅ Matches forecasts with actuals by part number and quarter
4. ✅ Calculates forecast errors and percentage errors
5. ✅ Detects systematic bias (over-forecasting vs under-forecasting)
6. ✅ Generates accuracy report for bias correction system
7. ✅ Creates detailed Excel analysis with recommendations

---

## Troubleshooting

### Error: "No matching data found"

**Cause:** Part numbers or date ranges don't align between files

**Fix:**
- Verify part numbers match exactly (case-sensitive)
- Check that actual sales covers at least one forecasted quarter
- Ensure date formats are correct in sales file

### Error: "No forecast columns found"

**Cause:** Old forecast file doesn't have quarter columns (25Q1, 25Q2, etc.)

**Fix:**
- Verify old forecast has columns named like: `25Q1`, `25Q2`, `25Q3`, `25Q4`
- Check that column names don't have extra spaces

### Script runs but accuracy report is empty

**Cause:** No overlapping quarters between forecast and actuals

**Fix:**
- Use a newer sales file that covers forecasted periods
- Or use an older forecast file that predicted current periods

---

## Quick Command Reference

```powershell
# Standard monthly update
python fix_forecast_comparison.py --old-forecast "output/last_forecast.csv" --actual-sales "data/current_sales.xlsx"

# Custom output location
python fix_forecast_comparison.py --old-forecast "old.csv" --actual-sales "sales.xlsx" --output "custom/path/accuracy.csv"

# Run normal forecast (bias applies automatically)
python -m src.app --input "sales_data.xlsx" --events-file "maintenance_events.csv"
```

---

## Tips for Best Results

💡 **Update regularly:** Monthly updates keep corrections accurate

💡 **Use recent data:** Compare forecasts 1-3 months old (not too old, not too new)

💡 **Review the analysis:** Check the Excel report to understand what's working and what's not

💡 **Track trends:** Save monthly analysis reports to see if forecast accuracy improves over time

💡 **Act on insights:** Review "Top_Errors" sheet to identify problematic parts

---

## Example Monthly Timeline

```
Month 1 (September):
  → Create forecast predicting Q4 2024 and Q1 2025

Month 2 (October):
  → Q4 2024 starts (actual sales begin)

Month 3 (November):
  → Q4 2024 ends (now have actual Q4 data)
  → UPDATE BIAS: Compare September forecast vs November actuals
  → Run: python fix_forecast_comparison.py ...

Month 4 (December):
  → Create new forecast (automatically uses November's bias corrections)
  → Predictions are now more accurate!
```

---

## Files Created Each Month

| File | Location | Purpose |
|------|----------|---------|
| `forecast_accuracy_report.csv` | `output/` | Used by forecasting system (overwritten each update) |
| `forecast_accuracy_report_analysis.xlsx` | `output/` | Detailed analysis for review (rename to save history) |
| `correction_factors.csv` | `output/` | Part-specific correction factors (reference only) |
| `forecast_output_Corrected.xlsx` | `output/` | **Bias-corrected forecast with summary sheet** ⭐ |

**Pro Tip:** Rename analysis files to keep history:
```powershell
# Save monthly snapshots
Rename-Item "output/forecast_accuracy_report_analysis.xlsx" "output/accuracy_Nov2024.xlsx"
Rename-Item "output/forecast_output_Corrected.xlsx" "output/forecast_Nov2024_Corrected.xlsx"
```

### What's in the Corrected Forecast Summary Sheet?

The `forecast_output_Corrected.xlsx` file includes a comprehensive summary sheet showing:

✅ **Bias Correction Stats** - Type of bias detected, correction factors applied  
✅ **Correction Impact** - How forecasts were adjusted (increased/decreased by %)  
✅ **Forecastability Tiers** - Distribution of parts by confidence level  
✅ **Confidence Intervals** - P10/P50/P90 ranges (all bias-corrected)  
✅ **Accuracy Improvement** - Expected reduction in forecast error (~72% → ~25%)  
✅ **Usage Recommendations** - Which file to use for planning

---

## Summary

**Monthly Task:** Run one command to update bias corrections

**What happens:** Future forecasts automatically improve

**Time investment:** 5 minutes per month

**Result:** Forecast accuracy improves from ~72% error to ~25% error

---

## Questions?

- **How often?** Monthly (or whenever you have new actual sales for a forecasted period)
- **What if I skip a month?** No problem - run it whenever you have data
- **Can I update multiple times?** Yes - latest update overwrites previous
- **Do I need to retrain models?** No - bias correction is separate from modeling

---

**Next Steps:**
1. Save this guide for reference
2. Schedule monthly bias update in your calendar
3. Run your first update today if you have the required files
