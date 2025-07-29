#!/usr/bin/env python3
"""
Script to rename all existing files to include amortization method in filename.
This script will:
1. Read each summary file to extract the amortization method
2. Rename the file to include the amortization method in the filename
3. Handle both raw and analyzed files
"""

import os
import csv
import re
import shutil
from pathlib import Path

def extract_amortization_from_summary(file_path):
    """Extract amortization method from a summary CSV file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('Parameter') == 'Amortization Method':
                    return row.get('Value', 'קרן_שווה')
        return 'קרן_שווה'  # Default fallback
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 'קרן_שווה'

def create_new_filename(old_filename, amortization_method):
    """Create new filename with amortization method included"""
    # Handle different file patterns
    if '_enhanced_summary.csv' in old_filename:
        # Pattern: loan_[channel]_int_[rate]_term_[months]_infl_[rate]_enhanced_summary.csv
        pattern = r'(loan_.*_int_.*_term_.*_infl_.*)_enhanced_summary\.csv'
        match = re.match(pattern, old_filename)
        if match:
            base = match.group(1)
            return f"{base}_amort_{amortization_method}_enhanced_summary.csv"
    
    elif '_enhanced_payments.csv' in old_filename:
        # Pattern: loan_[channel]_int_[rate]_term_[months]_infl_[rate]_enhanced_payments.csv
        pattern = r'(loan_.*_int_.*_term_.*_infl_.*)_enhanced_payments\.csv'
        match = re.match(pattern, old_filename)
        if match:
            base = match.group(1)
            return f"{base}_amort_{amortization_method}_enhanced_payments.csv"
    
    elif '_summary.csv' in old_filename:
        # Pattern: loan_[channel]_int_[rate]_term_[months]_infl_[rate]_summary.csv
        pattern = r'(loan_.*_int_.*_term_.*_infl_.*)_summary\.csv'
        match = re.match(pattern, old_filename)
        if match:
            base = match.group(1)
            return f"{base}_amort_{amortization_method}_summary.csv"
    
    elif '_payments.csv' in old_filename:
        # Pattern: loan_[channel]_int_[rate]_term_[months]_infl_[rate]_payments.csv
        pattern = r'(loan_.*_int_.*_term_.*_infl_.*)_payments\.csv'
        match = re.match(pattern, old_filename)
        if match:
            base = match.group(1)
            return f"{base}_amort_{amortization_method}_payments.csv"
    
    # If no pattern matches, return original filename
    return old_filename

def rename_files_in_directory(directory_path, file_type):
    """Rename all files in a directory to include amortization method"""
    print(f"\nProcessing {file_type} files in {directory_path}...")
    
    if not os.path.exists(directory_path):
        print(f"Directory {directory_path} does not exist, skipping...")
        return
    
    files = os.listdir(directory_path)
    renamed_count = 0
    error_count = 0
    
    for filename in files:
        if not filename.endswith('.csv'):
            continue
            
        file_path = os.path.join(directory_path, filename)
        
        # For summary files, extract amortization from content
        if 'summary' in filename:
            amortization_method = extract_amortization_from_summary(file_path)
        else:
            # For payment files, we need to find corresponding summary file
            # Extract the base name without extension
            base_name = filename.replace('_payments.csv', '').replace('_enhanced_payments.csv', '')
            
            # Look for corresponding summary file
            summary_filename = base_name + '_summary.csv'
            if 'enhanced' in filename:
                summary_filename = base_name + '_enhanced_summary.csv'
            
            summary_path = os.path.join(directory_path.replace('payments_files', 'summary_files'), summary_filename)
            
            if os.path.exists(summary_path):
                amortization_method = extract_amortization_from_summary(summary_path)
            else:
                print(f"Warning: No corresponding summary file found for {filename}, using default amortization")
                amortization_method = 'קרן_שווה'
        
        # Create new filename
        new_filename = create_new_filename(filename, amortization_method)
        
        if new_filename != filename:
            new_file_path = os.path.join(directory_path, new_filename)
            
            try:
                # Check if target file already exists
                if os.path.exists(new_file_path):
                    print(f"Warning: Target file {new_filename} already exists, skipping {filename}")
                    continue
                
                # Rename the file
                os.rename(file_path, new_file_path)
                print(f"Renamed: {filename} -> {new_filename}")
                renamed_count += 1
                
            except Exception as e:
                print(f"Error renaming {filename}: {e}")
                error_count += 1
        else:
            print(f"No change needed for {filename}")
    
    print(f"Completed {directory_path}: {renamed_count} files renamed, {error_count} errors")

def main():
    """Main function to rename all files"""
    print("Starting file renaming process to include amortization method...")
    
    # Directories to process
    directories = [
        ("data/raw/payments_files", "raw payments"),
        ("data/raw/summary_files", "raw summary"),
        ("data/analyzed/payments_files", "analyzed payments"),
        ("data/analyzed/summary_files", "analyzed summary")
    ]
    
    total_renamed = 0
    total_errors = 0
    
    for directory_path, file_type in directories:
        try:
            rename_files_in_directory(directory_path, file_type)
        except Exception as e:
            print(f"Error processing {directory_path}: {e}")
            total_errors += 1
    
    print(f"\nRenaming process completed!")
    print(f"Total files renamed: {total_renamed}")
    print(f"Total errors: {total_errors}")
    
    # Regenerate the combined summary file
    print("\nRegenerating combined summary file...")
    try:
        import subprocess
        result = subprocess.run(['python3', 'scripts/combine_summary_files.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("Combined summary file regenerated successfully!")
        else:
            print(f"Error regenerating combined summary: {result.stderr}")
    except Exception as e:
        print(f"Error running combine script: {e}")

if __name__ == "__main__":
    main() 