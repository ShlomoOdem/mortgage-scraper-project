#!/usr/bin/env python3
"""
Configurable Batch CP Programs Extractor
Reads scenarios from a JSON configuration file and runs them automatically
"""

import time
import json
import sys
from automated_cp_programs_extractor import extract_cp_programs_automated

def load_config(config_file="scenarios_config.json"):
    """Load scenarios and settings from configuration file"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Configuration file '{config_file}' not found!")
        print("Please create a scenarios_config.json file with your scenarios.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing configuration file: {e}")
        return None

def run_configurable_batch(config_file="scenarios_config.json", headless=True):
    """Run batch scenarios from configuration file"""
    config = load_config(config_file)
    if not config:
        return None
    
    scenarios = config.get('scenarios', [])
    settings = config.get('settings', {})
    
    if not scenarios:
        print("No scenarios found in configuration file!")
        return None
    
    print("Configurable Batch CP Programs Extractor")
    print("========================================")
    print(f"Configuration file: {config_file}")
    print(f"Running {len(scenarios)} scenarios...")
    print(f"Settings: {settings}")
    print()
    
    results = []
    # Use the headless parameter passed to the function, but allow config override
    config_headless = settings.get('headless', headless)
    wait_time = settings.get('wait_between_scenarios', 5)
    
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
            headless=config_headless
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
        
        # Wait between scenarios
        if i < len(scenarios):
            print(f"Waiting {wait_time} seconds before next scenario...")
            time.sleep(wait_time)
            print()
    
    # Save batch summary
    save_batch_summary(results, config_file)
    
    return results

def save_batch_summary(results, config_file):
    """Save a summary of all batch results"""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    summary_filename = f"configurable_batch_summary_{timestamp}.json"
    
    summary = {
        'timestamp': timestamp,
        'config_file': config_file,
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
    """Main function"""
    # Parse command line arguments
    config_file = "scenarios_config.json"
    headless = True  # Default to headless
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg.lower() in ['--no-headless', '-n', '--visible', '-v']:
            headless = False
            print("Running in visible mode (non-headless)")
        elif arg.lower() in ['--help', '-h']:
            print("Usage: python3 configurable_batch_extractor.py [OPTIONS] [CONFIG_FILE]")
            print("Options:")
            print("  --no-headless, -n    Run in visible mode (show browser)")
            print("  --visible, -v        Run in visible mode (show browser)")
            print("  --help, -h           Show this help message")
            print("")
            print("Examples:")
            print("  python3 configurable_batch_extractor.py")
            print("  python3 configurable_batch_extractor.py --no-headless")
            print("  python3 configurable_batch_extractor.py my_scenarios.json")
            print("  python3 configurable_batch_extractor.py --no-headless my_scenarios.json")
            return
        elif not arg.startswith('-'):
            # This is the config file
            config_file = arg
        i += 1
    
    print(f"Using configuration file: {config_file}")
    print(f"Headless mode: {headless}")
    print()
    
    # Run the configurable batch scenarios
    results = run_configurable_batch(config_file, headless)
    
    if not results:
        print("Batch extraction failed or no scenarios found!")
        return
    
    # Print final summary
    print("=" * 50)
    print("CONFIGURABLE BATCH EXTRACTION COMPLETED")
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