#!/usr/bin/env python3
"""
Test Modular Process - Demonstrates the modular extraction and analysis workflow
"""

import os
import sys
import csv
import json
from datetime import datetime

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def create_mock_mortgage_data():
    """Create mock mortgage data for testing"""
    print("Creating mock mortgage data...")
    
    # Create directories
    os.makedirs("data/raw/payments_files", exist_ok=True)
    os.makedirs("data/raw/summary_files", exist_ok=True)
    
    # Mock monthly payments for a 30-year mortgage
    monthly_payments = []
    loan_amount = 1000000  # 1M NIS
    monthly_payment = 4490  # Fixed monthly payment
    
    for month in range(1, 361):  # 30 years = 360 months
        payment = {
            'month': month,
            'month_payment': monthly_payment,
            'principal': monthly_payment * 0.3,  # Rough estimate
            'interest': monthly_payment * 0.7,   # Rough estimate
            'balance': loan_amount - (monthly_payment * 0.3 * month)
        }
        monthly_payments.append(payment)
    
    # Save payments file
    payments_filename = "data/raw/payments_files/loan_קבועה_צמודה_int_3.5_term_360_infl_2.0_payments.csv"
    with open(payments_filename, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['month', 'month_payment', 'principal', 'interest', 'balance']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for payment in monthly_payments:
            writer.writerow(payment)
    
    # Save summary file
    summary_filename = "data/raw/summary_files/loan_קבועה_צמודה_int_3.5_term_360_infl_2.0_summary.csv"
    summary_data = [
        {'Parameter': 'Loan Type', 'Value': 'קבועה צמודה'},
        {'Parameter': 'Interest Rate (%)', 'Value': '3.5'},
        {'Parameter': 'Loan Term (months)', 'Value': '360'},
        {'Parameter': 'Inflation Rate (%)', 'Value': '2.0'},
        {'Parameter': 'Loan Amount', 'Value': '1000000'},
        {'Parameter': 'Channel', 'Value': 'קבועה צמודה'},
        {'Parameter': 'Amortization Method', 'Value': 'שפיצר'},
        {'Parameter': 'Total Monthly Payments', 'Value': '360'},
        {'Parameter': 'Total Mortgage Interest', 'Value': '616400.00'},
        {'Parameter': 'Extraction Timestamp', 'Value': datetime.now().strftime("%Y%m%d_%H%M%S")}
    ]
    
    with open(summary_filename, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Parameter', 'Value']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in summary_data:
            writer.writerow(row)
    
    print(f"✅ Created mock data:")
    print(f"  Payments: {payments_filename}")
    print(f"  Summary: {summary_filename}")
    
    return payments_filename, summary_filename

def test_modular_analysis():
    """Test the modular analysis process"""
    print("\n" + "="*60)
    print("TESTING MODULAR ANALYSIS PROCESS")
    print("="*60)
    
    # Step 1: Create mock data (simulating extraction)
    print("\nSTEP 1: CREATING MOCK MORTGAGE DATA")
    print("-" * 40)
    payments_file, summary_file = create_mock_mortgage_data()
    
    # Step 2: Run analysis
    print("\nSTEP 2: RUNNING MODULAR ANALYSIS")
    print("-" * 40)
    
    try:
        from analyzers.modular_analyzer import analyze_single_mortgage
        
        result = analyze_single_mortgage(payments_file, summary_file, monthly_income=12000)
        
        if result:
            print("✅ Analysis completed successfully!")
            
            # Display key results
            investment_summary = result['investment_summary']
            weighted_result = result['weighted_result']
            
            print("\nKey Results:")
            print(f"  📊 Total Invested: {investment_summary['total_invested']:,.0f} NIS")
            print(f"  💰 Investment Profit: {investment_summary['total_profit_after_tax']:,.0f} NIS")
            print(f"  ⚖️  Weighted Payment: {weighted_result['weighted_monthly_payment']:,.0f} NIS")
            print(f"  📈 Effective Return: {investment_summary['effective_annual_return_after_tax']:.1%}")
            
            print(f"\nOutput Files:")
            print(f"  📁 {result['output_files']['payments_file']}")
            print(f"  📄 {result['output_files']['summary_file']}")
            
            return True
        else:
            print("❌ Analysis failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_batch_analysis():
    """Test batch analysis of multiple files"""
    print("\n" + "="*60)
    print("TESTING BATCH ANALYSIS")
    print("="*60)
    
    try:
        from analyzers.modular_analyzer import analyze_all_mortgages
        
        results = analyze_all_mortgages(monthly_income=12000)
        
        if results:
            print(f"✅ Batch analysis completed: {len(results)} files processed")
            
            # Show summary statistics
            total_profit = sum(r['investment_summary']['total_profit_after_tax'] for r in results)
            avg_weighted = sum(r['weighted_result']['weighted_monthly_payment'] for r in results) / len(results)
            
            print(f"\nBatch Results:")
            print(f"  📊 Files analyzed: {len(results)}")
            print(f"  💰 Total profit: {total_profit:,.0f} NIS")
            print(f"  ⚖️  Avg weighted payment: {avg_weighted:,.0f} NIS")
            
            return True
        else:
            print("❌ Batch analysis failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error during batch analysis: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("MODULAR PROCESS TEST")
    print("====================")
    print("This test demonstrates the modular extraction and analysis workflow:")
    print("1. Create mock mortgage data (simulating extraction)")
    print("2. Run modular analysis on the data")
    print("3. Test batch analysis capabilities")
    print()
    
    # Test single analysis
    success1 = test_modular_analysis()
    
    # Test batch analysis
    success2 = test_batch_analysis()
    
    if success1 and success2:
        print("\n🎉 ALL TESTS PASSED!")
        print("\nThe modular process is working correctly:")
        print("  ✅ Data extraction (simulated)")
        print("  ✅ Investment analysis")
        print("  ✅ Weighted payment calculation")
        print("  ✅ Batch processing")
        print("  ✅ File output generation")
    else:
        print("\n❌ Some tests failed!")
    
    return success1 and success2

if __name__ == "__main__":
    main() 