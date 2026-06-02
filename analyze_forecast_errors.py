"""
Analyze forecast errors to identify model-demand alignment issues
"""
import pandas as pd
import numpy as np

# Load the comparison results
comparison_df = pd.read_csv('forecast_accuracy_report.csv')

print("="*70)
print("FORECAST ERROR ANALYSIS - MODEL-DEMAND ALIGNMENT")
print("="*70)

# Basic stats
print(f"\nTotal comparisons: {len(comparison_df):,}")
print(f"\nOVERALL ACCURACY:")
print(f"  Average error: {comparison_df['Percentage_Error'].mean():.2f}%")
print(f"  Median error: {comparison_df['Percentage_Error'].median():.2f}%")
print(f"  Std deviation: {comparison_df['Percentage_Error'].std():.2f}%")
print(f"  Max over-forecast: +{comparison_df['Percentage_Error'].max():.2f}%")
print(f"  Max under-forecast: {comparison_df['Percentage_Error'].min():.2f}%")

# Bias detection (systematic over/under forecasting)
print(f"\n" + "="*70)
print("BIAS ANALYSIS (Systematic Over/Under Forecasting)")
print("="*70)
over_forecast = (comparison_df['Error'] > 0).sum()
under_forecast = (comparison_df['Error'] < 0).sum()
perfect = (comparison_df['Error'] == 0).sum()
print(f"  Over-forecasted: {over_forecast:,} ({over_forecast/len(comparison_df)*100:.1f}%)")
print(f"  Under-forecasted: {under_forecast:,} ({under_forecast/len(comparison_df)*100:.1f}%)")
print(f"  Perfect: {perfect:,} ({perfect/len(comparison_df)*100:.1f}%)")

if over_forecast > under_forecast * 1.2:
    print("  ⚠️ SYSTEMATIC OVER-FORECASTING DETECTED")
    print("     Your models consistently predict higher than actual demand")
elif under_forecast > over_forecast * 1.2:
    print("  ⚠️ SYSTEMATIC UNDER-FORECASTING DETECTED")
    print("     Your models consistently predict lower than actual demand")
else:
    print("  ✅ No systematic bias detected")

# Accuracy by quarter (time-based patterns)
print(f"\n" + "="*70)
print("ACCURACY BY QUARTER (Time-Based Patterns)")
print("="*70)
quarter_accuracy = comparison_df.groupby('Year_Q').agg({
    'Percentage_Error': ['mean', 'median', 'std', 'count']
}).round(2)
print(quarter_accuracy)

# Check if accuracy degrades over time
quarters = comparison_df.groupby('Year_Q')['Percentage_Error'].apply(lambda x: abs(x).mean()).sort_index()
print(f"\nForecast Horizon Analysis:")
for qtr, err in quarters.items():
    print(f"  {qtr}: {err:.2f}% average absolute error")

if len(quarters) > 1:
    trend = np.polyfit(range(len(quarters)), quarters.values, 1)[0]
    if trend > 5:
        print("  ⚠️ ACCURACY DEGRADES SIGNIFICANTLY OVER TIME")
        print("     Long-term forecasts are much less accurate (typical issue)")
    elif trend < -5:
        print("  ⚠️ NEAR-TERM FORECASTS WORSE THAN LONG-TERM")
        print("     Unusual pattern - may indicate reactive vs. strategic planning mismatch")

# Error distribution (identify outliers)
print(f"\n" + "="*70)
print("ERROR DISTRIBUTION")
print("="*70)
abs_errors = comparison_df['Percentage_Error'].abs()
print(f"  Within ±10%: {(abs_errors <= 10).sum():,} ({(abs_errors <= 10).sum()/len(comparison_df)*100:.1f}%)")
print(f"  Within ±25%: {(abs_errors <= 25).sum():,} ({(abs_errors <= 25).sum()/len(comparison_df)*100:.1f}%)")
print(f"  Within ±50%: {(abs_errors <= 50).sum():,} ({(abs_errors <= 50).sum()/len(comparison_df)*100:.1f}%)")
print(f"  Over 100% error: {(abs_errors > 100).sum():,} ({(abs_errors > 100).sum()/len(comparison_df)*100:.1f}%)")

# Top 10 worst forecasts
print(f"\n" + "="*70)
print("TOP 10 BIGGEST FORECAST ERRORS")
print("="*70)
top_errors = comparison_df.nlargest(10, 'Absolute_Error')[
    ['Part_number', 'Year_Q', 'Forecasted_Value', 'Value', 'Error', 'Percentage_Error']
]
print(top_errors.to_string(index=False))

# Analyze if errors concentrated in specific parts
print(f"\n" + "="*70)
print("PART-LEVEL ANALYSIS")
print("="*70)
part_errors = comparison_df.groupby('Part_number').agg({
    'Percentage_Error': lambda x: abs(x).mean()
}).sort_values('Percentage_Error', ascending=False)

print(f"Total unique parts: {len(part_errors)}")
print(f"\nWorst 10 parts (consistently inaccurate):")
print(part_errors.head(10))

high_error_parts = (part_errors['Percentage_Error'] > 50).sum()
print(f"\nParts with >50% avg error: {high_error_parts} ({high_error_parts/len(part_errors)*100:.1f}%)")

# Model-demand alignment diagnosis
print(f"\n" + "="*70)
print("MODEL-DEMAND ALIGNMENT DIAGNOSIS")
print("="*70)

issues = []
avg_abs_error = abs_errors.mean()

if avg_abs_error > 50:
    issues.append("❌ CRITICAL: Average error >50% - models fundamentally misaligned with demand")
elif avg_abs_error > 25:
    issues.append("⚠️ WARNING: Average error >25% - significant alignment issues")
else:
    issues.append("✅ Average error acceptable (<25%)")

if over_forecast > under_forecast * 1.3:
    issues.append("❌ Systematic over-forecasting - models assume higher demand than reality")
elif under_forecast > over_forecast * 1.3:
    issues.append("❌ Systematic under-forecasting - models miss actual demand patterns")

if (abs_errors > 100).sum() / len(comparison_df) > 0.05:
    issues.append("❌ Too many extreme outliers (>100% error) - missing demand signals")

if len(quarters) > 1 and np.polyfit(range(len(quarters)), quarters.values, 1)[0] > 5:
    issues.append("⚠️ Accuracy degrades over forecast horizon - models don't capture long-term patterns")

print("\nIdentified Issues:")
for i, issue in enumerate(issues, 1):
    print(f"{i}. {issue}")

print(f"\n" + "="*70)
print("RECOMMENDATIONS TO IMPROVE MODEL-DEMAND ALIGNMENT")
print("="*70)

print("""
Based on your forecast errors, here are specific actions to improve alignment:

1. **Check Input Data Quality**
   - Are you using lagging indicators instead of leading indicators?
   - Do your models see recent sales trends or only historical averages?
   - Missing seasonality, promotions, or market events?

2. **Review Model Assumptions**
   - Are models trained on representative historical periods?
   - Do models account for market changes (COVID impact, competition, trends)?
   - Are you using the right forecasting method for each product type?

3. **Demand Signal Alignment**
   - Fast-moving items: Need short-term reactive models
   - Slow-moving items: Need different approach (intermittent demand models)
   - New products: Can't rely on historical patterns alone

4. **Specific Fixes for Your Data**
""")

if over_forecast > under_forecast * 1.3:
    print("   - Your models are TOO OPTIMISTIC - reduce growth assumptions")
    print("   - Check if models use outdated 'good years' as baseline")
    print("   - Add pessimistic scenario weighting")

if (abs_errors > 100).sum() / len(comparison_df) > 0.05:
    print("   - Too many extreme misses - segment products by behavior")
    print("   - Apply different models to stable vs. volatile products")
    print("   - Flag and manually review low-volume/high-variance items")

if len(quarters) > 1 and np.polyfit(range(len(quarters)), quarters.values, 1)[0] > 5:
    print("   - Long-term forecasts need different approach than short-term")
    print("   - Consider ensemble models (combine methods for different horizons)")
    print("   - Review and adjust forecasts quarterly instead of annually")

print("\n5. **Quick Wins**")
print("   - Apply error thresholds: Flag items with >50% error for manual review")
print("   - Segment by ABC analysis: A items need more sophisticated models")
print("   - Use forecast bias correction: Adjust systematically high/low forecasts")
print("   - Implement safety stock for high-error items instead of 'fixing' forecasts")

print(f"\n" + "="*70)
print("NEXT STEPS")
print("="*70)
print("""
1. Review the worst 10 parts - what do they have in common?
2. Check if errors cluster in specific quarters (seasonality issues?)
3. Examine forecasting methodology for high-error segments
4. Consider hybrid approach: Statistical models + business judgment
5. Implement continuous monitoring and adjustment process

The goal isn't perfect forecasts - it's **alignment** between:
- What your models predict (supply planning)
- What customers actually demand (market reality)
- What your business can execute (operational capacity)
""")

print(f"\n✅ Analysis complete. Report saved to: forecast_accuracy_report.csv")
