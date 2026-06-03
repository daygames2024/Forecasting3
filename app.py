"""
Entry point for Streamlit Cloud deployment.
Redirects execution to forecast_dashboard.py
"""

import runpy
runpy.run_path("forecast_dashboard.py", run_name="__main__")
