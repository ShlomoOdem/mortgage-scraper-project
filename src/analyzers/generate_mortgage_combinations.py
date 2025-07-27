#!/usr/bin/env python3
"""
Generate All Mortgage Combinations Script
Creates comprehensive mortgage combinations based on interest rate tables
"""

import json
from datetime import datetime

def generate_mortgage_combinations():
    """Generate all mortgage combinations based on the interest rate tables"""
    
    # Fixed parameters
    loan_amount = "100000"
    
    # Loan terms in months (multiples of 5 years)
    loan_terms_months = [30,60,90, 120,150, 180,210,240,270, 300, 330, 360]  # 5, 10, 15, 20, 25, 30 years
    
    # Inflation rates
    inflation_rates = ["1.0", "2.0", "3.0", "4.0"]
    
    # Amortization methods
    amortization_methods = ["שפיצר", "קרן שווה", "בוליט"]
    
    # Interest rate tables based on the images
    # No inflation loans (Prime, Fixed Unlinked, Variable Unlinked Every 5)
    no_inflation_rates = {
        30: 5.04,    # From 1 to 5 years
        60: 5.04,   # From 5 to 10 years
        90: 4.92,   # From 10 to 15 years
        120: 4.92,   # From 15 to 20 years
        150: 4.83,   # From 20 to 25 years
        180: 4.83,   # More than 25 years
        210: 4.96,   # More than 25 years
        240: 4.96,   # More than 25 years
        270: 4.97,   # More than 25 years
        300: 4.97,   # More than 25 years
        330: 5.05,   # More than 25 years
        360: 5.05    # More than 25 years
    }
    
    # Inflation-adjusted loans (Fixed Linked, Variable Linked Every 5, Eligibility, Euro, Dollar, etc.)
    inflation_adjusted_rates = {
        30: 3.83,    # Up to and including 5 years
        60: 3.83,    # Up to and including 5 years
        90: 3.45,   # From 5 to 10 years
        120: 3.45,   # From 5 to 10 years
        150: 3.35,   # From 10 to 15 years
        180: 3.35,   # From 10 to 15 years
        210: 3.67,   # From 15 to 20 years
        240: 3.67,   # From 20 to 25 years
        270: 3.63,   # From 20 to 25 years
        300: 3.63,   # From 20 to 25 years
        330: 3.55,   # From 20 to 25 years
        360: 3.55    # More than 25 years
    }
    
    # Channel definitions
    no_inflation_channels = [
        "פריים",                    # Prime
        "קבועה לא צמודה",           # Fixed Unlinked
        "משתנה לא צמודה כל 5"       # Variable Unlinked Every 5
    ]
    
    inflation_adjusted_channels = [
        "קבועה צמודה",              # Fixed Linked
        "משתנה צמודה כל 5",         # Variable Linked Every 5
        "זכאות",                    # Eligibility
        "יורו",                     # Euro
        "דולר",                     # Dollar
        "עוגן מק\"מ",               # Anchor Makam
        "משתנה צמודה כל שנה",       # Variable Linked Every Year
        "משתנה צמודה כל 2",         # Variable Linked Every 2
        "משתנה צמודה כל 10"         # Variable Linked Every 10
    ]
    
    combinations = []
    
    # Generate combinations for no inflation loans
    for loan_term_months in loan_terms_months:
        interest_rate = no_inflation_rates[loan_term_months]
        for channel in no_inflation_channels:
            for inflation_rate in inflation_rates:
                for amortization in amortization_methods:
                    combination = {
                        'loan_amount': loan_amount,
                        'interest_rate': str(interest_rate),
                        'loan_term_months': str(loan_term_months),
                        'cpi_rate': inflation_rate,
                        'channel': channel,
                        'amortization': amortization
                    }
                    combinations.append(combination)
    
    # Generate combinations for inflation-adjusted loans
    for loan_term_months in loan_terms_months:
        interest_rate = inflation_adjusted_rates[loan_term_months]
        for channel in inflation_adjusted_channels:
            for inflation_rate in inflation_rates:
                for amortization in amortization_methods:
                    combination = {
                        'loan_amount': loan_amount,
                        'interest_rate': str(interest_rate),
                        'loan_term_months': str(loan_term_months),
                        'cpi_rate': inflation_rate,
                        'channel': channel,
                        'amortization': amortization
                    }
                    combinations.append(combination)
    
    return combinations

def save_combinations_to_file(combinations, filename=None):
    """Save combinations to a JSON file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mortgage_combinations_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(combinations, f, ensure_ascii=False, indent=2)
    
    return filename

def print_summary(combinations):
    """Print a summary of the generated combinations"""
    print(f"\n{'='*80}")
    print(f"MORTGAGE COMBINATIONS SUMMARY")
    print(f"{'='*80}")
    print(f"Total combinations generated: {len(combinations)}")
    
    # Count by channel type
    no_inflation_count = sum(1 for c in combinations if c['channel'] in ["פריים", "קבועה לא צמודה", "משתנה לא צמודה כל 5"])
    inflation_adjusted_count = len(combinations) - no_inflation_count
    
    print(f"No inflation loans: {no_inflation_count}")
    print(f"Inflation-adjusted loans: {inflation_adjusted_count}")
    
    # Count by loan term
    term_counts = {}
    for combo in combinations:
        term = combo['loan_term_months']
        term_counts[term] = term_counts.get(term, 0) + 1
    
    print(f"\nCombinations by loan term:")
    for term in sorted(term_counts.keys(), key=int):
        years = int(term) // 12
        print(f"  {term} months ({years} years): {term_counts[term]} combinations")
    
    # Show sample combinations
    print(f"\nSample combinations:")
    for i, combo in enumerate(combinations[:5]):
        print(f"  {i+1}. {combo['loan_amount']} @ {combo['interest_rate']}% for {combo['loan_term_months']} months")
        print(f"     Channel: {combo['channel']}, Amortization: {combo['amortization']}, CPI: {combo['cpi_rate']}%")
    
    if len(combinations) > 5:
        print(f"  ... and {len(combinations) - 5} more combinations")

def main():
    """Main function"""
    print("Generating All Mortgage Combinations")
    print("====================================")
    
    # Generate combinations
    combinations = generate_mortgage_combinations()
    
    # Print summary
    print_summary(combinations)
    
    # Save to file
    filename = save_combinations_to_file(combinations)
    print(f"\nCombinations saved to: {filename}")
    
    # Also save a smaller test set
    test_combinations = combinations[:20]  # First 20 combinations for testing
    test_filename = save_combinations_to_file(test_combinations, "test_mortgage_combinations.json")
    print(f"Test set (first 20) saved to: {test_filename}")
    
    print(f"\nReady to use with automated_cp_programs_extractor.py!")
    print(f"Copy the combinations from {filename} to the loan_combinations list in the main script.")

if __name__ == "__main__":
    main() 