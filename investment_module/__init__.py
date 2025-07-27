"""
Investment Module - Standalone Investment Calculation Package

This module provides comprehensive investment calculation functionality including:
- Future value calculations with compound interest
- Tax calculations on investment profits
- Inflation-adjusted returns
- Monthly investment planning
- Risk analysis and portfolio optimization

The module is completely independent and can be used in any Python project.
"""

from .calculator import InvestmentCalculator
from .models import InvestmentData, InvestmentResult, InvestmentSummary
from .utils import calculate_monthly_rate, calculate_annual_rate

__version__ = "1.0.0"
__author__ = "Investment Module Team"

__all__ = [
    "InvestmentCalculator",
    "InvestmentData", 
    "InvestmentResult",
    "InvestmentSummary",
    "calculate_monthly_rate",
    "calculate_annual_rate"
] 