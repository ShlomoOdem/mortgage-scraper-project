"""
Utility functions for investment calculations
"""

import math
from typing import List, Tuple


def calculate_monthly_rate(annual_rate: float) -> float:
    """
    Convert annual rate to monthly rate using compound interest formula
    
    Args:
        annual_rate: Annual interest rate (e.g., 0.07 for 7%)
        
    Returns:
        Monthly interest rate
    """
    return (1 + annual_rate) ** (1/12) - 1


def calculate_annual_rate(monthly_rate: float) -> float:
    """
    Convert monthly rate to annual rate using compound interest formula
    
    Args:
        monthly_rate: Monthly interest rate
        
    Returns:
        Annual interest rate
    """
    return (1 + monthly_rate) ** 12 - 1


def calculate_future_value(principal: float, annual_rate: float, years: float) -> float:
    """
    Calculate future value of a single investment with compound interest
    
    Args:
        principal: Initial investment amount
        annual_rate: Annual interest rate
        years: Number of years
        
    Returns:
        Future value of the investment
    """
    return principal * (1 + annual_rate) ** years


def calculate_present_value(future_value: float, annual_rate: float, years: float) -> float:
    """
    Calculate present value of a future amount
    
    Args:
        future_value: Future amount
        annual_rate: Annual discount rate
        years: Number of years
        
    Returns:
        Present value
    """
    return future_value / (1 + annual_rate) ** years


def calculate_annuity_future_value(monthly_payment: float, annual_rate: float, years: float) -> float:
    """
    Calculate future value of monthly payments (annuity)
    
    Args:
        monthly_payment: Monthly payment amount
        annual_rate: Annual interest rate
        years: Number of years
        
    Returns:
        Future value of all monthly payments
    """
    monthly_rate = calculate_monthly_rate(annual_rate)
    months = years * 12
    
    if monthly_rate == 0:
        return monthly_payment * months
    
    # Future Value of Annuity: FV = PMT * [((1 + r)^n - 1) / r]
    future_value = monthly_payment * (((1 + monthly_rate) ** months - 1) / monthly_rate)
    return future_value


def calculate_annuity_payment(future_value: float, annual_rate: float, years: float) -> float:
    """
    Calculate required monthly payment to reach a future value
    
    Args:
        future_value: Target future value
        annual_rate: Annual interest rate
        years: Number of years
        
    Returns:
        Required monthly payment
    """
    monthly_rate = calculate_monthly_rate(annual_rate)
    months = years * 12
    
    if monthly_rate == 0:
        return future_value / months
    
    # Payment = FV * r / ((1 + r)^n - 1)
    payment = future_value * monthly_rate / ((1 + monthly_rate) ** months - 1)
    return payment


def calculate_inflation_adjusted_value(nominal_value: float, inflation_rate: float, years: float) -> float:
    """
    Calculate inflation-adjusted value
    
    Args:
        nominal_value: Nominal value
        inflation_rate: Annual inflation rate
        years: Number of years
        
    Returns:
        Inflation-adjusted value
    """
    return nominal_value / (1 + inflation_rate) ** years


def calculate_real_rate(nominal_rate: float, inflation_rate: float) -> float:
    """
    Calculate real interest rate (nominal rate minus inflation)
    
    Args:
        nominal_rate: Nominal interest rate
        inflation_rate: Inflation rate
        
    Returns:
        Real interest rate
    """
    return (1 + nominal_rate) / (1 + inflation_rate) - 1


def calculate_compound_annual_growth_rate(initial_value: float, final_value: float, years: float) -> float:
    """
    Calculate Compound Annual Growth Rate (CAGR)
    
    Args:
        initial_value: Initial investment value
        final_value: Final investment value
        years: Number of years
        
    Returns:
        CAGR as a decimal
    """
    if initial_value <= 0 or years <= 0:
        return 0.0
    
    return (final_value / initial_value) ** (1 / years) - 1


def calculate_volatility(returns: List[float]) -> float:
    """
    Calculate volatility (standard deviation) of returns
    
    Args:
        returns: List of periodic returns
        
    Returns:
        Volatility as a decimal
    """
    if not returns:
        return 0.0
    
    mean_return = sum(returns) / len(returns)
    squared_diff_sum = sum((r - mean_return) ** 2 for r in returns)
    variance = squared_diff_sum / len(returns)
    return math.sqrt(variance)


def calculate_sharpe_ratio(returns: List[float], risk_free_rate: float = 0.03) -> float:
    """
    Calculate Sharpe ratio
    
    Args:
        returns: List of periodic returns
        risk_free_rate: Risk-free rate
        
    Returns:
        Sharpe ratio
    """
    if not returns:
        return 0.0
    
    mean_return = sum(returns) / len(returns)
    volatility = calculate_volatility(returns)
    
    if volatility == 0:
        return 0.0
    
    return (mean_return - risk_free_rate) / volatility


def calculate_max_drawdown(values: List[float]) -> float:
    """
    Calculate maximum drawdown
    
    Args:
        values: List of portfolio values over time
        
    Returns:
        Maximum drawdown as a decimal
    """
    if not values:
        return 0.0
    
    peak = values[0]
    max_drawdown = 0.0
    
    for value in values:
        if value > peak:
            peak = value
        drawdown = (peak - value) / peak
        max_drawdown = max(max_drawdown, drawdown)
    
    return max_drawdown


def calculate_value_at_risk(returns: List[float], confidence_level: float = 0.95) -> float:
    """
    Calculate Value at Risk (VaR)
    
    Args:
        returns: List of periodic returns
        confidence_level: Confidence level (e.g., 0.95 for 95%)
        
    Returns:
        Value at Risk as a decimal
    """
    if not returns:
        return 0.0
    
    sorted_returns = sorted(returns)
    index = int((1 - confidence_level) * len(sorted_returns))
    return abs(sorted_returns[index])


def format_currency(amount: float) -> str:
    """
    Format amount as currency string
    
    Args:
        amount: Amount to format
        
    Returns:
        Formatted currency string
    """
    return f"${amount:,.2f}"


def format_percentage(rate: float) -> str:
    """
    Format rate as percentage string
    
    Args:
        rate: Rate as decimal (e.g., 0.07 for 7%)
        
    Returns:
        Formatted percentage string
    """
    return f"{rate * 100:.2f}%" 