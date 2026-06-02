# How To: Validate Input Data Before Forecasting

## **What is This Tool?**

**Purpose:** Check your sales data and maintenance events files for common formatting issues **before** running forecasts. Catches date format problems, missing columns, and data quality issues early.

**Why use it:** Prevents forecast failures due to bad input data. Especially useful for catching date format mismatches that cause bias correction to fail.

---

## **Quick Start** ⚡

**Validate sales data only:**
```powershell
python validate_input_data.py --sales "sales_data.xlsx"
```

**Validate sales + maintenance events:**
```powershell
python validate_input_data.py --sales "sales_data.xlsx" --events "maintenance_events.csv"
```

**Validate AND auto-fix issues:**
```powershell
python validate_input_data.py --sales "sales_data.xlsx" --events "maintenance_events.csv" --fix
```

---

## **What It Checks**

### **Sales Data Validation** 📊

✅ **File Existence & Format**
- File exists and is readable
- File type is .xlsx or .csv

✅ **Required Columns**
- `Date` column exists
- `Part_number` column exists
- `Value` column exists

✅ **Date Column**
- All dates can be parsed
- Shows date range (min to max)
- Shows quarter distribution (23Q1, 23Q2, etc.)
- Identifies unparseable dates with examples

✅ **Part_number Column**
- No missing part numbers
- Shows unique part count
- Shows top 5 parts by transaction count

✅ **Value Column**
- All values are numeric
- No missing values
- Checks for negative values (warning)
- Shows min, max, mean, median

✅ **Data Quality**
- Checks for duplicate rows
- Identifies data integrity issues

---

### **Maintenance Events Validation** 🛠️

✅ **File Existence & Format**
- File exists and is CSV
- File is readable

✅ **Required Columns**
- `Check` column (event name)
- `Start Date` column
- `End Date` column

✅ **Event Names**
- No missing event names
- Shows event type distribution (C1, 6YR, etc.)

✅ **Dates**
- Start Date can be parsed
- End Date can be parsed
- End Date is after Start Date
- Shows event date range

---

### **Date Range Comparison** 📅

✅ **Overlap Check**
- Compares sales data range vs. events range
- Warns if no overlap
- Checks if events cover forecast period
- Identifies gaps in coverage

---

## **Step-by-Step Usage**

### **Step 1: Validate Your Data**

**Run validation (no changes):**
```powershell
python validate_input_data.py --sales "sales_data.xlsx" --events "maintenance_events.csv"
```

**Example output:**
```
======================================================================
VALIDATING SALES DATA
======================================================================
File: sales_data.xlsx

✅ Loaded Excel file: 45,678 rows

Checking required columns...
✅ All required columns found: ['Date', 'Part_number', 'Value']

Validating Date column...
⚠️  234 dates could not be parsed
   Examples of unparseable dates: ['01/15/2025', '02-30-2025', 'Invalid']
   Date range: 2022-01-01 to 2024-12-31

   Quarter distribution:
      22Q1: 2,345 rows
      22Q2: 2,456 rows
      22Q3: 2,567 rows
      ...

Validating Part_number column...
✅ No missing Part_numbers
   Unique parts: 1,234

   Top 5 parts by transaction count:
      ABC-123: 456 transactions
      DEF-456: 345 transactions
      ...

Validating Value column...
✅ All Values are numeric
   Min value: 0
   Max value: 1500
   Mean value: 23.45
   Median value: 12.00

======================================================================
VALIDATION SUMMARY
======================================================================
❌ Found 1 issue(s) that need attention
   1. 234 dates could not be parsed
```

---

### **Step 2: Review Issues**

**Common issues:**

**❌ "Missing required columns"**
- Your file doesn't have `Date`, `Part_number`, or `Value` columns
- **Fix:** Rename columns in Excel to match exactly

**❌ "X dates could not be parsed"**
- Date formats are inconsistent (e.g., mix of MM/DD/YYYY and DD-MM-YYYY)
- **Fix:** Use `--fix` flag to auto-standardize

**❌ "End Date before Start Date"**
- Maintenance events have end before start
- **Fix:** Use `--fix` flag to remove invalid events

**⚠️ "Events don't cover forecast period"**
- Your events file only has past events
- **Fix:** Add future events to your maintenance schedule

---

### **Step 3: Auto-Fix Issues**

**Run with --fix flag:**
```powershell
python validate_input_data.py --sales "sales_data.xlsx" --events "maintenance_events.csv" --fix
```

**What --fix does:**

**For Sales Data:**
1. Removes rows with missing Date, Part_number, or Value
2. Standardizes all dates to `YYYY-MM-DD` format
3. Sorts data by Part_number and Date
4. Saves to: `sales_data_FIXED.xlsx`

**For Events:**
1. Removes events with missing data
2. Removes events with invalid date ranges
3. Standardizes dates to `DD-MM-YY` format
4. Sorts by Start Date
5. Saves to: `maintenance_events_FIXED.csv`

**Example output:**
```
======================================================================
FIXING ISSUES
======================================================================
⚠️  Removed 234 rows with missing data
✅ Standardized dates to YYYY-MM-DD format
✅ Sorted data by Part_number and Date
✅ Fixed file saved to: sales_data_FIXED.xlsx

   Next steps:
   1. Review the fixed file: sales_data_FIXED.xlsx
   2. Run forecast with: python -m src.app --input "sales_data_FIXED.xlsx"
```

---

### **Step 4: Run Forecast with Fixed Files**

**After validation passes:**
```powershell
python -m src.app --input "sales_data_FIXED.xlsx" --events-file "maintenance_events_FIXED.csv"
```

---

## **Common Workflows**

### **Workflow 1: First-Time Data Prep** 📋

**Scenario:** Just exported data from ERP, need to prepare for forecasting

```powershell
# Step 1: Validate
python validate_input_data.py --sales "erp_export.xlsx"

# Step 2: Review console output for issues

# Step 3: Fix
python validate_input_data.py --sales "erp_export.xlsx" --fix

# Step 4: Run forecast
python -m src.app --input "erp_export_FIXED.xlsx"
```

---

### **Workflow 2: Troubleshooting Bias Correction** 🔧

**Scenario:** Bias correction not matching because of date format issues

```powershell
# Step 1: Validate both old forecast and actual sales
python validate_input_data.py --sales "2026_Q3_sales.xlsx" --fix

# Step 2: Check quarter distribution in console output
#         Make sure quarters match your forecast file (25Q1, 25Q2, etc.)

# Step 3: Re-run forecast comparison
python fix_forecast_comparison.py --old-forecast "2026-Q1_forecast.csv" --actual-sales "2026_Q3_sales_FIXED.xlsx"

# Step 4: Run forecast with corrected bias
python -m src.app --input "sales_data_FIXED.xlsx" --events-file "maintenance_events.csv"
```

---

### **Workflow 3: Monthly Data Refresh** 🔄

**Scenario:** Update with latest month of sales data

```powershell
# Step 1: Validate new export
python validate_input_data.py --sales "latest_sales_jan2025.xlsx" --fix

# Step 2: Verify date range extends to current month
#         (Check console output "Date range: ... to 2025-01-31")

# Step 3: Run forecast
python -m src.app --input "latest_sales_jan2025_FIXED.xlsx" --events-file "maintenance_events.csv"
```

---

## **Understanding the Output**

### **Date Range Analysis**

**Example:**
```
Date range: 2022-01-01 to 2024-12-31

Quarter distribution:
   22Q1: 2,345 rows
   22Q2: 2,456 rows
   22Q3: 2,567 rows
   23Q1: 2,678 rows
   ...
```

**What it means:**
- ✅ You have **3 years** of history (2022-2024)
- ✅ Data is relatively balanced across quarters
- ✅ Good for forecasting (need 2+ years minimum)

**Red flags:**
- ⚠️ Date range only 6 months → Not enough history
- ⚠️ Large gaps between quarters → Missing data
- ⚠️ Quarter labels wrong (e.g., all "24Q5") → Date parsing failed

---

### **Part Number Analysis**

**Example:**
```
Unique parts: 1,234

Top 5 parts by transaction count:
   ABC-123: 456 transactions
   DEF-456: 345 transactions
   GHI-789: 234 transactions
```

**What it means:**
- ✅ You have 1,234 unique parts
- ✅ Top parts have lots of history (good for forecasting)
- ✅ Enough data for reliable forecasts

**Red flags:**
- ⚠️ Unique parts: 1 → Only one part (check file)
- ⚠️ Top part: 2 transactions → Very sparse data
- ⚠️ Many parts with 1 transaction → Lots of Tier 4 parts

---

### **Date Range Comparison (Sales vs Events)**

**Good overlap:**
```
Sales data range:  2022-01-01 to 2024-12-31
Events data range: 2024-06-01 to 2026-12-31

✅ Date ranges overlap - events will be applied to forecasts

Expected forecast range: 2024-12-31 to 2026-06-30
✅ Events cover at least part of forecast period
```

**No overlap (problem):**
```
Sales data range:  2022-01-01 to 2024-12-31
Events data range: 2020-01-01 to 2021-12-31

⚠️  Events end BEFORE sales data starts - no overlap!
```

**Fix:** Update maintenance_events.csv with future events (2025-2026)

---

## **Troubleshooting**

### **Problem: "File not found"**

**Error:**
```
❌ File not found: sales_data.xlsx
```

**Solution:**
1. Check file path is correct
2. Check spelling (exact match required)
3. Use full path: `C:\Projects\Forecasting3\sales_data.xlsx`

---

### **Problem: "Missing required columns"**

**Error:**
```
❌ Missing required columns: ['Date']
   Found columns: ['Transaction_Date', 'Part_number', 'Value']
```

**Solution:**
1. Open file in Excel
2. Rename `Transaction_Date` to `Date`
3. Save and re-run validation

**Required column names (exact):**
- `Date` (not "Transaction Date" or "transaction_date")
- `Part_number` (not "Part Number" or "part_number")
- `Value` (not "Quantity" or "value")

---

### **Problem: "X dates could not be parsed"**

**Error:**
```
⚠️  234 dates could not be parsed
   Examples of unparseable dates: ['02-30-2025', 'N/A', '']
```

**Common causes:**
1. **Invalid dates:** Feb 30th doesn't exist
2. **Text values:** "N/A", "TBD", empty cells
3. **Wrong format:** Excel stored as text

**Solution:**
1. Use `--fix` flag to auto-remove bad rows
2. Or fix manually in Excel (remove invalid dates)
3. Re-export from ERP with clean data

---

### **Problem: "Dates parsed but wrong quarters"**

**Symptom:**
```
Quarter distribution:
   94Q1: 12,345 rows  ← Wrong! Should be 24Q1
```

**Cause:** Date parsing interpreted dates incorrectly

**Solution:**
1. Open Excel
2. Format Date column as Date (not text)
3. Check first few dates are correct format
4. Re-save and validate

---

### **Problem: Fixed file still has issues**

**Scenario:** Ran with `--fix` but forecast still fails

**Steps:**
1. Open the `_FIXED` file in Excel
2. Manually check:
   - Dates are in `YYYY-MM-DD` format
   - No blank rows
   - Part numbers are consistent
3. If issues remain, fix manually in Excel
4. Re-run validation (without `--fix`) to verify

---

## **Best Practices** ✅

### **Do:**
- ✅ **Always validate before forecasting** - Catches issues early
- ✅ **Run with --fix first time** - Automatically standardizes formats
- ✅ **Check console output** - Read the quarter distribution and date ranges
- ✅ **Verify fixed files** - Open in Excel to spot-check
- ✅ **Keep original files** - Tool creates `_FIXED` versions, doesn't overwrite

### **Don't:**
- ⛔ **Don't skip validation** - Saves time debugging later
- ⛔ **Don't ignore warnings** - Yellow warnings can cause forecast issues
- ⛔ **Don't edit _FIXED files** - Re-run validation instead
- ⛔ **Don't mix date formats** - Standardize in source system if possible

---

## **Command Reference** 📋

**Validate sales only:**
```powershell
python validate_input_data.py --sales "file.xlsx"
```

**Validate sales + events:**
```powershell
python validate_input_data.py --sales "file.xlsx" --events "events.csv"
```

**Auto-fix issues:**
```powershell
python validate_input_data.py --sales "file.xlsx" --fix
```

**Full validation with fix:**
```powershell
python validate_input_data.py --sales "file.xlsx" --events "events.csv" --fix
```

**Get help:**
```powershell
python validate_input_data.py --help
```

---

## **Files Created**

| Original File | Fixed File | Description |
|---------------|------------|-------------|
| `sales_data.xlsx` | `sales_data_FIXED.xlsx` | Sales data with standardized dates (YYYY-MM-DD) |
| `sales_data.csv` | `sales_data_FIXED.csv` | CSV version with standardized dates |
| `maintenance_events.csv` | `maintenance_events_FIXED.csv` | Events with standardized dates (DD-MM-YY) |

**Note:** Fixed files are only created when using `--fix` flag.

---

## **Integration with Forecasting Workflow**

**Recommended workflow:**

```
┌─────────────────────┐
│ 1. Export from ERP  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────┐
│ 2. Validate Input Data      │
│    python validate_input... │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────┐
│ 3. Review Issues    │
│    Fix if needed    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 4. Run Forecast     │
│    python -m src... │
└─────────────────────┘
```

**Time savings:**
- ⏱️ Validation: 10-30 seconds
- ⏱️ Manual debugging: 10-30 minutes (if you skip validation)

**ROI:** Always worth the 30 seconds! 🎯

---

## **Summary**

**Purpose:** Catch data quality issues before forecasting

**Key Benefits:**
- ✅ Prevents forecast failures
- ✅ Fixes date format mismatches (bias correction killer)
- ✅ Standardizes data automatically
- ✅ Shows data quality metrics
- ✅ Compares sales vs events date ranges

**When to use:**
- 🔄 Before every forecast run (best practice)
- 🆕 First time using new data source
- 🔧 Troubleshooting bias correction issues
- 📅 Monthly data refresh

**Next steps:**
1. Run validation on your current data
2. Review console output
3. Use `--fix` to auto-correct issues
4. Run forecast with fixed files
5. Enjoy accurate forecasts! 🚀
