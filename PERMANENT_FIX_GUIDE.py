"""
PERMANENT FIX FOR FORECASTING PROJECT - Model-Demand Alignment

This document outlines the permanent solution to fix the systematic
under-forecasting issue (72% average error, 17-27% too low by quarter).

Current Status:
- ✅ Bias correction module created (src/bias_corrector.py)
- ✅ Temporary corrections applied
- ⚠️ Root cause not yet addressed

Permanent Fix: 3-Phase Approach
"""

# ==============================================================================
# PHASE 1: INTEGRATE BIAS CORRECTION INTO AUTOMATED WORKFLOW
# ==============================================================================

"""
Short-term fix while investigating root cause.

STEP 1A: Add to app.py main() function
Location: End of main() function, after forecast CSV is written
"""

# Add this at the end of main() in app.py (around line 600+)
def main():
    # ... existing forecast generation code ...
    
    # Write forecasts to CSV
    forecast_file = Path(args.outdir) / args.outfile
    pd.DataFrame([res]).to_csv(forecast_file, mode='a', header=(i==0), index=False)
    
    # ============ NEW: AUTO-APPLY BIAS CORRECTION ============
    # Check if accuracy report exists
    accuracy_report = Path(args.outdir) / "forecast_accuracy_report.csv"
    
    if accuracy_report.exists():
        print("\n[Bias Correction] Applying model-demand alignment fix...")
        from .bias_corrector import apply_bias_correction_to_file
        
        corrected_file = apply_bias_correction_to_file(
            str(forecast_file),
            str(accuracy_report),
            output_file=str(Path(args.outdir) / f"{args.outfile.replace('.csv', '_Corrected.csv')}")
        )
        
        if corrected_file:
            print(f"[Bias Correction] ✓ Corrected forecasts saved to: {corrected_file}")
        else:
            print("[Bias Correction] ✗ Correction failed - using uncorrected forecasts")
    else:
        print("\n[Bias Correction] No accuracy report found - skipping correction")
        print(f"   Create one by running: python fix_forecast_comparison.py")
    # =========================================================


# ==============================================================================
# PHASE 2: INVESTIGATE ROOT CAUSES (PERMANENT FIX)
# ==============================================================================

"""
Your forecasts are systematically low because of model-demand misalignment.
Here's how to find and fix the root cause:
"""

# ROOT CAUSE 1: Input Data Quality
"""
PROBLEM: Models using wrong historical baseline

INVESTIGATE:
1. What historical period are models trained on?
   - Pre-COVID (2019-2020)? Market has changed!
   - Only looking at past 12 months? Missing long-term trends!

2. Are models seeing recent demand patterns?
   - Check: What's the latest date in training data?
   - Compare: 2024 sales vs historical average
   
FIX:
- Update training data to include recent periods (2023-2024)
- Weight recent data more heavily
- Remove outdated pre-COVID patterns
"""

# Example diagnostic script
def diagnose_input_data():
    """
    Run this to check your training data quality
    """
    import pandas as pd
    
    # Load your sales data
    df = pd.read_csv("output/2 year forecast verification data.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    
    print("=== INPUT DATA DIAGNOSTICS ===")
    print(f"\nDate range: {df['Date'].min()} to {df['Date'].max()}")
    
    # Check if data is recent
    latest_date = df['Date'].max()
    months_old = (pd.Timestamp.now() - latest_date).days / 30
    
    if months_old > 6:
        print(f"⚠️ WARNING: Data is {months_old:.0f} months old!")
        print("   Models can't see recent demand patterns")
    
    # Check for growth trends
    df['Year'] = df['Date'].dt.year
    yearly_sales = df.groupby('Year')['Value'].sum()
    
    print("\nYearly Sales Trends:")
    for year, sales in yearly_sales.items():
        print(f"  {year}: {sales:,.0f}")
    
    # Calculate growth rate
    if len(yearly_sales) > 1:
        recent_growth = (yearly_sales.iloc[-1] - yearly_sales.iloc[-2]) / yearly_sales.iloc[-2] * 100
        print(f"\nYoY Growth: {recent_growth:+.1f}%")
        
        if abs(recent_growth) > 20:
            print(f"⚠️ CRITICAL: Market changed significantly!")
            print(f"   Your models may be using outdated baseline assumptions")


# ROOT CAUSE 2: Model Assumptions
"""
PROBLEM: Models assume stable demand, but market is volatile

INVESTIGATE:
1. Check your forecaster.py - which models are being used?
   - Simple ETS? Can't handle volatility
   - ARIMA? Assumes stationary data
   - Prophet? Better for trend/seasonality
   
2. Are models trained per-part or globally?
   - Low-volume parts need different models than high-volume
   
FIX:
- Segment products by behavior (ABC analysis)
- Use different models for different segments:
  * A-items (high volume): Prophet, SARIMAX
  * B-items (medium): ETS with trend
  * C-items (low/intermittent): Croston's method, simple mean
"""

# Example: Segment-specific models
def recommend_model_by_segment(part_data):
    """
    Recommend forecasting model based on part behavior
    """
    volume = part_data['Value'].sum()
    cv = part_data['Value'].std() / (part_data['Value'].mean() + 1e-6)  # coefficient of variation
    zero_ratio = (part_data['Value'] == 0).sum() / len(part_data)
    
    if volume > 10000 and cv < 1.0:
        return "Prophet"  # High-volume stable
    elif volume > 1000 and zero_ratio < 0.3:
        return "SARIMAX"  # Medium-volume regular
    elif zero_ratio > 0.4:
        return "Croston"  # Intermittent demand
    else:
        return "Rolling_Mean"  # Low-volume volatile


# ROOT CAUSE 3: Missing Demand Signals
"""
PROBLEM: Models don't capture all demand drivers

INVESTIGATE:
1. Seasonality captured?
   - Check if forecasts drop in slow quarters
   
2. Promotions/Events tracked?
   - Are there sales spikes models don't expect?
   
3. External factors?
   - Competitor actions, market trends, economic indicators
   
FIX:
- Add seasonal decomposition
- Include promotion calendar as feature
- Use Prophet with custom regressors for external factors
"""

# Example: Add seasonality features
def add_demand_features(df):
    """
    Engineer features that capture demand patterns
    """
    df['Quarter'] = df['Date'].dt.quarter
    df['Month'] = df['Date'].dt.month
    df['DayOfWeek'] = df['Date'].dt.dayofweek
    
    # Seasonality indicators
    df['Is_Q4'] = (df['Quarter'] == 4).astype(int)  # Holiday season
    df['Is_Summer'] = df['Month'].isin([6,7,8]).astype(int)
    
    # Trend features
    df['Days_Since_Start'] = (df['Date'] - df['Date'].min()).dt.days
    
    return df


# ==============================================================================
# PHASE 3: IMPLEMENT ADAPTIVE FORECASTING (LONG-TERM)
# ==============================================================================

"""
Replace static models with adaptive system that learns from errors
"""

# STEP 3A: Continuous Monitoring
def setup_forecast_monitoring():
    """
    Track forecast accuracy over time and auto-adjust
    """
    import pandas as pd
    from pathlib import Path
    
    accuracy_log = Path("output/forecast_accuracy_history.csv")
    
    # Log format: Date, Quarter, Avg_Error, Bias_Type, Correction_Applied
    
    if not accuracy_log.exists():
        pd.DataFrame(columns=[
            'Analysis_Date', 'Quarter', 'Median_Error_Pct', 
            'Bias_Type', 'Correction_Factor', 'Sample_Count'
        ]).to_csv(accuracy_log, index=False)
    
    print(f"[Monitoring] Accuracy tracking enabled: {accuracy_log}")


# STEP 3B: Quarterly Recalibration
"""
Every quarter:
1. Run fix_forecast_comparison.py with latest actual data
2. Calculate new correction factors
3. Update bias_corrector.py
4. Retrain models with updated data
5. Compare corrected vs uncorrected accuracy

AUTOMATE THIS:
- Schedule job to run on first day of each quarter
- Email report to planning team
- Flag if bias >15% (needs investigation)
"""


# STEP 3C: Model Selection Logic (Advanced)
"""
Instead of one-size-fits-all, dynamically choose model per part
"""

def adaptive_forecast_selection(part_history, horizon=6):
    """
    Choose best forecasting method based on part characteristics
    """
    from src.forecaster import select_and_forecast
    
    # Assess part behavior
    volume = part_history['Value'].sum()
    volatility = part_history['Value'].std() / (part_history['Value'].mean() + 1e-6)
    intermittent = (part_history['Value'] == 0).sum() / len(part_history)
    
    # Decision tree for model selection
    if intermittent > 0.5:
        # Intermittent demand - use Croston's method
        method = "croston"
    elif volume < 100 and volatility > 1.5:
        # Low-volume volatile - use conservative estimate
        method = "percentile_75"  # Use 75th percentile of history
    elif volume > 5000 and volatility < 0.5:
        # High-volume stable - use Prophet
        method = "prophet"
    else:
        # Default to your existing method
        method = "auto"  # Your current select_and_forecast logic
    
    print(f"[Adaptive] Selected {method} for part (vol={volume:.0f}, cv={volatility:.2f}, intermittent={intermittent:.1%})")
    
    return select_and_forecast(part_history, horizon, method=method)


# ==============================================================================
# SUMMARY: ACTION PLAN
# ==============================================================================

"""
IMMEDIATE (This Week):
✓ Integrate bias_corrector.py into app.py (Phase 1)
✓ Apply corrections to current forecasts
✓ Share corrected forecasts with planning team

SHORT-TERM (This Month):
□ Run diagnose_input_data() to check training data quality
□ Review recent vs historical sales patterns
□ Update training data to include latest quarters
□ Retrain models with updated data

MID-TERM (This Quarter):
□ Implement segment-specific models (A/B/C analysis)
□ Add seasonality and promotion features
□ Test adaptive model selection on pilot segment
□ Set up quarterly accuracy monitoring

LONG-TERM (Next 6 Months):
□ Fully automated adaptive forecasting system
□ Continuous learning from forecast errors
□ Integration with inventory planning system
□ Executive dashboard for forecast accuracy tracking

GOAL:
Reduce average forecast error from 72% to <25% within 3 months
Achieve sustainable <15% error through continuous improvement
"""

# ==============================================================================
# QUICK START: Apply Phase 1 Now
# ==============================================================================

"""
RUN THIS NOW to integrate bias correction:

1. Open: C:\Projects\Forecasting3\src\app.py
2. Find: The end of main() function (around line 600+)
3. Add: The bias correction code from Phase 1 above
4. Save and test:
   
   cd C:\Projects\Forecasting3
   python -m src.app --input "Data/your_sales_data.xlsx" --outfile "forecast_output.csv"
   
5. Verify:
   - forecast_output.csv (original)
   - forecast_output_Corrected.csv (bias-corrected)

THAT'S IT! You now have automated bias correction while you work on root cause.
"""
