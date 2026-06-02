# 📊 Streamlit Forecast Dashboard

A beautiful, user-friendly web interface for your forecasting system. **All existing command-line functionality remains unchanged** - this is just a convenient GUI wrapper!

---

## 🎯 Quick Start

### 1. Install Streamlit

```bash
pip install streamlit
```

### 2. Launch Dashboard

```bash
streamlit run forecast_dashboard.py
```

### 3. Use the Interface

Your browser opens automatically to `http://localhost:8501` - start forecasting!

---

## ✨ What You Get

### 🏠 **Dashboard Tab**

```
┌─────────────────────────────────────────────────────────────┐
│  📊 Overview                                                 │
├──────────────┬──────────────┬──────────────┬───────────────┤
│ Total        │ Last Run     │ Bias         │ Output Files  │
│ Forecasts    │              │ Correction   │               │
│    12        │  Dec 15      │  Active ✅   │     48        │
└──────────────┴──────────────┴──────────────┴───────────────┘

📈 Latest Forecast Summary
[View embedded summary sheet from Excel]
[Download Excel button]

🕒 Recent Activity
✅ Forecast - Dec 15, 2024 - 1,234 parts processed
✅ Bias Update - Dec 12, 2024 - Updated from Sept forecast
✅ Forecast - Nov 18, 2024 - 1,189 parts processed
```

### 🎯 **Create Forecast Tab**

```
📊 Sales Data (Required)
┌─────────────────────────────────────────┐
│  Drag & drop or click to browse        │
│                                         │
│  📄 sales_Dec2024.xlsx                  │
│  ✅ Valid file (3 columns detected)     │
│  📁 Size: 2.3 MB                        │
└─────────────────────────────────────────┘

📅 Events File (Optional)
┌─────────────────────────────────────────┐
│  Drag & drop or click to browse        │
│                                         │
│  📄 maintenance_events.csv              │
│  ✅ Valid file (42 events detected)     │
└─────────────────────────────────────────┘

⚙️ Advanced Options [Expand ▼]

           [▶️ Run Forecast]

📥 Download Results
[⬇️ Original Forecast (CSV)]  [⬇️ Corrected Forecast (CSV)]
[⬇️ Original Forecast (Excel)] [⬇️ Corrected Forecast (Excel) ⭐]
```

### 🔄 **Update Bias Tab**

```
📊 Old Forecast (Required)     📈 Actual Sales (Required)
┌──────────────────────────┐  ┌──────────────────────────┐
│ Drag & drop old forecast │  │ Drag & drop actual sales │
│                          │  │                          │
│ 📄 Sept2024_forecast.csv │  │ 📄 sales_Nov2024.xlsx    │
│ ✅ Valid (1,234 parts)   │  │ ✅ Valid (45,678 rows)   │
└──────────────────────────┘  └──────────────────────────┘

           [🔄 Update Bias Correction]

📊 Current Bias Correction Status
┌──────────┬────────────┬──────────┬──────────────┐
│ Total    │ Avg Error  │ Median   │ Bias Type    │
│ Compares │            │ Error    │              │
│ 1,234    │   28.5%    │  22.3%   │ Over-        │
│          │            │          │ forecasting  │
└──────────┴────────────┴──────────┴──────────────┘
```

### 📜 **History Tab**

```
Filter by Type: [✓ Forecast] [✓ Bias Update]     [🗑️ Clear History]

🎯 Forecast            Dec 15, 2024 14:30
✅ 1,234 parts processed                           📁 forecast_output.csv

🔄 Bias Update         Dec 12, 2024 09:15
✅ Updated from Sept2024_forecast.csv              📁 accuracy_report.csv

🎯 Forecast            Nov 18, 2024 16:45
✅ 1,189 parts processed                           📁 forecast_output.csv

🔄 Bias Update         Nov 10, 2024 10:20
✅ Updated from Aug2024_forecast.csv               📁 accuracy_report.csv
```

### ⚙️ **Settings Tab**

```
📁 Default Folders
Input Folder:   data/
Output Folder:  output/
Plots Folder:   output/plots/

🔧 Default Forecast Parameters
Horizon:        [6] quarters
Aggregation:    [Sum ▼]
Skip Plots:     [✓]

ℹ️ System Information
Python Version:        3.11.5
Streamlit Version:     1.28.0
openpyxl (Excel):      ✅ Installed
Bias Correction:       ✅ Active

📚 Documentation
📄 HOW_TO_CREATE_FORECAST.md          [📖 Open]
📄 HOW_TO_UPDATE_BIAS_MONTHLY.md      [📖 Open]
📄 HOW_TO_BIAS_CORRECTION.md          [📖 Open]
```

---

## 🎨 Features

### ✅ **Drag & Drop**
No more typing file paths! Just drag files from your computer.

### ✅ **Real-Time Validation**
See if files are valid before running - saves time!

### ✅ **Progress Indicators**
Know exactly what's happening with spinners and status messages.

### ✅ **Instant Downloads**
Click to download CSV or Excel files directly from the dashboard.

### ✅ **History Tracking**
Never lose track of what you ran and when.

### ✅ **Status at a Glance**
See bias correction status, file counts, and recent activity instantly.

### ✅ **Error Messages**
Clear error messages with expandable details for troubleshooting.

### ✅ **No CLI Required**
Point-and-click interface - perfect for non-technical users.

---

## 🔄 Workflow Examples

### Monthly Forecast Creation

```
1. Open dashboard (streamlit run forecast_dashboard.py)
2. Go to "Create Forecast" tab
3. Drag sales_Dec2024.xlsx → Sales Data box
4. Drag maintenance_events.csv → Events File box
5. Wait for validation (✅ appears)
6. Click "▶️ Run Forecast"
7. Wait for completion (~2-5 minutes)
8. Download results with one click
```

**Before Dashboard:** Type long command, copy-paste file paths, check output folder manually  
**With Dashboard:** Drag, drop, click, download - Done! ✨

### Monthly Bias Update

```
1. Go to "Update Bias" tab
2. Drag Sept2024_forecast.csv → Old Forecast box
3. Drag sales_Nov2024.xlsx → Actual Sales box
4. Click "🔄 Update Bias Correction"
5. Review analysis results in dashboard
6. Download accuracy report
```

**Before Dashboard:** Type command with two file paths, hope they're correct  
**With Dashboard:** Drag two files, click once - Done! ✨

---

## 💡 Key Benefits

### For You (Technical User)

✅ **Faster workflow** - No typing file paths  
✅ **Visual feedback** - See what's happening  
✅ **History tracking** - Know what you ran  
✅ **CLI still works** - Use whichever you prefer  
✅ **Same results** - Dashboard just wraps existing scripts

### For Non-Technical Users

✅ **No command line needed** - Point and click  
✅ **Clear instructions** - Tooltips and help text  
✅ **Validation before running** - Catch errors early  
✅ **Professional interface** - Looks like a real app  
✅ **Easy downloads** - One-click download buttons

---

## 📊 Technical Details

### Architecture

```
User Interface (Streamlit)
         ↓
Dashboard (forecast_dashboard.py)
         ↓
Existing Python Scripts
         ↓
Output Files (same as before)
```

**Nothing changes in your core logic** - the dashboard just:
1. Accepts file uploads
2. Saves them temporarily
3. Calls your existing Python scripts
4. Shows the results
5. Provides download links

### File Flow

```
1. User uploads file → Saved to temp folder
2. Dashboard validates → Shows ✅ or ❌
3. User clicks Run → Calls python -m src.app ...
4. Script runs → Same as command line
5. Files created → In output/ folder (same location)
6. Dashboard shows → Download buttons
7. Temp files → Auto-deleted
```

### Session State

Dashboard uses Streamlit session state to track:
- Forecast history (saved to `output/forecast_history.json`)
- Last run status
- Uploaded files (temporary)

**All persistent data stays in your `output/` folder** - nothing hidden!

---

## 🛠️ Customization

The dashboard is easy to customize:

### Change Colors

Edit the CSS in `forecast_dashboard.py`:

```python
st.markdown("""
<style>
    .main-header {
        color: #366092;  ← Change this
    }
</style>
""", unsafe_allow_html=True)
```

### Add New Metrics

Add to the Dashboard tab:

```python
with col5:
    st.metric("Your Metric", "Value")
```

### Add New Tabs

```python
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Dashboard", 
    "🎯 Create Forecast", 
    "🔄 Update Bias", 
    "📜 History",
    "⚙️ Settings",
    "📊 Your New Tab"  ← Add here
])

with tab6:
    st.header("Your New Feature")
    # Your code here
```

---

## 🚀 Future Enhancements (Ideas)

### Phase 1 (Current)
- ✅ Drag and drop file uploads
- ✅ Real-time validation
- ✅ Progress indicators
- ✅ History tracking
- ✅ Download buttons

### Phase 2 (Coming Soon)
- [ ] Charts and graphs (accuracy trends)
- [ ] Side-by-side forecast comparison
- [ ] Email notifications on completion
- [ ] Dark mode
- [ ] Export to PDF

### Phase 3 (Future)
- [ ] Multi-user support
- [ ] Database integration
- [ ] Scheduled forecasts
- [ ] Mobile app
- [ ] API endpoints

---

## 📱 Mobile Support

The dashboard works on tablets and phones, but best experience is on desktop:

- **Desktop** ✅ Recommended - Full features
- **Tablet** ⚠️ Works - Some buttons small
- **Phone** ⚠️ Limited - Best for viewing only

---

## 🔒 Security & Privacy

### Local Only
- Runs on **your computer only** (`localhost:8501`)
- **No internet** connection needed (after install)
- Files **never uploaded** to cloud
- **No external** data sharing

### File Handling
- Uploaded files → Saved temporarily
- Processing complete → Files deleted
- Results → Saved to `output/` folder (same as CLI)

---

## 🆚 Dashboard vs Command Line

| Feature | Dashboard | Command Line |
|---------|-----------|--------------|
| **Ease of Use** | ⭐⭐⭐⭐⭐ Drag & drop | ⭐⭐⭐ Type paths |
| **Speed** | ⭐⭐⭐⭐ Click buttons | ⭐⭐⭐⭐⭐ Faster typing (if you know commands) |
| **Validation** | ⭐⭐⭐⭐⭐ Real-time | ⭐⭐ Only on run |
| **History** | ⭐⭐⭐⭐⭐ Built-in | ⭐ Manual tracking |
| **Downloads** | ⭐⭐⭐⭐⭐ One-click | ⭐⭐⭐ Find files manually |
| **Automation** | ⭐⭐ Manual clicks | ⭐⭐⭐⭐⭐ Scriptable |
| **Non-tech Users** | ⭐⭐⭐⭐⭐ Perfect | ⭐ Scary |

**Bottom Line:** Use whichever you prefer! Both produce identical results.

---

## 📞 Support

### Having Issues?

1. **Check validation** - Files must be valid before running
2. **Try CLI** - If dashboard fails, try command line to isolate issue
3. **Check console** - Look at terminal where you ran `streamlit run`
4. **Expand errors** - Click error boxes to see full details

### Common Issues

**Dashboard won't start:**
```bash
pip install streamlit
```

**Files not uploading:**
- Check file size (very large files may timeout)
- Try smaller test file first
- Check file format matches required type

**Forecast fails:**
- Expand error details
- Try same file via command line
- Check that file is valid

---

## 🎯 Best Practices

1. **Test with small files first** - Verify everything works
2. **Check validation before running** - Wait for ✅
3. **Review history regularly** - Track what you've run
4. **Download important results** - Don't rely only on output folder
5. **Update bias monthly** - Use the Update Bias tab

---

## 📚 Documentation

- **STREAMLIT_DASHBOARD_GUIDE.md** - Complete user guide (this file)
- **HOW_TO_UPDATE_BIAS_MONTHLY.md** - Monthly bias update workflow
- **CORRECTED_FORECAST_SUMMARY_FEATURE.md** - Excel summary feature
- **HOW_TO_BIAS_CORRECTION.md** - Full bias correction guide

All accessible from the **Settings** tab!

---

## ✅ Requirements

```bash
# Core forecasting (already installed)
pip install -r requirements.txt

# Dashboard (new - optional)
pip install streamlit
```

That's it! No other dependencies needed.

---

## 🎉 Summary

**The Streamlit dashboard gives you:**

✨ **Beautiful interface** - Modern, professional look  
⚡ **Faster workflow** - Drag, drop, click - done!  
📊 **Better visibility** - See status, history, metrics  
👥 **User-friendly** - Perfect for non-technical users  
🔄 **Fully compatible** - CLI still works exactly the same

**Nothing changes in your existing workflow - this is pure enhancement!**

---

**Start using it today:**

```bash
pip install streamlit
streamlit run forecast_dashboard.py
```

**Your browser opens → Start forecasting! 🚀**
