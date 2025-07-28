"""
Weighted Monthly Payment Calculator for Mortgage Analysis
Calculates the weighted monthly payment that represents the break-even cost of a mortgage
"""

from typing import List, Dict, Any
import math


class WeightedPaymentCalculator:
    """
    Calculates the weighted monthly payment for mortgage analysis.
    
    The weighted monthly payment is a fixed payment amount for 30 years that represents
    the break-even cost of a mortgage, accounting for investment opportunities.
    """
    
    def __init__(self, monthly_payments: List[Dict[str, Any]], loan_amount: float, 
                 annual_return_rate: float = 0.07, annual_inflation_rate: float = 0.00, tax_rate: float = 0.25):
        """
        Initialize the weighted payment calculator.
        
        Args:
            monthly_payments: List of monthly payment dictionaries with 'month_payment' key
            loan_amount: Original loan amount
            annual_return_rate: Annual return rate for investments (default 7%)
            annual_inflation_rate: Annual inflation rate (default 3%)
            tax_rate: Tax rate on investment profits (default 25%)
        """
        self.monthly_payments = monthly_payments
        self.loan_amount = loan_amount
        self.annual_return_rate = annual_return_rate
        self.annual_inflation_rate = annual_inflation_rate
        self.tax_rate = tax_rate
        self.monthly_return_rate = (1 + annual_return_rate) ** (1/12) - 1
        self.monthly_inflation_rate = (1 + annual_inflation_rate) ** (1/12) - 1
        self.total_months = len(monthly_payments)
        
        # Calculate total mortgage payments
        self.total_mortgage_payments = sum(payment.get('month_payment', 0) for payment in monthly_payments)
        self.total_mortgage_interest_and_inflation = self.total_mortgage_payments - self.loan_amount
        
        # For short-term mortgages, we need to account for the full 30-year period
        # The weighted payment should be calculated for a full 30-year period
        self.full_period_months = 360  # 30 years
    
    def _calculate_single_investment(self, investment_amount: float, months_growing: int) -> Dict[str, float]:
        """
        Calculate the future value of a single investment.
        
        Args:
            investment_amount: Amount to invest (can be negative)
            months_growing: Number of months the investment grows
            
        Returns:
            Dictionary with investment details
        """
        if months_growing <= 0:
            return {
                'investment_amount': investment_amount,
                'final_value': investment_amount,
                'profit_after_tax': 0,
                'net_value_after_tax': investment_amount
            }
        
        # Calculate final value with compound interest
        final_value = investment_amount * ((1 + self.monthly_return_rate) ** months_growing)
        inflation_adjusted_amount = investment_amount * ((1 + self.monthly_inflation_rate) ** months_growing)
        # Calculate profit and tax
        profit_before_inflation = final_value - investment_amount
        profit_after_inflation = final_value - inflation_adjusted_amount
        tax = profit_after_inflation * self.tax_rate if profit_after_inflation > 0 else 0
        
        profit_after_tax = profit_before_inflation - tax
        
        net_value_after_tax = final_value - tax
        
        return {
            'investment_amount': investment_amount,
            'final_value': final_value,
            'profit_after_tax': profit_after_tax,
            'net_value_after_tax': net_value_after_tax
        }
    
    def _calculate_weighted_cost(self, weighted_payment: float) -> float:
        """
        Calculate the weighted cost for a given weighted monthly payment.
        
        Args:
            weighted_payment: The weighted monthly payment to test
            
        Returns:
            The weighted cost (investment_profit - mortgage_interest)
        """
        total_investment_profit = 0
        
        # For the actual mortgage period
        for month, payment in enumerate(self.monthly_payments, 1):
            actual_payment = payment.get('month_payment', 0)
            difference = weighted_payment - actual_payment
            
            # Calculate months remaining for investment (always 30 years = 360 months)
            months_growing = 360 - month + 1
            
            # Calculate investment result
            investment_result = self._calculate_single_investment(difference, months_growing)
            total_investment_profit += investment_result['profit_after_tax']
        
        # For the remaining period after mortgage ends (if mortgage is shorter than 30 years)
        mortgage_months = len(self.monthly_payments)
        for month in range(mortgage_months + 1, 361):  # From month after mortgage ends to month 360
            # No actual mortgage payment, so difference is the full weighted payment
            difference = weighted_payment
            
            # Calculate months remaining for investment
            months_growing = 360 - month + 1
            
            # Calculate investment result
            investment_result = self._calculate_single_investment(difference, months_growing)
            total_investment_profit += investment_result['profit_after_tax']
        
        # Weighted cost = investment_profit - mortgage_interest
        weighted_cost = total_investment_profit - self.total_mortgage_interest_and_inflation
        
        return weighted_cost
    
    def calculate_weighted_payment(self, tolerance: float = 1.0, max_iterations: int = 10000) -> Dict[str, Any]:
        """
        Calculate the weighted monthly payment using binary search optimization.
        
        Args:
            tolerance: Tolerance for convergence in NIS (default 1 NIS)
            max_iterations: Maximum number of iterations (default 50)
            
        Returns:
            Dictionary with weighted payment and calculation details
        """
        # Initial bounds for binary search
        # For a 30-year mortgage, the weighted payment should be close to the actual monthly payment
        # Use the actual monthly payments as a reference
        if self.monthly_payments:
            avg_monthly_payment = sum(payment.get('month_payment', 0) for payment in self.monthly_payments) / len(self.monthly_payments)
            min_payment = avg_monthly_payment * 0.7  # Lower bound
            max_payment = avg_monthly_payment * 2.0  # Upper bound
        else:
            # Fallback to loan amount based estimation
            estimated_monthly_payment = self.loan_amount / 360  # Principal only
            min_payment = estimated_monthly_payment * 0.5  # Lower bound
            max_payment = estimated_monthly_payment * 3.0  # Upper bound (accounts for interest)
        min_payment = 0
        max_payment = self.loan_amount
        # Ensure we have reasonable bounds
        
        print(f"Searching for weighted payment between {min_payment:.2f} and {max_payment:.2f} NIS")
        
        # Binary search
        for iteration in range(max_iterations):
            weighted_payment = (min_payment + max_payment) / 2
            weighted_cost = self._calculate_weighted_cost(weighted_payment)
            
            # Only print every 10th iteration to reduce output
            if iteration % 10 == 0 or iteration < 30:
                print(f"Iteration {iteration + 1}: weighted_payment={weighted_payment:.2f}, cost={weighted_cost:.2f}")
            
            # Check if we've converged
            if abs(weighted_cost) <= tolerance:
                print(f"Converged after {iteration + 1} iterations")
                break
            
            # Update bounds
            if weighted_cost > 0:
                # Cost is positive, need to increase weighted payment
                max_payment = weighted_payment
            else:
                # Cost is negative, need to decrease weighted payment
                min_payment = weighted_payment
        
        # Final calculation with the converged weighted payment
        final_weighted_cost = self._calculate_weighted_cost(weighted_payment)
        
        # Calculate additional metrics
        total_investment_profit = final_weighted_cost + self.total_mortgage_interest_and_inflation
        
        return {
            'weighted_monthly_payment': weighted_payment,
            'weighted_cost': final_weighted_cost,
            'total_mortgage_payments': self.total_mortgage_payments,
            'total_mortgage_interest_and_inflation': self.total_mortgage_interest_and_inflation,
            'total_investment_profit': total_investment_profit,
            'loan_amount': self.loan_amount,
            'iterations': iteration + 1,
            'converged': abs(final_weighted_cost) <= tolerance
        }
    
    def get_monthly_breakdown(self, weighted_payment: float) -> List[Dict[str, Any]]:
        """
        Get detailed breakdown of monthly calculations for a given weighted payment.
        
        Args:
            weighted_payment: The weighted monthly payment
            
        Returns:
            List of monthly breakdown dictionaries
        """
        breakdown = []
        
        # For the actual mortgage period
        for month, payment in enumerate(self.monthly_payments, 1):
            actual_payment = payment.get('month_payment', 0)
            difference = weighted_payment - actual_payment
            months_growing = 360 - month + 1
            
            investment_result = self._calculate_single_investment(difference, months_growing)
            
            breakdown.append({
                'month': month,
                'actual_payment': actual_payment,
                'weighted_payment': weighted_payment,
                'difference': difference,
                'months_growing': months_growing,
                'investment_amount': investment_result['investment_amount'],
                'final_value': investment_result['final_value'],
                'profit_after_tax': investment_result['profit_after_tax'],
                'net_value_after_tax': investment_result['net_value_after_tax']
            })
        
        # For the remaining period after mortgage ends (if mortgage is shorter than 30 years)
        mortgage_months = len(self.monthly_payments)
        for month in range(mortgage_months + 1, 361):  # From month after mortgage ends to month 360
            actual_payment = 0  # No mortgage payment
            difference = weighted_payment  # Full weighted payment is invested
            months_growing = 360 - month + 1
            
            investment_result = self._calculate_single_investment(difference, months_growing)
            
            breakdown.append({
                'month': month,
                'actual_payment': actual_payment,
                'weighted_payment': weighted_payment,
                'difference': difference,
                'months_growing': months_growing,
                'investment_amount': investment_result['investment_amount'],
                'final_value': investment_result['final_value'],
                'profit_after_tax': investment_result['profit_after_tax'],
                'net_value_after_tax': investment_result['net_value_after_tax']
            })
        
        return breakdown 