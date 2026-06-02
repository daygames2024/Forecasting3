"""
Wrapper to run validate_input_data.py with error catching
"""
import sys
import traceback

try:
    # Run the validation script
    exec(open('validate_input_data.py').read())
except Exception as e:
    print("\n" + "="*70)
    print("ERROR OCCURRED")
    print("="*70)
    print(f"\nError type: {type(e).__name__}")
    print(f"Error message: {str(e)}")
    print("\nFull traceback:")
    print(traceback.format_exc())
    print("\n" + "="*70)
    input("\nPress Enter to exit...")
    sys.exit(1)
