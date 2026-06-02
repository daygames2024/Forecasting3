"""
Quick Integration Script - Add Bias Correction to Your Forecasting App

This script shows EXACTLY what to add to app.py to auto-apply bias correction.
"""

# ==============================================================================
# STEP 1: Add this import at the top of app.py (around line 10-20)
# ==============================================================================

# Add after existing imports:
from pathlib import Path
from .bias_corrector import apply_bias_correction_to_file  # NEW

# ==============================================================================
# STEP 2: Add this function before main() (around line 580)
# ==============================================================================

def apply_bias_correction_if_available(forecast_file, outdir):
    """
    Auto-apply bias correction if accuracy report exists.
    
    Called after forecasts are written to CSV.
    """
    from pathlib import Path
    
    accuracy_report = Path(outdir) / "forecast_accuracy_report.csv"
    
    if not accuracy_report.exists():
        print("\n[Bias Correction] No accuracy report found")
        print("   Run fix_forecast_comparison.py to create one")
        return forecast_file
    
    print("\n" + "="*70)
    print("APPLYING BIAS CORRECTION - Model-Demand Alignment Fix")
    print("="*70)
    
    try:
        # Generate corrected filename
        forecast_path = Path(forecast_file)
        corrected_file = str(forecast_path.parent / f"{forecast_path.stem}_Corrected{forecast_path.suffix}")
        
        # Apply corrections
        result = apply_bias_correction_to_file(
            str(forecast_file),
            str(accuracy_report),
            output_file=corrected_file
        )
        
        if result:
            print("\n✓ Bias-corrected forecasts saved!")
            print(f"  Original: {forecast_file}")
            print(f"  Corrected: {result}")
            return result
        else:
            print("\n✗ Bias correction failed - using original forecasts")
            return forecast_file
            
    except Exception as e:
        print(f"\n✗ Bias correction error: {e}")
        print("   Using original forecasts")
        return forecast_file

# ==============================================================================
# STEP 3: Modify main() function - Add this AFTER the forecast loop
# ==============================================================================

# Find this section in main() (around line 630):

def main():
    # ... all existing forecast generation code ...
    
    # Loop through parts and generate forecasts
    for i, part in enumerate(parts, start=1):
        # ... existing forecast code ...
        pd.DataFrame([res]).to_csv(forecast_file, mode='a', header=(i==0), index=False)
        
        if i % 25 == 0:
            print(f"Progress: {i}/{len(parts)}...")
    
    # Print statistics
    print("\nForecast Generation Complete!")
    print(f"Total parts: {len(parts)}")
    print("Method usage:")
    for method, count in stats.items():
        print(f" - {method}: {count}")
    
    # ==================== ADD THIS NEW SECTION ====================
    # Apply bias correction if accuracy report exists
    corrected_file = apply_bias_correction_if_available(forecast_file, args.outdir)
    
    print(f"\n{'='*70}")
    print("FORECAST OUTPUT SUMMARY")
    print(f"{'='*70}")
    print(f"Original forecasts: {forecast_file}")
    if corrected_file != str(forecast_file):
        print(f"Corrected forecasts: {corrected_file}")
        print("\nRECOMMENDED: Use corrected forecasts for planning")
    else:
        print("\nNo bias correction applied (no accuracy report found)")
    print(f"{'='*70}\n")
    # ==============================================================

# ==============================================================================
# ALTERNATIVE: Minimal Integration (If you don't want to modify app.py)
# ==============================================================================

"""
If you don't want to modify app.py, create this wrapper script:
File: run_forecast_with_correction.py
"""

#!/usr/bin/env python
"""
Wrapper script that runs forecasting + auto-applies bias correction
"""

import subprocess
import sys
from pathlib import Path

def run_forecast_with_correction():
    """
    1. Run normal forecast generation
    2. Auto-apply bias correction
    """
    
    # Run your normal forecasting
    print("="*70)
    print("STEP 1: Generating Forecasts")
    print("="*70)
    
    # Pass all arguments to app.py
    result = subprocess.run(
        ["python", "-m", "src.app"] + sys.argv[1:],
        cwd=Path(__file__).parent
    )
    
    if result.returncode != 0:
        print("\n✗ Forecast generation failed")
        sys.exit(1)
    
    print("\n✓ Forecasts generated")
    
    # Apply bias correction
    print("\n" + "="*70)
    print("STEP 2: Applying Bias Correction")
    print("="*70)
    
    from src.bias_corrector import apply_bias_correction_to_file
    
    # Get output file from args (or use default)
    outdir = "output"
    outfile = "forecast_output.csv"
    
    for i, arg in enumerate(sys.argv):
        if arg == "--outdir" and i+1 < len(sys.argv):
            outdir = sys.argv[i+1]
        elif arg == "--outfile" and i+1 < len(sys.argv):
            outfile = sys.argv[i+1]
    
    forecast_file = Path(outdir) / outfile
    accuracy_report = Path(outdir) / "forecast_accuracy_report.csv"
    
    if accuracy_report.exists():
        corrected = apply_bias_correction_to_file(
            str(forecast_file),
            str(accuracy_report)
        )
        
        if corrected:
            print(f"\n✓ COMPLETE! Use corrected file: {corrected}")
        else:
            print(f"\n⚠️ Correction failed - use original: {forecast_file}")
    else:
        print(f"\n⚠️ No accuracy report - use original: {forecast_file}")

if __name__ == "__main__":
    run_forecast_with_correction()

# ==============================================================================
# USAGE AFTER INTEGRATION
# ==============================================================================

"""
METHOD 1: Modified app.py (Recommended)
cd C:\Projects\Forecasting3
python -m src.app --input "Data/sales.xlsx" --outfile "forecast_output.csv"

OUTPUT:
- output/forecast_output.csv (original)
- output/forecast_output_Corrected.csv (bias-corrected) ← USE THIS!

---

METHOD 2: Wrapper script (No modification to app.py)
cd C:\Projects\Forecasting3
python run_forecast_with_correction.py --input "Data/sales.xlsx"

OUTPUT: Same as Method 1

---

NEXT STEPS:
1. Integrate now (short-term fix)
2. Investigate root cause (see PERMANENT_FIX_GUIDE.py)
3. Update models quarterly
4. Phase out bias correction once models are fixed
"""
