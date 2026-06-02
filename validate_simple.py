"""
Simplified Input Data Validation Tool (No openpyxl required)
Just validates and shows results in console - no Excel summary sheet

Usage:
    python validate_simple.py --sales "sales_data.xlsx"
"""

import pandas as pd
import argparse
import sys
from datetime import datetime
import os

def print_header(text):
    print("\n" + "="*70)
    print(text)
    print("="*70)

def print_success(text):
    print(f"✅ {text}")

def print_warning(text):
    print(f"⚠️  {text}")

def print_error(text):
    print(f"❌ {text}")

def validate_sales_data(filepath):
    """Validate sales data file format"""
    print_header("VALIDATING SALES DATA")
    print(f"File: {filepath}\n")

    issues = []
    is_valid = True

    # Check if file exists
    if not os.path.exists(filepath):
        print_error(f"File not found: {filepath}")
        return False, None, [f"File not found: {filepath}"]

    # Load file
    try:
        if filepath.endswith('.xlsx') or filepath.endswith('.xls'):
            df = pd.read_excel(filepath)
            print_success(f"Loaded Excel file: {len(df)} rows")
        elif filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
            print_success(f"Loaded CSV file: {len(df)} rows")
        else:
            print_error("File must be .xlsx, .xls, or .csv")
            return False, None, ["Unsupported file format"]
    except Exception as e:
        print_error(f"Error loading file: {e}")
        return False, None, [f"Error loading file: {e}"]

    # Check required columns
    required_columns = ['Date', 'Part_number', 'Value']
    print("\nChecking required columns...")

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        is_valid = False
        issue = f"Missing required columns: {missing_columns}"
        issues.append(issue)
        print_error(issue)
        print(f"   Found columns: {list(df.columns)}")
        print(f"   Expected columns: {required_columns}")
    else:
        print_success(f"All required columns found: {required_columns}")

    if not is_valid:
        return is_valid, df, issues

    # Validate Date column
    print("\nValidating Date column...")
    original_dates = df['Date'].copy()

    try:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        null_dates = df['Date'].isna()
        if null_dates.any():
            num_null = null_dates.sum()
            issue = f"{num_null} dates could not be parsed"
            issues.append(issue)
            print_warning(issue)

            bad_date_examples = original_dates[null_dates].head(5).tolist()
            print(f"   Examples of unparseable dates: {bad_date_examples}")
            is_valid = False
        else:
            print_success("All dates parsed successfully")

        if not df['Date'].isna().all():
            min_date = df['Date'].min()
            max_date = df['Date'].max()
            print(f"   Date range: {min_date.date()} to {max_date.date()}")

            df['Quarter'] = df['Date'].dt.quarter
            df['Year'] = df['Date'].dt.year
            df['Year_Q'] = df['Year'].astype(str).str[-2:] + 'Q' + df['Quarter'].astype(str)

            print("\n   Quarter distribution:")
            quarter_counts = df['Year_Q'].value_counts().sort_index()
            for quarter, count in quarter_counts.items():
                print(f"      {quarter}: {count:,} rows")

            df.drop(['Quarter', 'Year', 'Year_Q'], axis=1, inplace=True)

    except Exception as e:
        issue = f"Error parsing dates: {e}"
        issues.append(issue)
        print_error(issue)
        is_valid = False

    # Validate Part_number column
    print("\nValidating Part_number column...")

    null_parts = df['Part_number'].isna()
    if null_parts.any():
        num_null = null_parts.sum()
        issue = f"{num_null} rows have missing Part_number"
        issues.append(issue)
        print_warning(issue)
        is_valid = False
    else:
        print_success("No missing Part_numbers")

    unique_parts = df['Part_number'].nunique()
    print(f"   Unique parts: {unique_parts:,}")

    top_parts = df['Part_number'].value_counts().head(5)
    print("\n   Top 5 parts by transaction count:")
    for part, count in top_parts.items():
        print(f"      {part}: {count:,} transactions")

    # Validate Value column
    print("\nValidating Value column...")

    try:
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

        null_values = df['Value'].isna()
        if null_values.any():
            num_null = null_values.sum()
            issue = f"{num_null} rows have non-numeric or missing Values"
            issues.append(issue)
            print_warning(issue)
            is_valid = False
        else:
            print_success("All Values are numeric")

        negative_values = df['Value'] < 0
        if negative_values.any():
            num_negative = negative_values.sum()
            issue = f"{num_negative} rows have negative Values"
            issues.append(issue)
            print_warning(issue)

        if not df['Value'].isna().all():
            print(f"   Min value: {df['Value'].min()}")
            print(f"   Max value: {df['Value'].max()}")
            print(f"   Mean value: {df['Value'].mean():.2f}")
            print(f"   Median value: {df['Value'].median():.2f}")

    except Exception as e:
        issue = f"Error validating Values: {e}"
        issues.append(issue)
        print_error(issue)
        is_valid = False

    # Check for duplicates
    print("\nChecking for duplicates...")
    duplicates = df.duplicated(subset=['Date', 'Part_number'], keep=False)
    if duplicates.any():
        num_duplicates = duplicates.sum()
        issue = f"{num_duplicates} duplicate rows (same Date + Part_number)"
        issues.append(issue)
        print_warning(issue)
        print("   Note: Duplicates are OK if they represent multiple transactions per day")
    else:
        print_success("No duplicate Date + Part_number combinations")

    # Summary
    print_header("VALIDATION SUMMARY")
    if is_valid:
        print_success("Sales data is valid and ready for forecasting!")
    else:
        print_error(f"Found {len(issues)} issue(s) that need attention")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")

    return is_valid, df, issues

def main():
    parser = argparse.ArgumentParser(description='Simple validation tool (no Excel summary)')
    parser.add_argument('--sales', required=True, help='Path to sales data file')

    args = parser.parse_args()

    print_header("INPUT DATA VALIDATION TOOL (SIMPLE)")
    print(f"Sales file: {args.sales}")

    try:
        sales_valid, sales_df, sales_issues = validate_sales_data(args.sales)

        print_header("FINAL SUMMARY")

        if sales_valid:
            print_success("Validation passed!")
            print("\n✅ Your data is ready for forecasting")
            print("\nRun forecast with:")
            print(f'   python -m src.app --input "{args.sales}" --outdir "output" --skip-plots')
        else:
            print_error("Validation failed - please fix issues before forecasting")
            sys.exit(1)

    except Exception as e:
        print("\n" + "="*70)
        print("UNEXPECTED ERROR")
        print("="*70)
        print(f"Error: {e}")
        import traceback
        print("\nFull traceback:")
        print(traceback.format_exc())
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)
