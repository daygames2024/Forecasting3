import pandas as pd

# Load events
events = pd.read_csv('maintenance_events.csv')
print(f"Total rows in file: {len(events)}")
print(f"6YR events in file: {len(events[events['Check'].str.contains('6Y', na=False)])}")

# Parse dates (same way as app.py)
events['Start Date'] = pd.to_datetime(events['Start Date'], errors='coerce')
events['End Date'] = pd.to_datetime(events['End Date'], errors='coerce')

# Check valid dates
valid_events = events.dropna(subset=['Start Date', 'End Date'])
print(f"\nValid events after date parsing: {len(valid_events)}")
print(f"6YR events after parsing: {len(valid_events[valid_events['Check'].str.contains('6Y', na=False)])}")

# Show sample 6YR events
print("\nSample 6YR events:")
six_yr = valid_events[valid_events['Check'].str.contains('6Y', na=False)].head(5)
print(six_yr[['Check', 'Start Date', 'End Date']])

# Check if any overlap with 2025-2026 forecast period
print("\n\nChecking overlap with forecast periods (2025-2026):")
forecast_start = pd.Timestamp('2025-01-01')
forecast_end = pd.Timestamp('2026-12-31')

overlapping = valid_events[
    (valid_events['Start Date'] <= forecast_end) & 
    (valid_events['End Date'] >= forecast_start)
]

print(f"Total events overlapping 2025-2026: {len(overlapping)}")
print(f"6YR events overlapping 2025-2026: {len(overlapping[overlapping['Check'].str.contains('6Y', na=False)])}")

print("\n6YR events in forecast period:")
six_yr_forecast = overlapping[overlapping['Check'].str.contains('6Y', na=False)]
print(six_yr_forecast[['Check', 'Start Date', 'End Date']])
