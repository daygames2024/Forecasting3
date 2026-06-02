# HOW TO CREATE BIAS CORRECTION - 5 Historical Iterations

## Overview

This guide walks through creating a robust bias correction file by simulating 5 historical forecasts and comparing them to actual sales data. This approach validates the forecasting system across multiple years and economic cycles.

---

## Understanding Bias Correction

**What is it?**
- Bias correction adjusts future forecasts based on past forecasting errors
- Each part gets a correction factor (e.g., "typically over-forecasted by 25%")
- The system automatically applies these corrections to new forecasts

**How it works:**
1. Create a forecast from OLD data (simulate past forecast)
2. Compare that forecast to ACTUAL sales that happened after
3. Calculate the error pattern per part
4. Apply those patterns to future forecasts

**One-shot vs Accumulative:**
- Each iteration is INDEPENDENT (not cumulative)
- We merge 5 iterations by AVERAGING the error patterns
- Recent iterations weighted more heavily than old ones
- Result: Single master bias file representing typical forecast errors

---

## PHASE 1: DATA COLLECTION

### Step 1.1 - Download historical sales data files

Download these 6 files from your system (36 months each):

- [ ] **sales_2019.xlsx** - May 2019 to Apr 2022 (36 months)
- [ ] **sales_2020.xlsx** - May 2020 to Apr 2023 (36 months)
- [ ] **sales_2021.xlsx** - May 2021 to Apr 2024 (36 months)
- [ ] **sales_2022.xlsx** - May 2022 to Apr 2025 (36 months)
- [ ] **sales_2023.xlsx** - May 2023 to May 2026 (37 months)
- [ ] **sales_current.xlsx** - May 2025 to May 2026 (13 months - most recent)

**Why these dates?**
- Each file shifts forward 12 months
- Creates 12+ months of overlap for comparison
- Covers 7 years of market conditions (2019-2026)
- Includes COVID disruption and recovery (important validation period)

### Step 1.2 - Place files in workspace

- [ ] Create folder: `C:\Projects\Forecasting3\historical\`
- [ ] Save all 6 files to this folder
- [ ] Verify all files have columns: `Date`, `Part_number`, `Value`

---

## PHASE 2: VALIDATE & FIX ALL FILES

**Why validate?**
- Ensures date formats are consistent
- Removes invalid data
- Sorts data properly for forecasting

### Step 2.1 - Validate sales_2019.xlsx
```sh
cd C:\Projects\Forecasting3
python validate_input_data.py --sales "historical\sales_2019.xlsx" --fix
```
**Expected output:** `historical\sales_2019_FIXED.xlsx`

### Step 2.2 - Validate sales_2020.xlsx
```sh
python validate_input_data.py --sales "historical\sales_2020.xlsx" --fix
```
**Expected output:** `historical\sales_2020_FIXED.xlsx`

### Step 2.3 - Validate sales_2021.xlsx
```sh
python validate_input_data.py --sales "historical\sales_2021.xlsx" --fix
```
**Expected output:** `historical\sales_2021_FIXED.xlsx`

### Step 2.4 - Validate sales_2022.xlsx
```sh
python validate_input_data.py --sales "historical\sales_2022.xlsx" --fix
```
**Expected output:** `historical\sales_2022_FIXED.xlsx`

### Step 2.5 - Validate sales_2023.xlsx
```sh
python validate_input_data.py --sales "historical\sales_2023.xlsx" --fix
```
**Expected output:** `historical\sales_2023_FIXED.xlsx`

### Step 2.6 - Validate sales_current.xlsx
```sh
python validate_input_data.py --sales "historical\sales_current.xlsx" --fix
```
**Expected output:** `historical\sales_current_FIXED.xlsx`

---

## PHASE 3: ITERATION 1 (2019 → 2020)

**What we're doing:**
- Create a forecast using May 2019 - Apr 2022 data (simulates forecast made in May 2022)
- Compare that forecast to May 2020 - Apr 2023 actual sales
- Calculate the errors for overlapping quarters

### Step 3.1 - Create forecast from 2019 data
```sh
python -m src.app --input "historical\sales_2019_FIXED.xlsx" --outfile "forecast_2019.csv"
```
**Expected output:** `output\forecast_2019.csv` (forecast for 2022-2025 quarters)

### Step 3.2 - Compare 2019 forecast to 2020 actuals
```sh
python fix_forecast_comparison.py --old-forecast "output\forecast_2019.csv" --actual-sales "historical\sales_2020_FIXED.xlsx" --output "output\bias_iter1.csv"
```
**Expected output:** 
- `output\bias_iter1.csv` (bias correction file)
- `output\bias_iter1_analysis.xlsx` (detailed Excel report with 6 sheets)

**Check:** Note the number of matched forecast-actual pairs in the output (expect 1000+ matches)

**Review the Excel report:**
- Open `output\bias_iter1_analysis.xlsx`
- **Summary** tab: Overall statistics and accuracy bands
- **By_Quarter** tab: Accuracy trends by quarter
- **Top_Errors** tab: 50 biggest forecast misses (color-coded)
- **All_Parts** tab: Complete comparison sorted by error
- **Part_Summary** tab: Aggregated accuracy per part
- **Recommendations** tab: Actionable insights and next steps

---

## PHASE 4: ITERATION 2 (2020 → 2021)

### Step 4.1 - Create forecast from 2020 data
```sh
python -m src.app --input "historical\sales_2020_FIXED.xlsx" --outfile "forecast_2020.csv"
```
**Expected output:** `output\forecast_2020.csv`

### Step 4.2 - Compare 2020 forecast to 2021 actuals
```sh
python fix_forecast_comparison.py --old-forecast "output\forecast_2020.csv" --actual-sales "historical\sales_2021_FIXED.xlsx" --output "output\bias_iter2.csv"
```
**Expected output:** 
- `output\bias_iter2.csv`
- `output\bias_iter2_analysis.xlsx`

---

## PHASE 5: ITERATION 3 (2021 → 2022)

### Step 5.1 - Create forecast from 2021 data
```sh
python -m src.app --input "historical\sales_2021_FIXED.xlsx" --outfile "forecast_2021.csv"
```
**Expected output:** `output\forecast_2021.csv`

### Step 5.2 - Compare 2021 forecast to 2022 actuals
```sh
python fix_forecast_comparison.py --old-forecast "output\forecast_2021.csv" --actual-sales "historical\sales_2022_FIXED.xlsx" --output "output\bias_iter3.csv"
```
**Expected output:** 
- `output\bias_iter3.csv`
- `output\bias_iter3_analysis.xlsx`

---

## PHASE 6: ITERATION 4 (2022 → 2023)

### Step 6.1 - Create forecast from 2022 data
```sh
python -m src.app --input "historical\sales_2022_FIXED.xlsx" --outfile "forecast_2022.csv"
```
**Expected output:** `output\forecast_2022.csv`

### Step 6.2 - Compare 2022 forecast to 2023 actuals
```sh
python fix_forecast_comparison.py --old-forecast "output\forecast_2022.csv" --actual-sales "historical\sales_2023_FIXED.xlsx" --output "output\bias_iter4.csv"
```
**Expected output:** 
- `output\bias_iter4.csv`
- `output\bias_iter4_analysis.xlsx`

---

## PHASE 7: ITERATION 5 (2023 → Current)

### Step 7.1 - Create forecast from 2023 data
```sh
python -m src.app --input "historical\sales_2023_FIXED.xlsx" --outfile "forecast_2023.csv"
```
**Expected output:** `output\forecast_2023.csv`

### Step 7.2 - Compare 2023 forecast to current actuals
```sh
python fix_forecast_comparison.py --old-forecast "output\forecast_2023.csv" --actual-sales "historical\sales_current_FIXED.xlsx" --output "output\bias_iter5.csv"
```
**Expected output:** 
- `output\bias_iter5.csv`
- `output\bias_iter5_analysis.xlsx`

---

## PHASE 8: MERGE BIAS FILES

**What happens here:**
- Combine all 5 bias files into one master file
- Average the error patterns per part
- Weight recent iterations more heavily (2025 > 2021)
- Create final `forecast_accuracy_report.csv`

### Step 8.1 - Verify all 5 bias files exist
Check that these files were created:
- [ ] `output\bias_iter1.csv`
- [ ] `output\bias_iter2.csv`
- [ ] `output\bias_iter3.csv`
- [ ] `output\bias_iter4.csv`
- [ ] `output\bias_iter5.csv`

### Step 8.2 - Merge bias files into master
```sh
python merge_bias_files.py --input "output\bias_iter*.csv" --output "output\forecast_accuracy_report.csv"
```

**What the merge does:**
1. Loads all 5 iteration files
2. Groups by Part_number
3. Calculates weighted average error:
   - 2021 iteration: weight 1.0x
   - 2022 iteration: weight 1.2x
   - 2023 iteration: weight 1.4x
   - 2024 iteration: weight 1.6x
   - 2025 iteration: weight 2.0x (most recent)
4. Saves master bias file

**Expected output:** `output\forecast_accuracy_report.csv`

---

## PHASE 9: PRODUCTION FORECAST

### Step 9.1 - Create final forecast with master bias
```sh
python -m src.app --input "historical\sales_current_FIXED.xlsx"
```

**What happens:**
- System auto-detects `output\forecast_accuracy_report.csv`
- Applies bias correction to all forecasted parts
- Creates forecast for Jun 2026 - May 2027 quarters (and beyond)

**Expected:** Look for this message in output:
```
📊 Applying bias correction from output/forecast_accuracy_report.csv
   Applied to XXXX parts
```

### Step 9.2 - Verify bias was applied
Check the forecast output for:
- [ ] Message showing bias correction applied
- [ ] Number of parts adjusted
- [ ] Overall correction factor

### Step 9.3 - Review final forecast
- [ ] Open `output\forecast_output.xlsx`
- [ ] Check Forecast_Summary tab shows bias correction stats
- [ ] Verify forecasts look reasonable (not wildly different from previous forecasts)
- [ ] Review high-value parts to ensure corrections make sense

---

## Understanding the Results

### Excel Analysis Reports

Each iteration creates a detailed Excel workbook with 6 sheets:

**1. Summary Sheet**
- Overall statistics (mean, median, std deviation of errors)
- Bias detection (over vs under forecasting)
- Accuracy bands breakdown:
  - Excellent: <10% error
  - Good: 10-25% error
  - Fair: 25-50% error
  - Poor: 50-100% error
  - Critical: >100% error

**2. By_Quarter Sheet**
- Accuracy metrics per quarter (mean, median, std dev)
- Helps identify if accuracy changes over time
- Useful for spotting seasonal patterns in errors

**3. Top_Errors Sheet**
- 50 parts with biggest absolute errors
- Color-coded:
  - Red: >100% error (critical)
  - Yellow: 50-100% error (poor)
  - White: <50% error
- Review these parts manually

**4. All_Parts Sheet**
- Complete forecast vs actual for all parts
- Sorted by error magnitude
- Use for detailed investigation

**5. Part_Summary Sheet**
- Aggregated accuracy per part across all quarters
- Shows total forecast, total actual, average error
- Identifies chronically problematic parts

**6. Recommendations Sheet**
- Diagnosis of systematic bias
- Root cause analysis
- Suggested correction factors
- Immediate and long-term action items

### What to expect from 5-iteration bias correction:

**Good signs:**
- ✅ 500+ matched parts per iteration
- ✅ Average error trending down across iterations
- ✅ Consistent error patterns (same parts always over/under)
- ✅ Final forecast shows 10-30% adjustment vs uncorrected

**Warning signs:**
- ⚠️ <100 matched parts per iteration (insufficient data)
- ⚠️ Average error >500% (fundamental model issues)
- ⚠️ Random error patterns (no consistency)
- ⚠️ Final forecast changes >80% (over-correcting)

### Interpreting bias correction statistics:

**Overall correction factor: 0.85x**
- Means: Forecasts typically 15% too high
- Action: System reduces future forecasts by 15%

**Overall correction factor: 1.20x**
- Means: Forecasts typically 20% too low
- Action: System increases future forecasts by 20%

**Per-part corrections:**
- Some parts may have +100% correction (chronic under-forecasting)
- Some parts may have -50% correction (chronic over-forecasting)
- This is NORMAL for intermittent demand items

---

## Monthly Update Workflow

After initial 5-iteration setup, maintain bias correction monthly:

**Each month:**
1. Download latest sales data (36 months ending current month)
2. Validate and fix: `python validate_input_data.py --sales "sales_current.xlsx" --fix`
3. Create forecast: `python -m src.app --input "sales_current_FIXED.xlsx"`
4. Compare last month's forecast to current actuals:
   ```sh
   python fix_forecast_comparison.py --old-forecast "output\forecast_lastmonth.csv" --actual-sales "sales_current_FIXED.xlsx" --output "output\bias_current.csv"
   ```
5. Merge current bias with master:
   ```sh
   python merge_bias_files.py --input "output\bias_current.csv" --existing "output\forecast_accuracy_report.csv" --output "output\forecast_accuracy_report.csv" --decay 0.95
   ```

The `--decay 0.95` parameter:
- Keeps 95% of old bias weight
- Adds 5% weight to new bias
- Prevents wild swings month-to-month
- Gradually adapts to changing patterns

---

## Troubleshooting

### Problem: Very few matched parts (<100 per iteration)

**Causes:**
- Date ranges don't overlap enough
- Quarter columns mismatch
- Part numbers changed between years

**Solutions:**
- Verify forecast quarters match actual sales quarters
- Check that forecast file has columns like "24Q1", "24Q2", etc.
- Ensure part numbering is consistent across years

### Problem: Huge error percentages (>1000%)

**Causes:**
- Aircraft parts have intermittent demand
- Single large order vs forecast of zero (or vice versa)
- Normal for low-volume, high-value parts

**Solutions:**
- This is EXPECTED for aircraft parts
- Bias correction handles outliers automatically
- Focus on median error, not average error
- Review top 20 parts manually, ignore extreme outliers

### Problem: Bias correction makes forecasts worse

**Causes:**
- Historical patterns not representative of future
- Market conditions changed dramatically
- Too few iterations (need more data)

**Solutions:**
- Run 10 iterations instead of 5
- Use shorter time windows (quarterly vs yearly)
- Segment parts by behavior (fast-moving vs slow-moving)
- Apply bias only to A/B items, not C items

### Problem: merge_bias_files.py doesn't exist yet

**Solution:**
- This script will be created in Step 8.2
- Wait for instruction to proceed with merge
- Manual merge possible if needed (average in Excel)

---

## Benefits of This Approach

### Statistical Validation
- ✅ 5 independent validation periods
- ✅ Catches seasonal patterns across multiple years
- ✅ Includes various market conditions (COVID, recovery, normalization)
- ✅ High confidence in bias correction accuracy

### Operational Benefits
- ✅ Reduces chronic over-forecasting (excess inventory)
- ✅ Reduces chronic under-forecasting (stockouts)
- ✅ Improves buyer confidence in forecasts
- ✅ Reduces manual adjustments needed

### Continuous Improvement
- ✅ Monthly updates keep bias current
- ✅ Adapts to changing demand patterns
- ✅ Tracks forecast accuracy over time
- ✅ Identifies parts needing special attention

---

## File Structure After Completion

```
C:\Projects\Forecasting3\
├── historical\
│   ├── sales_2019.xlsx
│   ├── sales_2019_FIXED.xlsx
│   ├── sales_2020.xlsx
│   ├── sales_2020_FIXED.xlsx
│   ├── sales_2021.xlsx
│   ├── sales_2021_FIXED.xlsx
│   ├── sales_2022.xlsx
│   ├── sales_2022_FIXED.xlsx
│   ├── sales_2023.xlsx
│   ├── sales_2023_FIXED.xlsx
│   ├── sales_current.xlsx
│   └── sales_current_FIXED.xlsx
│
├── output\
│   ├── forecast_2019.csv
│   ├── forecast_2020.csv
│   ├── forecast_2021.csv
│   ├── forecast_2022.csv
│   ├── forecast_2023.csv
│   ├── bias_iter1.csv
│   ├── bias_iter2.csv
│   ├── bias_iter3.csv
│   ├── bias_iter4.csv
│   ├── bias_iter5.csv
│   ├── forecast_accuracy_report.csv  (MASTER BIAS FILE)
│   └── forecast_output.xlsx  (FINAL FORECAST)
│
├── validate_input_data.py
├── fix_forecast_comparison.py
├── merge_bias_files.py  (created in Step 8.2)
└── src\
    └── app.py
```

---

## Next Steps

**Start with Phase 1, Step 1.1:**
Download the 6 historical sales files and place them in the `historical\` folder.

**After each step:**
- Verify expected output files were created
- Check for error messages
- Note statistics (matched parts, error rates)

**When stuck:**
- Review troubleshooting section
- Check file paths and naming
- Verify date formats in source files

**After completion:**
- Archive the 5 iteration bias files (keep for reference)
- Use master bias file for all future forecasts
- Update monthly to keep bias current

---

## Summary

This 5-iteration approach gives you:
- **Robust bias correction** validated across 5 years
- **Production-ready forecasts** with proven accuracy improvements
- **Continuous improvement** workflow for monthly updates
- **Confidence** in forecast adjustments based on historical performance

The investment in this setup pays off through:
- Better inventory planning
- Reduced stockouts and excess inventory
- Higher forecast accuracy
- Less time spent on manual forecast adjustments

**Time investment:**
- Initial setup: 2-3 hours
- Monthly updates: 15 minutes
- Payback: Immediate improvement in forecast accuracy
