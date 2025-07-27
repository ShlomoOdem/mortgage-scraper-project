# Investment Module Migration Guide

This guide explains how to use the isolated investment module in your new project.

## What Was Extracted

The investment module has been completely isolated from the mortgage planner project and includes:

### Core Components
- **InvestmentCalculator**: Main calculation class with all investment methods
- **Data Models**: Clean dataclasses for input/output data
- **Utility Functions**: Mathematical and formatting utilities
- **Risk Analysis**: Volatility, Sharpe ratio, VaR calculations
- **Monte Carlo Simulations**: Scenario analysis capabilities

### Key Features Preserved
- ✅ Future value calculations with compound interest
- ✅ Tax calculations with inflation adjustments
- ✅ Monthly investment planning
- ✅ Risk metrics calculation
- ✅ Monte Carlo simulations
- ✅ Portfolio analysis tools

### Dependencies Removed
- ❌ SQLAlchemy database models
- ❌ FastAPI web framework
- ❌ Mortgage-specific calculations
- ❌ Database connections
- ❌ Web API endpoints

## Installation in New Project

### 1. Copy the Module
Copy the entire `investment_module` directory to your new project:

```bash
cp -r investment_module/ /path/to/your/new/project/
```

### 2. Install Dependencies
```bash
cd /path/to/your/new/project/
pip install -r investment_module/requirements.txt
```

### 3. Import and Use
```python
from investment_module import InvestmentCalculator, InvestmentData

# Your investment calculations here
```

## API Changes

### Old API (Mortgage Planner)
```python
# Old way - required database and mortgage context
from app.services.investment_calculator import InvestmentCalculator
from app.models.investment import Investment
from app.core.database import get_db

# Required database session and mortgage objects
result = InvestmentCalculator.calculate_monthly_investments_detailed(
    mortgage_payment_schedule=payment_schedule,
    monthly_income=5000,
    stock_annual_rate=0.07,
    inflation_rate=0.02
)
```

### New API (Isolated Module)
```python
# New way - standalone, no database required
from investment_module import InvestmentCalculator, InvestmentData

# Clean, simple API
data = InvestmentData(
    monthly_investment=1000,
    stock_annual_rate=0.07,
    inflation_rate=0.02,
    years=30
)

result = InvestmentCalculator.calculate_monthly_investment_with_tax(
    monthly_payment=data.monthly_investment,
    annual_rate=data.stock_annual_rate,
    inflation_rate=data.inflation_rate,
    years=data.years
)
```

## Key Method Mappings

| Old Method | New Method | Notes |
|------------|------------|-------|
| `calculate_monthly_investment_with_tax()` | `calculate_monthly_investment_with_tax()` | Same signature |
| `calculate_monthly_investments_detailed()` | `calculate_monthly_investments_detailed()` | Same signature |
| `calculate_investment_summary()` | `calculate_investment_summary()` | Same signature |
| `calculate_tax_on_profit()` | `calculate_tax_on_profit()` | Same signature |
| N/A | `calculate_risk_metrics()` | New risk analysis |
| N/A | `run_monte_carlo_simulation()` | New Monte Carlo |

## Data Structure Changes

### Old Database Models
```python
# Old - SQLAlchemy models
class Investment(Base):
    __tablename__ = "investments"
    id = Column(Integer, primary_key=True)
    mortgage_id = Column(Integer, ForeignKey("mortgages.id"))
    # ... database fields
```

### New Data Classes
```python
# New - Clean dataclasses
@dataclass
class InvestmentData:
    monthly_investment: float
    stock_annual_rate: float = 0.07
    inflation_rate: float = 0.02
    years: int = 30
    tax_rate: float = 0.25

@dataclass
class InvestmentResult:
    month: int
    investment_amount: float
    future_value: float
    # ... calculation results
```

## Example Migration

### Before (Mortgage Planner)
```python
from app.services.investment_calculator import InvestmentCalculator
from app.models.mortgage import Mortgage
from app.core.database import get_db

def analyze_investment(mortgage_id: int, db: Session):
    mortgage = db.query(Mortgage).filter(Mortgage.id == mortgage_id).first()
    payment_schedule = get_mortgage_payment_schedule(mortgage)
    
    result = InvestmentCalculator.calculate_monthly_investments_detailed(
        mortgage_payment_schedule=payment_schedule,
        monthly_income=5000,
        stock_annual_rate=0.07,
        inflation_rate=0.02
    )
    
    return result
```

### After (Isolated Module)
```python
from investment_module import InvestmentCalculator, InvestmentData

def analyze_investment(monthly_income: float, mortgage_payments: list = None):
    # Create payment schedule (can be empty for pure investment)
    payment_schedule = mortgage_payments or []
    
    result = InvestmentCalculator.calculate_monthly_investments_detailed(
        payment_schedule=payment_schedule,
        monthly_income=monthly_income,
        stock_annual_rate=0.07,
        inflation_rate=0.02
    )
    
    return result
```

## Testing the Module

Run the included test example:

```bash
cd investment_module
python test_example.py
```

This will demonstrate all the key functionality and verify the module works correctly.

## Integration with Web Frameworks

### FastAPI Integration
```python
from fastapi import FastAPI
from investment_module import InvestmentCalculator, InvestmentData
from pydantic import BaseModel

app = FastAPI()

class InvestmentRequest(BaseModel):
    monthly_investment: float
    stock_annual_rate: float = 0.07
    inflation_rate: float = 0.02
    years: int = 30

@app.post("/calculate-investment")
async def calculate_investment(request: InvestmentRequest):
    result = InvestmentCalculator.calculate_monthly_investment_with_tax(
        monthly_payment=request.monthly_investment,
        annual_rate=request.stock_annual_rate,
        inflation_rate=request.inflation_rate,
        years=request.years
    )
    return result
```

### Flask Integration
```python
from flask import Flask, request, jsonify
from investment_module import InvestmentCalculator

app = Flask(__name__)

@app.route('/calculate-investment', methods=['POST'])
def calculate_investment():
    data = request.get_json()
    
    result = InvestmentCalculator.calculate_monthly_investment_with_tax(
        monthly_payment=data['monthly_investment'],
        annual_rate=data['stock_annual_rate'],
        inflation_rate=data['inflation_rate'],
        years=data['years']
    )
    
    return jsonify(result)
```

## Advanced Features

### Risk Analysis
```python
from investment_module import InvestmentCalculator

# Get monthly portfolio values
monthly_values = detailed_result['summary']['monthly_values']

# Calculate risk metrics
risk_metrics = InvestmentCalculator.calculate_risk_metrics(
    monthly_values=monthly_values,
    risk_free_rate=0.03
)

print(f"Volatility: {risk_metrics.volatility:.2%}")
print(f"Sharpe Ratio: {risk_metrics.sharpe_ratio:.2f}")
```

### Monte Carlo Simulation
```python
from investment_module import InvestmentCalculator

mc_result = InvestmentCalculator.run_monte_carlo_simulation(
    monthly_investment=1000,
    mean_return=0.07,
    volatility=0.15,
    inflation_rate=0.02,
    years=30,
    simulations=10000,
    target_value=1000000
)

print(f"Success rate: {mc_result.success_rate:.1%}")
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure the `investment_module` directory is in your Python path
2. **Missing Dependencies**: Install requirements with `pip install -r requirements.txt`
3. **Data Type Errors**: Use the provided dataclasses for input data

### Getting Help

- Check the `test_example.py` file for usage examples
- Review the `README.md` for comprehensive documentation
- The module is self-contained and should work independently

## Next Steps

1. **Test the Module**: Run `python test_example.py` to verify functionality
2. **Integrate**: Import and use in your new project
3. **Customize**: Modify parameters and add your own business logic
4. **Extend**: Add new calculation methods as needed

The investment module is now completely independent and ready for use in any Python project! 