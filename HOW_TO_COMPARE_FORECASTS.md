# How To: Compare Forecasts with Actual Sales

## **What is Forecast Comparison?**

**Purpose:** Measure how accurate your past forecasts were by comparing them to actual sales data. This is the **first step** in setting up bias correction.

**Use Case:** After a quarter ends and you have actual sales data, compare it with the forecasts you made 3-6 months ago to see:
- Were you over-forecasting? (predicted too high)
- Were you under-forecasting? (predicted too low)
- Which parts have the biggest errors?
- Is there a systematic pattern to fix?

---

## **Quick Start** ⚡

**What you need:**
1. An old forecast file (CSV with columns like 25Q1, 25Q2, 26Q1, etc.)
2. Actual sales data (Excel or CSV with Date, Part_number, Value columns)

**Command:**
```powershell
python fix_forecast_comparison.py --old-forecast "old_forecast.csv" --actual-sales "actual_sales.xlsx"
```

**Output:**
- Creates `output/forecast_accuracy_report.csv`
- Shows accuracy analysis in console
- Diagnoses systematic over/under-forecasting

---

## **Step-by-Step Guide**

### **Step 1: Gather Required Files** 📁

#### **File 1: Old Forecast (CSV)**

This is a forecast you created in the past (3-6 months ago).

**Format:**
```csv
Part_number,25Q1,25Q2,25Q3,25Q4,26Q1,26Q2
ABC-123,100,105,110,115,120,125
DEF-456,50,52,55,58,60,62
GHI-789,200,205,210,215,220,225
```

**Requirements:**
- Must have `Part_number` column
- Must have quarter columns (format: `25Q1`, `26Q2`, etc.)
- Can have other columns (they'll be ignored)

**Where to find it:**
- Your `output` folder from past forecast runs
- Archive folder where you save old forecasts
- Example: `2026-Q1_forecast.csv` (created in January 2026)

---

#### **File 2: Actual Sales (Excel or CSV)**

This is your actual sales data showing what really happened.

**Format:**
```csv
Part_number,Date,Value
ABC-123,01-01-25,18
ABC-123,15-01-25,22
ABC-123,01-02-25,19
ABC-123,15-02-25,15
DEF-456,10-01-25,12
DEF-456,20-01-25,8
```

**Requirements:**
- Must have `Part_number` column
- Must have `Date` column (any date format recognized by Excel)
- Must have `Value` column (sales quantity per transaction)
- Can be Excel (.xlsx) or CSV format

**Where to get it:**
- Export from your ERP/sales system
- Historical sales report
- Example: `2026_Q3_sales.xlsx`

---

### **Step 2: Run Comparison Script** 🚀

**Option A: Run from Root Directory (Recommended)**

Open PowerShell in your main forecast directory (`C:\Projects\Forecasting3`) and run:

```powershell
python fix_forecast_comparison.py --old-forecast "output26\2026-Q1_forecast.csv" --actual-sales "output26\2026_Q3_sales.xlsx"
```

**Option B: Run from Output Folder**

If your files are in a specific output folder (e.g., `output26`), navigate there first:

```powershell
cd output26
python fix_forecast_comparison.py --old-forecast "2026-Q1_forecast.csv" --actual-sales "2026_Q3_sales.xlsx" --output "../output/forecast_accuracy_report.csv"
```

**Note:** The `--output` parameter ensures the accuracy report is saved to the main `output` folder where the forecasting system expects it.

**What happens:**

1. **Loads files:**
   ```
   ======================================================================
   FORECAST COMPARISON TOOL
   ======================================================================
   Loading forecast file: 2026-Q1_forecast.csv
   Loading actual sales file: 2026_Q3_sales.xlsx
   
   ✅ Loaded forecast data: 1,234 parts
   ✅ Loaded actual sales data: 45,678 rows
   ```

2. **Processes data:**
   ```
   ======================================================================
   PROCESSING DATA
   ======================================================================
   ✅ Aggregated actual sales by quarter: 3,456 part-quarter combinations
   ✅ Detected forecast columns: ['25Q2', '25Q3', '25Q4', '26Q1', '26Q2', '26Q3']
   ✅ Matched 2,987 forecast-actual pairs
   ```

3. **Shows analysis:**
   ```
   ======================================================================
   FORECAST ACCURACY ANALYSIS
   ======================================================================
   
   Total comparisons: 2,987
   
   Overall Statistics:
     Average error: 28.4%
     Median error: 18.2%
     Max over-forecast: 542.8%
     Max under-forecast: -89.3%
   
   Accuracy by Quarter:
             mean  median    std
   Year_Q                       
   25Q2     32.1    21.5   45.2
   25Q3     28.7    19.8   42.1
   25Q4     24.3    15.1   38.9
   
   Top 10 Biggest Forecast Errors:
      Part_number  Year_Q  Forecast  Actual  Percentage_Error
   0    XYZ-999     25Q2       150      12            1150.0
   1    AAA-111     25Q3       200      25             700.0
   ...
   ```

4. **Diagnoses problems:**
   ```
   ======================================================================
   MODEL-DEMAND ALIGNMENT DIAGNOSIS
   ======================================================================
   
   Bias Detection:
     Over-forecasted: 2,034 (68.1%)
     Under-forecasted: 953 (31.9%)
   
   ⚠️ SYSTEMATIC OVER-FORECASTING DETECTED
      Your models consistently predict HIGHER than actual demand
   
      Root Cause: Model-Demand Misalignment
      → Models are TOO OPTIMISTIC
      → Check if using outdated 'good years' as baseline
      → Reduce growth rate assumptions
   
      Suggested correction factor: 0.845x
   
   Accuracy Assessment:
      ⚠️ WARNING: 28.4% average error
         Significant alignment issues
   
   Extreme Outliers: 156 (5.2% with >100% error)
   ```

5. **Saves report:**
   ```
   ✅ Full report saved to: output/forecast_accuracy_report.csv
   ```

---

### **Step 3: Review Output File** 📊

Open `output/forecast_accuracy_report.csv` in Excel:

**Columns:**
- `Part_number` - Part identifier
- `Year_Q` - Quarter (25Q1, 25Q2, etc.)
- `Forecast` - What you predicted
- `Actual` - What really happened
- `Error` - Difference (Forecast - Actual)
- `Percentage_Error` - Error as percentage of actual

**Example:**
```
Part_number | Year_Q | Forecast | Actual | Error | Percentage_Error
ABC-123     | 25Q2   | 100      | 72     | +28   | +38.9%
ABC-123     | 25Q3   | 105      | 85     | +20   | +23.5%
DEF-456     | 25Q2   | 50       | 55     | -5    | -9.1%
DEF-456     | 25Q3   | 52       | 48     | +4    | +8.3%
```

**What to look for:**
- ✅ **Low errors (<20%)** = Good forecast accuracy
- ⚠️ **Medium errors (20-50%)** = Room for improvement
- ❌ **High errors (>50%)** = Poor forecast accuracy

---

### **Step 4: Use Report for Bias Correction** 🔧

This accuracy report is **automatically used** by your forecasting system.

**Next time you run a forecast:**
1. The system checks if `forecast_accuracy_report.csv` exists
2. If yes → Analyzes historical errors
3. Calculates correction factors per quarter
4. Applies corrections to new forecasts
5. Saves corrected forecasts

**No additional steps needed!** Just make sure the report file is in the `output` folder.

---

## **Command Options**

### **Basic Usage:**
```powershell
python fix_forecast_comparison.py --old-forecast "FILE1" --actual-sales "FILE2"
```

### **All Options:**
```powershell
python fix_forecast_comparison.py `
    --old-forecast "2026-Q1_forecast.csv" `
    --actual-sales "2026_Q3_sales.xlsx" `
    --output "custom_path/accuracy_report.csv"
```

**Parameters:**

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `--old-forecast` | ✅ Yes | Path to old forecast CSV file | `"2026-Q1_forecast.csv"` |
| `--actual-sales` | ✅ Yes | Path to actual sales Excel/CSV | `"2026_Q3_sales.xlsx"` |
| `--output` | ⛔ No | Custom output path (default: `output/forecast_accuracy_report.csv`) | `"reports/accuracy.csv"` |

---

## **Troubleshooting** 🔧

### **Problem: "FileNotFoundError: all working.csv"**

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'all working.csv'
```

**Cause:** You're running an **old version** of the script with hardcoded file names.

**Solution:**
1. Make sure you're using the **updated** `fix_forecast_comparison.py` from the root folder
2. If you have copies in other folders (like `output26`), delete them or copy the fixed version:
   ```powershell
   Copy-Item "fix_forecast_comparison.py" "output26/fix_forecast_comparison.py"
   ```
3. Or run the script from the root directory instead:
   ```powershell
   cd C:\Projects\Forecasting3
   python fix_forecast_comparison.py --old-forecast "output26\file.csv" --actual-sales "output26\sales.xlsx"
   ```

---

### **Problem: "FileNotFoundError: No such file or directory"**

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: '2026-Q1_forecast.csv'
```

**Solution:**
1. Check file exists: `ls 2026-Q1_forecast.csv`
2. Check spelling (exact match required)
3. Use full path if file is in different folder:
   ```powershell
   python fix_forecast_comparison.py --old-forecast "C:\path\to\forecast.csv" --actual-sales "C:\path\to\sales.xlsx"
   ```

---

### **Problem: "No matching data found!"**

**Error:**
```
❌ No matching data found!
   Possible issues:
   - Part numbers don't match between files
   - Quarter formats don't match (check Year_Q column)
   - Date ranges don't overlap
```

**Cause:** Forecast file and sales file have no overlapping parts or time periods.

**Solutions:**

**Issue 1: Part numbers don't match**
- Forecast file has: `ABC-123`
- Sales file has: `ABC123` (no hyphen)

**Fix:** Make sure part numbers are **exactly the same** in both files.

---

**Issue 2: Date ranges don't overlap**
- Forecast file has quarters: `26Q1, 26Q2, 26Q3`
- Sales file has dates: `01-01-25, 02-01-25, 03-01-25` (2025, not 2026)

**Fix:** Make sure sales data covers the same time period as the forecasts.

---

**Issue 3: Column names wrong**

**Required columns in forecast file:**
- `Part_number` (exact spelling)
- Quarter columns like `25Q1`, `26Q2`

**Required columns in sales file:**
- `Part_number` (exact spelling)
- `Date` (exact spelling)
- `Value` (exact spelling)

**Fix:** Rename columns in Excel to match exactly.

---

### **Problem: "No forecast columns found"**

**Error:**
```
❌ No forecast columns found (expected format: 25Q1, 26Q2, etc.)
```

**Cause:** Script couldn't find columns in format `##Q#` (e.g., 25Q1, 26Q2).

**Solutions:**
1. Check column names in forecast CSV
2. Make sure quarters follow format: `25Q1`, `25Q2`, `26Q1`, `26Q2`
3. Don't use spaces: `25 Q1` won't work
4. Don't use full year: `2025Q1` won't work (use `25Q1`)

---

### **Problem: Script runs but creates empty report**

**Cause:** Files loaded but no matching data after merge.

**Check:**
1. Open both files in Excel
2. Find 3-5 part numbers that appear in BOTH files
3. Verify these parts have:
   - Same exact spelling/format
   - Overlapping time periods
4. If no parts match → Fix part number format consistency

---

## **Best Practices** ✅

### **Do:**
- ✅ Wait at least **3 months** after forecast before comparing (gives time for sales to materialize)
- ✅ Compare **multiple quarters** for better accuracy analysis (minimum 50-100 matched records)
- ✅ Keep old forecast files archived (name with date created, e.g., `2026-01-15_forecast.csv`)
- ✅ Run comparison **quarterly** as new actual sales data becomes available
- ✅ Use Excel to spot-check a few parts manually before running script

### **Don't:**
- ⛔ Don't compare current quarter (not enough sales data yet)
- ⛔ Don't compare forecasts >1 year old (market conditions change)
- ⛔ Don't mix different product lines (compare aircraft parts separately from other products)
- ⛔ Don't use forecasts that were manually adjusted heavily (defeats purpose of measuring model accuracy)

---

## **Example Workflow** 📅

### **Scenario: It's October 2026**

**Goal:** Measure accuracy of forecasts made in January 2026

**Step 1: Identify files**
- Old forecast: `2026-Q1_forecast.csv` (created January 2026)
- Actual sales: Export Q2 and Q3 sales from ERP system

**Step 2: Export actual sales**
```
Open ERP → Sales Reports → Date Range: April 1 - Sept 30, 2026
Export as Excel → Save as "2026_Q2-Q3_sales.xlsx"
```

**Step 3: Run comparison**
```powershell
python fix_forecast_comparison.py --old-forecast "2026-Q1_forecast.csv" --actual-sales "2026_Q2-Q3_sales.xlsx"
```

**Step 4: Review results**
- Check console output for bias diagnosis
- Open `output/forecast_accuracy_report.csv` in Excel
- Sort by `Percentage_Error` to find worst offenders

**Step 5: Next forecast will auto-correct**
- Next time you run forecast (November 2026)
- System automatically loads `forecast_accuracy_report.csv`
- Applies corrections based on Q2/Q3 errors
- Saves corrected forecasts

---

## **Understanding the Output**

### **Console Statistics**

**Total comparisons:**
- Number of part-quarter pairs matched
- Example: 2,987 means 2,987 combinations of (part × quarter) were compared

**Average error:**
- Mean of all percentage errors
- Positive = over-forecasting on average
- Negative = under-forecasting on average

**Median error:**
- Middle value of all percentage errors
- More robust than average (less affected by outliers)
- **THIS is used to calculate bias correction factors**

**Accuracy by Quarter:**
- Shows if errors vary by quarter
- Example: Q1 might be +30%, Q2 might be +15%
- Helps identify seasonal bias patterns

---

### **Bias Diagnosis**

**Over-forecasted vs Under-forecasted:**
- If >60% over-forecasted → Systematic over-forecasting
- If >60% under-forecasted → Systematic under-forecasting
- If balanced (40-60% each) → No systematic bias

**Suggested correction factor:**
- Calculated as: `1 / (1 + median_error/100)`
- Example: Median error = +30% → Factor = 0.769x (reduce forecasts by 23%)
- This factor is automatically applied by the bias correction system

---

## **Files Reference** 📁

| File | Location | Purpose |
|------|----------|---------|
| **fix_forecast_comparison.py** | Root folder | Script to compare forecasts with actuals |
| **Old forecast CSV** | Root or archive folder | Past forecast you want to evaluate |
| **Actual sales Excel/CSV** | Root or exports folder | Real sales data from ERP |
| **forecast_accuracy_report.csv** | `output/` | ✅ Output - accuracy analysis (used by bias correction) |

---

## **Quick Commands** 🚀

**Help:**
```powershell
python fix_forecast_comparison.py --help
```

**Basic comparison:**
```powershell
python fix_forecast_comparison.py --old-forecast "old.csv" --actual-sales "actual.xlsx"
```

**Custom output location:**
```powershell
python fix_forecast_comparison.py --old-forecast "old.csv" --actual-sales "actual.xlsx" --output "reports/accuracy.csv"
```

**Check if output exists:**
```powershell
Test-Path "output/forecast_accuracy_report.csv"
```

**View first 10 rows:**
```powershell
Import-Csv "output/forecast_accuracy_report.csv" | Select-Object -First 10
```

---

## **Summary** 🎯

**Purpose:**
Compare old forecasts with actual sales to measure accuracy and enable bias correction.

**Input:**
1. Old forecast CSV (with quarter columns)
2. Actual sales Excel/CSV (with Date, Part_number, Value)

**Output:**
1. Console analysis (statistics, diagnosis, recommendations)
2. `forecast_accuracy_report.csv` (detailed comparison data)

**Next Step:**
Accuracy report is automatically used by forecasting system to apply bias corrections.

**Frequency:**
Run quarterly as new actual sales data becomes available.

**Result:**
Better forecast accuracy through systematic bias correction.
