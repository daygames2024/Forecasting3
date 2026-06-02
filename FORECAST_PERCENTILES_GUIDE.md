# Forecast Percentiles Guide - P10, P50, P90 Explained

## **What They Mean:**

Think of the forecast as a **range of possible outcomes**, not just one number:

```
P90 (Optimistic):  "90% chance actual demand will be BELOW this"
P50 (Most Likely):  "50% chance actual demand will be ABOVE or BELOW this"
P10 (Conservative): "90% chance actual demand will be ABOVE this"
```

---

## **Visual Example:**

```
Part ABC123 - Q1 2025 Forecast:

P10: 100 units  ◄─── Conservative estimate
P50: 150 units  ◄─── Most likely (median)
P90: 220 units  ◄─── Optimistic estimate

		┌─────────────────────────────┐
		│  10% chance below this      │
	100 ├─────────────────────────────┤ P10
		│                             │
		│  40% of outcomes here       │
		│                             │
	150 ├─────────────────────────────┤ P50 (MEDIAN)
		│                             │
		│  40% of outcomes here       │
		│                             │
	220 ├─────────────────────────────┤ P90
		│  10% chance above this      │
		└─────────────────────────────┘
```

---

## **Which One to Use? (Decision Guide)**

### **P10 - Conservative (Safety Stock Planning)**
✅ **Use when:**
- Calculating **minimum inventory** needed
- **Must-not-run-out** scenarios (critical spare parts)
- Setting **safety stock levels**
- Risk-averse planning

**Example:**
> "We need at least P10 (100 units) in stock. There's only a 10% chance demand will be lower than this."

**Risk:** May carry excess inventory, but unlikely to stock out.

---

### **P50 - Most Likely (Primary Planning)**
✅ **Use when:**
- **Standard financial budgeting**
- **Primary production planning**
- **Cost optimization** (balance between shortage and excess)
- Reporting to management

**Example:**
> "We expect P50 (150 units) as our baseline forecast. This is the middle of the road."

**Risk:** Balanced - 50% chance of over/under.

---

### **P90 - Optimistic (Capacity Planning)**
✅ **Use when:**
- **Maximum capacity planning** (warehouse space, staff)
- **Upper bound budgeting** (what if demand is high?)
- **Supply chain capacity** (can suppliers deliver this much?)
- Best-case scenario planning

**Example:**
> "In a high-demand scenario, we could need up to P90 (220 units). Can our warehouse handle it?"

**Risk:** May over-prepare, but won't be caught off-guard by demand spikes.

---

## **Real-World Decision Framework:**

| **Decision Type** | **Use This** | **Why** |
|-------------------|--------------|---------|
| Order minimum stock | **P10** | Avoid stockouts on critical items |
| Set budget forecast | **P50** | Balanced, realistic expectation |
| Plan max warehouse space | **P90** | Ensure capacity for demand spikes |
| Safety stock calculation | **P10** | Conservative, reduces risk |
| Production schedule | **P50** | Efficient, cost-optimized |
| Supplier capacity check | **P90** | Make sure they can handle peaks |

---

## **Which is "Better"?**

**There is no single "better" - it depends on the cost of being wrong:**

### **High Cost of Stockout (Critical Parts):**
→ Use **P10** or even P50  
*Example: Aircraft spare parts - can't afford to run out*

### **High Cost of Excess Inventory:**
→ Use **P50** or P90  
*Example: Perishable goods, expensive items*

### **Balanced Approach (Most Common):**
→ Use **P50** for planning, **P10** for safety stock, **P90** for capacity checks

---

## **Simple Analogy:**

**Planning a wedding:**
- **P10 (100 guests):** Order this much food at minimum - you'll definitely need it
- **P50 (150 guests):** Your best guess - use this for the caterer quote
- **P90 (220 guests):** Book a venue this size - just in case more people show up

You wouldn't order food for 220 people (expensive!), but you'd book a venue that can hold them (cheap insurance).

---

## **How the System Calculates This:**

The forecasting models run **multiple scenarios** and analyze the **distribution of outcomes**:

1. Runs 9 different forecasting models
2. Each model produces a range of predictions
3. Combines them into a probability distribution
4. Extracts the 10th, 50th, and 90th percentile values

**The wider the range (P10 to P90), the more uncertain the forecast.**

---

## **Forecast Output Columns Explained:**

Your forecast Excel/CSV files contain these columns for each quarter:

### **Main Forecast Columns:**
- **`25Q1`, `25Q2`, etc.** - The **P50 (median)** forecast
- **Primary column** to use for standard planning

### **Confidence Interval Columns:**
- **`25Q1_P10`** - Conservative estimate (90% chance demand will be higher)
- **`25Q1_P50`** - Same as main column (most likely)
- **`25Q1_P90`** - Optimistic estimate (90% chance demand will be lower)

### **Example Row:**
```
Part      | 25Q1 | 25Q1_P10 | 25Q1_P50 | 25Q1_P90
ABC123    | 150  | 100      | 150      | 220
```

---

## **Bottom Line Recommendation:**

**For most businesses:**

✅ **Primary planning:** Use **P50** (or the main quarter columns like `25Q1`)  
✅ **Safety stock:** Use **P10** columns (like `25Q1_P10`)  
✅ **Capacity planning:** Use **P90** columns (like `25Q1_P90`)  

**All three together give you the full picture of risk and opportunity!** 📊

---

## **Quick Reference Card:**

| Percentile | What It Means | When to Use | Risk Profile |
|------------|---------------|-------------|--------------|
| **P10** | 90% of outcomes will be HIGHER | Safety stock, critical parts | Conservative - rarely stockout |
| **P50** | Middle estimate, 50/50 chance | Standard planning, budgets | Balanced - cost-optimized |
| **P90** | 90% of outcomes will be LOWER | Capacity, best-case scenario | Optimistic - prepared for spikes |

---

## **Common Questions:**

**Q: Why don't we just use one number?**  
A: Real demand is uncertain. A range shows the risk and helps you plan for different scenarios.

**Q: What if P10 and P90 are very far apart?**  
A: That means high uncertainty. The forecast is less reliable - you might need more data or the part has erratic demand.

**Q: Can I use P50 for everything?**  
A: You can, but you'll miss opportunities to optimize. Use P10 for critical items (avoid stockouts) and P90 for capacity (avoid being caught unprepared).

**Q: Which percentile does bias correction affect?**  
A: All of them! Bias correction shifts the entire forecast distribution based on historical accuracy.

---

## **Related Documentation:**

- `HOW_TO_CREATE_FORECAST.md` - Creating forecasts
- `HOW_TO_UPDATE_BIAS_MONTHLY.md` - Improving forecast accuracy
- `STREAMLIT_DASHBOARD_GUIDE.md` - Using the web interface

---

*For questions or support, refer to the main documentation or contact your system administrator.*
