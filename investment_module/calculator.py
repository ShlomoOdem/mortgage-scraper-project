"""
Main investment calculator class with comprehensive calculation methods
"""

from typing import List, Dict, Any, Optional
import math
from models import (
    InvestmentData, InvestmentResult, InvestmentSummary, 
    MonthlyInvestmentData
)
from utils import (
    calculate_monthly_rate, calculate_future_value, 
    calculate_inflation_adjusted_value, calculate_annuity_future_value
)


class InvestmentCalculator:
    """Comprehensive investment calculator with tax and inflation considerations"""
    
    TAX_RATE = 0.25  # 25% tax on profit
    YEARS_TO_SELL = 30  # Sell after 30 years
    
    @staticmethod
    def calculate_future_value(principal: float, annual_rate: float, years: float) -> float:
        """Calculate future value of investment with compound interest"""
        return principal * (1 + annual_rate) ** years
    
    @staticmethod
    def calculate_monthly_investment_future_value(monthly_payment: float, annual_rate: float, years: float) -> float:
        """Calculate future value of monthly investment (Future Value of Annuity)
        
        Args:
            monthly_payment: Monthly payment
            annual_rate: Annual interest rate
            years: Number of years
            
        Returns:
            Future value of all monthly investments
        """
        monthly_rate = calculate_monthly_rate(annual_rate)
        months = years * 12
        
        if monthly_rate == 0:
            return monthly_payment * months
        
        # Future Value of Annuity: FV = PMT * [((1 + r)^n - 1) / r]
        future_value = monthly_payment * (((1 + monthly_rate) ** months - 1) / monthly_rate)
        return future_value
    
    @staticmethod
    def calculate_inflation_adjusted_value(nominal_value: float, inflation_rate: float, years: float) -> float:
        """Calculate inflation-adjusted value"""
        return nominal_value / (1 + inflation_rate) ** years
    
    @staticmethod
    def calculate_tax_on_profit(invested_amount: float, future_value: float, inflation_rate: float, years: float) -> Dict[str, float]:
        """Calculate tax on profit after inflation adjustment
        
        Args:
            invested_amount: Amount invested
            future_value: Future value before tax
            inflation_rate: Annual inflation rate
            years: Number of years
            
        Returns:
            Dictionary with tax and profit details
        """
        # Inflation-adjusted value of original investment
        inflation_adjusted_principal = invested_amount * (1 + inflation_rate) ** years
        
        # Nominal profit
        nominal_profit = future_value - invested_amount
        
        # Inflation-adjusted profit (for tax)
        taxable_profit = max(0, future_value - inflation_adjusted_principal)
        
        # Tax
        tax_amount = taxable_profit * InvestmentCalculator.TAX_RATE
        
        # Profit after tax
        net_profit = nominal_profit - tax_amount
        
        # Final value after tax
        final_value = invested_amount + net_profit
        
        return {
            "nominal_profit": nominal_profit,
            "inflation_adjusted_principal": inflation_adjusted_principal,
            "taxable_profit": taxable_profit,
            "tax_amount": tax_amount,
            "net_profit": net_profit,
            "final_value": final_value
        }
    
    @staticmethod
    def calculate_monthly_investment_with_tax(monthly_payment: float, annual_rate: float, inflation_rate: float, years: float) -> Dict[str, float]:
        """Calculate monthly investment with tax - corrected version
        
        Uses the exact method that matches the reference tax calculation.
        
        Args:
            monthly_payment: Monthly payment
            annual_rate: Annual interest rate
            inflation_rate: Annual inflation rate
            years: Number of years
            
        Returns:
            Dictionary with complete investment and tax details
        """
        return InvestmentCalculator.calculate_monthly_investment_reference_method(
            monthly_payment, annual_rate, inflation_rate, years
        )
    
    @staticmethod
    def calculate_monthly_investment_reference_method(monthly_payment: float, annual_rate: float, inflation_rate: float, years: float) -> Dict[str, float]:
        """Calculate monthly investment using the exact reference method
        
        This method matches exactly the reference calculation provided by the user.
        Uses Future Value of Annuity with weighted inflation adjustment.
        
        Args:
            monthly_payment: Monthly payment
            annual_rate: Annual interest rate  
            inflation_rate: Annual inflation rate
            years: Number of years
            
        Returns:
            Dictionary with exact calculation matching reference data
        """
        months = int(years * 12)
        total_invested = monthly_payment * months
        
        # Calculate Future Value using Annuity formula (matches reference exactly)
        monthly_rate = calculate_monthly_rate(annual_rate)
        
        if monthly_rate == 0:
            future_value = total_invested
        else:
            # Future Value of Annuity: FV = PMT * [((1 + r)^n - 1) / r]
            future_value = monthly_payment * (((1 + monthly_rate) ** months - 1) / monthly_rate)
        
        # Calculate weighted inflation adjustment (key to matching reference)
        # This represents the average inflation impact across all investments
        total_weighted_inflation_factor = 0
        for month in range(1, months + 1):
            years_held = (months - month + 1) / 12
            inflation_factor = (1 + inflation_rate) ** years_held
            month_weight = 1 / months  # Equal weight for each monthly investment
            total_weighted_inflation_factor += inflation_factor * month_weight
        
        # Apply weighted inflation adjustment to total investment
        inflation_adjusted_investment = total_invested * total_weighted_inflation_factor
        
        # Calculate tax on profit above inflation adjustment
        nominal_profit = future_value - total_invested
        taxable_profit = max(0, future_value - inflation_adjusted_investment)
        tax_amount = taxable_profit * InvestmentCalculator.TAX_RATE
        
        # Calculate final values
        net_profit = nominal_profit - tax_amount
        final_value = total_invested + net_profit
        
        return {
            "monthly_payment": monthly_payment,
            "total_invested": total_invested,
            "future_value": future_value,
            "nominal_profit": nominal_profit,
            "inflation_adjusted_principal": inflation_adjusted_investment,
            "taxable_profit": taxable_profit,
            "tax_amount": tax_amount,
            "net_profit": net_profit,
            "final_value": final_value,
            "effective_annual_return": (final_value / total_invested) ** (1/years) - 1,
            "weighted_inflation_factor": total_weighted_inflation_factor,
            "calculation_method": "reference_weighted_inflation"
        }

    @staticmethod
    def calculate_single_month_investment_accurate(
        month: int,
        investment_amount: float,
        stock_annual_rate: float,
        inflation_rate: float,
        total_months: int = 360
    ) -> Dict[str, float]:
        """Calculate accurate investment for a single month with proper compound interest
        
        This method calculates exactly as the correct tax calculation provided by the user.
        
        Args:
            month: Month number (1-360)
            investment_amount: Monthly investment amount
            stock_annual_rate: Annual stock return rate
            inflation_rate: Annual inflation rate
            total_months: Total investment period in months (default 360 = 30 years)
            
        Returns:
            Dictionary with detailed monthly investment calculation
        """
        # Calculate exact years this investment will be held until sale
        months_to_sell = total_months - month + 1
        years_to_sell = months_to_sell / 12.0
        
        # Use precise monthly compound rate calculation
        monthly_rate = calculate_monthly_rate(stock_annual_rate)
        
        # Calculate future value using compound interest
        future_value = investment_amount * (1 + monthly_rate) ** months_to_sell
        
        # Calculate inflation-adjusted principal for tax purposes
        inflation_adjusted_principal = investment_amount * (1 + inflation_rate) ** years_to_sell
        
        # Calculate profits and taxes
        nominal_profit = future_value - investment_amount
        taxable_profit = max(0, future_value - inflation_adjusted_principal)
        tax_amount = taxable_profit * InvestmentCalculator.TAX_RATE
        net_profit = nominal_profit - tax_amount
        final_value = investment_amount + net_profit
        
        return {
            "month": month,
            "investment_amount": investment_amount,
            "years_to_sell": years_to_sell,
            "future_value": future_value,
            "nominal_profit": nominal_profit,
            "inflation_adjusted_principal": inflation_adjusted_principal,
            "taxable_profit": taxable_profit,
            "tax_amount": tax_amount,
            "net_profit": net_profit,
            "final_value": final_value
        }
    
    @staticmethod
    def calculate_investment_for_month(
        month: int,
        investment_amount: float,
        stock_annual_rate: float,
        inflation_rate: float
    ) -> Dict[str, float]:
        """Calculate investment for a specific month
        
        Args:
            month: Month number (1-360)
            investment_amount: Monthly investment amount
            stock_annual_rate: Annual stock return rate
            inflation_rate: Annual inflation rate
            
        Returns:
            Dictionary with monthly investment calculation
        """
        return InvestmentCalculator.calculate_single_month_investment_accurate(
            month, investment_amount, stock_annual_rate, inflation_rate
        )
    
    @staticmethod
    def calculate_monthly_investments_detailed(
        payment_schedule: List[Dict[str, Any]],
        monthly_income: float,
        stock_annual_rate: float,
        inflation_rate: float
    ) -> Dict[str, Any]:
        """Calculate detailed monthly investments with mortgage payment consideration
        
        Args:
            payment_schedule: List of payment data (can be empty for pure investment)
            monthly_income: Monthly income available
            stock_annual_rate: Annual stock return rate
            inflation_rate: Annual inflation rate
            
        Returns:
            Dictionary with detailed investment analysis
        """
        investments = []
        total_invested = 0
        total_future_value = 0
        total_nominal_profit = 0
        total_tax = 0
        total_net_profit = 0
        
        # If no payment schedule provided, create one for pure investment
        if not payment_schedule:
            months = 360  # 30 years
            payment_schedule = [{"month": i, "total_payment": 0} for i in range(1, months + 1)]
        
        for payment in payment_schedule:
            month = payment.get("month", len(investments) + 1)
            total_mortgage_payment = payment.get("total_payment", 0)
            
            # Calculate investment amount (difference between income and mortgage payment)
            investment_amount = monthly_income - total_mortgage_payment
            
            if investment_amount < 0:
                raise ValueError(f"Monthly income ({monthly_income}) is less than mortgage payment ({total_mortgage_payment}) in month {month}")
            
            # Calculate investment for this month
            investment_result = InvestmentCalculator.calculate_investment_for_month(
                month, investment_amount, stock_annual_rate, inflation_rate
            )
            
            # Update totals
            total_invested += investment_amount
            total_future_value += investment_result["future_value"]
            total_nominal_profit += investment_result["nominal_profit"]
            total_tax += investment_result["tax_amount"]
            total_net_profit += investment_result["net_profit"]
            
            # Add to investments list
            investments.append({
                "month": month,
                "investment_amount": investment_amount,
                "mortgage_payment": total_mortgage_payment,
                "future_value": investment_result["future_value"],
                "nominal_profit": investment_result["nominal_profit"],
                "tax_amount": investment_result["tax_amount"],
                "net_profit": investment_result["net_profit"],
                "final_value": investment_result["final_value"]
            })
        
        final_portfolio_value = total_invested + total_net_profit
        
        return {
            "investments": investments,
            "summary": {
                "total_invested": total_invested,
                "total_future_value": total_future_value,
                "total_nominal_profit": total_nominal_profit,
                "total_tax": total_tax,
                "total_net_profit": total_net_profit,
                "final_portfolio_value": final_portfolio_value,
                "effective_annual_return": (final_portfolio_value / total_invested) ** (1/30) - 1 if total_invested > 0 else 0
            },
            "parameters": {
                "monthly_income": monthly_income,
                "stock_annual_rate": stock_annual_rate,
                "inflation_rate": inflation_rate,
                "tax_rate": InvestmentCalculator.TAX_RATE
            }
        }
    
    @staticmethod
    def calculate_monthly_investments(
        payment_schedule: List[Dict[str, Any]],
        monthly_income: float,
        stock_annual_rate: float,
        inflation_rate: float
    ) -> List[Dict[str, Any]]:
        """Calculate monthly investments (simplified version)
        
        Args:
            payment_schedule: Mortgage payment schedule
            monthly_income: Monthly income available
            stock_annual_rate: Annual stock return rate
            inflation_rate: Annual inflation rate
            
        Returns:
            List of monthly investment results
        """
        detailed_result = InvestmentCalculator.calculate_monthly_investments_detailed(
            payment_schedule, monthly_income, stock_annual_rate, inflation_rate
        )
        return detailed_result["investments"]
    
    @staticmethod
    def calculate_investment_summary_enhanced(detailed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate enhanced investment summary with additional metrics
        
        Args:
            detailed_data: Detailed investment calculation result
            
        Returns:
            Enhanced summary with additional metrics
        """
        summary = detailed_data["summary"]
        investments = detailed_data["investments"]
        
        # Calculate additional metrics
        total_months = len(investments)
        years = total_months / 12
        
        # Annualized return
        annualized_return = (summary["final_portfolio_value"] / summary["total_invested"]) ** (1/years) - 1 if summary["total_invested"] > 0 else 0
        
        # Inflation-adjusted return
        inflation_rate = detailed_data["parameters"]["inflation_rate"]
        inflation_adjusted_final_value = summary["final_portfolio_value"] / (1 + inflation_rate) ** years
        inflation_adjusted_return = (inflation_adjusted_final_value / summary["total_invested"]) ** (1/years) - 1 if summary["total_invested"] > 0 else 0
        
        # Tax efficiency
        tax_efficiency = (summary["total_net_profit"] / summary["total_nominal_profit"]) if summary["total_nominal_profit"] > 0 else 1
        
        # Monthly breakdown for analysis
        monthly_values = []
        cumulative_invested = 0
        cumulative_future_value = 0
        
        for inv in investments:
            cumulative_invested += inv["investment_amount"]
            cumulative_future_value += inv["future_value"]
            monthly_values.append({
                "month": inv["month"],
                "cumulative_invested": cumulative_invested,
                "cumulative_future_value": cumulative_future_value,
                "net_value": cumulative_future_value - cumulative_invested
            })
        
        return {
            **summary,
            "annualized_return": annualized_return,
            "inflation_adjusted_return": inflation_adjusted_return,
            "tax_efficiency": tax_efficiency,
            "total_months": total_months,
            "years": years,
            "monthly_values": monthly_values
        }
    
    @staticmethod
    def calculate_investment_summary(investments: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate basic investment summary
        
        Args:
            investments: List of investment results
            
        Returns:
            Basic summary dictionary
        """
        total_invested = sum(inv["investment_amount"] for inv in investments)
        total_future_value = sum(inv["future_value"] for inv in investments)
        total_nominal_profit = sum(inv["nominal_profit"] for inv in investments)
        total_tax = sum(inv["tax_amount"] for inv in investments)
        total_net_profit = sum(inv["net_profit"] for inv in investments)
        final_portfolio_value = total_invested + total_net_profit
        
        return {
            "total_invested": total_invested,
            "total_future_value": total_future_value,
            "total_nominal_profit": total_nominal_profit,
            "total_tax": total_tax,
            "total_net_profit": total_net_profit,
            "final_portfolio_value": final_portfolio_value
        }
    
    @staticmethod
    def calculate_net_mortgage_cost(
        total_mortgage_payments: float,
        total_interest_paid: float,
        investment_summary: Dict[str, float]
    ) -> Dict[str, float]:
        """Calculate net mortgage cost considering investment offset
        
        Args:
            total_mortgage_payments: Total mortgage payments
            total_interest_paid: Total interest paid
            investment_summary: Investment summary
            
        Returns:
            Dictionary with net cost calculations
        """
        final_portfolio_value = investment_summary["final_portfolio_value"]
        net_mortgage_cost = total_interest_paid - investment_summary["total_net_profit"]
        net_wealth = final_portfolio_value - total_mortgage_payments
        
        return {
            "total_mortgage_payments": total_mortgage_payments,
            "total_interest_paid": total_interest_paid,
            "investment_profit": investment_summary["total_net_profit"],
            "net_mortgage_cost": net_mortgage_cost,
            "final_portfolio_value": final_portfolio_value,
            "net_wealth": net_wealth
        }
    
    @staticmethod
    def calculate_monthly_investment_tax_accurate(monthly_payment: float, annual_rate: float, inflation_rate: float, years: float) -> Dict[str, float]:
        """Calculate monthly investment with accurate tax treatment
        
        Args:
            monthly_payment: Monthly investment amount
            annual_rate: Annual return rate
            inflation_rate: Annual inflation rate
            years: Investment period
            
        Returns:
            Dictionary with accurate tax calculation
        """
        return InvestmentCalculator.calculate_monthly_investment_reference_method(
            monthly_payment, annual_rate, inflation_rate, years
        ) 