# Example: Validation Summary Sheet

## What the "Validation_Summary" Tab Looks Like

When you run `validate_input_data.py` on an Excel file, it creates a new tab as the **first sheet** in your workbook:

```
┌─────────────────────────────────────────────────────────────────┐
│ Tab: Validation_Summary  │  Tab: Sheet1 (your sales data)       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Sheet Contents (Formatted in Excel)

```
╔══════════════════════════════════════════════════════════════════╗
║ FORECAST INPUT DATA VALIDATION SUMMARY                           ║  ← Dark Blue Header
╚══════════════════════════════════════════════════════════════════╝
Generated:                         2025-01-15 14:32:45


╔══════════════════════════════════════════════════════════════════╗
║ SALES DATA VALIDATION                                            ║  ← Blue Section Header
╚══════════════════════════════════════════════════════════════════╝
File:                              sales_data.xlsx
Total Rows:                        45,678


Date Range:                                                            ← Bold Sub-header
  Min Date:                        2022-01-01
  Max Date:                        2024-12-31


Quarter Distribution:              Row Count                           ← Bold Sub-header
  22Q1                             2,345
  22Q2                             2,456
  22Q3                             2,567
  22Q4                             2,678
  23Q1                             3,123
  23Q2                             3,234
  23Q3                             3,345
  23Q4                             3,456
  24Q1                             3,567
  24Q2                             3,678
  24Q3                             3,789
  24Q4                             3,940


Part Numbers:                                                          ← Bold Sub-header
  Unique Parts:                    1,234


Top 10 Parts by Transaction Count:    Transactions                    ← Bold Sub-header
  ABC-123                          456
  DEF-456                          345
  GHI-789                          234
  JKL-012                          198
  MNO-345                          187
  PQR-678                          156
  STU-901                          143
  VWX-234                          129
  YZA-567                          112
  BCD-890                          98


Value Statistics:                                                      ← Bold Sub-header
  Min:                             0
  Max:                             1,500
  Mean:                            23.45
  Median:                          12.00
  Total:                           1,071,181


Validation Issues:                                                     ← Bold Sub-header
  ✅ No issues found                                                   ← Green Text


╔══════════════════════════════════════════════════════════════════╗
║ MAINTENANCE EVENTS VALIDATION                                    ║  ← Blue Section Header
╚══════════════════════════════════════════════════════════════════╝
Total Events:                      420


Event Types:                       Count                               ← Bold Sub-header
  C1                               145
  6YR                              101
  C2                               98
  Plant Shutdown                   76


Event Date Range:                                                      ← Bold Sub-header
  Earliest Start:                  2024-06-01
  Latest End:                      2026-12-31


╔══════════════════════════════════════════════════════════════════╗
║ FORECAST READINESS                                               ║  ← Blue Section Header
╚══════════════════════════════════════════════════════════════════╝
Status:                            ✅ READY FOR FORECASTING           ← Green Text


╔══════════════════════════════════════════════════════════════════╗
║ NEXT STEPS                                                       ║  ← Blue Section Header
╚══════════════════════════════════════════════════════════════════╝
1.                                 Review validation issues above
2.                                 Fix any critical issues
3.                                 Run forecast command:
                                   python -m src.app --input "sales_data.xlsx" --events-file "maintenance_events.csv"
```

---

## Color Coding

The sheet uses color coding for easy reading:

| Element | Color | Purpose |
|---------|-------|---------|
| **Main Header** | Dark Blue (White Text) | FORECAST INPUT DATA VALIDATION SUMMARY |
| **Section Headers** | Blue (White Text) | SALES DATA VALIDATION, MAINTENANCE EVENTS VALIDATION, etc. |
| **Sub-headers** | Bold Black | Date Range:, Quarter Distribution:, etc. |
| **✅ Success** | Green | No issues found, READY FOR FORECASTING |
| **⚠️ Warning** | Orange | Non-critical issues |
| **❌ Error** | Red | Critical issues that must be fixed |

---

## Example with Issues

If validation found problems, it would look like:

```
Validation Issues:                                                     ← Bold Sub-header
  ⚠️  Issue 1:                   234 dates could not be parsed        ← Orange Text
  ⚠️  Issue 2:                   14656 duplicate rows (same Date + Part_number)  ← Orange Text


╔══════════════════════════════════════════════════════════════════╗
║ FORECAST READINESS                                               ║
╚══════════════════════════════════════════════════════════════════╝
Status:                            ⚠️  HAS ISSUES - Review above      ← Orange Text
```

---

## How to Use the Summary Sheet

### **Before Running Forecast:**
1. Open your sales data Excel file
2. Click on **"Validation_Summary"** tab (first tab)
3. Check **"FORECAST READINESS"** section:
   - ✅ Green = Ready to forecast
   - ⚠️ Orange = Has issues, review needed
4. Review **"Quarter Distribution"** to see data coverage
5. Review **"Top 10 Parts"** to verify expected parts
6. Copy **forecast command** from "NEXT STEPS" section

### **After Running Forecast:**
1. Keep the summary tab as documentation
2. Shows what data was used to create the forecast
3. Timestamp shows when data was validated
4. Useful for audit trail and troubleshooting

### **For Monthly Updates:**
1. Each time you validate, summary tab is updated
2. Old summary is replaced with new one
3. Always shows most recent validation results

---

## Benefits

✅ **Built-in Documentation**
- No need to save validation console output
- Summary travels with your sales file
- Always know when data was last validated

✅ **Quick Reference**
- See quarter distribution without running queries
- Check top parts at a glance
- Verify date ranges cover forecast period

✅ **Audit Trail**
- Shows validation timestamp
- Documents issues found
- Proves data quality before forecasting

✅ **Easy Sharing**
- Share sales file with validation results included
- Colleagues can see data quality status
- No separate documentation needed

---

## Tips

💡 **Check the summary before forecasting:**
```
1. Open sales_data.xlsx
2. Look at Validation_Summary tab
3. Verify: ✅ READY FOR FORECASTING
4. Run the command shown in NEXT STEPS
```

💡 **Use for troubleshooting:**
```
If forecast fails, check Validation_Summary:
- Are there validation issues?
- Does quarter distribution look correct?
- Do dates cover the expected range?
```

💡 **Keep historical records:**
```
Before updating sales data:
1. Save a copy: sales_data_2025-01.xlsx
2. Validate includes summary tab
3. Create archive folder
4. Keep monthly snapshots with validation summaries
```

---

## Summary Sheet vs Console Output

| Feature | Console Output | Summary Sheet |
|---------|---------------|---------------|
| **Where** | Terminal window | Excel tab in your file |
| **Persistence** | Lost when window closes | Saved with file forever |
| **Formatting** | Plain text | Color-coded, formatted |
| **Portability** | Must copy/paste | Travels with file |
| **Timestamp** | ✅ Yes | ✅ Yes |
| **Quarter Distribution** | ✅ Yes | ✅ Yes |
| **Top Parts** | ✅ Yes | ✅ Yes |
| **Next Steps** | ✅ Yes | ✅ Yes |
| **File Size** | 0 bytes | ~50 KB added to Excel |

**Recommendation:** Use both!
- Console output for immediate feedback
- Summary sheet for documentation and reference
