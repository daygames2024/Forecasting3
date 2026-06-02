# 🚀 Quick Reference - Streamlit Dashboard

## Start Dashboard

```bash
streamlit run forecast_dashboard.py
```

Opens browser at: `http://localhost:8501`

---

## 🎯 Create Forecast (3 Steps)

1. **Drag & drop** `sales_data.xlsx` → Sales Data box
2. **Drag & drop** `events.csv` → Events File box (optional)
3. **Click** "▶️ Run Forecast"

**Download:** Click any of 4 download buttons when complete

---

## 🔄 Update Bias (3 Steps)

1. **Drag & drop** `old_forecast.csv` → Old Forecast box
2. **Drag & drop** `actual_sales.xlsx` → Actual Sales box
3. **Click** "🔄 Update Bias Correction"

**Next forecast:** Automatically uses updated corrections!

---

## 📊 Required File Formats

### Sales Data (.xlsx or .csv)
```
Date       | Part_number | Value
2024-10-01 | ABC-123     | 25
2024-10-08 | ABC-123     | 18
```

### Events File (.csv)
```
Check      | Start Date | End Date
Overhaul-1 | 2025-01-15 | 2025-02-28
```

### Old Forecast (.csv)
```
Part_number | 25Q1 | 25Q2 | 25Q3
ABC-123     | 100  | 105  | 110
```

---

## ✅ Validation Indicators

- ✅ **Green** = File valid, ready to run
- ❌ **Red** = File invalid, fix before running
- 📁 Shows file size and details

---

## 📥 Output Files

After forecast runs, you get **4 downloadable files:**

1. `forecast_output.csv` - Original forecast
2. `forecast_output.xlsx` - Original with summary
3. `forecast_output_Corrected.csv` - Bias-corrected
4. `forecast_output_Corrected.xlsx` - **Corrected with summary ⭐**

---

## 🔍 Tabs Overview

| Tab | Purpose | Key Actions |
|-----|---------|-------------|
| 🏠 Dashboard | Overview & stats | View summary, download latest |
| 🎯 Create Forecast | Generate forecasts | Upload files, run forecast |
| 🔄 Update Bias | Monthly corrections | Upload files, update bias |
| 📜 History | Past runs | View history, filter, clear |
| ⚙️ Settings | Config & docs | Check status, open docs |

---

## 🚨 Common Issues

### File won't upload
- **Fix:** Check file size (<100MB), verify format (.xlsx or .csv)

### Validation fails
- **Fix:** Check required columns (case-sensitive!)
- **Sales:** `Date`, `Part_number`, `Value`
- **Events:** `Check`, `Start Date`, `End Date`
- **Forecast:** `Part_number` + quarter columns (25Q1, etc.)

### Forecast fails to run
- **Fix:** Expand error details, try CLI: `python -m src.app --input "file.xlsx"`

---

## 💡 Pro Tips

✅ **Wait for validation** - See ✅ before clicking Run  
✅ **Use descriptive names** - `sales_Dec2024.xlsx` not `data.xlsx`  
✅ **Check history** - Review past runs before new forecast  
✅ **Download important results** - Don't rely only on output folder  
✅ **Update bias monthly** - Keep corrections current

---

## 📞 Help

- **Dashboard Guide:** See `STREAMLIT_DASHBOARD_GUIDE.md`
- **Bias Updates:** See `HOW_TO_UPDATE_BIAS_MONTHLY.md`
- **CLI Still Works:** All command-line functionality unchanged!

---

## ⌨️ CLI Quick Reference (Still Works!)

```bash
# Create forecast
python -m src.app --input "sales.xlsx" --events-file "events.csv"

# Update bias
python fix_forecast_comparison.py --old-forecast "old.csv" --actual-sales "sales.xlsx"
```

**Dashboard is just a convenient wrapper - use whichever you prefer!**

---

**Quick Start:**
```bash
pip install streamlit
streamlit run forecast_dashboard.py
```

**Your browser opens → Start forecasting! 🚀**
