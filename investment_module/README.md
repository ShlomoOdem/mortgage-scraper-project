# Investment Module

A comprehensive Python module for investment calculations with tax and inflation considerations. This module provides accurate financial calculations for investment planning, portfolio analysis, and risk assessment.

## Features

- **Future Value Calculations**: Compound interest calculations for single investments and annuities
- **Tax Calculations**: Accurate tax calculations on investment profits with inflation adjustments
- **Inflation Adjustments**: Real return calculations accounting for inflation
- **Monthly Investment Planning**: Detailed monthly investment analysis
- **Risk Analysis**: Volatility, Sharpe ratio, maximum drawdown, and Value at Risk calculations
- **Monte Carlo Simulations**: Scenario analysis for investment planning
- **Portfolio Optimization**: Tools for portfolio analysis and comparison

## Installation

### From Source
```bash
git clone https://github.com/yourusername/investment-module.git
cd investment-module
pip install -e .
```

### From PyPI (when published)
```bash
pip install investment-module
```

## Quick Start

```python
from investment_module import InvestmentCalculator, InvestmentData

# Create investment data
data = InvestmentData(
    monthly_investment=1000,
    stock_annual_rate=0.07,
    inflation_rate=0.02,
    years=30
)

# Calculate investment with tax
result = InvestmentCalculator.calculate_monthly_investment_with_tax(
    monthly_payment=data.monthly_investment,
    annual_rate=data.stock_annual_rate,
    inflation_rate=data.inflation_rate,
    years=data.years
)

print(f"Total invested: ${result['total_invested']:,.2f}")
print(f"Future value: ${result['future_value']:,.2f}")
print(f"Net profit after tax: ${result['net_profit']:,.2f}")
print(f"Final value: ${result['final_value']:,.2f}")
```

## Core Components

### InvestmentCalculator

The main calculator class with comprehensive investment calculation methods:

- `calculate_future_value()`: Basic compound interest calculation
- `calculate_monthly_investment_future_value()`: Future value of monthly payments
- `calculate_monthly_investment_with_tax()`: Complete investment calculation with tax
- `calculate_monthly_investments_detailed()`: Detailed monthly investment analysis
- `calculate_risk_metrics()`: Risk analysis for investment portfolios
- `run_monte_carlo_simulation()`: Monte Carlo scenario analysis

### Data Models

- `InvestmentData`: Input parameters for calculations
- `InvestmentResult`: Results of individual investment calculations
- `InvestmentSummary`: Portfolio summary statistics
- `RiskMetrics`: Risk analysis metrics
- `MonteCarloResult`: Monte Carlo simulation results

### Utility Functions

- `calculate_monthly_rate()`: Convert annual to monthly rates
- `calculate_annuity_future_value()`: Future value of annuity payments
- `calculate_inflation_adjusted_value()`: Inflation-adjusted calculations
- `calculate_volatility()`: Portfolio volatility calculation
- `calculate_sharpe_ratio()`: Risk-adjusted return calculation

## Advanced Usage

### Detailed Monthly Investment Analysis

```python
from investment_module import InvestmentCalculator

# Create payment schedule (can be empty for pure investment)
payment_schedule = []  # Empty for pure investment

# Calculate detailed investments
detailed_result = InvestmentCalculator.calculate_monthly_investments_detailed(
    payment_schedule=payment_schedule,
    monthly_income=5000,
    stock_annual_rate=0.07,
    inflation_rate=0.02
)

print(f"Total invested: ${detailed_result['summary']['total_invested']:,.2f}")
print(f"Final portfolio value: ${detailed_result['summary']['final_portfolio_value']:,.2f}")
```

### Risk Analysis

```python
from investment_module import InvestmentCalculator

# Get monthly values from detailed calculation
monthly_values = detailed_result['summary']['monthly_values']

# Calculate risk metrics
risk_metrics = InvestmentCalculator.calculate_risk_metrics(
    monthly_values=monthly_values,
    risk_free_rate=0.03
)

print(f"Volatility: {risk_metrics.volatility:.2%}")
print(f"Sharpe Ratio: {risk_metrics.sharpe_ratio:.2f}")
print(f"Maximum Drawdown: {risk_metrics.max_drawdown:.2%}")
```

### Monte Carlo Simulation

```python
from investment_module import InvestmentCalculator

# Run Monte Carlo simulation
mc_result = InvestmentCalculator.run_monte_carlo_simulation(
    monthly_investment=1000,
    mean_return=0.07,
    volatility=0.15,
    inflation_rate=0.02,
    years=30,
    simulations=10000,
    target_value=1000000
)

print(f"Mean final value: ${mc_result.mean_final_value:,.2f}")
print(f"95th percentile: ${mc_result.percentile_95:,.2f}")
print(f"Success rate: {mc_result.success_rate:.1%}")
```

## Tax Calculation Method

The module uses a sophisticated tax calculation method that:

1. **Calculates Future Value**: Uses the Future Value of Annuity formula for monthly investments
2. **Applies Weighted Inflation**: Accounts for different holding periods of monthly investments
3. **Determines Taxable Profit**: Only taxes profit above inflation-adjusted principal
4. **Calculates Net Return**: Provides after-tax investment returns

This method matches real-world tax calculations and provides accurate after-tax investment analysis.

## Examples

### Basic Investment Calculation

```python
# Calculate $1000 monthly investment for 30 years
result = InvestmentCalculator.calculate_monthly_investment_with_tax(
    monthly_payment=1000,
    annual_rate=0.07,
    inflation_rate=0.02,
    years=30
)

# Results:
# Total invested: $360,000
# Future value: $1,220,000
# Net profit after tax: $645,000
# Final value: $1,005,000
```

### Investment vs. Mortgage Comparison

```python
# Calculate investment with mortgage payment consideration
mortgage_payments = [
    {"month": i, "total_payment": 2000} for i in range(1, 361)
]

detailed_result = InvestmentCalculator.calculate_monthly_investments_detailed(
    payment_schedule=mortgage_payments,
    monthly_income=8000,
    stock_annual_rate=0.07,
    inflation_rate=0.02
)

# Calculate net mortgage cost
net_cost = InvestmentCalculator.calculate_net_mortgage_cost(
    total_mortgage_payments=720000,  # 30 years * 12 months * $2000
    total_interest_paid=400000,
    investment_summary=detailed_result['summary']
)
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=investment_module

# Run specific test file
pytest tests/test_calculator.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This module is for educational and planning purposes only. It does not constitute financial advice. Always consult with a qualified financial advisor before making investment decisions.

## Support

For support, please open an issue on GitHub or contact the development team. 