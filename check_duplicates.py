"""
Quick script to check if duplicates are legitimate transactions
"""
import pandas as pd

# Load your sales data
sales = pd.read_excel("2026_Q3_sales.xlsx")  # Change to your file

# Find duplicates (same Date + Part_number)
duplicates = sales[sales.duplicated(subset=['Date', 'Part_number'], keep=False)]

# Sort by Date and Part_number to see them together
duplicates = duplicates.sort_values(['Part_number', 'Date', 'Value'])

print(f"Total duplicate rows: {len(duplicates)}")
print(f"\nFirst 20 duplicate rows:")
print(duplicates[['Date', 'Part_number', 'Value']].head(20))

# Check if Values are different (suggests real transactions)
print("\n" + "="*70)
print("DUPLICATE ANALYSIS")
print("="*70)

# Group by Date + Part_number and check if Values vary
dup_groups = duplicates.groupby(['Date', 'Part_number'])['Value'].agg(['count', 'sum', 'mean', 'std'])
dup_groups = dup_groups[dup_groups['count'] > 1]

print(f"\nParts with duplicates: {len(dup_groups)}")
print(f"\nSample of duplicate groups (different Values = real transactions):")
print(dup_groups.head(10))

# Check if all duplicates have same value (suspicious)
same_value_dups = dup_groups[dup_groups['std'] == 0]
if len(same_value_dups) > 0:
    print(f"\n⚠️  Warning: {len(same_value_dups)} duplicate groups have IDENTICAL values")
    print("   This might indicate data quality issues (same row imported twice)")
    print("\n   Examples:")
    print(same_value_dups.head(10))
else:
    print("\n✅ All duplicates have different Values - these are legitimate multiple transactions per day")
