"""
Merge multiple bias iteration files into single master bias correction file
Applies recency weighting - more recent iterations weighted higher

Usage:
    python merge_bias_files.py --iterations 4
    python merge_bias_files.py --iterations 5 --decay 0.95
"""

import pandas as pd
import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(description='Merge multiple bias correction files')
    parser.add_argument('--iterations', type=int, default=4, help='Number of iteration files to merge (default: 4)')
    parser.add_argument('--input-dir', default='output', help='Directory containing bias_iterX.csv files')
    parser.add_argument('--output', default='output/forecast_accuracy_report.csv', help='Output master bias file')
    parser.add_argument('--decay', type=float, default=1.0, help='Weight decay factor (1.0 = equal weights, <1.0 = favor recent)')
    args = parser.parse_args()

    print("="*70)
    print("BIAS FILE MERGER")
    print("="*70)
    print(f"Merging {args.iterations} iteration files")
    print(f"Input directory: {args.input_dir}")
    print(f"Output file: {args.output}")
    print(f"Recency weighting: {args.decay if args.decay < 1.0 else 'Equal weights'}")
    print()

    # Load all iteration files
    all_bias_data = []
    weights = []

    for i in range(1, args.iterations + 1):
        input_file = os.path.join(args.input_dir, f'bias_iter{i}.csv')

        if not os.path.exists(input_file):
            print(f"⚠️ Warning: {input_file} not found, skipping")
            continue

        try:
            df = pd.read_csv(input_file)

            # Calculate weight (more recent = higher weight)
            # Weight formula: base_weight * (iteration_number / total_iterations)
            # This gives iteration 1 the lowest weight, iteration N the highest
            if args.decay < 1.0:
                # With decay: exponentially favor recent iterations
                weight = args.decay ** (args.iterations - i)
            else:
                # Without decay: linear weighting by recency
                weight = i / args.iterations

            weights.append(weight)

            df['iteration'] = i
            df['weight'] = weight
            all_bias_data.append(df)

            print(f"✅ Loaded {input_file}: {len(df)} parts (weight: {weight:.3f})")

        except Exception as e:
            print(f"❌ Error loading {input_file}: {e}")
            continue

    if len(all_bias_data) == 0:
        print("\n❌ No bias files found! Check the input directory.")
        sys.exit(1)

    print(f"\n✅ Loaded {len(all_bias_data)} iteration files")

    # Combine all iterations
    combined_df = pd.concat(all_bias_data, ignore_index=True)

    print("\n" + "="*70)
    print("PROCESSING DATA")
    print("="*70)

    # Group by Part_number and calculate weighted average of Percentage_Error
    print("\nCalculating weighted average errors per part...")

    # For each part, calculate weighted mean of percentage errors across iterations
    def weighted_avg(group):
        return (group['Percentage_Error'] * group['weight']).sum() / group['weight'].sum()

    master_bias = combined_df.groupby('Part_number').apply(
        lambda x: pd.Series({
            'Percentage_Error': weighted_avg(x),
            'iterations': len(x),
            'min_error': x['Percentage_Error'].min(),
            'max_error': x['Percentage_Error'].max(),
            'std_error': x['Percentage_Error'].std()
        })
    ).reset_index()

    print(f"✅ Processed {len(master_bias)} unique parts")

    # Show statistics
    print("\n" + "="*70)
    print("MASTER BIAS STATISTICS")
    print("="*70)

    print(f"\nParts Coverage:")
    print(f"  Total unique parts: {len(master_bias):,}")
    print(f"  Parts in all {len(all_bias_data)} iterations: {(master_bias['iterations'] == len(all_bias_data)).sum():,}")
    print(f"  Parts in 1 iteration only: {(master_bias['iterations'] == 1).sum():,}")

    print(f"\nOverall Bias Correction:")
    print(f"  Average correction: {master_bias['Percentage_Error'].mean():.2f}%")
    print(f"  Median correction: {master_bias['Percentage_Error'].median():.2f}%")
    print(f"  Std deviation: {master_bias['Percentage_Error'].std():.2f}%")

    over_forecast = (master_bias['Percentage_Error'] > 0).sum()
    under_forecast = (master_bias['Percentage_Error'] < 0).sum()

    print(f"\nBias Direction:")
    print(f"  Over-forecasted parts: {over_forecast:,} ({over_forecast/len(master_bias)*100:.1f}%)")
    print(f"  Under-forecasted parts: {under_forecast:,} ({under_forecast/len(master_bias)*100:.1f}%)")

    print(f"\nCorrection Magnitude:")
    print(f"  Small (<10%): {(master_bias['Percentage_Error'].abs() < 10).sum():,}")
    print(f"  Moderate (10-25%): {((master_bias['Percentage_Error'].abs() >= 10) & (master_bias['Percentage_Error'].abs() < 25)).sum():,}")
    print(f"  Large (25-50%): {((master_bias['Percentage_Error'].abs() >= 25) & (master_bias['Percentage_Error'].abs() < 50)).sum():,}")
    print(f"  Extreme (>50%): {(master_bias['Percentage_Error'].abs() >= 50).sum():,}")

    print(f"\nTop 10 Parts Needing Largest Corrections:")
    top_corrections = master_bias.nlargest(10, 'Percentage_Error', keep='first')[['Part_number', 'Percentage_Error', 'iterations']]
    for idx, row in top_corrections.iterrows():
        print(f"  {row['Part_number']}: {row['Percentage_Error']:+.1f}% (from {int(row['iterations'])} iterations)")

    # Save master bias file in the format BiasCorrector expects
    # Need: Part_number, Year_Q, Forecast, Actual, Error, Percentage_Error
    # Use the most recent iteration's data but with the weighted average Percentage_Error

    # Get the most recent iteration for each part to preserve Year_Q, Forecast, Actual
    most_recent = combined_df.sort_values('iteration', ascending=False).groupby('Part_number').first().reset_index()

    # Merge with our calculated weighted average errors
    output_df = most_recent[['Part_number', 'Year_Q', 'Forecast', 'Actual']].copy()
    output_df = output_df.merge(
        master_bias[['Part_number', 'Percentage_Error']], 
        on='Part_number', 
        how='left'
    )

    # Recalculate Error based on weighted Percentage_Error
    output_df['Error'] = (output_df['Percentage_Error'] / 100.0) * output_df['Actual']

    # Reorder columns to match expected format
    output_df = output_df[['Part_number', 'Year_Q', 'Forecast', 'Actual', 'Error', 'Percentage_Error']]

    output_df.to_csv(args.output, index=False)

    print(f"\n✅ Master bias file saved to: {args.output}")
    print(f"   Format: Part_number, Year_Q, Forecast, Actual, Error, Percentage_Error")

    # Save detailed statistics file
    stats_file = args.output.replace('.csv', '_detailed.csv')
    master_bias.to_csv(stats_file, index=False)
    print(f"✅ Detailed statistics saved to: {stats_file}")

    print("\n" + "="*70)
    print("NEXT STEPS")
    print("="*70)
    print(f"""
1. Review the master bias file: {args.output}
2. This file will be AUTO-DETECTED when you run forecasts
3. Run your production forecast with latest data:

   python -m src.app --input "historical\\sales_current_FIXED.xlsx"

4. The system will automatically apply bias corrections
5. Monitor forecast accuracy and update bias monthly

Bias correction is now ready for production use!
""")

if __name__ == '__main__':
    main()
