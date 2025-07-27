#!/usr/bin/env python3
"""
Batch CP Programs Extractor
Runs multiple mortgage scenarios automatically and extracts cp_programs data for each
"""

import time
import json
from automated_cp_programs_extractor import extract_cp_programs_automated

def run_batch_scenarios(scenarios, headless=True):
    """Run multiple scenarios and extract cp_programs data for each"""
    print("Batch CP Programs Extractor")
    print("===========================")
    print(f"Running {len(scenarios)} scenarios...")
    print(f"Headless Mode: {headless}")
    print()
    
    results = []
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"Scenario {i}/{len(scenarios)}: {scenario['name']}")
        print(f"  Loan Amount: {scenario['loan_amount']}")
        print(f"  Interest Rate: {scenario['interest_rate']}%")
        print(f"  Loan Term: {scenario['loan_term']} years")
        print(f"  CPI Rate: {scenario['cpi_rate']}%")
        
        # Extract data for this scenario
        result = extract_cp_programs_automated(
            loan_amount=scenario['loan_amount'],
            interest_rate=scenario['interest_rate'],
            loan_term=scenario['loan_term'],
            cpi_rate=scenario['cpi_rate'],
            headless=headless
        )
        
        if result:
            scenario_result = {
                'scenario_name': scenario['name'],
                'parameters': scenario,
                'files': result,
                'status': 'success'
            }
            print(f"  ✓ Success - Files saved")
        else:
            scenario_result = {
                'scenario_name': scenario['name'],
                'parameters': scenario,
                'files': None,
                'status': 'failed'
            }
            print(f"  ✗ Failed")
        
        results.append(scenario_result)
        print()
        
        # Wait between scenarios to avoid overwhelming the server
        if i < len(scenarios):
            print("Waiting 5 seconds before next scenario...")
            time.sleep(5)
            print()
    
    # Save batch summary
    save_batch_summary(results)
    
    return results

def save_batch_summary(results):
    """Save a summary of all batch results"""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    summary_filename = f"batch_summary_{timestamp}.json"
    
    summary = {
        'timestamp': timestamp,
        'total_scenarios': len(results),
        'successful_scenarios': len([r for r in results if r['status'] == 'success']),
        'failed_scenarios': len([r for r in results if r['status'] == 'failed']),
        'results': results
    }
    
    with open(summary_filename, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"Batch summary saved to: {summary_filename}")
    print(f"Total scenarios: {summary['total_scenarios']}")
    print(f"Successful: {summary['successful_scenarios']}")
    print(f"Failed: {summary['failed_scenarios']}")

def main():
    """Main function with predefined scenarios"""
    import sys
    
    # Check for command line arguments
    headless = True  # Default to headless
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ['--no-headless', '-n', '--visible', '-v']:
            headless = False
            print("Running batch in visible mode (non-headless)")
        elif sys.argv[1].lower() in ['--help', '-h']:
            print("Usage: python3 batch_cp_programs_extractor.py [OPTION]")
            print("Options:")
            print("  --no-headless, -n    Run in visible mode (show browser)")
            print("  --visible, -v        Run in visible mode (show browser)")
            print("  --help, -h           Show this help message")
            print("")
            print("Examples:")
            print("  python3 batch_cp_programs_extractor.py")
            print("  python3 batch_cp_programs_extractor.py --no-headless")
            print("  python3 batch_cp_programs_extractor.py -n")
            return
    
    # Define your scenarios here
    scenarios = [
        {
            'name': 'Basic_Mortgage',
            'loan_amount': '1000000',
            'interest_rate': '3.5',
            'loan_term': '30',
            'cpi_rate': '2.0'
        },
        {
            'name': 'High_Amount_Mortgage',
            'loan_amount': '2000000',
            'interest_rate': '4.0',
            'loan_term': '25',
            'cpi_rate': '2.5'
        },
        {
            'name': 'Low_Interest_Test',
            'loan_amount': '800000',
            'interest_rate': '2.8',
            'loan_term': '20',
            'cpi_rate': '1.5'
        },
        {
            'name': 'Short_Term_Mortgage',
            'loan_amount': '1500000',
            'interest_rate': '3.2',
            'loan_term': '15',
            'cpi_rate': '2.2'
        },
        {
            'name': 'High_CPI_Mortgage',
            'loan_amount': '1200000',
            'interest_rate': '4.5',
            'loan_term': '30',
            'cpi_rate': '3.5'
        }
    ]
    
    # Run the batch scenarios
    results = run_batch_scenarios(scenarios, headless)
    
    # Print final summary
    print("=" * 50)
    print("BATCH EXTRACTION COMPLETED")
    print("=" * 50)
    
    successful = [r for r in results if r['status'] == 'success']
    failed = [r for r in results if r['status'] == 'failed']
    
    print(f"Total scenarios processed: {len(results)}")
    print(f"Successful extractions: {len(successful)}")
    print(f"Failed extractions: {len(failed)}")
    
    if successful:
        print("\nSuccessful scenarios:")
        for result in successful:
            print(f"  ✓ {result['scenario_name']}")
            if result['files']:
                for file_type, filename in result['files'].items():
                    if filename:
                        print(f"    - {file_type}: {filename}")
    
    if failed:
        print("\nFailed scenarios:")
        for result in failed:
            print(f"  ✗ {result['scenario_name']}")

if __name__ == "__main__":
    main() 