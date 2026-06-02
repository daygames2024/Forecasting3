# Streamlit Dashboard - Quick Start Guide

## 🚀 Getting Started

### Step 1: Install Streamlit

```bash
pip install streamlit
```

### Step 2: Run the Dashboard

```bash
streamlit run forecast_dashboard.py
```

Your browser will automatically open to `http://localhost:8501`

---

## 📊 Dashboard Features

### 🏠 **Dashboard Tab**
- **Overview metrics** - Total forecasts, last run, bias status, output files
- **Latest forecast summary** - View and download most recent forecast
- **Recent activity** - See history of last 5 operations
- **Quick stats** at a glance

### 🎯 **Create Forecast Tab**
- **Drag & drop** sales data (Excel/CSV)
- **Optional events file** upload
- **Real-time file validation** - See if files are valid before running
- **Advanced options** - Horizon, aggregation, fast mode, etc.
- **One-click forecast generation**
- **Instant download links** for all outputs (CSV + Excel)

### 🔄 **Update Bias Tab**
- **Drag & drop** old forecast and actual sales
- **File validation** before processing
- **One-click bias update**
- **View analysis results** in the dashboard
- **Current bias status** showing accuracy metrics
- **Download accuracy reports**

### 📜 **History Tab**
- **Complete history** of all forecast runs
- **Filter by type** (Forecast or Bias Update)
- **Status indicators** (success/error)
- **Expandable details** for each run
- **Clear history** option

### ⚙️ **Settings Tab**
- **System information** - Python version, dependencies, etc.
- **Default parameters** configuration (coming soon)
- **Documentation links** - Quick access to all guides
- **Dependency status** - Check if openpyxl is installed

---

## 💡 Key Features

### ✅ **Preserves All Existing Functionality**
- **Command-line still works** - No changes to your existing workflow
- **Same Python scripts** - Dashboard just calls them
- **Same output files** - Everything saves to the same `output/` folder

### ✅ **User-Friendly**
- **No typing file paths** - Drag and drop files
- **Real-time validation** - See errors before running
- **Progress indicators** - Know what's happening
- **Download buttons** - Easy access to results

### ✅ **Smart Features**
- **History tracking** - Never lose track of what you ran
- **File size display** - Know how big your files are
- **Status indicators** - See bias correction status at a glance
- **Recent activity** - Quick access to recent forecasts

---

## 📁 File Handling

### Drag & Drop Support

All file uploads support **drag and drop**:

1. **Click the upload area** OR
2. **Drag files from your computer** and drop them in the box

### Supported Formats

| File Type | Formats | Used For |
|-----------|---------|----------|
| Sales Data | `.xlsx`, `.csv` | Creating forecasts, bias updates |
| Events File | `.csv` | Optional maintenance events |
| Old Forecast | `.csv` | Bias correction updates |

### Validation

Files are **validated automatically** when uploaded:

✅ **Sales Data:**
- Checks for `Date`, `Part_number`, `Value` columns
- Shows file size and row count preview

✅ **Events File:**
- Checks for `Check`, `Start Date`, `End Date` columns
- Shows event count

✅ **Forecast File:**
- Checks for `Part_number` column
- Checks for quarter columns (25Q1, 25Q2, etc.)
- Shows parts and quarters count

---

## 🎯 Typical Workflows

### Monthly Forecast Creation

```
1. Go to "Create Forecast" tab
2. Drag & drop sales_data.xlsx
3. Drag & drop maintenance_events.csv (optional)
4. Click "Run Forecast"
5. Wait for automatic validation with --fix
6. Wait for forecast completion (progress spinner shows)
7. Download results (CSV + Excel)
```

**Time:** 2-5 minutes depending on data size

**New:** The system automatically validates and fixes your sales data before forecasting!

### Monthly Bias Update

```
1. Go to "Update Bias" tab
2. Drag & drop old forecast from last month
3. Drag & drop current actual sales data
4. Click "Update Bias Correction"
5. Review analysis results
6. Download accuracy report
```

**Time:** 1-2 minutes

### Review History

```
1. Go to "History" tab
2. See all past runs
3. Filter by type if needed
4. Click "Details" to see parameters used
```

---

## 🔧 Advanced Options

### Forecast Parameters

| Option | Default | Description |
|--------|---------|-------------|
| Horizon | 6 | Number of quarters to forecast |
| Aggregation | sum | How to aggregate daily data (sum/mean) |
| Skip Plots | ✓ | Faster runtime, no charts generated |
| Fast Mode | ☐ | Use fewer models (faster but less accurate) |
| Output Name | forecast_output.csv | Custom output filename |

### Accessing Advanced Options

1. In "Create Forecast" tab
2. Click **"⚙️ Advanced Options"** expander
3. Adjust parameters as needed
4. Run forecast

---

## 📥 Downloads

### Automatic Downloads Available

After a successful forecast run, you get **instant download buttons** for:

✅ **Original Forecast (CSV)** - Raw forecast data  
✅ **Original Forecast (Excel)** - With summary sheet  
✅ **Corrected Forecast (CSV)** - Bias-corrected data  
✅ **Corrected Forecast (Excel)** - With correction summary ⭐

After a bias update, you get:

✅ **Accuracy Report (CSV)** - For bias correction system  
✅ **Detailed Analysis (Excel)** - 6-sheet analysis workbook

---

## 🎨 User Interface Elements

### Status Indicators

- ✅ **Green Success** - Operation completed successfully
- ❌ **Red Error** - Operation failed (click to see details)
- ⚠️ **Yellow Warning** - Warning message
- ℹ️ **Blue Info** - Informational message

### Metric Cards

Dashboard shows key metrics in colored cards:
- **Total Forecasts** - How many forecasts you've run
- **Last Run** - Date of most recent forecast
- **Bias Correction** - Active ✅ or Inactive ⚠️
- **Output Files** - Number of files in output folder

### Expandable Sections

Click **▼** to expand and see:
- Console output from runs
- File validation details
- Run parameters
- Error messages

---

## 🚨 Troubleshooting

### Dashboard won't start

**Issue:** `streamlit: command not found`

**Fix:**
```bash
pip install streamlit
```

---

### Files not validating

**Issue:** "Missing columns" error

**Fix:**
- Check your file has the required columns
- Column names are case-sensitive
- Remove any extra spaces in column names

**Sales file needs:** `Date`, `Part_number`, `Value`  
**Events file needs:** `Check`, `Start Date`, `End Date`  
**Forecast file needs:** `Part_number` + quarter columns (25Q1, 25Q2, etc.)

---

### Forecast fails to run

**Issue:** Error message after clicking "Run Forecast"

**Fix:**
1. Click the error expander to see full error message
2. Check that your files are valid (validation should pass)
3. Try with a smaller file first
4. Check command-line still works: `python -m src.app --input "file.xlsx"`

---

### Can't download files

**Issue:** Download button doesn't work

**Fix:**
- Files might not exist in output folder
- Check output folder manually: `output/forecast_output.csv`
- Browser might be blocking downloads
- Try different browser

---

### History not showing

**Issue:** History tab is empty even though you've run forecasts

**Fix:**
- History is stored in `output/forecast_history.json`
- If file is corrupted, delete it and start fresh
- Old runs (before dashboard) won't appear in history

---

## 💻 Command Line Still Works!

### Nothing has changed with your existing workflow:

```bash
# Create forecast (still works!)
python -m src.app --input "sales.xlsx" --events-file "events.csv"

# Update bias (still works!)
python fix_forecast_comparison.py --old-forecast "old.csv" --actual-sales "sales.xlsx"

# Validate data (still works!)
python validate_input_data.py --sales "sales.xlsx" --fix
```

The dashboard is just a **convenience wrapper** around these commands!

---

## 📂 Folder Structure

```
Forecasting3/
├── forecast_dashboard.py          ← New Streamlit interface
├── src/
│   ├── app.py                     ← Main forecasting logic (unchanged)
│   ├── bias_corrector.py          ← Bias correction (unchanged)
│   └── ...
├── fix_forecast_comparison.py     ← Bias update script (unchanged)
├── output/
│   ├── forecast_output.csv        ← Output files (same as before)
│   ├── forecast_output.xlsx
│   ├── forecast_output_Corrected.csv
│   ├── forecast_output_Corrected.xlsx
│   ├── forecast_history.json      ← New: Dashboard history
│   └── ...
└── temp_input/                    ← New: Temp folder for uploads (auto-deleted)
```

---

## 🎯 Best Practices

### 1. **File Naming**
- Use descriptive names: `sales_Dec2024.xlsx` not `data.xlsx`
- Include dates: `forecast_2024-12-15.csv`
- Helps track versions in history

### 2. **Regular Bias Updates**
- Update bias correction **monthly**
- Use "Update Bias" tab for quick updates
- Check "Current Bias Status" section

### 3. **Check History**
- Review history tab before important forecasts
- Verify last run was successful
- Download past forecasts if needed

### 4. **Validate First**
- Wait for validation messages (✅ or ❌)
- Don't run forecasts with invalid files
- Fix file issues before running

### 5. **Save Important Results**
- Download and rename important forecasts
- Don't rely only on `output/` folder
- Keep monthly archive of corrected forecasts

---

## 🔐 Security Notes

### Local Only

The dashboard runs **locally on your computer**:
- Only accessible at `localhost:8501`
- Files never leave your machine
- No internet connection required (except for initial install)

### File Handling

- Uploaded files saved temporarily
- Deleted after processing
- Original files in `output/` folder remain

---

## 🎨 Customization (Future)

Coming soon:
- [ ] Custom themes (dark mode)
- [ ] Adjustable dashboard layout
- [ ] More chart types
- [ ] Custom metric cards
- [ ] Email notifications
- [ ] Scheduled forecasts

---

## 📞 Getting Help

### If you encounter issues:

1. **Check the error message** - Expand error details in the dashboard
2. **Try command-line** - If dashboard fails, try CLI to isolate issue
3. **Check documentation** - Settings tab has links to all guides
4. **Check files** - Validation should catch most issues

### Useful Resources:

- **Streamlit Docs:** https://docs.streamlit.io
- **Project README:** `README.md`
- **Bias Guide:** `HOW_TO_UPDATE_BIAS_MONTHLY.md`
- **Feature Docs:** `CORRECTED_FORECAST_SUMMARY_FEATURE.md`

---

## 🚀 Next Steps

1. **Install Streamlit:** `pip install streamlit`
2. **Run Dashboard:** `streamlit run forecast_dashboard.py`
3. **Test with sample data** - Try uploading files
4. **Create your first forecast** - Use the dashboard!
5. **Check history** - See your runs logged
6. **Update bias monthly** - Use the Update Bias tab

---

**Enjoy your new forecasting dashboard!** 📊✨

Any issues? The command-line still works exactly as before - this is just a convenience layer on top!
