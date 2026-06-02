# Summary Sheets in Forecast Files

## **Overview**

The forecasting system now creates **two summary sheets** to document your process:

1. **Validation Summary** - Added to your input sales file
2. **Forecast Summary** - Added to your output forecast file

---

## **1. Validation Summary Sheet**

### **Where:** In your sales data Excel file (e.g., `sales_data.xlsx`)

### **When Created:** When you run `validate_input_data.py`

### **Command:**
```powershell
python validate_input_data.py --sales "sales_data.xlsx"
```

### **What's Included:**

📊 **Data Overview:**
- Total rows, date range, unique parts
- Quarter distribution (22Q1, 22Q2, 23Q1, etc.)
- Top 10 parts by transaction count

📈 **Statistics:**
- Value min/max/mean/median/total
- Validation timestamp

⚠️ **Issues Found:**
- Missing data warnings
- Date parsing errors
- Data quality problems

✅ **Forecast Readiness:**
- Status (ready or needs fixes)
- Next steps command

### **Location:** First tab named `"Validation_Summary"`

---

## **2. Forecast Summary Sheet**

### **Where:** In your forecast output Excel file (e.g., `forecast_output.xlsx`)

### **When Created:** Automatically when forecast completes

### **Command:**
```powershell
python -m src.app --input "sales_data.xlsx" --outdir "output" --skip-plots
```

### **What's Included:**

📊 **Input Data:**
- Sales file used
- Events file used
- Total parts processed

⚙️ **Forecast Parameters:**
- Horizon (quarters)
- Aggregation method
- Last quarter in data
- Fast mode (yes/no)
- Plots generated (yes/no)

📈 **Momentum Distribution:**
```
ACCELERATING:         1,234
SLOWING:              2,456
STABLE / MIXED:       5,678
REVERSAL (RECOVERY):    567
REVERSAL (DOWNTURN):    223
```

🎯 **Forecastability Tiers:**
```
Tier_1_High:              3,456
Tier_2_Medium:            4,567
Tier_3_Volume_Only:       1,234
Tier_4_Not_Forecastable:    901
```

💡 **Confidence Levels:**
```
High:      3,456
Medium:    4,567
Low:       2,135
```

⚠️ **High Usage Alerts:**
- Parts flagged for review

🛠️ **Maintenance Events:**
- Total events
- Parts affected by events

📁 **Output Files:**
- Forecast file location
- Corrected file (if bias correction applied)

### **Location:** First tab named `"Forecast_Summary"`

---

## **Complete Workflow Example**

### **Step 1: Validate Input Data**

```powershell
python validate_input_data.py --sales "sales_data.xlsx"
```

**Result:**
- ✅ `sales_data.xlsx` now has `Validation_Summary` tab
- Shows data quality, quarters, top parts

### **Step 2: Run Forecast**

```powershell
python -m src.app --input "sales_data.xlsx" --events-file "maintenance_events.csv" --outdir "output" --skip-plots
```

**Result:**
- ✅ `output/forecast_output.csv` created
- ✅ `output/forecast_output.xlsx` created with summary
  - Tab 1: `Forecast_Summary` (stats)
  - Tab 2: `Forecast_Data` (results)

### **Step 3: Review Both Summaries**

**Input Summary (`sales_data.xlsx`):**
- Check quarter distribution
- Verify date range covers forecast period
- Review data quality issues

**Forecast Summary (`forecast_output.xlsx`):**
- Check tier distribution
- Review momentum status counts
- Verify events were applied
- Check alert counts

---

## **Benefits**

✅ **Built-in Documentation:**
- No need to save console output
- Summaries travel with files
- Always know processing parameters

✅ **Audit Trail:**
- Timestamps on both summaries
- Shows input files used
- Documents validation results

✅ **Quick Reference:**
- See stats at a glance
- No need to re-run scripts
- Easy to share with team

✅ **Troubleshooting:**
- Check if data was validated
- Verify parameters used
- Review distribution of tiers

---

## **File Structure**

### **Before Validation:**
```
sales_data.xlsx
└── Sheet1 (your data)
```

### **After Validation:**
```
sales_data.xlsx
├── Validation_Summary ⭐ NEW
└── Sheet1 (your data)
```

### **After Forecast:**
```
output/
├── forecast_output.csv
└── forecast_output.xlsx ⭐ NEW
    ├── Forecast_Summary (stats)
    └── Forecast_Data (results)
```

---

## **Troubleshooting**

### **Validation summary not created?**

**Check if openpyxl is installed:**
```powershell
python -c "import openpyxl; print('Installed')"
```

**If error, install:**
```powershell
python -m pip install openpyxl
```

**Then re-run validation:**
```powershell
python validate_input_data.py --sales "sales_data.xlsx"
```

---

### **Forecast summary not created?**

**Check console output:**
- Look for: "✅ Excel file created with summary"
- If you see: "⚠️ Could not create Excel summary" - openpyxl missing

**Install openpyxl:**
```powershell
python -m pip install openpyxl
```

**Re-run forecast:**
```powershell
python -m src.app --input "sales_data.xlsx" --outdir "output" --skip-plots
```

---

### **CSV file created instead of Excel?**

**Check your command:**
- CSV output: `--outfile "forecast_output.csv"`
- Excel output: `--outfile "forecast_output.xlsx"`

**Or:** System auto-creates Excel from CSV if openpyxl is available

---

## **Summary**

**Two Summary Sheets:**
1. ✅ Validation Summary (in sales file)
2. ✅ Forecast Summary (in forecast file)

**Requirement:**
- Install openpyxl: `python -m pip install openpyxl`

**Benefits:**
- Built-in documentation
- Audit trail
- Quick reference
- Easy sharing

**Next Steps:**
1. Install openpyxl
2. Run validation on your sales file
3. Run forecast
4. Open Excel files to see summaries
