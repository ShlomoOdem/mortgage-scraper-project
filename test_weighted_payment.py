#!/usr/bin/env python3
"""
Test script for WeightedPaymentCalculator
"""

from src.calculators.weighted_payment_calculator import WeightedPaymentCalculator

def test_weighted_payment():
    """Test the weighted payment calculation with sample data"""
    
    # Sample monthly payments for a 30-year mortgage (simplified)
    # For a 1M NIS loan at 3.5% interest, monthly payment would be around 4,490 NIS
    monthly_payments = []
    for i in range(360):  # 30 years = 360 months
        monthly_payments.append({'month_payment': 4490})  # Fixed monthly payment
    
    loan_amount = 1000000  # 1 million NIS
    annual_return_rate = 0.07  # 7%
    tax_rate = 0.25  # 25%
    
    print("Testing WeightedPaymentCalculator...")
    print(f"Loan Amount: {loan_amount:,.2f} NIS")
    print(f"Monthly Payments: {len(monthly_payments)} months (30 years)")
    print(f"Monthly Payment: {monthly_payments[0]['month_payment']:,.2f} NIS")
    print(f"Annual Return Rate: {annual_return_rate:.1%}")
    print(f"Tax Rate: {tax_rate:.1%}")
    
    # Create calculator
    calculator = WeightedPaymentCalculator(
        monthly_payments=monthly_payments,
        loan_amount=loan_amount,
        annual_return_rate=annual_return_rate,
        tax_rate=tax_rate
    )
    
    # Calculate weighted payment
    result = calculator.calculate_weighted_payment()
    
    print("\nResults:")
    print(f"Weighted Monthly Payment: {result['weighted_monthly_payment']:,.2f} NIS")
    print(f"Weighted Cost: {result['weighted_cost']:,.2f} NIS")
    print(f"Total Investment Profit: {result['total_investment_profit']:,.2f} NIS")
    print(f"Total Mortgage Interest: {result['total_mortgage_interest']:,.2f} NIS")
    print(f"Calculation Converged: {result['converged']}")
    print(f"Iterations: {result['iterations']}")
    
    # Test monthly breakdown
    print("\nMonthly Breakdown (first 3 months):")
    breakdown = calculator.get_monthly_breakdown(result['weighted_monthly_payment'])
    for i, month_data in enumerate(breakdown[:3]):
        print(f"Month {i+1}:")
        print(f"  Actual Payment: {month_data['actual_payment']:,.2f} NIS")
        print(f"  Weighted Payment: {month_data['weighted_payment']:,.2f} NIS")
        print(f"  Difference: {month_data['difference']:,.2f} NIS")
        print(f"  Investment Profit: {month_data['profit_after_tax']:,.2f} NIS")

if __name__ == "__main__":
    test_weighted_payment() 