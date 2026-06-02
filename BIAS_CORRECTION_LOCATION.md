# Bias Correction Central Storage Design

## Overview

The bias correction system uses a **central storage model** where the accuracy report is kept in one location and shared across all forecasts, regardless of where individual forecast outputs are saved.

## File Locations

### ✅ Central Files (Always in `output/`)

These files are **always** stored in the `output/` folder:

- **`forecast_accuracy_report.csv`** - Historical accuracy data used for bias correction
- **`forecast_accuracy_report_analysis.xlsx`** - Detailed analysis workbook

**Why?** These files represent your **accumulated learning** from past forecasts. They should be:
- Shared across all forecasts
- Not duplicated in multiple folders
- Easy to find and maintain
- Updated monthly with new accuracy data

### 📁 Custom Files (Configurable via Dashboard Settings)

These files can be saved to **any folder** you configure:

- **`forecast_output.csv`** / **`forecast_output.xlsx`** - Original forecast
- **`forecast_output_Corrected.csv`** / **`forecast_output_Corrected.xlsx`** - Bias-corrected forecastI 
- **`correction_factors.csv`** - Factors used for this specific correction

## How It Works

### 1. Creating Forecasts

```
Dashboard Settings: Output Folder = "Test for mean and mtc events/"

When you run a forecast:
├── Custom folder: Test for mean and mtc events/
│   ├── forecast_output.xlsx          ← Original forecast
│   ├── forecast_output_Corrected.xlsx ← Corrected forecast
│   └── correction_factors.csv         ← Correction factors used
│
└── Central folder: output/
	└── forecast_accuracy_report.csv   ← Shared bias data
```

### 2. Updating Bias Correction

When you upload old forecast + actual sales data:

1. Analysis is performed
2. **Results always save to:** `output/forecast_accuracy_report.csv`
3. All future forecasts automatically use this file for correction

### 3. Automatic Bias Correction

Every forecast run:

1. Looks for `output/forecast_accuracy_report.csv`
2. If found, applies corrections automatically
3. Writes corrected output to your **custom output folder**

## Benefits

✅ **Single source of truth** - One accuracy report, not scattered copies  
✅ **Easy maintenance** - Update once, all forecasts benefit  
✅ **Flexible output** - Save forecasts anywhere without losing correction ability  
✅ **No confusion** - Clear separation between "learning data" and "forecast outputs"  

## Monthly Workflow

1. **Run forecast** → Saves to your custom folder (e.g., "Q1 Planning/")
2. **Wait for actuals** → Collect real sales data
3. **Update bias** → Uploads old forecast + actuals
   - Saves to `output/forecast_accuracy_report.csv`
4. **Next forecast** → Automatically uses updated corrections
   - Saves to any folder you choose

## Quick Reference

| File | Location | Purpose | Shared? |
|------|----------|---------|---------|
| `forecast_accuracy_report.csv` | `output/` | Bias correction learning data | ✅ Yes |
| `forecast_output.xlsx` | Custom folder | Original forecast | ❌ No |
| `forecast_output_Corrected.xlsx` | Custom folder | Corrected forecast | ❌ No |
| `correction_factors.csv` | Custom folder | Snapshot of factors used | ❌ No |

## Important Notes

⚠️ **Don't move `forecast_accuracy_report.csv`** - The system always looks in `output/` for this file.

⚠️ **Backup this file** - It contains valuable historical accuracy data.

💡 **Custom folders are for organization** - Use them to separate forecasts by quarter, scenario, or project.

💡 **The central report accumulates knowledge** - Each bias update makes all future forecasts better.
