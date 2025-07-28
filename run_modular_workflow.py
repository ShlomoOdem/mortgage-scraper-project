#!/usr/bin/env python3
"""
Modular Mortgage Workflow Runner
Demonstrates the complete modular extraction and analysis workflow
"""

import os
import sys
import argparse

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import utility functions
from utils.combination_loader import load_combinations, validate_combinations, create_sample_combination_file
from utils.verification_system import VerificationSystem

def run_extraction(combinations, headless=True, verifier=None):
    """Run the extraction phase"""
    print("="*60)
    print("PHASE 1: MORTGAGE DATA EXTRACTION")
    print("="*60)
    
    try:
        from extractors.automated_cp_programs_extractor import extract_multiple_combinations
        
        # Filter combinations that need extraction
        if verifier:
            needs_extraction, _, _ = verifier.filter_combinations(combinations, skip_extracted=False, skip_analyzed=True)
            if not needs_extraction:
                print("✅ All combinations already extracted. Skipping extraction phase.")
                return True
            
            print(f"Found {len(needs_extraction)} combinations that need extraction")
            combinations_to_process = needs_extraction
        else:
            combinations_to_process = combinations
        
        print(f"Extracting data for {len(combinations_to_process)} mortgage combinations...")
        results = extract_multiple_combinations(combinations_to_process, headless=headless)
        
        if results:
            successful = [r for r in results if r['status'] == 'success']
            failed = [r for r in results if r['status'] == 'failed']
            
            print(f"\nExtraction Results:")
            print(f"  ✅ Successful: {len(successful)}")
            print(f"  ❌ Failed: {len(failed)}")
            
            if successful:
                print(f"\nFiles saved to:")
                print(f"  📁 data/raw/payments_files/")
                print(f"  📄 data/raw/summary_files/")
            
            return len(successful) > 0
        else:
            print("❌ Extraction failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error during extraction: {e}")
        return False

def run_analysis(monthly_income=12000, verifier=None, combinations=None):
    """Run the analysis phase"""
    print("\n" + "="*60)
    print("PHASE 2: MORTGAGE ANALYSIS")
    print("="*60)
    
    try:
        from analyzers.modular_analyzer import analyze_all_mortgages
        
        print(f"Analyzing all mortgage files with monthly income: {monthly_income:,.0f} NIS")
        
        # If verifier is provided, we need to check which files need analysis
        if verifier:
            # Get combinations that need analysis from the verification system
            _ , needs_analysis, _ = verifier.filter_combinations(combinations, skip_extracted=True, skip_analyzed=False)
            if not needs_analysis:
                print("✅ All combinations already analyzed. Skipping analysis phase.")
                return True
            
            print(f"Found {len(needs_analysis)} combinations that need analysis")
            combinations_to_process = needs_analysis
        else:
            combinations_to_process = combinations
        
        results = analyze_all_mortgages(monthly_income=monthly_income)
        
        if results:
            print(f"\nAnalysis Results:")
            print(f"  ✅ Files analyzed: {len(results)}")
            
            # Calculate summary statistics
            total_profit = sum(r['investment_summary']['total_profit_after_tax'] for r in results)
            avg_weighted = sum(r['weighted_result']['weighted_monthly_payment'] for r in results) / len(results)
            
            print(f"  💰 Total investment profit: {total_profit:,.0f} NIS")
            print(f"  ⚖️  Average weighted payment: {avg_weighted:,.0f} NIS")
            
            print(f"\nFiles saved to:")
            print(f"  📁 data/analyzed/payments_files/")
            print(f"  📄 data/analyzed/summary_files/")
            
            return True
        else:
            print("❌ Analysis failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return False

def main(extract=False, analyze=False, full=False, no_headless=False, income=12000, combinations=5, combination_file=None):
    """Main workflow function"""
    # Check if running with direct parameters or command line arguments
    import sys
    
    if len(sys.argv) > 1:
        # Command line mode
        parser = argparse.ArgumentParser(description='Modular Mortgage Workflow')
        parser.add_argument('--extract', action='store_true', help='Run extraction phase')
        parser.add_argument('--analyze', action='store_true', help='Run analysis phase')
        parser.add_argument('--full', action='store_true', help='Run both extraction and analysis')
        parser.add_argument('--no-headless', action='store_true', help='Run browser in visible mode')
        parser.add_argument('--income', type=float, default=12000, help='Monthly income for analysis (default: 12000)')
        parser.add_argument('--combinations', type=int, default=2, help='Number of mortgage combinations to extract (default: 2)')
        parser.add_argument('--combination-file', type=str, help='Load combinations from file (.json, .csv, .yml)')
        parser.add_argument('--create-sample', action='store_true', help='Create a sample combination file')
        parser.add_argument('--status', action='store_true', help='Show processing status without running workflow')
        
        args = parser.parse_args()
        
        # Override with command line arguments
        extract = args.extract
        analyze = args.analyze
        full = args.full
        no_headless = args.no_headless
        income = args.income
        combinations = args.combinations
        combination_file = args.combination_file
        
        # Handle special commands
        if args.create_sample:
            create_sample_combination_file("sample_combinations.json")
            return True
        
        if args.status and combination_file:
            try:
                combinations_list = load_combinations(combination_file)
                verifier = VerificationSystem()
                verifier.print_status_report(combinations_list)
                return True
            except Exception as e:
                print(f"Error loading combinations: {e}")
                return False
    
    print("MODULAR MORTGAGE WORKFLOW")
    print("=========================")
    print("This script demonstrates the modular extraction and analysis workflow.")
    print()
    
    # Load combinations from file or use default
    if combination_file:
        try:
            print(f"Loading combinations from: {combination_file}")
            combinations_list = load_combinations(combination_file)
            valid_combinations = validate_combinations(combinations_list)
            print(f"Loaded {len(combinations_list)} combinations, {len(valid_combinations)} valid")
            
            if not valid_combinations:
                print("❌ No valid combinations found!")
                return False
            
            combinations_to_use = valid_combinations[:combinations] if combinations > 0 else valid_combinations
            
        except Exception as e:
            print(f"❌ Error loading combinations from file: {e}")
            return False
    else:
        # Define sample mortgage combinations
        sample_combinations = [
            {'loan_amount': '1000000', 'interest_rate': '3.5', 'loan_term_months': '360', 'cpi_rate': '2.0', 'channel': 'קבועה צמודה', 'amortization': 'שפיצר'},
            {'loan_amount': '1000000', 'interest_rate': '3.5', 'loan_term_months': '360', 'cpi_rate': '2.0', 'channel': 'קבועה לא צמודה', 'amortization': 'שפיצר'},
            {'loan_amount': '1000000', 'interest_rate': '4.0', 'loan_term_months': '360', 'cpi_rate': '2.0', 'channel': 'פריים', 'amortization': 'שפיצר'},
            {'loan_amount': '1000000', 'interest_rate': '3.5', 'loan_term_months': '240', 'cpi_rate': '2.0', 'channel': 'קבועה צמודה', 'amortization': 'שפיצר'},
            {'loan_amount': '1000000', 'interest_rate': '3.5', 'loan_term_months': '360', 'cpi_rate': '3.0', 'channel': 'קבועה צמודה', 'amortization': 'שפיצר'},
        ]
        
        # Use only the requested number of combinations
        combinations_to_use = sample_combinations[:combinations]
    
    # Initialize verification system
    verifier = VerificationSystem()
    
    # Show status report
    verifier.print_status_report(combinations_to_use)
    
    success = True
    
    # Run extraction if requested
    if extract or full:
        success = run_extraction(combinations_to_use, headless=not no_headless, verifier=verifier)
        if not success:
            print("\n❌ Extraction phase failed. Stopping workflow.")
            return False
    
    # Run analysis if requested
    if analyze or full:
        success = run_analysis(monthly_income=income, verifier=verifier, combinations=combinations_to_use)
        if not success:
            print("\n❌ Analysis phase failed.")
            return False
    
    # If no specific phase was requested, show help
    if not (extract or analyze or full):
        print("No action specified. Use one of the following options:")
        print("  --extract    Run only the extraction phase")
        print("  --analyze    Run only the analysis phase")
        print("  --full       Run both extraction and analysis phases")
        print("  --combination-file <file>  Load combinations from file (.json, .csv, .yml)")
        print("  --create-sample            Create a sample combination file")
        print("  --status                   Show processing status without running workflow")
        print("\nExamples:")
        print("  python3 run_modular_workflow.py --extract")
        print("  python3 run_modular_workflow.py --analyze --income 15000")
        print("  python3 run_modular_workflow.py --full --no-headless")
        print("  python3 run_modular_workflow.py --combination-file my_combinations.json --full")
        print("  python3 run_modular_workflow.py --combination-file my_combinations.json --status")
        print("  python3 run_modular_workflow.py --create-sample")
        return False
    
    if success:
        print("\n🎉 WORKFLOW COMPLETED SUCCESSFULLY!")
        print("\nThe modular process has:")
        print("  ✅ Extracted mortgage data from web calculator")
        print("  ✅ Calculated investment opportunities")
        print("  ✅ Computed weighted monthly payments")
        print("  ✅ Generated comprehensive analysis reports")
        print("\nResults are available in:")
        print("  📁 data/raw/     - Raw extracted data")
        print("  📁 data/analyzed/ - Analysis results")
    
    return success

if __name__ == "__main__":
    main(extract=False, analyze=True, full=True, no_headless=True, income=12000, combinations=0,combination_file="data/combinations_001.json") 