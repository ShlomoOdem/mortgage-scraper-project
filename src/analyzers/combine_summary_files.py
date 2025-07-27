#!/usr/bin/env python3
"""
Combine Summary Files Script
Combines all summary CSV files from summary_files/ into one comprehensive CSV file
"""

import os
import csv
import glob
import pandas as pd
from datetime import datetime

def combine_summary_files():
    """Combine all summary files into one comprehensive CSV"""
    
    summary_dir = "summary_files"
    output_file = f"combined_mortgage_summaries_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    print("="*80)
    print("COMBINING MORTGAGE SUMMARY FILES")
    print("="*80)
    
    # Check if summary_files directory exists
    if not os.path.exists(summary_dir):
        print(f"Error: Directory '{summary_dir}' not found!")
        return False
    
    # Find all summary CSV files
    summary_files = glob.glob(os.path.join(summary_dir, "*_summary.csv"))
    
    if not summary_files:
        print(f"No summary files found in '{summary_dir}' directory!")
        return False
    
    print(f"Found {len(summary_files)} summary files")
    
    # List of all data to combine
    all_data = []
    
    # Process each summary file
    for i, file_path in enumerate(summary_files, 1):
        filename = os.path.basename(file_path)
        print(f"Processing {i}/{len(summary_files)}: {filename}")
        
        try:
            # Read the CSV file
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                # Create a row for this mortgage
                mortgage_data = {}
                
                # Extract data from the summary file
                for row in reader:
                    parameter = row.get('Parameter', '')
                    value = row.get('Value', '')
                    
                    # Map parameters to standardized column names
                    if 'Loan Type' in parameter:
                        mortgage_data['loan_type'] = value
                    elif 'Interest Rate' in parameter:
                        mortgage_data['interest_rate'] = value
                    elif 'Loan Term' in parameter:
                        mortgage_data['loan_term_months'] = value
                    elif 'Inflation Rate' in parameter:
                        mortgage_data['inflation_rate'] = value
                    elif 'Loan Amount' in parameter:
                        mortgage_data['loan_amount'] = value
                    elif 'Channel' in parameter:
                        mortgage_data['channel'] = value
                    elif 'Amortization Method' in parameter:
                        mortgage_data['amortization_method'] = value
                    elif 'Total Monthly Payments' in parameter:
                        mortgage_data['total_monthly_payments'] = value
                    elif 'Total Mortgage Interest' in parameter:
                        mortgage_data['total_mortgage_interest'] = value
                    elif 'Total Investment Amount' in parameter:
                        mortgage_data['total_investment_amount'] = value
                    elif 'Total Investment Final Value' in parameter:
                        mortgage_data['total_investment_final_value'] = value
                    elif 'Total Investment Profit' in parameter:
                        mortgage_data['total_investment_profit'] = value
                    elif 'Total Investment Taxes' in parameter:
                        mortgage_data['total_investment_taxes'] = value
                    elif 'Total Investment Profit After Tax' in parameter:
                        mortgage_data['total_investment_profit_after_tax'] = value
                    elif 'Total Investment Net Value After Tax' in parameter:
                        mortgage_data['total_investment_net_value_after_tax'] = value
                    elif 'Total Cost' in parameter:
                        mortgage_data['total_cost_interest_minus_profit'] = value
                    elif 'Weighted Monthly Payment' in parameter:
                        mortgage_data['weighted_monthly_payment'] = value
                    elif 'Weighted Cost' in parameter:
                        mortgage_data['weighted_cost'] = value
                    elif 'Weighted Investment Profit' in parameter:
                        mortgage_data['weighted_investment_profit'] = value
                    elif 'Weighted Calculation Converged' in parameter:
                        mortgage_data['weighted_calculation_converged'] = value
                    elif 'Extraction Timestamp' in parameter:
                        mortgage_data['extraction_timestamp'] = value
                
                # Add filename for reference
                mortgage_data['source_file'] = filename
                
                # Add to the combined data
                all_data.append(mortgage_data)
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue
    
    if not all_data:
        print("No data extracted from summary files!")
        return False
    
    # Create comprehensive CSV with all data
    print(f"\nCreating combined CSV file: {output_file}")
    
    # Define the column order
    columns = [
        'loan_type', 'interest_rate', 'loan_term_months', 'inflation_rate', 
        'loan_amount', 'channel', 'amortization_method', 'total_monthly_payments',
        'total_mortgage_interest', 'total_investment_amount', 'total_investment_final_value',
        'total_investment_profit', 'total_investment_taxes', 'total_investment_profit_after_tax',
        'total_investment_net_value_after_tax', 'total_cost_interest_minus_profit',
        'extraction_timestamp', 'source_file'
    ]
    
    # Write the combined CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        
        for data in all_data:
            # Ensure all columns exist in the data
            row = {}
            for col in columns:
                row[col] = data.get(col, '')
            writer.writerow(row)
    
    print(f"Successfully created combined file: {output_file}")
    print(f"Total mortgages combined: {len(all_data)}")
    
    # Create a summary report
    print(f"\n{'SUMMARY REPORT':-^80}")
    
    # Count by loan type
    loan_types = {}
    for data in all_data:
        loan_type = data.get('loan_type', 'Unknown')
        loan_types[loan_type] = loan_types.get(loan_type, 0) + 1
    
    print("Mortgages by Loan Type:")
    for loan_type, count in sorted(loan_types.items()):
        print(f"  {loan_type}: {count}")
    
    # Count by amortization method
    amortization_methods = {}
    for data in all_data:
        method = data.get('amortization_method', 'Unknown')
        amortization_methods[method] = amortization_methods.get(method, 0) + 1
    
    print("\nMortgages by Amortization Method:")
    for method, count in sorted(amortization_methods.items()):
        print(f"  {method}: {count}")
    
    # Show some statistics
    print(f"\nFile Statistics:")
    print(f"  Total mortgages: {len(all_data)}")
    print(f"  Output file: {output_file}")
    print(f"  File size: {os.path.getsize(output_file):,} bytes")
    
    return True

def create_analysis_summary():
    """Create a quick analysis summary of the combined data"""
    
    # Find the most recent combined file
    combined_files = glob.glob("combined_mortgage_summaries_*.csv")
    if not combined_files:
        print("No combined summary file found. Run combine_summary_files() first.")
        return
    
    latest_file = max(combined_files, key=os.path.getmtime)
    print(f"\nAnalyzing: {latest_file}")
    
    try:
        # Read the combined data
        df = pd.read_csv(latest_file)
        
        print(f"\n{'QUICK ANALYSIS':-^80}")
        print(f"Total mortgages analyzed: {len(df)}")
        
        # Convert numeric columns
        numeric_cols = ['interest_rate', 'loan_term_months', 'inflation_rate', 'loan_amount',
                       'total_mortgage_interest', 'total_investment_amount', 
                       'total_investment_final_value', 'total_investment_profit',
                       'total_investment_taxes', 'total_investment_profit_after_tax',
                       'total_investment_net_value_after_tax', 'total_cost_interest_minus_profit',
                       'weighted_monthly_payment', 'weighted_cost', 'weighted_investment_profit']
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Show some key statistics
        if 'total_cost_interest_minus_profit' in df.columns:
            print(f"\nCost Analysis (Interest - Investment Profit):")
            print(f"  Average cost: {df['total_cost_interest_minus_profit'].mean():.2f}")
            print(f"  Minimum cost: {df['total_cost_interest_minus_profit'].min():.2f}")
            print(f"  Maximum cost: {df['total_cost_interest_minus_profit'].max():.2f}")
        
        if 'total_investment_profit_after_tax' in df.columns:
            print(f"\nInvestment Profit After Tax:")
            print(f"  Average profit: {df['total_investment_profit_after_tax'].mean():.2f}")
            print(f"  Total profit across all mortgages: {df['total_investment_profit_after_tax'].sum():.2f}")
        
        # Show weighted payment statistics
        if 'weighted_monthly_payment' in df.columns:
            print(f"\nWeighted Monthly Payment Analysis:")
            print(f"  Average weighted payment: {df['weighted_monthly_payment'].mean():.2f} NIS")
            print(f"  Minimum weighted payment: {df['weighted_monthly_payment'].min():.2f} NIS")
            print(f"  Maximum weighted payment: {df['weighted_monthly_payment'].max():.2f} NIS")
            
            # Show best and worst by weighted payment
            best_weighted = df.loc[df['weighted_monthly_payment'].idxmin()]
            worst_weighted = df.loc[df['weighted_monthly_payment'].idxmax()]
            
            print(f"\nBest Mortgage (Lowest Weighted Payment):")
            print(f"  Type: {best_weighted['loan_type']}")
            print(f"  Interest: {best_weighted['interest_rate']}%")
            print(f"  Term: {best_weighted['loan_term_months']} months")
            print(f"  Weighted Payment: {best_weighted['weighted_monthly_payment']:.2f} NIS")
            
            print(f"\nWorst Mortgage (Highest Weighted Payment):")
            print(f"  Type: {worst_weighted['loan_type']}")
            print(f"  Interest: {worst_weighted['interest_rate']}%")
            print(f"  Term: {worst_weighted['loan_term_months']} months")
            print(f"  Weighted Payment: {worst_weighted['weighted_monthly_payment']:.2f} NIS")
        
        # Show best and worst mortgages by cost
        if 'total_cost_interest_minus_profit' in df.columns:
            best_mortgage = df.loc[df['total_cost_interest_minus_profit'].idxmin()]
            worst_mortgage = df.loc[df['total_cost_interest_minus_profit'].idxmax()]
            
            print(f"\nBest Mortgage (Lowest Cost):")
            print(f"  Type: {best_mortgage['loan_type']}")
            print(f"  Interest: {best_mortgage['interest_rate']}%")
            print(f"  Term: {best_mortgage['loan_term_months']} months")
            print(f"  Cost: {best_mortgage['total_cost_interest_minus_profit']:.2f}")
            
            print(f"\nWorst Mortgage (Highest Cost):")
            print(f"  Type: {worst_mortgage['loan_type']}")
            print(f"  Interest: {worst_mortgage['interest_rate']}%")
            print(f"  Term: {worst_mortgage['loan_term_months']} months")
            print(f"  Cost: {worst_mortgage['total_cost_interest_minus_profit']:.2f}")
        
    except Exception as e:
        print(f"Error analyzing data: {e}")

def main():
    """Main function"""
    print("Mortgage Summary File Combiner")
    print("="*50)
    
    # Combine the files
    success = combine_summary_files()
    
    if success:
        # Create analysis summary
        create_analysis_summary()
        
        print(f"\n{'SUCCESS':-^80}")
        print("All summary files have been combined into one comprehensive CSV file!")
        print("You can now analyze all mortgage scenarios in one place.")
        print("\nNext steps:")
        print("1. Open the combined CSV file in Excel or Google Sheets")
        print("2. Use the data for further analysis and comparison")
        print("3. Create charts and visualizations")
        print("4. Identify the best mortgage options for different scenarios")
    else:
        print("Failed to combine summary files. Check the error messages above.")

if __name__ == "__main__":
    main() 