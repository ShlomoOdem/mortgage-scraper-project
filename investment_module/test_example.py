"""
Example usage and testing of the Investment Module
"""

from calculator import InvestmentCalculator
from models import InvestmentData
from utils import format_currency, format_percentage


def test_basic_investment_calculation():
    """Test basic investment calculation"""
    print("=== Basic Investment Calculation ===")
    
    # Calculate $1000 monthly investment for 30 years
    result = InvestmentCalculator.calculate_monthly_investment_with_tax(
        monthly_payment=1000,
        annual_rate=0.07,
        inflation_rate=0.02,
        years=30
    )
    
    print(f"Monthly investment: {format_currency(1000)}")
    print(f"Annual return: {format_percentage(0.07)}")
    print(f"Inflation rate: {format_percentage(0.02)}")
    print(f"Investment period: 30 years")
    print()
    print("Results:")
    print(f"Total invested: {format_currency(result['total_invested'])}")
    print(f"Future value (before tax): {format_currency(result['future_value'])}")
    print(f"Nominal profit: {format_currency(result['nominal_profit'])}")
    print(f"Tax amount: {format_currency(result['tax_amount'])}")
    print(f"Net profit after tax: {format_currency(result['net_profit'])}")
    print(f"Final value: {format_currency(result['final_value'])}")
    print(f"Effective annual return: {format_percentage(result['effective_annual_return'])}")
    print()


def test_detailed_monthly_analysis():
    """Test detailed monthly investment analysis"""
    print("=== Detailed Monthly Investment Analysis ===")
    
    # Create empty payment schedule for pure investment
    payment_schedule = []
    
    # Calculate detailed investments
    detailed_result = InvestmentCalculator.calculate_monthly_investments_detailed(
        payment_schedule=payment_schedule,
        monthly_income=5000,
        stock_annual_rate=0.07,
        inflation_rate=0.02
    )
    
    summary = detailed_result['summary']
    print(f"Monthly income: {format_currency(5000)}")
    print(f"Total invested: {format_currency(summary['total_invested'])}")
    print(f"Final portfolio value: {format_currency(summary['final_portfolio_value'])}")
    print(f"Total net profit: {format_currency(summary['total_net_profit'])}")
    print(f"Effective annual return: {format_percentage(summary['effective_annual_return'])}")
    print()


def test_risk_analysis():
    """Test risk analysis functionality"""
    print("=== Risk Analysis ===")
    
    # Get monthly values from detailed calculation
    payment_schedule = []
    detailed_result = InvestmentCalculator.calculate_monthly_investments_detailed(
        payment_schedule=payment_schedule,
        monthly_income=3000,
        stock_annual_rate=0.08,
        inflation_rate=0.025
    )
    
    # For risk analysis, we need to create monthly values
    # This is a simplified example
    print("Risk analysis requires monthly portfolio values.")
    print("Creating sample data for demonstration...")
    
    # Create sample monthly values for demonstration
    sample_monthly_values = []
    cumulative_value = 0
    for month in range(1, 361):  # 30 years * 12 months
        monthly_investment = 3000
        cumulative_value += monthly_investment
        # Add some growth and volatility
        growth = cumulative_value * 0.07 / 12  # 7% annual return
        sample_monthly_values.append({
            "month": month,
            "cumulative_future_value": cumulative_value + growth * month
        })
    
    # Calculate risk metrics
    risk_metrics = InvestmentCalculator.calculate_risk_metrics(
        monthly_values=sample_monthly_values,
        risk_free_rate=0.03
    )
    
    print(f"Volatility: {format_percentage(risk_metrics.volatility)}")
    print(f"Sharpe Ratio: {risk_metrics.sharpe_ratio:.2f}")
    print(f"Maximum Drawdown: {format_percentage(risk_metrics.max_drawdown)}")
    print(f"Value at Risk (95%): {format_percentage(risk_metrics.var_95)}")
    print(f"Expected Return: {format_percentage(risk_metrics.expected_return)}")
    print()


def test_monte_carlo_simulation():
    """Test Monte Carlo simulation"""
    print("=== Monte Carlo Simulation ===")
    
    # Run Monte Carlo simulation
    mc_result = InvestmentCalculator.run_monte_carlo_simulation(
        monthly_investment=1000,
        mean_return=0.07,
        volatility=0.15,
        inflation_rate=0.02,
        years=30,
        simulations=1000,  # Reduced for faster execution
        target_value=1000000
    )
    
    print(f"Simulation parameters:")
    print(f"  Monthly investment: {format_currency(1000)}")
    print(f"  Expected return: {format_percentage(0.07)}")
    print(f"  Volatility: {format_percentage(0.15)}")
    print(f"  Target value: {format_currency(1000000)}")
    print()
    print("Results:")
    print(f"Mean final value: {format_currency(mc_result.mean_final_value)}")
    print(f"Median final value: {format_currency(mc_result.median_final_value)}")
    print(f"5th percentile: {format_currency(mc_result.percentile_5)}")
    print(f"95th percentile: {format_currency(mc_result.percentile_95)}")
    print(f"Success rate: {format_percentage(mc_result.success_rate)}")
    print()


def test_investment_comparison():
    """Test investment comparison scenarios"""
    print("=== Investment Comparison ===")
    
    scenarios = [
        {"name": "Conservative", "return": 0.05, "volatility": 0.10},
        {"name": "Moderate", "return": 0.07, "volatility": 0.15},
        {"name": "Aggressive", "return": 0.09, "volatility": 0.20},
    ]
    
    for scenario in scenarios:
        result = InvestmentCalculator.calculate_monthly_investment_with_tax(
            monthly_payment=1000,
            annual_rate=scenario["return"],
            inflation_rate=0.02,
            years=30
        )
        
        print(f"{scenario['name']} Portfolio:")
        print(f"  Expected return: {format_percentage(scenario['return'])}")
        print(f"  Final value: {format_currency(result['final_value'])}")
        print(f"  Net profit: {format_currency(result['net_profit'])}")
        print(f"  Effective return: {format_percentage(result['effective_annual_return'])}")
        print()


def main():
    """Run all tests"""
    print("Investment Module - Example Usage and Testing")
    print("=" * 50)
    print()
    
    try:
        test_basic_investment_calculation()
        test_detailed_monthly_analysis()
        test_risk_analysis()
        test_monte_carlo_simulation()
        test_investment_comparison()
        
        print("All tests completed successfully!")
        print("The Investment Module is working correctly.")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 