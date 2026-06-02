# Quick Reference Card - Aircraft Parts Forecasting System

## 🚀 Most Common Commands

### Daily/Weekly Operations

```sh
# 1. Validate new sales data
python validate_input_data.py --sales "sales_data.xlsx" --fix

# 2. Create forecast (bias auto-applied if available)
python -m src.app --input "sales_data_FIXED.xlsx"

# 3. Review forecast
# Open: output/forecast_output.xlsx
# Check: Forecast_Summary tab
```

### Monthly Bias Update

```sh
# 1. Compare last month's forecast to this month's actuals
python fix_forecast_comparison.py \
  --old-forecast "output/forecast_lastmonth.csv" \
  --actual-sales "sales_thismonth_FIXED.xlsx" \
  --output "output/bias_current.csv"

# 2. Review Excel analysis
# Open: output/bias_current_analysis.xlsx
# Check: Top_Errors and Recommendations tabs

# 3. Re-merge bias (if updating master)
python merge_bias_files.py --iterations 4
```

---

## 📂 Key File Locations

| File | Location | Purpose |
|------|----------|---------|
| Sales data (raw) | `sales_data.xlsx` | Your input |
| Sales data (validated) | `sales_data_FIXED.xlsx` | After validation |
| Forecast output | `output/forecast_output.xlsx` | Main deliverable |
| Master bias file | `output/forecast_accuracy_report.csv` | Auto-detected |
| Bias analysis | `output/bias_iterX_analysis.xlsx` | Review accuracy |

---

## ✅ What to Check After Running Forecast

### Console Output - Look For:
```
✅ [BiasCorrector] Applying PART-SPECIFIC corrections...
   Parts with specific corrections: 5,234
   Parts using global correction: 1,912
```

### Excel File - Check These Tabs:
1. **Forecast_Summary** - Processing stats, bias applied
2. **Forecast Data** - Actual forecast values by quarter

### Red Flags:
- ❌ "Bias correction failed - using original forecasts"
  - **Fix:** Re-run `merge_bias_files.py`

- ⚠️ "Parts using global correction: 12,000" (all parts)
  - **Fix:** Your bias file might be empty or wrong format

---

## 🔧 Troubleshooting Quick Fixes

### Problem: Validation fails with date errors
```sh
# Check what's wrong
python validate_input_data.py --sales "sales_data.xlsx"

# Fix it automatically
python validate_input_data.py --sales "sales_data.xlsx" --fix
```

### Problem: Bias correction not applying
```sh
# Check if file exists
dir output\forecast_accuracy_report.csv

# Regenerate if missing
python merge_bias_files.py --iterations 4
```

### Problem: Forecast too slow
```sh
# Use fast mode (skips detailed analysis)
python -m src.app --input "sales_FIXED.xlsx" --fast-mode
```

### Problem: Excel summary not created
```sh
# Install openpyxl
python -m pip install openpyxl

# Re-run validation
python validate_input_data.py --sales "sales_data.xlsx" --fix
```

---

## 📊 Understanding Your Results

### Validation Summary (in Excel)
| Metric | Good ✅ | Warning ⚠️ |
|--------|---------|-----------|
| Date parsing | 100% success | Any failures |
| Missing values | 0 | >1% missing |
| Duplicate rows | <20% | >50% duplicates |

### Forecast Accuracy (in bias_iterX_analysis.xlsx)
| Error % | Rating | Action |
|---------|--------|--------|
| <10% | ✅ Excellent | No action |
| 10-25% | ✅ Good | Monitor |
| 25-50% | ⚠️ Fair | Review part |
| 50-100% | ❌ Poor | Investigate |
| >100% | ❌ Critical | Manual review |

### Bias Correction Factors
| Factor | Meaning | Example |
|--------|---------|---------|
| 0.5x | Cut forecast in half | Was over-forecasting 100% |
| 0.8x | Reduce 20% | Was over-forecasting 25% |
| 1.0x | No change | Historically accurate |
| 1.2x | Increase 20% | Was under-forecasting 17% |
| 2.0x | Double forecast | Was under-forecasting 50% |

### Confidence Intervals (NEW!)
| Percentile | Use For | Example (if P50=100) |
|------------|---------|---------------------|
| **P10** | Safety stock, high-value parts | 70-85 units (conservative) |
| **P50** | Primary forecast, budgeting | 100 units (most likely) |
| **P90** | Capacity planning, max scenario | 125-160 units (optimistic) |

**Interval Width:**
- Tier 1 (High confidence): Narrow (±20-25%)
- Tier 2 (Medium): Moderate (±30-40%)  
- Tier 3-4 (Low): Wide (±40-60%)

**See:** `CONFIDENCE_INTERVALS_GUIDE.md` for detailed usage

---

## 🎯 Decision Making Guide

### Should I use --fix flag?
- ✅ **YES** if: First time using file, dates inconsistent, known issues
- ❌ **NO** if: Data already validated, just checking quality

### Should I include maintenance events?
- ✅ **YES** if: Planning major overhauls, >50 scheduled events, long planning horizon
- ❌ **NO** if: Normal operations, <20 events, short-term forecast

### How many bias iterations?
- **1-2 iterations:** Quick test, emergency forecast
- **3-4 iterations:** Production quality (recommended)
- **5+ iterations:** Maximum accuracy, multi-year validation

### When to update bias?
- **Monthly:** If high forecast volume, fast-changing demand
- **Quarterly:** Normal operations, stable demand
- **Annually:** Slow-moving parts, low transaction volume

---

## 🔍 File Format Quick Reference

### Sales Data (Input)
```csv
Date,Part_number,Value
2023-01-15,ABC123,5
2023-01-20,ABC123,3
2023-01-22,DEF456,12
```

### Maintenance Events (Input)
```csv
Check,Start Date,End Date
C-Check,2026-03-01,2026-04-15
D-Check,2026-06-01,2026-09-30
```

### Forecast Output
```csv
Part_number,Tier,26Q2,26Q3,26Q4,27Q1,27Q2,27Q3
ABC123,A,45,48,52,50,49,51
DEF456,B,12,15,14,16,15,17
```

### Bias File
```csv
Part_number,Year_Q,Forecast,Actual,Error,Percentage_Error
ABC123,25Q4,100,75,25,33.3
DEF456,25Q4,50,65,-15,-23.1
```

---

## 📞 Where to Get Help

1. **Check console output** - errors usually explain the issue
2. **Review HOW_TO guides** - step-by-step for each operation
3. **Check CHANGELOG.md** - recent changes and migration guide
4. **Look at Excel analysis** - visual insights into problems

---

## ⚡ Performance Tips

- ✅ Use `--fast-mode` for quick forecasts
- ✅ Use `--fix` only when needed (slow)
- ✅ Keep bias file up-to-date (faster loading)
- ✅ Use FIXED files for forecasting (already validated)
- ❌ Don't validate the same file multiple times

---

## 🎓 Learning Path

1. **Week 1:** Run basic forecasts, understand output
2. **Week 2:** Build bias correction (1-2 iterations)
3. **Week 3:** Complete 4-5 iteration bias validation
4. **Week 4:** Set up monthly update workflow
5. **Ongoing:** Monitor accuracy, refine bias monthly

---

**System Version:** 2.0 (Part-Specific Bias Correction)  
**Last Updated:** Current session
