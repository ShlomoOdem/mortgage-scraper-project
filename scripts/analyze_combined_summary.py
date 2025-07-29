#!/usr/bin/env python3
"""
Analyze the combined summary file and show key statistics
"""

import pandas as pd
import os

def analyze_combined_summary():
    """Analyze the combined summary file"""
    
    file_path = "data/analyzed/combined_summary_files.csv"
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    print("Analyzing Combined Summary File")
    print("===============================")
    
    # Read the CSV file
    print("Loading data...")
    df = pd.read_csv(file_path)
    
    print(f"\nFile Information:")
    print(f"  Total rows: {len(df):,}")
    print(f"  Total columns: {len(df.columns)}")
    print(f"  File size: {os.path.getsize(file_path) / (1024*1024):.1f} MB")
    
    print(f"\nColumn Information:")
    for col in df.columns:
        print(f"  {col}: {df[col].dtype}")
    
    print(f"\nKey Statistics:")
    
    # Channel distribution
    if 'Channel' in df.columns:
        channel_counts = df['Channel'].value_counts()
        print(f"\nChannel Distribution:")
        for channel, count in channel_counts.items():
            print(f"  {channel}: {count:,} ({count/len(df)*100:.1f}%)")
    
    # Interest rate statistics
    if 'Interest_Rate' in df.columns:
        print(f"\nInterest Rate Statistics:")
        print(f"  Min: {df['Interest_Rate'].min():.2f}%")
        print(f"  Max: {df['Interest_Rate'].max():.2f}%")
        print(f"  Mean: {df['Interest_Rate'].mean():.2f}%")
        print(f"  Unique values: {df['Interest_Rate'].nunique()}")
    
    # Term statistics
    if 'Term_Months' in df.columns:
        print(f"\nTerm Statistics:")
        print(f"  Min: {df['Term_Months'].min()} months")
        print(f"  Max: {df['Term_Months'].max()} months")
        print(f"  Mean: {df['Term_Months'].mean():.1f} months")
        print(f"  Unique values: {df['Term_Months'].nunique()}")
    
    # Inflation rate statistics
    if 'Inflation_Rate' in df.columns:
        print(f"\nInflation Rate Statistics:")
        print(f"  Min: {df['Inflation_Rate'].min():.2f}%")
        print(f"  Max: {df['Inflation_Rate'].max():.2f}%")
        print(f"  Mean: {df['Inflation_Rate'].mean():.2f}%")
        print(f"  Unique values: {df['Inflation_Rate'].nunique()}")
    
    # Weighted payment statistics
    if 'Weighted Monthly Payment (30 years)' in df.columns:
        # Convert to numeric, removing any currency symbols and commas
        weighted_payments = pd.to_numeric(df['Weighted Monthly Payment (30 years)'].str.replace('$', '').str.replace(',', ''), errors='coerce')
        print(f"\nWeighted Monthly Payment Statistics:")
        print(f"  Min: ${weighted_payments.min():,.2f}")
        print(f"  Max: ${weighted_payments.max():,.2f}")
        print(f"  Mean: ${weighted_payments.mean():,.2f}")
    
    # Investment profit statistics
    if 'Total Investment Profit After Tax' in df.columns:
        # Convert to numeric, removing any currency symbols and commas
        profits = pd.to_numeric(df['Total Investment Profit After Tax'].str.replace('$', '').str.replace(',', ''), errors='coerce')
        print(f"\nInvestment Profit After Tax Statistics:")
        print(f"  Min: ${profits.min():,.2f}")
        print(f"  Max: ${profits.max():,.2f}")
        print(f"  Mean: ${profits.mean():,.2f}")
    
    print(f"\nSample Data (first 3 rows):")
    print(df.head(3).to_string())

if __name__ == "__main__":
    analyze_combined_summary() 