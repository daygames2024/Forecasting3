"""
Forecast Management Dashboard - Streamlit Interface

This is a user-friendly interface for the forecasting system.
All existing command-line functionality remains unchanged.

To run:
    streamlit run forecast_dashboard.py
"""

import streamlit as st
import pandas as pd
import os
import subprocess
import json
from pathlib import Path
from datetime import datetime
import shutil
import tempfile

# Page configuration
st.set_page_config(
    page_title="Forecast Management Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #366092;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4472C4;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        font-size: 1.1rem;
    }
    /* Auto-fit dataframe text */
    .stDataFrame {
        font-size: 0.85rem;
    }
    .stDataFrame td {
        white-space: normal !important;
        word-wrap: break-word !important;
        max-width: 300px;
    }
    .stDataFrame th {
        font-size: 0.9rem;
        white-space: normal !important;
    }
    /* Ensure dataframes are scrollable */
    .stDataFrame > div {
        overflow-x: auto;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'forecast_history' not in st.session_state:
    st.session_state.forecast_history = []
    # Load history from file if exists
    history_file = Path("output/forecast_history.json")
    if history_file.exists():
        try:
            with open(history_file, 'r') as f:
                st.session_state.forecast_history = json.load(f)
        except:
            pass

if 'last_run_status' not in st.session_state:
    st.session_state.last_run_status = None

# Initialize settings with defaults
if 'settings' not in st.session_state:
    # Try to load saved settings
    settings_file = Path("dashboard_settings.json")
    if settings_file.exists():
        try:
            with open(settings_file, 'r') as f:
                st.session_state.settings = json.load(f)
        except:
            # Default settings if loading fails
            st.session_state.settings = {
                'output_folder': 'output/',
                'default_horizon': 6,
                'default_agg': 'sum',
                'skip_plots': True
            }
    else:
        # Default settings
        st.session_state.settings = {
            'output_folder': 'output/',
            'default_horizon': 6,
            'default_agg': 'sum',
            'skip_plots': True
        }

# Helper functions
def save_history():
    """Save forecast history to JSON file"""
    output_folder = st.session_state.settings.get('output_folder', 'output/') if 'settings' in st.session_state else 'output/'
    history_file = Path(output_folder) / "forecast_history.json"
    history_file.parent.mkdir(exist_ok=True)
    with open(history_file, 'w') as f:
        json.dump(st.session_state.forecast_history, f, indent=2)

def add_to_history(entry):
    """Add a forecast run to history"""
    st.session_state.forecast_history.insert(0, entry)  # Add to beginning
    # Keep only last 50 runs
    st.session_state.forecast_history = st.session_state.forecast_history[:50]
    save_history()

def validate_sales_file(file_path):
    """Validate sales data file"""
    try:
        if str(file_path).endswith('.xlsx'):
            df = pd.read_excel(file_path, nrows=5)
        else:
            df = pd.read_csv(file_path, nrows=5)

        required_cols = ['Date', 'Part_number', 'Value']
        missing_cols = [col for col in required_cols if col not in df.columns]

        if missing_cols:
            return False, f"Missing columns: {', '.join(missing_cols)}"

        return True, f"✅ Valid file ({len(df.columns)} columns detected)"
    except Exception as e:
        return False, f"Error reading file: {str(e)}"

def validate_events_file(file_path):
    """Validate events file"""
    try:
        df = pd.read_csv(file_path, nrows=5)
        required_cols = ['Check', 'Start Date', 'End Date']

        # Check for columns (case-insensitive)
        df.columns = df.columns.str.strip()
        cols_lower = {col.lower(): col for col in df.columns}

        missing = []
        for req in required_cols:
            if req.lower() not in cols_lower:
                missing.append(req)

        if missing:
            return False, f"Missing columns: {', '.join(missing)}"

        return True, f"✅ Valid file ({len(df)} events detected)"
    except Exception as e:
        return False, f"Error reading file: {str(e)}"

def validate_forecast_file(file_path):
    """Validate forecast file"""
    try:
        df = pd.read_csv(file_path, nrows=5)

        # Check for Part_number
        if 'Part_number' not in df.columns:
            return False, "Missing 'Part_number' column"

        # Check for quarter columns (e.g., 25Q1, 25Q2)
        quarter_cols = [col for col in df.columns if len(col) >= 4 and col[0:2].isdigit() and 'Q' in col]

        if not quarter_cols:
            return False, "No quarter columns found (expected format: 25Q1, 25Q2, etc.)"

        return True, f"✅ Valid file ({len(df)} parts, {len(quarter_cols)} quarters)"
    except Exception as e:
        return False, f"Error reading file: {str(e)}"

def get_latest_forecast_summary():
    """Get summary from the most recent forecast"""
    # Get output folder from settings if available
    if 'settings' in st.session_state:
        output_dir = Path(st.session_state.settings.get('output_folder', 'output/'))
    else:
        output_dir = Path("output")


    if not output_dir.exists():
        return None

    # Look for forecast Excel files with multiple patterns
    excel_files = []

    # Pattern 1: forecast_output*.xlsx (standard output)
    excel_files.extend(list(output_dir.glob("*forecast_output*.xlsx")))

    # Pattern 2: Any file with "forecast" in name (but exclude old yearly forecasts)
    for file in output_dir.glob("*forecast*.xlsx"):
        # Exclude yearly forecast files (forecast_2019.xlsx, etc.)
        if not file.stem.startswith("forecast_20"):
            if file not in excel_files:
                excel_files.append(file)

    if not excel_files:
        return None

    # Get most recent file
    latest_file = max(excel_files, key=lambda x: x.stat().st_mtime)

    try:
        # Try to read the summary sheet with different possible names
        sheet_names = ['Forecast_Summary', 'Corrected_Forecast_Summary', 'Summary']

        for sheet_name in sheet_names:
            try:
                df = pd.read_excel(latest_file, sheet_name=sheet_name, header=None)
                return df, latest_file
            except:
                continue

        # If no summary sheet found, return None
        return None
    except:
        return None

def format_file_size(size_bytes):
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

# Sidebar
with st.sidebar:
    st.markdown("## 📊 Forecast Pro")
    st.markdown("**Demand Forecasting Suite**")
    st.markdown("---")

    st.markdown("### 📊 Quick Actions")
    if st.button("🔄 Refresh Dashboard", use_container_width=True):
        st.rerun()

    st.markdown("---")

    st.markdown("### 📁 Output Folder")
    output_path = Path(st.session_state.settings.get('output_folder', 'output/'))
    if output_path.exists():
        files = list(output_path.glob("*"))
        st.metric("Files", len(files))
        if files:
            for f in sorted(files):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.caption(f.name)
                with col2:
                    st.download_button(
                        "⬇️",
                        data=open(f, 'rb').read(),
                        file_name=f.name,
                        key=f"sidebar_dl_{f.name}"
                    )
    else:
        st.info("No output folder yet")

    st.markdown("---")

    st.markdown("### ℹ️ About")
    st.caption("Forecast Management Dashboard v1.0")
    st.caption("Built with Streamlit")
    st.caption("All existing CLI commands still work!")

# Main content
st.markdown('<div class="main-header">📊 Forecast Management Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Streamlined interface for demand forecasting and bias correction</div>', unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Dashboard", 
    "🎯 Create Forecast", 
    "🔄 Update Bias", 
    "⚙️ Settings"
])

# ============================================================================
# TAB 1: DASHBOARD
# ============================================================================
with tab1:
    st.header("📊 Overview")

    # Quick stats
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        total_forecasts = len(st.session_state.forecast_history)
        st.metric("Total Forecasts", total_forecasts)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        if st.session_state.forecast_history:
            last_run = st.session_state.forecast_history[0]
            st.metric("Last Run", last_run.get('date', 'N/A'))
        else:
            st.metric("Last Run", "Never")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        # Bias correction report is always in the central output/ folder
        bias_file = Path("output") / "forecast_accuracy_report.csv"
        st.metric("Bias Correction", "Active ✅" if bias_file.exists() else "Inactive ⚠️")
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        output_folder = Path(st.session_state.settings.get('output_folder', 'output/'))
        output_files = list(output_folder.glob("forecast_output*.csv")) if output_folder.exists() else []
        st.metric("Output Files", len(output_files))
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Latest forecast summary
    st.subheader("📈 Latest Forecast Summary")

    summary_data = get_latest_forecast_summary()
    if summary_data:
        df, file_path = summary_data

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"""
            <div style="background-color: #e3f2fd; padding: 0.75rem; border-radius: 0.5rem; border-left: 4px solid #2196f3;">
                <p style="margin: 0; font-size: 0.85rem; line-height: 1.4;">
                    <strong>📄 File:</strong> {file_path.name}<br>
                    <strong>🕒 Modified:</strong> {datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            if st.download_button(
                "⬇️ Download Excel", 
                data=open(file_path, 'rb').read(),
                file_name=file_path.name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            ):
                st.success("Download started!")

        # Display summary in expandable section
        with st.expander("📋 View Summary Details", expanded=False):
            st.dataframe(df, use_container_width=True, hide_index=True, height=400)
    else:
        st.info("No forecast summaries found. Create your first forecast in the **Create Forecast** tab!")

    st.markdown("---")

    # Recent activity
    col_header1, col_header2 = st.columns([3, 1])

    with col_header1:
        st.subheader("🕒 Recent Activity")

    with col_header2:
        if st.session_state.forecast_history:
            if st.button("🗑️ Clear All", use_container_width=True):
                if st.session_state.get('confirm_clear_dashboard'):
                    st.session_state.forecast_history = []
                    save_history()
                    st.session_state.confirm_clear_dashboard = False
                    st.success("History cleared!")
                    st.rerun()
                else:
                    st.session_state.confirm_clear_dashboard = True
                    st.warning("Click again to confirm")

    if st.session_state.forecast_history:
        recent = st.session_state.forecast_history[:5]

        for idx, run in enumerate(recent):
            # Get the original index in the full history
            original_idx = st.session_state.forecast_history.index(run)

            with st.container():
                col1, col2, col3, col4 = st.columns([2, 2, 0.8, 0.4])

                with col1:
                    st.markdown(f"**{run.get('type', 'Forecast')}**")
                    st.caption(run.get('date', 'Unknown date'))

                with col2:
                    if run.get('status') == 'success':
                        st.success(f"✅ {run.get('message', 'Completed successfully')}")
                    elif run.get('status') == 'error':
                        st.error(f"❌ {run.get('message', 'Failed')}")
                    else:
                        st.warning(f"⚠️ {run.get('message', 'Unknown status')}")

                with col3:
                    if run.get('output_file'):
                        # The stored path is CSV, but we want to prefer Excel if it exists
                        csv_path = Path(run['output_file'])
                        excel_path = Path(str(csv_path).replace('.csv', '.xlsx'))

                        # Prefer Excel (has summary), fallback to CSV
                        download_path = excel_path if excel_path.exists() else csv_path

                        if download_path.exists():
                            # Determine file type and extension
                            file_ext = download_path.suffix.lower()

                            # Set mime type based on extension
                            if file_ext == '.xlsx':
                                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                label = "📥 Excel"
                            elif file_ext == '.csv':
                                mime_type = "text/csv"
                                label = "📥 CSV"
                            else:
                                mime_type = "application/octet-stream"
                                label = "📥"

                            # Create download button
                            st.download_button(
                                label=label,
                                data=open(download_path, 'rb').read(),
                                file_name=download_path.name,
                                mime=mime_type,
                                key=f"dl_recent_{idx}_{run.get('date')}",
                                use_container_width=True,
                                help=f"Download {download_path.name}"
                            )
                        else:
                            st.caption("❌ File deleted")
                    else:
                        st.caption("—")

                with col4:
                    if st.button("🗑️", key=f"delete_dashboard_{original_idx}", help="Delete this entry"):
                        st.session_state.forecast_history.pop(original_idx)
                        save_history()
                        st.rerun()

                st.markdown("---")
    else:
        st.info("No activity yet. Start by creating a forecast!")

# ============================================================================
# TAB 2: CREATE FORECAST
# ============================================================================
with tab2:
    st.header("🎯 Create New Forecast")

    st.markdown("""
    Upload your sales data and optionally an events file to generate demand forecasts.
    The system will automatically apply bias correction if available.
    """)

    st.markdown("---")

    # File uploads
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Sales Data (Required) Ensure Columns and Values are correct")
        sales_file = st.file_uploader(
            "Upload sales data file",
            type=['xlsx', 'csv'],
            help="Excel or CSV file with columns: Date, Part_number, Value",
            key="sales_upload"
        )

        if sales_file:
            # Save to temp file for validation
            temp_sales = Path(tempfile.gettempdir()) / sales_file.name
            with open(temp_sales, 'wb') as f:
                f.write(sales_file.getbuffer())

            valid, message = validate_sales_file(temp_sales)
            if valid:
                st.success(message)

                # Show file info
                st.info(f"📁 **Size:** {format_file_size(sales_file.size)}  \n📄 **Name:** {sales_file.name}")
            else:
                st.error(message)

    with col2:
        st.subheader("📅 Events File (Optional)")
        events_file = st.file_uploader(
            "Upload maintenance events file",
            type=['csv'],
            help="CSV file with columns: Check, Start Date, End Date",
            key="events_upload"
        )

        if events_file:
            # Save to temp file for validation
            temp_events = Path(tempfile.gettempdir()) / events_file.name
            with open(temp_events, 'wb') as f:
                f.write(events_file.getbuffer())

            valid, message = validate_events_file(temp_events)
            if valid:
                st.success(message)
                st.info(f"📁 **Size:** {format_file_size(events_file.size)}  \n📄 **Name:** {events_file.name}")
            else:
                st.error(message)

    st.markdown("---")

    # Correction factors upload
    st.subheader("🔧 Correction Factors (Optional)")
    st.caption("Upload your saved `correction_factors.csv` to apply bias correction to this forecast.")

    correction_file = st.file_uploader(
        "Upload correction factors file",
        type=['csv'],
        help="CSV file previously downloaded after a bias correction run",
        key="correction_upload"
    )

    if correction_file:
        st.success(f"✅ Correction factors loaded — {correction_file.name}")
        st.info(f"📁 **Size:** {format_file_size(correction_file.size)}  \n📄 **Name:** {correction_file.name}")

    st.markdown("---")

    # Advanced options
    with st.expander("⚙️ Advanced Options", expanded=False):
        col1, col2, col3 = st.columns(3)

        with col1:
            horizon = st.number_input("Forecast Horizon (quarters)", min_value=1, max_value=12, value=6)

        with col2:
            aggregation = st.selectbox("Aggregation Method", ["sum", "mean"])

        with col3:
            skip_plots = st.checkbox("Skip Plots (faster)", value=True)

        col1, col2 = st.columns(2)

        with col1:
            fast_mode = st.checkbox("Fast Mode (fewer models)", value=False)

        with col2:
            output_name = st.text_input("Output Filename", value="forecast_output.csv")

    st.markdown("---")

    # Run forecast button
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button("▶️ Run Forecast", type="primary", use_container_width=True):
            if not sales_file:
                st.error("❌ Please upload sales data file!")
            else:
                with st.spinner("🔄 Running forecast... This may take a few minutes."):
                    try:
                        # Save files to input folder
                        input_folder = Path("temp_input")
                        input_folder.mkdir(exist_ok=True)

                        # Save sales file
                        sales_path = input_folder / sales_file.name
                        with open(sales_path, 'wb') as f:
                            f.write(sales_file.getbuffer())

                        # STEP 1: Validate and fix sales data
                        st.info("🔍 Step 1/2: Validating and fixing sales data...")

                        validate_cmd = [
                            sys.executable, "validate_input_data.py",
                            "--sales", str(sales_path),
                            "--fix"
                        ]

                        validate_result = subprocess.run(
                            validate_cmd,
                            capture_output=True,
                            text=True
                        )

                        # Check if validation created a _FIXED file
                        fixed_sales_path = sales_path.parent / f"{sales_path.stem}_FIXED{sales_path.suffix}"

                        if fixed_sales_path.exists():
                            st.success("✅ Sales data validated and fixed!")
                            # Use the fixed file for forecasting
                            final_sales_path = fixed_sales_path

                            # Copy fixed file to output folder for retention (use settings folder)
                            output_dir = Path(st.session_state.settings.get('output_folder', 'output/'))
                            output_dir.mkdir(exist_ok=True)
                            saved_fixed_path = output_dir / fixed_sales_path.name
                            shutil.copy2(fixed_sales_path, saved_fixed_path)
                            st.info(f"💾 Fixed file saved to: {saved_fixed_path}")

                            # Show validation summary in expander
                            with st.expander("📋 View Validation Details", expanded=False):
                                st.code(validate_result.stdout, language="text")
                        elif validate_result.returncode == 0:
                            st.success("✅ Sales data validated (no fixes needed)!")
                            final_sales_path = sales_path
                        else:
                            st.error("❌ Sales data validation failed!")
                            with st.expander("❌ View Validation Errors", expanded=True):
                                st.code(validate_result.stderr if validate_result.stderr else validate_result.stdout, language="text")

                            # Clean up and abort
                            shutil.rmtree(input_folder, ignore_errors=True)
                            st.stop()

                        # STEP 2: Run forecast with validated data
                        st.info("📊 Step 2/2: Running forecast models...")

                        # Get output folder from settings
                        output_folder_path = Path(st.session_state.settings.get('output_folder', 'output/'))
                        output_folder_path.mkdir(parents=True, exist_ok=True)

                        # Save correction factors to output folder if uploaded
                        if correction_file:
                            correction_path = output_folder_path / "correction_factors.csv"
                            with open(correction_path, 'wb') as f:
                                f.write(correction_file.getbuffer())
                            st.info("🔧 Correction factors saved — bias correction will be applied automatically.")

                        # Build command
                        cmd = [
                            sys.executable, "-m", "src.app",
                            "--input", str(final_sales_path),
                            "--horizon", str(horizon),
                            "--agg", aggregation,
                            "--outdir", str(output_folder_path),
                            "--outfile", output_name
                        ]

                        # If using fixed Excel file, specify the sheet name
                        if final_sales_path.suffix == '.xlsx' and final_sales_path != sales_path:
                            cmd.extend(["--sheet-name", "Sales_Data"])

                        if events_file:
                            events_path = input_folder / events_file.name
                            with open(events_path, 'wb') as f:
                                f.write(events_file.getbuffer())
                            cmd.extend(["--events-file", str(events_path)])

                        if skip_plots:
                            cmd.append("--skip-plots")

                        if fast_mode:
                            cmd.append("--fast-mode")

                        # Run forecast
                        result = subprocess.run(
                            cmd,
                            capture_output=True,
                            text=True
                        )

                        # Clean up temp folder
                        shutil.rmtree(input_folder, ignore_errors=True)

                        if result.returncode == 0:
                            st.success("✅ Forecast completed successfully!")

                            # Get output folder from settings
                            output_folder_path = Path(st.session_state.settings.get('output_folder', 'output/'))

                            # Add to history
                            add_to_history({
                                'type': 'Forecast',
                                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                'status': 'success',
                                'message': f'{sales_file.name} processed',
                                'output_file': str(output_folder_path / output_name),
                                'params': {
                                    'horizon': horizon,
                                    'aggregation': aggregation,
                                    'events': events_file.name if events_file else None
                                }
                            })

                            # Show output
                            with st.expander("📋 View Console Output", expanded=False):
                                st.code(result.stdout, language="text")

                            # Show download links
                            st.markdown("### 📥 Download Results")

                            output_dir = Path(st.session_state.settings.get('output_folder', 'output/'))
                            csv_file = output_dir / output_name
                            excel_file = output_dir / output_name.replace('.csv', '.xlsx')
                            corrected_csv = output_dir / output_name.replace('.csv', '_Corrected.csv')
                            corrected_excel = output_dir / output_name.replace('.csv', '_Corrected.xlsx')

                            # Check if fixed file was saved
                            fixed_file_in_output = None
                            for f in output_dir.glob("*_FIXED.*"):
                                if f.stat().st_mtime > (datetime.now().timestamp() - 300):  # Within last 5 minutes
                                    fixed_file_in_output = f
                                    break

                            # Show fixed file download if it exists
                            if fixed_file_in_output:
                                st.markdown("#### 🔧 Validated Data")
                                col_fixed = st.columns(1)[0]
                                with col_fixed:
                                    st.download_button(
                                        "⬇️ Download Fixed Sales Data",
                                        data=open(fixed_file_in_output, 'rb').read(),
                                        file_name=fixed_file_in_output.name,
                                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" if fixed_file_in_output.suffix == '.xlsx' else "text/csv",
                                        use_container_width=True
                                    )
                                st.caption("💡 Use this cleaned file for future forecasts to skip validation")

                            st.markdown("#### 📊 Forecast Results")

                            col1, col2 = st.columns(2)

                            with col1:
                                if csv_file.exists():
                                    st.download_button(
                                        "⬇️ Original Forecast (CSV)",
                                        data=open(csv_file, 'rb').read(),
                                        file_name=csv_file.name,
                                        use_container_width=True
                                    )

                                if excel_file.exists():
                                    st.download_button(
                                        "⬇️ Original Forecast (Excel)",
                                        data=open(excel_file, 'rb').read(),
                                        file_name=excel_file.name,
                                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                        use_container_width=True
                                    )

                            with col2:
                                if corrected_csv.exists():
                                    st.download_button(
                                        "⬇️ Corrected Forecast (CSV)",
                                        data=open(corrected_csv, 'rb').read(),
                                        file_name=corrected_csv.name,
                                        use_container_width=True
                                    )

                                if corrected_excel.exists():
                                    st.download_button(
                                        "⬇️ Corrected Forecast (Excel) ⭐",
                                        data=open(corrected_excel, 'rb').read(),
                                        file_name=corrected_excel.name,
                                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                        use_container_width=True
                                    )

                            st.balloons()

                        else:
                            st.error("❌ Forecast failed!")

                            # Add to history
                            add_to_history({
                                'type': 'Forecast',
                                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                'status': 'error',
                                'message': 'Forecast failed - see error details',
                                'params': {
                                    'horizon': horizon,
                                    'aggregation': aggregation
                                }
                            })

                            with st.expander("❌ View Error Details", expanded=True):
                                st.code(result.stderr if result.stderr else result.stdout, language="text")

                    except Exception as e:
                        st.error(f"❌ Error running forecast: {str(e)}")

                        # Add to history
                        add_to_history({
                            'type': 'Forecast',
                            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'status': 'error',
                            'message': str(e)
                        })

# ============================================================================
# TAB 3: UPDATE BIAS CORRECTION
# ============================================================================
with tab3:
    st.header("🔄 Update Bias Correction")

    st.markdown("""
    Compare an old forecast with actual sales data to update bias correction factors.
    This should be done monthly as new actual sales data becomes available.
    """)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Old Forecast (Required)")
        old_forecast_file = st.file_uploader(
            "Upload old forecast CSV",
            type=['csv'],
            help="Forecast file from 1-3 months ago with quarter columns (25Q1, 25Q2, etc.)",
            key="old_forecast_upload"
        )

        if old_forecast_file:
            temp_forecast = Path(tempfile.gettempdir()) / old_forecast_file.name
            with open(temp_forecast, 'wb') as f:
                f.write(old_forecast_file.getbuffer())

            valid, message = validate_forecast_file(temp_forecast)
            if valid:
                st.success(message)
                st.info(f"📁 **Size:** {format_file_size(old_forecast_file.size)}  \n📄 **Name:** {old_forecast_file.name}")
            else:
                st.error(message)

    with col2:
        st.subheader("📈 Actual Sales (Required)")
        actual_sales_file = st.file_uploader(
            "Upload actual sales data",
            type=['xlsx', 'csv'],
            help="Sales data covering the period that was forecasted",
            key="actual_sales_upload"
        )

        if actual_sales_file:
            temp_actuals = Path(tempfile.gettempdir()) / actual_sales_file.name
            with open(temp_actuals, 'wb') as f:
                f.write(actual_sales_file.getbuffer())

            valid, message = validate_sales_file(temp_actuals)
            if valid:
                st.success(message)
                st.info(f"📁 **Size:** {format_file_size(actual_sales_file.size)}  \n📄 **Name:** {actual_sales_file.name}")
            else:
                st.error(message)

    st.markdown("---")

    # Run update button
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button("🔄 Update Bias Correction", type="primary", use_container_width=True):
            if not old_forecast_file or not actual_sales_file:
                st.error("❌ Please upload both old forecast and actual sales files!")
            else:
                with st.spinner("🔄 Updating bias correction... This may take a minute."):
                    try:
                        # Save files to temp folder
                        temp_folder = Path("temp_bias")
                        temp_folder.mkdir(exist_ok=True)

                        # Save old forecast
                        forecast_path = temp_folder / old_forecast_file.name
                        with open(forecast_path, 'wb') as f:
                            f.write(old_forecast_file.getbuffer())

                        # Save actual sales
                        actuals_path = temp_folder / actual_sales_file.name
                        with open(actuals_path, 'wb') as f:
                            f.write(actual_sales_file.getbuffer())

                        # Build command
                        cmd = [
                            sys.executable, "fix_forecast_comparison.py",
                            "--old-forecast", str(forecast_path),
                            "--actual-sales", str(actuals_path)
                        ]

                        # Run comparison
                        result = subprocess.run(
                            cmd,
                            capture_output=True,
                            text=True
                        )

                        # Clean up temp folder
                        shutil.rmtree(temp_folder, ignore_errors=True)

                        if result.returncode == 0:
                            st.success("✅ Bias correction updated successfully!")

                            # Add to history
                            add_to_history({
                                'type': 'Bias Update',
                                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                'status': 'success',
                                'message': f'Updated from {old_forecast_file.name}',
                                'output_file': str(Path('output') / 'forecast_accuracy_report.csv')
                            })

                            # Show output
                            with st.expander("📋 View Analysis Results", expanded=True):
                                st.code(result.stdout, language="text")

                            # Show download links
                            st.markdown("### 📥 Download Analysis")

                            # Bias correction reports are always saved to central output/ folder
                            output_dir = Path("output")
                            accuracy_csv = output_dir / "forecast_accuracy_report.csv"
                            accuracy_excel = output_dir / "forecast_accuracy_report_analysis.xlsx"

                            col1, col2 = st.columns(2)

                            with col1:
                                if accuracy_csv.exists():
                                    st.download_button(
                                        "⬇️ Accuracy Report (CSV)",
                                        data=open(accuracy_csv, 'rb').read(),
                                        file_name=accuracy_csv.name,
                                        use_container_width=True
                                    )

                            with col2:
                                if accuracy_excel.exists():
                                    st.download_button(
                                        "⬇️ Detailed Analysis (Excel)",
                                        data=open(accuracy_excel, 'rb').read(),
                                        file_name=accuracy_excel.name,
                                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                        use_container_width=True
                                    )

                            st.info("💡 **Next Steps:** Your next forecast will automatically use these updated correction factors!")

                        else:
                            st.error("❌ Bias correction update failed!")

                            # Add to history
                            add_to_history({
                                'type': 'Bias Update',
                                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                'status': 'error',
                                'message': 'Update failed - see error details'
                            })

                            with st.expander("❌ View Error Details", expanded=True):
                                st.code(result.stderr if result.stderr else result.stdout, language="text")

                    except Exception as e:
                        st.error(f"❌ Error updating bias correction: {str(e)}")

                        # Add to history
                        add_to_history({
                            'type': 'Bias Update',
                            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'status': 'error',
                            'message': str(e)
                        })

    st.markdown("---")

    # Current bias status
    st.subheader("📊 Current Bias Correction Status")

    output_folder = Path(st.session_state.settings.get('output_folder', 'output/'))
    accuracy_file = output_folder / "forecast_accuracy_report.csv"
    if accuracy_file.exists():
        try:
            df = pd.read_csv(accuracy_file)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Comparisons", len(df))

            with col2:
                avg_error = df['Percentage_Error'].mean()
                st.metric("Avg Error", f"{avg_error:.1f}%")

            with col3:
                median_error = df['Percentage_Error'].median()
                st.metric("Median Error", f"{median_error:.1f}%")

            with col4:
                over_count = (df['Error'] > 0).sum()
                under_count = (df['Error'] < 0).sum()
                if over_count > under_count * 1.2:
                    bias_type = "Over-forecasting"
                elif under_count > over_count * 1.2:
                    bias_type = "Under-forecasting"
                else:
                    bias_type = "Balanced"
                st.metric("Bias Type", bias_type)

            with st.expander("📋 View Accuracy Data", expanded=False):
                st.dataframe(df.head(20), use_container_width=True)

        except Exception as e:
            st.error(f"Error reading accuracy report: {str(e)}")
    else:
        st.warning("⚠️ No bias correction data available. Upload files above to create your first accuracy report.")

# ============================================================================
# TAB 4: SETTINGS
# ============================================================================
with tab4:
    st.header("⚙️ Settings & Configuration")

    st.markdown("### 📁 Default Folders")

    st.info("""
    ℹ️ **Important:** The **bias correction report** (`forecast_accuracy_report.csv`) is always stored in the central `output/` folder, 
    regardless of your custom output folder setting. This allows all forecasts to share the same correction factors.

    Your custom output folder setting controls where **forecast files** are saved.
    """)

    col1, col2 = st.columns(2)

    with col1:
        input_folder_setting = st.text_input("Default Input Folder", value="data/", key="input_folder_setting")
        output_folder_setting = st.text_input("Default Output Folder", value=st.session_state.settings.get('output_folder', 'output/'), key="output_folder_setting")

    with col2:
        plots_folder_setting = st.text_input("Plots Folder", value="output/plots/", key="plots_folder_setting")

    st.markdown("---")

    st.markdown("### 🔧 Default Forecast Parameters")

    col1, col2, col3 = st.columns(3)

    with col1:
        default_horizon = st.number_input("Default Horizon", min_value=1, max_value=12, value=st.session_state.settings.get('default_horizon', 6), key="default_horizon_setting")

    with col2:
        default_agg = st.selectbox("Default Aggregation", ["sum", "mean"], index=0 if st.session_state.settings.get('default_agg', 'sum') == 'sum' else 1, key="default_agg_setting")

    with col3:
        default_skip_plots = st.checkbox("Skip Plots by Default", value=st.session_state.settings.get('skip_plots', True), key="default_skip_plots_setting")

    st.markdown("---")

    st.markdown("### 📊 Dashboard Preferences")

    col1, col2 = st.columns(2)

    with col1:
        max_history = st.number_input("Max History Items", min_value=10, max_value=500, value=50, key="max_history_setting")

    with col2:
        auto_refresh = st.checkbox("Auto-refresh dashboard", value=False, key="auto_refresh_setting")

    st.markdown("---")

    if st.button("💾 Save Settings", type="primary"):
        # Save settings to session state
        st.session_state.settings = {
            'output_folder': output_folder_setting.rstrip('/') + '/',
            'default_horizon': default_horizon,
            'default_agg': default_agg,
            'skip_plots': default_skip_plots
        }

        # Save to file for persistence
        settings_file = Path("dashboard_settings.json")
        try:
            with open(settings_file, 'w') as f:
                json.dump(st.session_state.settings, f, indent=2)
            st.success("✅ Settings saved successfully!")
        except Exception as e:
            st.error(f"❌ Error saving settings: {e}")

    st.markdown("---")

    st.markdown("### ℹ️ System Information")

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"""
        **Python Version:** {subprocess.run(['python', '--version'], capture_output=True, text=True).stdout.strip()}

        **Working Directory:** {Path.cwd()}

        **Streamlit Version:** {st.__version__}
        """)

    with col2:
        # Check for key dependencies
        try:
            import openpyxl
            excel_status = "✅ Installed"
        except:
            excel_status = "❌ Not installed"

        st.info(f"""
        **openpyxl (Excel support):** {excel_status}

        **Output folder exists:** {'✅ Yes' if Path('output').exists() else '❌ No'}

        **Bias correction active:** {'✅ Yes' if Path('output/forecast_accuracy_report.csv').exists() else '❌ No'}
        """)

        st.markdown("### 📚 Documentation")

    def show_doc(doc_file, description, key_prefix):
        if Path(doc_file).exists():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"📄 **{doc_file}** - {description}")
            with col2:
                if st.button("📖 Open", key=f"{key_prefix}_{doc_file}"):
                    toggle_key = f"show_doc_{doc_file}"
                    st.session_state[toggle_key] = not st.session_state.get(toggle_key, False)
            if st.session_state.get(f"show_doc_{doc_file}", False):
                with st.expander(f"📖 {doc_file}", expanded=True):
                    st.markdown(Path(doc_file).read_text(encoding="utf-8"))

    st.markdown("#### Understanding Forecasts")
    for doc_file, description in [
        ("FORECAST_PERCENTILES_GUIDE.md", "P10, P50, P90 explained - Which to use?"),
        ("BIAS_CORRECTION_LOCATION.md", "Where bias correction files are stored"),
    ]:
        show_doc(doc_file, description, "concepts")

    st.markdown("#### Forecasting Guides")
    for doc_file, description in [
        ("HOW_TO_CREATE_FORECAST.md", "Creating forecasts"),
        ("HOW_TO_UPDATE_BIAS_MONTHLY.md", "Monthly bias updates"),
        ("HOW_TO_BIAS_CORRECTION.md", "Bias correction guide"),
        ("HOW_TO_CREATE_BIAS_CORRECTION.md", "5-iteration bias creation"),
        ("CORRECTED_FORECAST_SUMMARY_FEATURE.md", "Summary sheet feature"),
    ]:
        show_doc(doc_file, description, "forecast")

    st.markdown("#### Dashboard Guides")
    for doc_file, description in [
        ("STREAMLIT_DASHBOARD_README.md", "Dashboard overview & features"),
        ("STREAMLIT_DASHBOARD_GUIDE.md", "Complete dashboard user guide"),
        ("DASHBOARD_QUICK_REFERENCE.md", "Quick reference card"),
    ]:
        show_doc(doc_file, description, "dashboard")



# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p>Forecast Management Dashboard v1.0 | Built with ❤️ using Streamlit</p>
    <p>💡 <b>Pro Tip:</b> All command-line functionality still works! This is just a convenient interface.</p>
</div>
""", unsafe_allow_html=True)
