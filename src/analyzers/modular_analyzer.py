#!/usr/bin/env python3
"""
Modular Mortgage Analyzer
Processes extracted CSV files and applies investment and weighted payment calculations
"""

import os
import csv
import json
import glob
from datetime import datetime
import sys

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'calculators'))

from invesment import StockInvestment
from weighted_payment_calculator import WeightedPaymentCalculator

def load_mortgage_data(payments_file):
    """Load mortgage data from CSV file"""
    monthly_payments = []
    
    with open(payments_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            monthly_payments.append(row)
    
    return monthly_payments

def load_mortgage_summary(summary_file):
    """Load mortgage summary from CSV file"""
    summary_data = {}
    
    with open(summary_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            parameter = row.get('Parameter', '')
            value = row.get('Value', '')
            summary_data[parameter] = value
    
    return summary_data

def calculate_investment_analysis(monthly_payments, monthly_income=12000, annual_return_rate=0.07, annual_inflation_rate=0.03, tax_rate=0.25):
    """Calculate investment analysis for mortgage payments"""
    print("Calculating investment analysis...")
    
    # Extract monthly payment amounts
    payment_amounts = []
    for payment in monthly_payments:
        payment_amount = float(payment.get('month_payment', payment.get('payment', 0)))
        payment_amounts.append(payment_amount)
    
    # Calculate investment amounts (income - mortgage payment)
    investment_amounts = []
    for payment_amount in payment_amounts:
        investment_amount = max(0, monthly_income - payment_amount)
        investment_amounts.append(investment_amount)
    
    # Create investment calculator
    investment = StockInvestment(
        monthly_investments=investment_amounts,
        annual_return_rate=annual_return_rate,
        annual_inflation_rate=annual_inflation_rate,
        tax_rate=tax_rate
    )
    
    # Get investment summary
    investment_summary = investment.get_summary()
    
    return investment_summary, investment_amounts

def calculate_weighted_payment_analysis(monthly_payments, loan_amount, annual_return_rate=0.07, annual_inflation_rate=0.03, tax_rate=0.25):
    """Calculate weighted payment analysis for mortgage"""
    print("Calculating weighted payment analysis...")
    
    # Convert payments to format expected by WeightedPaymentCalculator
    monthly_payments_for_weighted = []
    for payment in monthly_payments:
        monthly_payments_for_weighted.append({
            'month_payment': float(payment.get('month_payment', payment.get('payment', 0)))
        })
    
    # Create weighted payment calculator
    weighted_calculator = WeightedPaymentCalculator(
        monthly_payments=monthly_payments_for_weighted,
        loan_amount=loan_amount,
        annual_return_rate=annual_return_rate,
        annual_inflation_rate=annual_inflation_rate,
        tax_rate=tax_rate
    )
    
    # Calculate weighted payment
    weighted_result = weighted_calculator.calculate_weighted_payment()
    
    return weighted_result

def save_analysis_results(original_summary, investment_summary, weighted_result, monthly_income, investment_amounts, monthly_payments, output_dir="data/analyzed"):
    """Save analysis results to files"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create output directories
    payments_dir = os.path.join(output_dir, "payments_files")
    summary_dir = os.path.join(output_dir, "summary_files")
    os.makedirs(payments_dir, exist_ok=True)
    os.makedirs(summary_dir, exist_ok=True)
    
    # Extract loan parameters from original summary
    loan_type = original_summary.get('Loan Type', 'Unknown')
    interest_rate = original_summary.get('Interest Rate (%)', 'Unknown')
    loan_term_months = original_summary.get('Loan Term (months)', 'Unknown')
    inflation_rate = original_summary.get('Inflation Rate (%)', 'Unknown')
    
    # Get amortization method from original summary
    amortization_method = original_summary.get('Amortization Method', 'קרן_שווה')
    
    # Create filename with loan parameters
    base_filename = f"loan_{loan_type}_int_{interest_rate}_term_{loan_term_months}_infl_{inflation_rate}_amort_{amortization_method}"
    
    # Save enhanced payments data
    payments_filename = os.path.join(payments_dir, f"{base_filename}_enhanced_payments.csv")
    
    # Create enhanced payments data with investment information
    enhanced_payments = []
    for i, payment in enumerate(monthly_payments):
        enhanced_payment = payment.copy()
        enhanced_payment['monthly_income'] = monthly_income
        enhanced_payment['monthly_investment'] = investment_amounts[i] if i < len(investment_amounts) else 0
        enhanced_payments.append(enhanced_payment)
    
    with open(payments_filename, 'w', newline='', encoding='utf-8') as f:
        if enhanced_payments:
            fieldnames = enhanced_payments[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for payment in enhanced_payments:
                writer.writerow(payment)
    
    # Save enhanced summary
    summary_filename = os.path.join(summary_dir, f"{base_filename}_enhanced_summary.csv")
    
    summary_data = []
    
    # Add original mortgage data
    for key, value in original_summary.items():
        summary_data.append({'Parameter': key, 'Value': value})
    
    # Add investment analysis
    summary_data.append({
        'Parameter': 'Monthly Income',
        'Value': f"{monthly_income:,.2f}"
    })
    summary_data.append({
        'Parameter': 'Total Investment Amount',
        'Value': f"{investment_summary.get('total_invested', 0):,.2f}"
    })
    summary_data.append({
        'Parameter': 'Total Investment Final Value',
        'Value': f"{investment_summary.get('total_final_value', 0):,.2f}"
    })
    summary_data.append({
        'Parameter': 'Total Investment Profit After Tax',
        'Value': f"{investment_summary.get('total_profit_after_tax', 0):,.2f}"
    })
    summary_data.append({
        'Parameter': 'Effective Annual Return After Tax',
        'Value': f"{investment_summary.get('effective_annual_return_after_tax', 0):.2%}"
    })
    
    # Add weighted payment analysis
    summary_data.append({
        'Parameter': 'Weighted Monthly Payment (30 years)',
        'Value': f"{weighted_result.get('weighted_monthly_payment', 0):,.2f}"
    })
    summary_data.append({
        'Parameter': 'Weighted Cost (should be ~0)',
        'Value': f"{weighted_result.get('weighted_cost', 0):,.2f}"
    })
    summary_data.append({
        'Parameter': 'Weighted Investment Profit',
        'Value': f"{weighted_result.get('total_investment_profit', 0):,.2f}"
    })
    summary_data.append({
        'Parameter': 'Weighted Calculation Converged',
        'Value': 'Yes' if weighted_result.get('converged', False) else 'No'
    })
    

    
    with open(summary_filename, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Parameter', 'Value']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in summary_data:
            writer.writerow(row)
    
    return {
        'payments_file': payments_filename,
        'summary_file': summary_filename
    }

def analyze_single_mortgage(payments_file, summary_file, monthly_income=12000):
    """Analyze a single mortgage file"""
    print(f"Analyzing: {payments_file}")
    
    # Load data
    monthly_payments = load_mortgage_data(payments_file)
    original_summary = load_mortgage_summary(summary_file)
    
    if not monthly_payments:
        print("No payment data found")
        return None
    
    # Extract loan amount from summary
    loan_amount_str = original_summary.get('Loan Amount', '0')
    try:
        loan_amount = float(loan_amount_str)
    except:
        # Estimate loan amount from payments
        total_payments = sum(float(payment.get('month_payment', payment.get('payment', 0))) for payment in monthly_payments)
        loan_amount = total_payments * 0.7  # Rough estimate
    
    print(f"Loan amount: {loan_amount:,.2f} NIS")
    print(f"Monthly payments: {len(monthly_payments)}")
    
    # Calculate investment analysis
    investment_summary, investment_amounts = calculate_investment_analysis(monthly_payments, monthly_income)
    
    # Calculate weighted payment analysis
    weighted_result = calculate_weighted_payment_analysis(monthly_payments, loan_amount)
    
    # Save results
    output_files = save_analysis_results(
        original_summary, 
        investment_summary, 
        weighted_result, 
        monthly_income, 
        investment_amounts,
        monthly_payments
    )
    
    print(f"Analysis completed:")
    print(f"  Enhanced payments: {output_files['payments_file']}")
    print(f"  Enhanced summary: {output_files['summary_file']}")
    
    return {
        'original_summary': original_summary,
        'investment_summary': investment_summary,
        'weighted_result': weighted_result,
        'output_files': output_files
    }

def analyze_all_mortgages(raw_data_dir="data/raw", monthly_income=12000):
    """Analyze all mortgage files in the raw data directory"""
    print("Starting analysis of all mortgage files...")
    
    # Find all summary files
    summary_pattern = os.path.join(raw_data_dir, "summary_files", "*_summary.csv")
    summary_files = glob.glob(summary_pattern)
    
    if not summary_files:
        print(f"No summary files found in {summary_pattern}")
        return []
    
    print(f"Found {len(summary_files)} mortgage files to analyze")
    
    results = []
    
    for summary_file in summary_files:
        # Find corresponding payments file
        base_name = os.path.basename(summary_file).replace('_summary.csv', '')
        payments_file = os.path.join(raw_data_dir, "payments_files", f"{base_name}_payments.csv")
        
        if os.path.exists(payments_file):
            try:
                result = analyze_single_mortgage(payments_file, summary_file, monthly_income)
                if result:
                    results.append(result)
                    print(f"✓ Successfully analyzed: {base_name}")
                else:
                    print(f"✗ Failed to analyze: {base_name}")
            except Exception as e:
                print(f"✗ Error analyzing {base_name}: {e}")
        else:
            print(f"✗ Payments file not found: {payments_file}")
    
    print(f"\nAnalysis completed: {len(results)} successful, {len(summary_files) - len(results)} failed")
    
    return results

def main():
    """Main function"""
    import sys
    
    print("Modular Mortgage Analyzer")
    print("=========================")
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print("Usage: python3 modular_analyzer.py [OPTIONS]")
            print("Options:")
            print("  --all                    Analyze all mortgage files in data/raw/")
            print("  --file PAYMENTS SUMMARY  Analyze specific files")
            print("  --income AMOUNT          Set monthly income (default: 12000)")
            print("  --help, -h               Show this help message")
            return
    
    # Default to analyzing all files
    if len(sys.argv) == 1 or '--all' in sys.argv:
        monthly_income = 12000
        for arg in sys.argv:
            if arg.startswith('--income'):
                try:
                    monthly_income = float(arg.split('=')[1])
                except:
                    pass
        
        print(f"Analyzing all mortgages with monthly income: {monthly_income:,.2f} NIS")
        results = analyze_all_mortgages(monthly_income=monthly_income)
        
        if results:
            print(f"\nAnalysis Summary:")
            print(f"  Total analyzed: {len(results)}")
            print(f"  Output directory: data/analyzed/")
            
            # Show some key statistics
            total_investment_profit = sum(r['investment_summary']['total_profit_after_tax'] for r in results)
            avg_weighted_payment = sum(r['weighted_result']['weighted_monthly_payment'] for r in results) / len(results)
            
            print(f"  Total investment profit: {total_investment_profit:,.0f} NIS")
            print(f"  Average weighted payment: {avg_weighted_payment:,.0f} NIS")
    
    elif '--file' in sys.argv:
        # Analyze specific files
        try:
            payments_file = sys.argv[sys.argv.index('--file') + 1]
            summary_file = sys.argv[sys.argv.index('--file') + 2]
            
            monthly_income = 12000
            for arg in sys.argv:
                if arg.startswith('--income'):
                    try:
                        monthly_income = float(arg.split('=')[1])
                    except:
                        pass
            
            print(f"Analyzing specific files with monthly income: {monthly_income:,.2f} NIS")
            result = analyze_single_mortgage(payments_file, summary_file, monthly_income)
            
            if result:
                print("Analysis completed successfully!")
            else:
                print("Analysis failed!")
                
        except IndexError:
            print("Error: --file requires PAYMENTS and SUMMARY file paths")
            print("Usage: python3 modular_analyzer.py --file payments.csv summary.csv")
    
    else:
        print("No action specified. Use --all to analyze all files or --file to analyze specific files.")
        print("Use --help for more information.")

if __name__ == "__main__":
    main() 