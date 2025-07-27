#!/usr/bin/env python3
"""
Comprehensive Mortgage Analysis Runner
Loads generated combinations and runs the mortgage scraper
"""

import json
import sys
import os
from automated_cp_programs_extractor import extract_multiple_combinations, filter_unprocessed_combinations

def load_combinations_from_file(filename):
    """Load mortgage combinations from JSON file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            combinations = json.load(f)
        print(f"Loaded {len(combinations)} combinations from {filename}")
        return combinations
    except FileNotFoundError:
        print(f"Error: File {filename} not found!")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {filename}: {e}")
        return None

def show_tracking_status(combinations_file, tracking_file="processed_combinations.json"):
    """Show the status of processed combinations"""
    combinations = load_combinations_from_file(combinations_file)
    if not combinations:
        return
    
    unprocessed, already_processed = filter_unprocessed_combinations(combinations, tracking_file)
    
    print(f"\n{'='*60}")
    print(f"TRACKING STATUS")
    print(f"{'='*60}")
    print(f"Total combinations: {len(combinations)}")
    print(f"Already processed: {already_processed}")
    print(f"Remaining to process: {len(unprocessed)}")
    print(f"Progress: {already_processed/len(combinations)*100:.1f}%")
    
    if already_processed > 0:
        print(f"\nTracking file: {tracking_file}")
        try:
            with open(tracking_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                last_updated = data.get('last_updated', 'Unknown')
                print(f"Last updated: {last_updated}")
        except:
            print("Could not read tracking file details")
    
    if len(unprocessed) > 0:
        print(f"\nNext combinations to process:")
        for i, combo in enumerate(unprocessed[:5]):
            print(f"  {i+1}. {combo['loan_amount']} @ {combo['interest_rate']}% for {combo['loan_term_months']} months")
            print(f"     Channel: {combo['channel']}, Amortization: {combo['amortization']}, CPI: {combo['cpi_rate']}%")
        
        if len(unprocessed) > 5:
            print(f"  ... and {len(unprocessed) - 5} more")

def run_comprehensive_analysis(combinations_file, headless=True, max_combinations=None, tracking_file="processed_combinations.json"):
    """Run comprehensive mortgage analysis"""
    print("Comprehensive Mortgage Analysis")
    print("===============================")
    
    # Load combinations
    combinations = load_combinations_from_file(combinations_file)
    if not combinations:
        return False
    
    # Limit combinations if specified
    if max_combinations and max_combinations < len(combinations):
        combinations = combinations[:max_combinations]
        print(f"Limited to first {max_combinations} combinations for testing")
    
    print(f"Processing {len(combinations)} combinations...")
    print(f"Headless mode: {headless}")
    print(f"Tracking file: {tracking_file}")
    
    # Run the analysis
    results = extract_multiple_combinations(combinations, headless, tracking_file)
    
    if results:
        print(f"\n{'='*80}")
        print(f"COMPREHENSIVE ANALYSIS COMPLETE")
        print(f"{'='*80}")
        
        successful = [r for r in results if r['status'] == 'success']
        failed = [r for r in results if r['status'] == 'failed']
        
        print(f"Total combinations processed: {len(results)}")
        print(f"Successful: {len(successful)} ({len(successful)/len(results)*100:.1f}%)")
        print(f"Failed: {len(failed)} ({len(failed)/len(results)*100:.1f}%)")
        
        if successful:
            print(f"\nSuccessful extractions:")
            for result in successful[:10]:  # Show first 10
                combo = result['combination']
                print(f"  ✓ {combo['loan_amount']} @ {combo['interest_rate']}% for {combo['loan_term_months']} months")
                print(f"    Channel: {combo['channel']}, Amortization: {combo['amortization']}, CPI: {combo['cpi_rate']}%")
            
            if len(successful) > 10:
                print(f"  ... and {len(successful) - 10} more successful extractions")
        
        if failed:
            print(f"\nFailed extractions (first 10):")
            for result in failed[:10]:
                combo = result['combination']
                print(f"  ✗ {combo['loan_amount']} @ {combo['interest_rate']}% for {combo['loan_term_months']} months")
                print(f"    Channel: {combo['channel']}, Amortization: {combo['amortization']}, CPI: {combo['cpi_rate']}%")
            
            if len(failed) > 10:
                print(f"  ... and {len(failed) - 10} more failed extractions")
        
        return True
    else:
        print("Analysis failed!")
        return False

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run comprehensive mortgage analysis')
    parser.add_argument('--combinations', '-c', default='test_mortgage_combinations.json',
                       help='JSON file with mortgage combinations (default: test_mortgage_combinations.json)')
    parser.add_argument('--no-headless', '-n', action='store_true',
                       help='Run in visible mode (non-headless)')
    parser.add_argument('--max', '-m', type=int,
                       help='Maximum number of combinations to process (for testing)')
    parser.add_argument('--full', '-f', action='store_true',
                       help='Use full combinations file (mortgage_combinations_*.json)')
    parser.add_argument('--tracking', '-t', default='processed_combinations.json',
                       help='Tracking file for processed combinations (default: processed_combinations.json)')
    parser.add_argument('--reset-tracking', '-r', action='store_true',
                       help='Reset tracking file (start fresh)')
    parser.add_argument('--status', '-s', action='store_true',
                       help='Show tracking status without running analysis')
    
    args = parser.parse_args()
    
    # Handle tracking file reset
    if args.reset_tracking:
        if os.path.exists(args.tracking):
            os.remove(args.tracking)
            print(f"Reset tracking file: {args.tracking}")
        else:
            print(f"Tracking file {args.tracking} does not exist, nothing to reset.")
        return
    
    # Determine which file to use
    if args.full:
        # Find the most recent full combinations file
        import glob
        files = glob.glob('mortgage_combinations_*.json')
        if files:
            # Sort by modification time and get the most recent
            files.sort(key=os.path.getmtime, reverse=True)
            combinations_file = files[0]
            print(f"Using full combinations file: {combinations_file}")
        else:
            print("No full combinations file found. Run generate_mortgage_combinations.py first.")
            return
    else:
        combinations_file = args.combinations
    
    # Show status if requested
    if args.status:
        show_tracking_status(combinations_file, args.tracking)
        return
    
    # Run the analysis
    success = run_comprehensive_analysis(
        combinations_file, 
        headless=not args.no_headless,
        max_combinations=args.max,
        tracking_file=args.tracking
    )
    
    if success:
        print(f"\nAnalysis completed successfully!")
        print(f"Check the payments_files/ and summary_files/ directories for results.")
    else:
        print(f"\nAnalysis failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 