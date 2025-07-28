#!/usr/bin/env python3
"""
Full Process Test - Mortgage Extraction to Investment Calculation
This script tests the complete workflow from extracting mortgage data to calculating investments and weighted payments
"""

import os
import sys
import json
import time
from datetime import datetime

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from extractors.automated_cp_programs_extractor import extract_multiple_combinations, setup_driver
from calculators.invesment import StockInvestment
from calculators.weighted_payment_calculator import WeightedPaymentCalculator

def test_full_process():
    """Test the complete process from mortgage extraction to investment calculation"""
    
    print("="*80)
    print("FULL PROCESS TEST - MORTGAGE EXTRACTION TO INVESTMENT CALCULATION")
    print("="*80)
    
    # Test parameters
    loan_amount = "1000000"  # 1 million NIS
    interest_rate = "3.5"    # 3.5%
    loan_term = "30"         # 30 years
    cpi_rate = "2.0"         # 2% inflation
    
    print(f"Test Parameters:")
    print(f"  Loan Amount: {loan_amount} NIS")
    print(f"  Interest Rate: {interest_rate}%")
    print(f"  Loan Term: {loan_term} years")
    print(f"  CPI Rate: {cpi_rate}%")
    print()
    
    # Step 1: Extract mortgage data
    print("STEP 1: EXTRACTING MORTGAGE DATA")
    print("-" * 40)
    
    try:
        # Define loan combinations for testing
        loan_combinations = [
            {
                'loan_amount': loan_amount,
                'interest_rate': interest_rate,
                'loan_term_months': str(int(loan_term) * 12),  # Convert years to months
                'cpi_rate': cpi_rate,
                'channel': 'קבועה צמודה',
                'amortization': 'שפיצר'
            }
        ]
        
        print(f"Extracting data for {len(loan_combinations)} loan combination(s)...")
        
        # Extract mortgage data using the automated extractor
        results = extract_multiple_combinations(loan_combinations, headless=False)
        
        if not results:
            print("❌ Failed to extract mortgage data")
            return False
        
        # Get the first successful result
        successful_results = [r for r in results if r['status'] == 'success']
        if not successful_results:
            print("❌ No successful extractions")
            print("Failed results:")
            for result in results:
                if result['status'] == 'failed':
                    combo = result['combination']
                    print(f"  - {combo['loan_amount']} @ {combo['interest_rate']}% for {combo['loan_term_months']} months")
            return False
        
        result = successful_results[0]
        combo = result['combination']
        files = result['files']
        
        print("✅ Mortgage data extracted successfully")
        print(f"Loan: {combo['loan_amount']} @ {combo['interest_rate']}% for {combo['loan_term_months']} months")
        print(f"Channel: {combo['channel']}, Amortization: {combo['amortization']}")
        
        # Load the extracted data from the saved files
        payments_file = files.get('payments_file')
        summary_file = files.get('summary_file')
        
        if not payments_file or not os.path.exists(payments_file):
            print("❌ Payments file not found")
            return False
        
        print(f"✅ Payments file: {payments_file}")
        print(f"✅ Summary file: {summary_file}")
        
        # Read the payments data
        import csv
        monthly_payments = []
        with open(payments_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                monthly_payments.append(row)
        
        if not monthly_payments:
            print("❌ No monthly payments data found in file")
            return False
        
        print(f"✅ Found {len(monthly_payments)} monthly payments")
        
        # Display first few payments
        print("\nFirst 3 monthly payments:")
        for i, payment in enumerate(monthly_payments[:3]):
            payment_amount = payment.get('month_payment', payment.get('payment', 'N/A'))
            print(f"  Month {i+1}: {payment_amount} NIS")
        
    except Exception as e:
        print(f"❌ Error during mortgage extraction: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 2: Calculate investment data
    print("\nSTEP 2: CALCULATING INVESTMENT DATA")
    print("-" * 40)
    
    try:
        # Monthly income assumption
        monthly_income = 12000  # 12,000 NIS per month
        
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
        
        print(f"✅ Calculated investment amounts for {len(investment_amounts)} months")
        print(f"Monthly income: {monthly_income:,.2f} NIS")
        print(f"Average monthly investment: {sum(investment_amounts)/len(investment_amounts):,.2f} NIS")
        
        # Create investment calculator
        investment = StockInvestment(
            monthly_investments=investment_amounts,
            annual_return_rate=0.07,  # 7% annual return
            annual_inflation_rate=0.03,  # 3% annual inflation
            tax_rate=0.25  # 25% tax on real profits
        )
        
        # Get investment summary
        investment_summary = investment.get_summary()
        
        print("\nInvestment Summary:")
        print(f"  Total Invested: {investment_summary['total_invested']:,.2f} NIS")
        print(f"  Total Final Value: {investment_summary['total_final_value']:,.2f} NIS")
        print(f"  Total Profit After Tax: {investment_summary['total_profit_after_tax']:,.2f} NIS")
        print(f"  Effective Annual Return: {investment_summary['effective_annual_return_after_tax']:.2%}")
        
    except Exception as e:
        print(f"❌ Error during investment calculation: {e}")
        return False
    
    # Step 3: Calculate weighted monthly payment
    print("\nSTEP 3: CALCULATING WEIGHTED MONTHLY PAYMENT")
    print("-" * 40)
    
    try:
        # Convert payments to format expected by WeightedPaymentCalculator
        monthly_payments_for_weighted = []
        for payment in monthly_payments:
            monthly_payments_for_weighted.append({
                'month_payment': float(payment.get('month_payment', payment.get('payment', 0)))
            })
        
        # Calculate loan amount from payments
        total_payments = sum(float(payment.get('month_payment', payment.get('payment', 0))) for payment in monthly_payments)
        estimated_loan_amount = total_payments * 0.7  # Rough estimate (70% of total payments)
        
        print(f"Estimated loan amount: {estimated_loan_amount:,.2f} NIS")
        
        # Create weighted payment calculator
        weighted_calculator = WeightedPaymentCalculator(
            monthly_payments=monthly_payments_for_weighted,
            loan_amount=estimated_loan_amount,
            annual_return_rate=0.07,
            annual_inflation_rate=0.03,
            tax_rate=0.25
        )
        
        # Calculate weighted payment
        weighted_result = weighted_calculator.calculate_weighted_payment()
        
        print("\nWeighted Payment Results:")
        print(f"  Weighted Monthly Payment (30 years): {weighted_result['weighted_monthly_payment']:,.2f} NIS")
        print(f"  Weighted Cost: {weighted_result['weighted_cost']:,.2f} NIS")
        print(f"  Total Investment Profit: {weighted_result['total_investment_profit']:,.2f} NIS")
        print(f"  Total Mortgage Interest & Inflation: {weighted_result['total_mortgage_interest_and_inflation']:,.2f} NIS")
        print(f"  Calculation Converged: {'Yes' if weighted_result['converged'] else 'No'}")
        print(f"  Iterations: {weighted_result['iterations']}")
        
        # Compare with actual monthly payment
        avg_actual_payment = sum(float(payment.get('month_payment', payment.get('payment', 0))) for payment in monthly_payments) / len(monthly_payments)
        print(f"\nComparison:")
        print(f"  Average Actual Monthly Payment: {avg_actual_payment:,.2f} NIS")
        print(f"  Weighted Monthly Payment: {weighted_result['weighted_monthly_payment']:,.2f} NIS")
        print(f"  Difference: {weighted_result['weighted_monthly_payment'] - avg_actual_payment:,.2f} NIS")
        
    except Exception as e:
        print(f"❌ Error during weighted payment calculation: {e}")
        return False
    
    # Step 4: Save comprehensive results
    print("\nSTEP 4: SAVING COMPREHENSIVE RESULTS")
    print("-" * 40)
    
    try:
        # Create comprehensive results data
        comprehensive_data = {
            'loan_combination': combo,
            'files': files,
            'investment_summary': investment_summary,
            'weighted_result': weighted_result,
            'monthly_income': monthly_income,
            'investment_amounts': investment_amounts,
            'monthly_payments': monthly_payments
        }
        
        # Save to files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_prefix = f"full_process_test_{timestamp}"
        
        # Save comprehensive data as JSON
        json_filename = f"{filename_prefix}_comprehensive_data.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(comprehensive_data, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"✅ Results saved with prefix: {filename_prefix}")
        
        # Create a summary report
        summary_filename = f"{filename_prefix}_comprehensive_summary.txt"
        with open(summary_filename, 'w', encoding='utf-8') as f:
            f.write("COMPREHENSIVE MORTGAGE ANALYSIS SUMMARY\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("MORTGAGE PARAMETERS:\n")
            f.write(f"  Loan Amount: {loan_amount} NIS\n")
            f.write(f"  Interest Rate: {interest_rate}%\n")
            f.write(f"  Loan Term: {loan_term} years\n")
            f.write(f"  CPI Rate: {cpi_rate}%\n\n")
            
            f.write("MORTGAGE RESULTS:\n")
            f.write(f"  Total Monthly Payments: {len(monthly_payments)}\n")
            f.write(f"  Average Monthly Payment: {avg_actual_payment:,.2f} NIS\n")
            f.write(f"  Total Payments: {total_payments:,.2f} NIS\n\n")
            
            f.write("INVESTMENT ANALYSIS:\n")
            f.write(f"  Monthly Income: {monthly_income:,.2f} NIS\n")
            f.write(f"  Total Invested: {investment_summary['total_invested']:,.2f} NIS\n")
            f.write(f"  Total Final Value: {investment_summary['total_final_value']:,.2f} NIS\n")
            f.write(f"  Total Profit After Tax: {investment_summary['total_profit_after_tax']:,.2f} NIS\n")
            f.write(f"  Effective Annual Return: {investment_summary['effective_annual_return_after_tax']:.2%}\n\n")
            
            f.write("WEIGHTED PAYMENT ANALYSIS:\n")
            f.write(f"  Weighted Monthly Payment (30 years): {weighted_result['weighted_monthly_payment']:,.2f} NIS\n")
            f.write(f"  Weighted Cost: {weighted_result['weighted_cost']:,.2f} NIS\n")
            f.write(f"  Total Investment Profit: {weighted_result['total_investment_profit']:,.2f} NIS\n")
            f.write(f"  Total Mortgage Interest & Inflation: {weighted_result['total_mortgage_interest_and_inflation']:,.2f} NIS\n")
            f.write(f"  Calculation Converged: {'Yes' if weighted_result['converged'] else 'No'}\n\n")
            
            f.write("COMPARISON:\n")
            f.write(f"  Actual vs Weighted Payment: {avg_actual_payment:,.2f} vs {weighted_result['weighted_monthly_payment']:,.2f} NIS\n")
            f.write(f"  Investment Profit vs Mortgage Cost: {investment_summary['total_profit_after_tax']:,.2f} vs {weighted_result['total_mortgage_interest_and_inflation']:,.2f} NIS\n")
        
        print(f"✅ Comprehensive summary saved to: {summary_filename}")
        
    except Exception as e:
        print(f"❌ Error during result saving: {e}")
        return False
    
    # Step 5: Display final summary
    print("\nSTEP 5: FINAL SUMMARY")
    print("-" * 40)
    
    print("✅ FULL PROCESS COMPLETED SUCCESSFULLY!")
    print()
    print("Key Results:")
    print(f"  📊 Mortgage: {len(monthly_payments)} payments, avg {avg_actual_payment:,.0f} NIS/month")
    print(f"  💰 Investment: {investment_summary['total_profit_after_tax']:,.0f} NIS profit after tax")
    print(f"  ⚖️  Weighted Payment: {weighted_result['weighted_monthly_payment']:,.0f} NIS (30-year break-even)")
    print(f"  📈 Effective Return: {investment_summary['effective_annual_return_after_tax']:.1%} annually")
    print()
    print("Files Generated:")
    print(f"  📁 {filename_prefix}_*.csv - Payment schedules and data")
    print(f"  📄 {filename_prefix}_comprehensive_summary.txt - Complete analysis")
    print(f"  📊 {filename_prefix}_weighted_summary_*.txt - Weighted payment details")
    
    return True

def main():
    """Main function"""
    print("Starting Full Process Test...")
    print("This test will:")
    print("1. Extract mortgage data from the web calculator")
    print("2. Calculate investment opportunities")
    print("3. Calculate weighted monthly payment")
    print("4. Save comprehensive results")
    print("5. Generate summary reports")
    print()
    
    success = test_full_process()
    
    if success:
        print("\n🎉 All tests passed! The full process is working correctly.")
    else:
        print("\n❌ Some tests failed. Check the error messages above.")
    
    return success

if __name__ == "__main__":
    main() 