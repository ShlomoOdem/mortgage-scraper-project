#!/usr/bin/env python3
"""
Combination Generator Script
Generates all possible mortgage combinations based on user-defined ranges
"""

import json
import itertools
import os
from typing import List, Dict, Any

def generate_combinations(
    interest_min: float = 2.0,
    interest_max: float = 6.0,
    interest_step: float = 0.25,
    inflation_min: float = 1.0,
    inflation_max: float = 4.0,
    inflation_step: float = 0.25,
    term_min: int = 60,
    term_max: int = 360,
    term_step: int = 12,
    loan_amount: str = "1000000",
    output_dir: str = "data",
    combinations_per_file: int = 5000
) -> List[str]:
    """
    Generate all possible mortgage combinations and split into multiple files
    
    Args:
        interest_min/max/step: Interest rate range and step
        inflation_min/max/step: Inflation rate range and step  
        term_min/max/step: Loan term range and step (in months)
        loan_amount: Fixed loan amount
        output_dir: Output directory for files
        combinations_per_file: Number of combinations per file
    
    Returns:
        List of generated file paths
    """
    
    # Define all possible channels and amortization methods
    channels = [
        "קבועה צמודה",
        "קבועה לא צמודה", 
        "פריים",
        "משתנה צמודה",
        "משתנה לא צמודה",
        "זכאות"
    ]
    
    amortization_methods = [
        "שפיצר",
        "קרן שווה",
    ]
    
    # Generate ranges
    interest_rates = [round(interest_min + i * interest_step, 2) 
                     for i in range(int((interest_max - interest_min) / interest_step) + 1)]
    
    inflation_rates = [round(inflation_min + i * inflation_step, 1)
                      for i in range(int((inflation_max - inflation_min) / inflation_step) + 1)]
    
    loan_terms = list(range(term_min, term_max + 1, term_step))
    
    print(f"Generating combinations with:")
    print(f"  Interest rates: {interest_min}% to {interest_max}% (step: {interest_step}%)")
    print(f"  Inflation rates: {inflation_min}% to {inflation_max}% (step: {inflation_step}%)")
    print(f"  Loan terms: {term_min} to {term_max} months (step: {term_step})")
    print(f"  Channels: {len(channels)} options")
    print(f"  Amortization methods: {len(amortization_methods)} options")
    print(f"  Loan amount: {loan_amount}")
    
    # Calculate total combinations
    total_combinations = (len(interest_rates) * len(inflation_rates) * len(loan_terms) * 
                         len(channels) * len(amortization_methods))
    
    print(f"\nTotal possible combinations: {total_combinations:,}")
    print(f"Combinations per file: {combinations_per_file:,}")
    
    # Generate all combinations
    combinations = []
    
    for interest_rate in interest_rates:
        for inflation_rate in inflation_rates:
            for loan_term in loan_terms:
                for channel in channels:
                    if (channel == "משתנה לא צמודה" or channel == "משתנה צמודה") and (loan_term % 60 != 0):
                        continue
                    for amortization in amortization_methods:
                        combination = {
                            'loan_amount': loan_amount,
                            'interest_rate': str(interest_rate),
                            'loan_term_months': str(loan_term),
                            'cpi_rate': str(inflation_rate),
                            'channel': channel,
                            'amortization': amortization
                        }
                        combinations.append(combination)
    
    print(f"Generated {len(combinations):,} combinations")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Split combinations into files
    file_paths = []
    total_files = (len(combinations) + combinations_per_file - 1) // combinations_per_file
    
    print(f"\nSplitting into {total_files} files...")
    
    for i in range(0, len(combinations), combinations_per_file):
        file_index = i // combinations_per_file + 1
        chunk = combinations[i:i + combinations_per_file]
        
        # Create filename with index
        filename = f"combinations_{file_index:03d}.json"
        file_path = os.path.join(output_dir, filename)
        
        # Save chunk to file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(chunk, f, ensure_ascii=False, indent=2)
        
        file_paths.append(file_path)
        print(f"  Saved file {file_index}/{total_files}: {filename} ({len(chunk):,} combinations)")
    
    # Create a master index file
    index_file = os.path.join(output_dir, "combinations_index.json")
    index_data = {
        "total_combinations": len(combinations),
        "total_files": total_files,
        "combinations_per_file": combinations_per_file,
        "files": [
            {
                "file": os.path.basename(file_path),
                "combinations": len(json.load(open(file_path, 'r', encoding='utf-8')))
            }
            for file_path in file_paths
        ],
        "parameters": {
            "interest_min": interest_min,
            "interest_max": interest_max,
            "interest_step": interest_step,
            "inflation_min": inflation_min,
            "inflation_max": inflation_max,
            "inflation_step": inflation_step,
            "term_min": term_min,
            "term_max": term_max,
            "term_step": term_step,
            "loan_amount": loan_amount,
            "channels": channels,
            "amortization_methods": amortization_methods
        }
    }
    
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Successfully generated {len(combinations):,} combinations")
    print(f"📁 Saved to {total_files} files in: {output_dir}/")
    print(f"📋 Index file: {index_file}")
    
    return file_paths

def main():
    """Main function with example usage"""
    
    # Generate combinations
    file_paths = generate_combinations()
    
    print(f"\nYou can now use these files with the workflow:")
    print(f"  # Check status of first file")
    print(f"  python3 run_modular_workflow.py --combination-file data/combinations_001.json --status")
    print(f"  # Process all files")
    for file_path in file_paths[:3]:  # Show first 3 files as example
        print(f"  python3 run_modular_workflow.py --combination-file {file_path} --extract")
    if len(file_paths) > 3:
        print(f"  # ... and {len(file_paths) - 3} more files")

if __name__ == "__main__":
    main() 