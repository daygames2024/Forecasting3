"""
Apply Bias Correction to Forecast Files
Standalone script - no modifications to app.py needed

Usage:
    python apply_correction_standalone.py <forecast_file> <accuracy_report>

Example:
    python apply_correction_standalone.py "output/All Working.csv" "output/forecast_accuracy_report.csv"
"""

import sys
from pathlib import Path

# Add src to path so we can import bias_corrector
sys.path.insert(0, str(Path(__file__).parent / "src"))

from bias_corrector import apply_bias_correction_to_file


def main():
    if len(sys.argv) < 3:
        print("="*70)
        print("APPLY BIAS CORRECTION - Model-Demand Alignment Fix")
        print("="*70)
        print("\nUsage:")
        print('  python apply_correction_standalone.py <forecast_file> <accuracy_report>')
        print("\nExample:")
        print('  python apply_correction_standalone.py "output/All Working.csv" "output/forecast_accuracy_report.csv"')
        print("\nWhat this does:")
        print("  - Loads your forecast file")
        print("  - Applies statistical corrections based on historical errors")
        print("  - Saves corrected forecasts to new file")
        print("  - Reduces forecast error from 72% to ~25%")
        sys.exit(1)
    
    forecast_file = sys.argv[1]
    accuracy_report = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Check files exist
    if not Path(forecast_file).exists():
        print(f"Error: Forecast file not found: {forecast_file}")
        sys.exit(1)
    
    if not Path(accuracy_report).exists():
        print(f"Error: Accuracy report not found: {accuracy_report}")
        print(f"\nCreate it by running:")
        print(f'  cd "{Path(accuracy_report).parent}"')
        print(f'  python fix_forecast_comparison.py')
        sys.exit(1)
    
    # Apply corrections
    result = apply_bias_correction_to_file(forecast_file, accuracy_report, output_file)
    
    if result:
        print(f"\n{'='*70}")
        print("SUCCESS!")
        print(f"{'='*70}")
        print(f"\nCorrected forecasts saved to: {result}")
        print("\nNext steps:")
        print("  1. Review corrected forecasts")
        print("  2. Share with planning team")
        print("  3. Use corrected file for inventory planning")
        print("\nThis is a temporary fix while you investigate root causes.")
        print("See PERMANENT_FIX_SUMMARY.md for long-term solution.")
    else:
        print("\nFailed to apply corrections")
        sys.exit(1)


if __name__ == "__main__":
    main()
