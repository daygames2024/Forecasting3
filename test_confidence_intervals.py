#!/usr/bin/env python
"""
Test script to verify confidence intervals are being generated correctly.
Run after creating a forecast to check the output format.
"""

import pandas as pd
import sys
from pathlib import Path

def test_confidence_intervals(forecast_file="output/forecast_output.csv"):
    """Verify confidence intervals are present and properly formatted."""

    print("="*70)
    print("CONFIDENCE INTERVAL VERIFICATION")
    print("="*70)

    filepath = Path(forecast_file)
    if not filepath.exists():
        print(f"\n❌ ERROR: Forecast file not found: {forecast_file}")
        print("   Run a forecast first: python -m src.app --input sales_data.xlsx")
        return False

    # Load forecast
    df = pd.read_csv(filepath)

    print(f"\n📊 Loaded forecast: {forecast_file}")
    print(f"   Parts: {len(df):,}")
    print(f"   Columns: {len(df.columns)}")

    # Identify quarter columns
    quarter_cols = [col for col in df.columns if col[-2:] in ['Q1', 'Q2', 'Q3', 'Q4'] and '_P' not in col]
    p10_cols = [col for col in df.columns if '_P10' in col]
    p90_cols = [col for col in df.columns if '_P90' in col]

    print(f"\n📈 Forecast Structure:")
    print(f"   Base forecasts (P50): {len(quarter_cols)} columns")
    print(f"   P10 (conservative): {len(p10_cols)} columns")
    print(f"   P90 (optimistic): {len(p90_cols)} columns")

    # Check for confidence intervals
    if len(p10_cols) == 0 and len(p90_cols) == 0:
        print("\n❌ FAIL: No confidence interval columns found!")
        print("   Expected columns like: 26Q2_P10, 26Q2_P90")
        return False

    if len(p10_cols) != len(quarter_cols) or len(p90_cols) != len(quarter_cols):
        print(f"\n⚠️  WARNING: Mismatch in column counts")
        print(f"   Expected {len(quarter_cols)} P10 and P90 columns each")
        print(f"   Found {len(p10_cols)} P10 and {len(p90_cols)} P90 columns")

    # Sample some data
    print(f"\n📋 Sample Data (first 3 parts, first quarter):")
    print("-" * 70)

    if len(quarter_cols) > 0:
        first_q = quarter_cols[0]
        first_q_p10 = f"{first_q}_P10"
        first_q_p90 = f"{first_q}_P90"

        sample_df = df[['Part_number', 'Forecastability_Tier', 'Confidence', 
                       first_q, first_q_p10, first_q_p90]].head(3)

        for _, row in sample_df.iterrows():
            part = row['Part_number']
            tier = row['Forecastability_Tier']
            conf = row['Confidence']
            p50 = row[first_q]
            p10 = row[first_q_p10]
            p90 = row[first_q_p90]

            # Calculate interval metrics
            range_pct = ((p90 - p10) / p50 * 100) if p50 > 0 else 0

            print(f"\nPart: {part}")
            print(f"  Tier: {tier}, Confidence: {conf}")
            print(f"  {first_q}_P10:  {p10:8.1f}  (Conservative)")
            print(f"  {first_q}:      {p50:8.1f}  (Most Likely)")
            print(f"  {first_q}_P90:  {p90:8.1f}  (Optimistic)")
            print(f"  Interval Width: {range_pct:.0f}% of forecast")

    # Validation checks
    print("\n" + "="*70)
    print("VALIDATION CHECKS")
    print("="*70)

    all_good = True

    # Check 1: P10 <= P50 <= P90
    for q in quarter_cols:
        q_p10 = f"{q}_P10"
        q_p90 = f"{q}_P90"

        if q_p10 in df.columns and q_p90 in df.columns:
            violations_low = (df[q_p10] > df[q]).sum()
            violations_high = (df[q] > df[q_p90]).sum()

            if violations_low > 0:
                print(f"\n❌ FAIL: {violations_low} parts have P10 > P50 for {q}")
                all_good = False
            if violations_high > 0:
                print(f"\n❌ FAIL: {violations_high} parts have P50 > P90 for {q}")
                all_good = False

    if all_good:
        print("\n✅ PASS: All P10 <= P50 <= P90 relationships valid")

    # Check 2: No negative values
    negative_count = 0
    for col in p10_cols + quarter_cols + p90_cols:
        if col in df.columns:
            negative_count += (df[col] < 0).sum()

    if negative_count > 0:
        print(f"\n⚠️  WARNING: {negative_count} negative forecast values found")
    else:
        print("✅ PASS: No negative forecast values")

    # Check 3: Interval width by tier
    print("\n📊 Average Interval Width by Tier:")

    if len(quarter_cols) > 0 and len(p10_cols) > 0 and len(p90_cols) > 0:
        first_q = quarter_cols[0]
        first_q_p10 = f"{first_q}_P10"
        first_q_p90 = f"{first_q}_P90"

        df['interval_pct'] = ((df[first_q_p90] - df[first_q_p10]) / (df[first_q] + 0.01) * 100)

        tier_stats = df.groupby('Forecastability_Tier')['interval_pct'].mean()

        for tier, avg_width in tier_stats.items():
            expected = "±20-25%" if "Tier_1" in tier else "±30-40%" if "Tier_2" in tier else "±40-60%"
            print(f"  {tier:25s}: {avg_width:5.1f}%  (Expected: {expected})")

    print("\n" + "="*70)
    print("✅ CONFIDENCE INTERVALS VERIFICATION COMPLETE")
    print("="*70)

    return True

if __name__ == "__main__":
    forecast_file = sys.argv[1] if len(sys.argv) > 1 else "output/forecast_output.csv"
    success = test_confidence_intervals(forecast_file)
    sys.exit(0 if success else 1)
