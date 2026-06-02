# How To: Update Bias Correction

> **⚠️ NOTE:** This guide covers the basic bias correction workflow. For the complete **5-iteration historical validation** approach, see **HOW_TO_CREATE_BIAS_CORRECTION.md**.

> **🆕 IMPORTANT UPDATE:** Bias correction is now **PART-SPECIFIC**. Each of your 12,000+ parts gets its own correction factor based on its individual historical accuracy, not blanket corrections per quarter. See CHANGELOG.md for details.

## **What is Bias Correction?**

**Problem:** Forecasting models sometimes consistently predict **too high** or **too low** compared to actual demand. This is called "systematic bias."

**Example:**
- Your forecast says you'll need **100 units** next quarter
- Actual demand is only **72 units**
- You over-ordered by **28%** → Excess inventory costs

**Solution:** The bias correction system learns from past forecast errors and automatically adjusts future forecasts to be more accurate.

**Result:** Reduces forecast error from ~72% to ~25% (based on historical testing).

---

## **How Bias Correction Works (3-Step Process)**

### **Step 1: System Compares Past Forecasts to Actual Sales** 📊

The system needs historical data showing:
- What you **forecasted** for each quarter
- What **actually happened** (actual sales)

This data is stored in: `forecast_accuracy_report.csv`

**Example Report:**
```
Part_number | Year_Q | Forecast | Actual | Error | Percentage_Error
ABC-123     | 24Q1   | 100      | 72     | +28   | +28%
DEF-456     | 24Q1   | 50       | 55     | -5    | -9%
GHI-789     | 24Q2   | 200      | 180    | +20   | +10%
```

---

### **Step 2: System Learns Correction Factors** 🧮

The bias corrector analyzes the accuracy report:

**What it looks for:**
- Do forecasts **consistently over-predict**? (Most errors are positive)
- Do forecasts **consistently under-predict**? (Most errors are negative)
- Does bias **vary by quarter**? (e.g., Q1 always over-forecasts by 30%)

**What it calculates:**
- **Correction factors** for each quarter
- Example: If Q1 forecasts average +30% too high, apply **0.77x correction** (1 / 1.30 = 0.77)

**Example Output:**
```
Quarter | Median Error | Correction Factor | Parts Analyzed
24Q1    | +28%        | 0.781x           | 1,234
24Q2    | +15%        | 0.870x           | 1,189
24Q3    | -5%         | 1.053x           | 1,256
```

---

### **Step 3: System Applies Corrections to New Forecasts** ✅

When you run a new forecast, the system automatically:
1. Generates raw forecasts (using your 9 models)
2. Checks if `forecast_accuracy_report.csv` exists
3. If yes → Applies correction factors to each quarter
4. Saves **two files**:
   - `forecast_output.csv` (original forecasts)
   - `forecast_output_Corrected.csv` (bias-corrected forecasts)

---

## **How to Set Up Bias Correction**

### **Prerequisites** 📋

You need **historical data** with:
1. **Past forecasts** (what you predicted months ago)
2. **Actual sales** (what really happened)

**Minimum Requirements:**
- At least **50 parts** with both forecast and actual data
- Data from at least **1-2 quarters** ago

---

### **Option A: If You Already Have an Accuracy Report** ✅

**Step 1:** Make sure `forecast_accuracy_report.csv` is in your `output` folder

**Required columns:**
- `Part_number` - Part identifier
- `Year_Q` - Quarter (e.g., "24Q1", "24Q2")
- `Forecast` - What was forecasted
- `Actual` - What actually happened
- `Error` - Difference (Forecast - Actual)
- `Percentage_Error` - Error as percentage

**Step 2:** Run your forecast as usual:
```powershell
python -m src.app --input "sales_data.xlsx" --events-file "maintenance_events.csv"
```

**Step 3:** Check console output at the end:
```
==========================================
APPLYING BIAS CORRECTION - Model-Demand Alignment Fix
==========================================
[INFO] Loaded 420 maintenance events

[BiasCorrector] Loading accuracy report from: output\forecast_accuracy_report.csv
[BiasCorrector] Loaded 1,234 historical comparisons

[BiasCorrector] Analyzing forecast bias by quarter:
   24Q1: +28.0% error → 0.781x correction
   24Q2: +15.0% error → 0.870x correction
   24Q3: -5.0% error → 1.053x correction

[BiasCorrector] SYSTEMATIC OVER-FORECASTING detected (68.3%)
[BiasCorrector] Global correction factor: 0.826x

[BiasCorrector] Applying corrections to 6 quarters...
   25Q1: Applied 0.781x to 1,234 parts
   25Q2: Applied 0.870x to 1,234 parts
   ...

FORECAST OUTPUT SUMMARY
==========================================
Original forecasts:  output\forecast_output.csv
Corrected forecasts: output\forecast_output_Corrected.csv

⚠️  RECOMMENDED: Use corrected forecasts for planning
   (Reduces error from 72% to ~25%)
==========================================
```

**Step 4:** Use the **corrected** file for planning:
- ✅ **Use:** `forecast_output_Corrected.csv`
- ⛔ **Don't use:** `forecast_output.csv` (original, uncorrected)

---

### **Option B: If You DON'T Have an Accuracy Report** 📝

You need to create one by comparing past forecasts to actual sales.

**Method 1: Manual Creation in Excel**

1. **Open past forecast file** (from several months ago)
2. **Open actual sales data** (what really happened)
3. **Create comparison spreadsheet:**

```
Part_number | Year_Q | Forecast | Actual | Error           | Percentage_Error
ABC-123     | 24Q1   | 100      | 72     | =(C2-D2)       | =(E2/D2)*100
DEF-456     | 24Q1   | 50       | 55     | =(C3-D3)       | =(E3/D3)*100
```

4. **Save as:** `forecast_accuracy_report.csv` in `output` folder

**Method 2: Use Python Script** (Recommended)

Use the `fix_forecast_comparison.py` script to automatically generate the report:

```powershell
python fix_forecast_comparison.py --old-forecast "old_forecasts.csv" --actual-sales "actual_sales.xlsx"
```

**Parameters:**
- `--old-forecast`: Path to your old forecast CSV file
- `--actual-sales`: Path to actual sales data (Excel or CSV)
- `--output`: (Optional) Output path for report (default: `output/forecast_accuracy_report.csv`)

**Example:**
```powershell
python fix_forecast_comparison.py --old-forecast "2026-Q1_forecast.csv" --actual-sales "2026_Q3_sales.xlsx"
```

**What it does:**
1. Loads your old forecast file and actual sales data
2. Matches forecasts with actual sales by part number and quarter
3. Calculates errors and percentage errors
4. Generates `forecast_accuracy_report.csv` automatically
5. Shows diagnosis of systematic over/under-forecasting

**Required file formats:**

*Old Forecast CSV:*
```
Part_number | 25Q1 | 25Q2 | 25Q3 | 25Q4 | 26Q1 | 26Q2
ABC-123     | 100  | 105  | 110  | 115  | 120  | 125
DEF-456     | 50   | 52   | 55   | 58   | 60   | 62
```

*Actual Sales Excel/CSV:*
```
Part_number | Date       | Value
ABC-123     | 01-01-25   | 18
ABC-123     | 15-01-25   | 22
ABC-123     | 01-02-25   | 19
DEF-456     | 10-01-25   | 12
```

The script automatically:
- Detects quarter columns (25Q1, 26Q2, etc.)
- Aggregates actual sales by quarter
- Matches part numbers
- Calculates all error metrics

---

## **Understanding the Correction**

### **Example: Over-Forecasting Correction**

**Before Correction:**
```
Part: ABC-123
Forecast 25Q1: 100 units
Forecast 25Q2: 105 units
```

**Bias Analysis Shows:**
- Q1 forecasts average **+28% too high**
- Q2 forecasts average **+15% too high**

**After Correction:**
```
Part: ABC-123
Forecast 25Q1: 78 units  (100 × 0.781 = 78)
Forecast 25Q2: 91 units  (105 × 0.870 = 91)
```

**Impact:**
- ✅ Avoid over-ordering 22 units in Q1
- ✅ Reduce excess inventory costs
- ✅ More accurate planning

---

### **Example: Under-Forecasting Correction**

**Before Correction:**
```
Part: XYZ-789
Forecast 25Q3: 50 units
```

**Bias Analysis Shows:**
- Q3 forecasts average **-20% too low** (under-predicting)

**After Correction:**
```
Part: XYZ-789
Forecast 25Q3: 63 units  (50 × 1.25 = 63)
```

**Impact:**
- ✅ Avoid stockouts (don't order only 50 when you need 63)
- ✅ Better service levels
- ✅ Fewer emergency orders

---

## **How to Update Bias Correction** 🔄

**When to Update:**
- After each quarter when actual sales data is available
- Minimum: **Once per quarter**
- Recommended: **Monthly** as new data becomes available

**Step-by-Step Process:**

### **1. Collect New Data**

Wait until you have:
- ✅ Past forecasts (at least 3 months old)
- ✅ Actual sales for those same periods
- ✅ At least 50-100 parts with both data points

**Example Timeline:**
```
Today = July 2025
└─ Can compare: 24Q4 forecasts (made in Oct 2024) vs. 24Q4 actuals (Jan-Mar 2025)
└─ Can compare: 25Q1 forecasts (made in Jan 2025) vs. 25Q1 actuals (Apr-Jun 2025)
```

---

### **2. Create Updated Accuracy Report**

**Option A: Update Existing Report (Recommended)**

Open `forecast_accuracy_report.csv` and **add new rows**:

```csv
Part_number,Year_Q,Forecast,Actual,Error,Percentage_Error
ABC-123,25Q1,100,85,15,17.6
ABC-123,25Q2,105,95,10,10.5
DEF-456,25Q1,50,52,-2,-3.8
...
```

**Option B: Regenerate from Scratch**

If you have the comparison script:
```powershell
python fix_forecast_comparison.py --old-forecast "2026-Q1_forecast.csv" --actual-sales "2026_Q3_sales.xlsx"
```

Or update manually by adding new rows (see Method 1 above).

---

### **3. Run Forecast with Updated Report**

```powershell
python -m src.app --input "sales_data.xlsx" --events-file "maintenance_events.csv" --outdir "output"
```

The system will:
1. Load the **updated** accuracy report
2. Recalculate correction factors (based on new data)
3. Apply updated corrections to new forecasts

---

### **4. Review Correction Changes**

Check console output for changes:

**Before Update:**
```
24Q1: +28% error → 0.781x correction (1,234 parts)
```

**After Adding More Data:**
```
24Q1: +25% error → 0.800x correction (1,456 parts)
```

**What Changed:**
- More data = more reliable correction
- Median error improved from +28% to +25%
- Sample size increased from 1,234 to 1,456 parts

---

## **Troubleshooting** 🔧

### **Problem: "No accuracy report found"**

**Console Message:**
```
[INFO] No accuracy report found at: output\forecast_accuracy_report.csv
       Run fix_forecast_comparison.py to enable bias correction
```

**Solution:**
1. Create `forecast_accuracy_report.csv` (see Option B above)
2. Make sure it's in the `output` folder
3. Re-run forecast

---

### **Problem: "Not enough samples for quarter X"**

**Console Message:**
```
Warning: 25Q1 has only 35 samples (min 50)
```

**Meaning:** Not enough historical data to reliably calculate correction for that quarter.

**What System Does:**
- Uses **global correction factor** instead of quarter-specific
- Still applies correction, just less precise

**Solution:**
- Wait until you have more historical data
- Or reduce `min_samples` parameter (not recommended)

---

### **Problem: Corrections seem wrong**

**Check These:**

1. **Is accuracy report correct?**
   - Open `forecast_accuracy_report.csv`
   - Verify `Forecast` and `Actual` columns match reality
   - Check `Error` = Forecast - Actual

2. **Is data recent enough?**
   - Old data (>1 year) may not reflect current patterns
   - Remove outdated rows from accuracy report

3. **Are there outliers?**
   - System uses **median** (not mean) to reduce outlier impact
   - But extreme errors can still skew corrections

---

## **Best Practices** ✅

### **Do:**
- ✅ Update accuracy report **every quarter** as new data arrives
- ✅ Use **corrected** forecasts for planning (not original)
- ✅ Keep accuracy report for at least **4 quarters** (1 year) of data
- ✅ Review correction factors each run (console output)
- ✅ Compare corrected vs. original to understand bias magnitude

### **Don't:**
- ⛔ Don't update accuracy report with **current quarter** data (too soon)
- ⛔ Don't use corrections if sample size < 50 parts
- ⛔ Don't mix data from different product lines (create separate reports)
- ⛔ Don't ignore console warnings about insufficient samples

---

## **Files Reference** 📁

| File | Location | Purpose |
|------|----------|---------|
| **forecast_accuracy_report.csv** | `output/` | Historical forecast vs. actual comparison data |
| **forecast_output.csv** | `output/` | Original forecasts (uncorrected) |
| **forecast_output_Corrected.csv** | `output/` | ✅ **USE THIS** - Bias-corrected forecasts |
| **correction_factors.csv** | `output/` | Correction factors applied (for reference) |

---

## **Quick Reference: Correction Formula** 📐

```
Correction Factor = 1 / (1 + (Median Error % / 100))

Examples:
- Median Error = +30% → Factor = 1 / 1.30 = 0.769x (reduce by 23%)
- Median Error = +15% → Factor = 1 / 1.15 = 0.870x (reduce by 13%)
- Median Error = -10% → Factor = 1 / 0.90 = 1.111x (increase by 11%)
- Median Error = 0%   → Factor = 1.000x (no change)

Corrected Forecast = Original Forecast × Correction Factor
```

---

## **Summary** 🎯

**Setup (One-Time):**
1. Create `forecast_accuracy_report.csv` with historical forecast vs. actual data
2. Place in `output` folder

**Ongoing (Every Run):**
1. System automatically detects accuracy report
2. Calculates corrections based on historical bias
3. Applies corrections to new forecasts
4. Saves both original and corrected files
5. **Use corrected file** for planning

**Maintenance (Quarterly):**
1. Add new forecast vs. actual comparisons to accuracy report
2. Re-run forecast to update correction factors
3. Review console output for changes

**Result:** More accurate forecasts, better inventory planning, reduced costs.
