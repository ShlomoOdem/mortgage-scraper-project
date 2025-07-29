#!/usr/bin/env python3
"""
Combine all summary files from data/analyzed/summary_files into one comprehensive CSV file.
This script will:
1. Read all summary files in the directory
2. Extract filename information as additional columns
3. Combine them into one CSV file with all data
"""

import os
import csv
import glob
import re
from datetime import datetime

def parse_filename_info(filename):
    """Extract information from the filename"""
    # Remove the .csv extension and get the base name
    base_name = os.path.splitext(os.path.basename(filename))[0]
    
    # Parse the filename pattern: loan_[channel]_int_[rate]_term_[months]_infl_[rate]_amort_[method]_enhanced_summary
    pattern = r'loan_(.+)_int_([\d.]+)_term_(\d+)_infl_([\d.]+)_amort_(.+)_enhanced_summary'
    match = re.match(pattern, base_name)
    
    if match:
        channel = match.group(1)
        interest_rate = float(match.group(2))
        term_months = int(match.group(3))
        inflation_rate = float(match.group(4))
        amortization_method = match.group(5)
        
        return {
            'filename': base_name,
            'channel': channel,
            'interest_rate': interest_rate,
            'term_months': term_months,
            'inflation_rate': inflation_rate,
            'amortization_method': amortization_method
        }
    else:
        # Try the old pattern without amortization for backward compatibility
        old_pattern = r'loan_(.+)_int_([\d.]+)_term_(\d+)_infl_([\d.]+)_enhanced_summary'
        match = re.match(old_pattern, base_name)
        
        if match:
            channel = match.group(1)
            interest_rate = float(match.group(2))
            term_months = int(match.group(3))
            inflation_rate = float(match.group(4))
            
            return {
                'filename': base_name,
                'channel': channel,
                'interest_rate': interest_rate,
                'term_months': term_months,
                'inflation_rate': inflation_rate,
                'amortization_method': 'Unknown'
            }
        else:
            # Fallback for files that don't match any pattern
            return {
                'filename': base_name,
                'channel': 'Unknown',
                'interest_rate': 0.0,
                'term_months': 0,
                'inflation_rate': 0.0,
                'amortization_method': 'Unknown'
            }

def read_summary_file(filepath):
    """Read a single summary file and return its data as a dictionary"""
    data = {}
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                parameter = row['Parameter']
                value = row['Value']
                data[parameter] = value
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None
    
    return data

def combine_summary_files():
    """Combine all summary files into one comprehensive CSV file"""
    
    # Define paths
    summary_dir = "data/analyzed/summary_files"
    output_file = "data/analyzed/combined_summary_files.csv"
    
    # Get all CSV files in the directory (excluding lock files)
    csv_files = glob.glob(os.path.join(summary_dir, "*.csv"))
    csv_files = [f for f in csv_files if not f.endswith('#') and not '.~lock.' in f]
    
    print(f"Found {len(csv_files)} summary files to combine")
    
    if not csv_files:
        print("No summary files found!")
        return
    
    # Prepare the combined data
    combined_data = []
    
    for filepath in csv_files:
        print(f"Processing: {os.path.basename(filepath)}")
        
        # Parse filename information
        filename_info = parse_filename_info(filepath)
        
        # Read the summary file
        summary_data = read_summary_file(filepath)
        
        if summary_data:
            # Combine filename info with summary data
            row_data = {
                'Filename': filename_info['filename'],
                'Channel': filename_info['channel'],
                'Interest_Rate': filename_info['interest_rate'],
                'Term_Months': filename_info['term_months'],
                'Inflation_Rate': filename_info['inflation_rate'],
                'Amortization_Method': filename_info['amortization_method']
            }
            
            # Add all summary data
            row_data.update(summary_data)
            
            combined_data.append(row_data)
        else:
            print(f"  Skipped due to error: {os.path.basename(filepath)}")
    
    if not combined_data:
        print("No valid data to combine!")
        return
    
    # Write the combined data to CSV
    try:
        # Get all unique column names
        all_columns = set()
        for row in combined_data:
            all_columns.update(row.keys())
        
        # Sort columns for consistent output
        column_order = [
            'Filename', 'Channel', 'Interest_Rate', 'Term_Months', 'Inflation_Rate', 'Amortization_Method',
            'Loan Type', 'Interest Rate (%)', 'Loan Term (months)', 'Inflation Rate (%)',
            'Loan Amount', 'Amortization Method', 'Total Monthly Payments',
            'Total Mortgage Interest', 'Extraction Timestamp', 'Monthly Income',
            'Total Investment Amount', 'Total Investment Final Value',
            'Total Investment Profit After Tax', 'Effective Annual Return After Tax',
            'Weighted Monthly Payment (30 years)', 'Weighted Cost (should be ~0)',
            'Weighted Investment Profit', 'Weighted Calculation Converged'
        ]
        
        # Add any additional columns that might exist
        for col in sorted(all_columns):
            if col not in column_order:
                column_order.append(col)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=column_order)
            writer.writeheader()
            
            for row in combined_data:
                # Ensure all columns exist in the row
                for col in column_order:
                    if col not in row:
                        row[col] = ''
                
                writer.writerow(row)
        
        print(f"\nSuccessfully combined {len(combined_data)} summary files")
        print(f"Output file: {output_file}")
        print(f"Total rows: {len(combined_data)}")
        print(f"Total columns: {len(column_order)}")
        
        # Show some statistics
        channels = set(row['Channel'] for row in combined_data)
        interest_rates = set(row['Interest_Rate'] for row in combined_data)
        terms = set(row['Term_Months'] for row in combined_data)
        inflation_rates = set(row['Inflation_Rate'] for row in combined_data)
        
        print(f"\nSummary Statistics:")
        print(f"  Channels: {len(channels)} ({', '.join(sorted(channels))})")
        print(f"  Interest Rates: {len(interest_rates)} (range: {min(interest_rates)} - {max(interest_rates)}%)")
        print(f"  Terms: {len(terms)} (range: {min(terms)} - {max(terms)} months)")
        print(f"  Inflation Rates: {len(inflation_rates)} (range: {min(inflation_rates)} - {max(inflation_rates)}%)")
        
    except Exception as e:
        print(f"Error writing combined file: {e}")

def main():
    """Main function"""
    print("Combining Summary Files")
    print("======================")
    
    combine_summary_files()

if __name__ == "__main__":
    main() 