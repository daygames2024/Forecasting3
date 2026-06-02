# Confidence Intervals Guide

## Overview

The forecasting system now includes **confidence intervals** for every forecast, providing uncertainty quantification to help with inventory planning decisions.

## What Are Confidence Intervals?

For each forecasted quarter, you'll now see **three values**:

- **P10 (Conservative)**: 10th percentile - Lower bound estimate
- **P50 (Most Likely)**: 50th percentile - Your main forecast (same as before)
- **P90 (Optimistic)**: 90th percentile - Upper bound estimate

### Example

For part ABC123 in 26Q2:
```
26Q2      = 150  (P50 - Most likely forecast)
26Q2_P10  = 105  (P10 - Conservative: 30% below)
26Q2_P90  = 210  (P90 - Optimistic: 40% above)
```

This means:
- **10% chance** demand will be below 105 units
- **50% chance** demand will be around 150 units (your primary forecast)
- **90% chance** demand will be below 210 units

## Interval Widths by Forecastability Tier

The width of confidence intervals automatically adjusts based on each part's forecastability:

| Tier | Confidence Level | P10 Factor | P90 Factor | Typical Range |
|------|-----------------|------------|------------|---------------|
| **Tier 1 (High)** | High confidence | 0.80 | 1.25 | ±20-25% |
| **Tier 2 (Medium)** | Medium confidence | 0.70 | 1.40 | ±30-40% |
| **Tier 3-4 (Low)** | Low confidence | 0.60 | 1.60 | ±40-60% |

**Additional adjustments:**
- **Volatile parts**: Wider intervals (±5-15% additional spread)
- **Intermittent parts**: Wider intervals (±10-20% additional spread)
- **High confidence parts**: Narrower intervals (tighter planning possible)

## How to Use Confidence Intervals

### 1. Safety Stock Calculations
**Use P10 (Conservative)**
- Ensures you can cover demand 90% of the time
- Appropriate for high-value or critical parts
- Protects against stockouts

```
Safety Stock = (P90 - P10) / 2
Reorder Point = P10 + Lead_Time_Demand
```

### 2. Primary Planning & Budgeting
**Use P50 (Most Likely)**
- Your main forecast value
- Use for budget projections
- Standard inventory planning
- Same value as before (backward compatible)

### 3. Maximum Capacity Planning
**Use P90 (Optimistic)**
- Plan warehouse space for peak scenarios
- Budget for maximum procurement needs
- Stress testing supply chain capacity

### 4. Risk Assessment
**Interval Width Analysis**
```
Uncertainty = (P90 - P10) / P50

High uncertainty (>100%): Review part segmentation, consider manual review
Medium uncertainty (50-100%): Normal for aircraft parts
Low uncertainty (<50%): High-confidence parts, safe to optimize inventory
```

## Excel Output Format

In your forecast Excel file, columns are now organized as:

```
Part_number | Tier | ... | 26Q2 | 26Q2_P10 | 26Q2_P90 | 26Q3 | 26Q3_P10 | 26Q3_P90 | ...
```

**Tip:** Create a pivot or filter to view just P10, P50, or P90 forecasts depending on your use case.

## Bias Correction Impact

**Important:** Bias corrections are applied to **all three confidence levels** (P10, P50, P90).

If a part historically over-forecasts by 20%, all three values are reduced proportionally:
```
Before bias correction:
  26Q2 = 150, 26Q2_P10 = 105, 26Q2_P90 = 210

After bias correction (0.833x factor):
  26Q2 = 125, 26Q2_P10 = 87, 26Q2_P90 = 175
```

This ensures confidence intervals reflect **both model uncertainty AND historical accuracy**.

## Best Practices

### For Buyers/Planners
1. **High-Value Parts (>$1000)**: Use P10 for procurement to minimize stockout risk
2. **Standard Parts**: Use P50 for normal planning
3. **Capacity Planning**: Use P90 to ensure you have enough warehouse space

### For Forecasters
1. **Monitor Tier Distribution**: More Tier 1 parts = narrower intervals = better planning
2. **Track Interval Coverage**: After each cycle, check if actuals fall within P10-P90 range
3. **Adjust for Events**: Maintenance events already factored into all three forecasts

### For Executives
1. **Budget Planning**: Use P50 for base case, P90 for stress testing
2. **Inventory Investment**: Use P50 × unit cost for financial planning
3. **Risk Metrics**: Monitor % of parts in Tier 3-4 (wide intervals = higher uncertainty)

## Example Scenarios

### Scenario 1: Critical AOG Part
```
Part: 777-ENG-4421
Tier: Tier_4_Not_Forecastable
26Q2 = 3, 26Q2_P10 = 2, 26Q2_P90 = 5

Strategy: Stock 5 units (P90) due to criticality and high cost of stockout
```

### Scenario 2: Steady Consumable
```
Part: WASHER-STD-125
Tier: Tier_1_High
26Q2 = 500, 26Q2_P10 = 400, 26Q2_P90 = 625

Strategy: Stock 500 units (P50), narrow interval = reliable forecast
```

### Scenario 3: Seasonal Part
```
Part: FILTER-AC-SUMMER
Tier: Tier_2_Medium
26Q2 = 200, 26Q2_P10 = 140, 26Q2_P90 = 280

Strategy: Stock 200 (P50) + safety buffer of (280-140)/2 = 70 units
```

## Technical Details

### Calculation Method
Intervals are calculated using **tier-adjusted multipliers** rather than statistical quantile regression:

```python
if Tier_1 or High Confidence:
    P10 = Forecast × 0.80
    P90 = Forecast × 1.25
elif Tier_2 or Medium Confidence:
    P10 = Forecast × 0.70
    P90 = Forecast × 1.40
else:  # Tier_3-4 or Low Confidence
    P10 = Forecast × 0.60
    P90 = Forecast × 1.60

# Additional adjustments for data quality
if Volatile:
    P10 *= 0.90 (wider interval)
    P90 *= 1.15 (wider interval)
if Intermittent:
    P10 *= 0.85 (wider interval)
    P90 *= 1.20 (wider interval)
```

### Why This Method?
- **Transparent**: Easy to understand and explain
- **Calibrated**: Widths match observed forecast accuracy patterns
- **Consistent**: Same approach across all parts
- **Fast**: No additional computation time

Future enhancement could use **quantile regression** based on historical forecast errors for more precise intervals.

## Validation

After each forecast cycle:

1. **Check Coverage**: What % of actuals fell within P10-P90?
   - Target: 80-90% (P10 to P90 represents 80% probability range)

2. **Check Calibration**: Are P10 and P90 equally likely to be exceeded?
   - Target: ~10% of actuals below P10, ~10% above P90

3. **Adjust if Needed**: If coverage consistently off, contact system administrator

## Summary

Confidence intervals give you **three forecasts instead of one**, helping you:
- ✅ Quantify forecast uncertainty
- ✅ Make risk-aware inventory decisions  
- ✅ Plan for best/worst case scenarios
- ✅ Optimize safety stock levels
- ✅ Improve communication with stakeholders

**Remember**: 
- P10 = Conservative (safety stock)
- P50 = Most Likely (primary forecast)
- P90 = Optimistic (capacity planning)

Choose the right percentile for your specific decision!
