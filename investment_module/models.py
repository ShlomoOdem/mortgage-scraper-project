"""
Data models for investment calculations
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class InvestmentData:
    """Input data for investment calculations"""
    monthly_investment: float
    stock_annual_rate: float = 0.07
    inflation_rate: float = 0.02
    years: int = 30
    tax_rate: float = 0.25


@dataclass
class InvestmentResult:
    """Result of a single investment calculation"""
    month: int
    investment_amount: float
    future_value: float
    nominal_profit: float
    inflation_adjusted_profit: float
    tax_amount: float
    net_profit: float
    final_value: float
    cumulative_invested: float
    cumulative_future_value: float


@dataclass
class InvestmentSummary:
    """Summary of investment portfolio"""
    total_invested: float
    total_future_value: float
    total_nominal_profit: float
    total_inflation_adjusted_profit: float
    total_tax: float
    total_net_profit: float
    final_portfolio_value: float
    annualized_return: float
    inflation_adjusted_return: float
    tax_efficiency: float


@dataclass
class MonthlyInvestmentData:
    """Data for monthly investment calculations"""
    month: int
    investment_amount: float
    mortgage_payment: float = 0.0
    available_for_investment: float = 0.0


@dataclass
class InvestmentComparison:
    """Comparison between different investment scenarios"""
    scenario_name: str
    investment_data: InvestmentData
    summary: InvestmentSummary
    monthly_results: List[InvestmentResult]


 