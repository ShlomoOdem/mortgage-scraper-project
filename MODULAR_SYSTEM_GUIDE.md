# Modular Mortgage Analysis System

## Overview

This system has been restructured to be completely modular, separating data extraction from analysis. This allows for:

1. **Independent operation** of each phase
2. **Reusability** of extracted data
3. **Flexibility** in analysis parameters
4. **Scalability** for batch processing

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   EXTRACTION    │    │     STORAGE     │    │    ANALYSIS     │
│     PHASE       │───▶│     PHASE       │───▶│     PHASE       │
│                 │    │                 │    │                 │
│ • Web scraping  │    │ • CSV files     │    │ • Investment    │
│ • Data parsing  │    │ • Raw data      │    │ • Weighted      │
│ • CSV output    │    │ • Metadata      │    │   payment       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Directory Structure

```
mortgage_scraper/
├── data/
│   ├── raw/                    # Raw extracted data
│   │   ├── payments_files/     # Monthly payment CSV files
│   │   └── summary_files/      # Basic summary CSV files
│   └── analyzed/               # Analysis results
│       ├── payments_files/     # Enhanced payment files
│       └── summary_files/      # Analysis summary files
├── src/
│   ├── extractors/             # Data extraction modules
│   │   ├── automated_cp_programs_extractor.py
│   │   └── final_mortgage_extractor.py
│   ├── analyzers/              # Analysis modules
│   │   ├── modular_analyzer.py
│   │   └── combine_summary_files.py
│   └── calculators/            # Calculation modules
│       ├── invesment.py
│       └── weighted_payment_calculator.py
├── test_modular_process.py     # Test script
├── run_modular_workflow.py     # Main workflow runner
└── MODULAR_SYSTEM_GUIDE.md     # This guide
```

## Phase 1: Data Extraction

### Purpose
Extract mortgage data from web calculators and save to CSV files without any analysis.

### Files
- **`src/extractors/automated_cp_programs_extractor.py`** - Main extraction module
- **`src/extractors/final_mortgage_extractor.py`** - Alternative extraction module

### Output
- **`data/raw/payments_files/`** - Monthly payment CSV files
- **`data/raw/summary_files/`** - Basic summary CSV files

### Usage
```bash
# Run extraction only
python3 run_modular_workflow.py --extract

# Run extraction with visible browser
python3 run_modular_workflow.py --extract --no-headless

# Extract specific number of combinations
python3 run_modular_workflow.py --extract --combinations 5
```

### File Naming Convention
```
loan_{CHANNEL}_int_{INTEREST_RATE}_term_{TERM_MONTHS}_infl_{INFLATION_RATE}_payments.csv
loan_{CHANNEL}_int_{INTEREST_RATE}_term_{TERM_MONTHS}_infl_{INFLATION_RATE}_summary.csv
```

Example:
```
loan_קבועה_צמודה_int_3.5_term_360_infl_2.0_payments.csv
loan_קבועה_צמודה_int_3.5_term_360_infl_2.0_summary.csv
```

## Phase 2: Data Analysis

### Purpose
Process the extracted CSV files and apply investment and weighted payment calculations.

### Files
- **`src/analyzers/modular_analyzer.py`** - Main analysis module
- **`src/calculators/invesment.py`** - Investment calculations
- **`src/calculators/weighted_payment_calculator.py`** - Weighted payment calculations

### Output
- **`data/analyzed/payments_files/`** - Enhanced payment CSV files
- **`data/analyzed/summary_files/`** - Analysis summary CSV files

### Usage
```bash
# Run analysis only
python3 run_modular_workflow.py --analyze

# Run analysis with custom monthly income
python3 run_modular_workflow.py --analyze --income 15000

# Run analysis on existing data
python3 src/analyzers/modular_analyzer.py --all
```

### Analysis Features

#### Investment Analysis
- Calculates investment opportunities from remaining income after mortgage payments
- Accounts for inflation and taxes
- Provides compound interest calculations over the mortgage term

#### Weighted Payment Analysis
- Calculates a fixed monthly payment for 30 years
- Balances investment profits against mortgage interest
- Uses iterative optimization to find the optimal payment amount

## Complete Workflow

### Run Both Phases
```bash
# Run complete workflow
python3 run_modular_workflow.py --full

# Run with custom parameters
python3 run_modular_workflow.py --full --income 15000 --combinations 3 --no-headless
```

### Step-by-Step Process
1. **Extraction**: Web scraping extracts mortgage data to CSV files
2. **Storage**: Raw data is saved in organized directory structure
3. **Analysis**: CSV files are processed for investment and weighted payment analysis
4. **Results**: Enhanced data and analysis summaries are generated

## Testing

### Test the Modular System
```bash
# Run comprehensive test
python3 test_modular_process.py
```

This test:
- Creates mock mortgage data
- Runs modular analysis
- Tests batch processing
- Validates file generation

## Key Benefits

### 1. Modularity
- Each phase can run independently
- Easy to debug and maintain
- Clear separation of concerns

### 2. Reusability
- Extracted data can be analyzed multiple times with different parameters
- No need to re-extract data for different analysis scenarios

### 3. Scalability
- Batch processing of multiple mortgage combinations
- Parallel processing capabilities
- Easy to add new analysis types

### 4. Flexibility
- Customizable analysis parameters (monthly income, return rates, etc.)
- Multiple extraction sources
- Extensible analysis modules

## File Formats

### Raw Payment Files
```csv
month,month_payment,principal,interest,balance
1,4490.00,1347.00,3143.00,998653.00
2,4490.00,1350.00,3140.00,997303.00
...
```

### Raw Summary Files
```csv
Parameter,Value
Loan Type,קבועה צמודה
Interest Rate (%),3.5
Loan Term (months),360
Inflation Rate (%),2.0
Loan Amount,1000000
Total Monthly Payments,360
Total Mortgage Interest,616400.00
Extraction Timestamp,20250125_123456
```

### Enhanced Payment Files
```csv
month,month_payment,principal,interest,balance,monthly_income,monthly_investment
1,4490.00,1347.00,3143.00,998653.00,12000,7510
2,4490.00,1350.00,3140.00,997303.00,12000,7510
...
```

### Enhanced Summary Files
```csv
Parameter,Value
Loan Type,קבועה צמודה
Interest Rate (%),3.5
...
Monthly Income,12000.00
Total Investment Amount,2703600.00
Total Investment Profit After Tax,3643930.00
Weighted Monthly Payment (30 years),5414.00
Weighted Cost (should be ~0),0.12
Analysis Timestamp,20250125_123456
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure `src/` is in Python path
   - Check file permissions

2. **Web Scraping Failures**
   - Try `--no-headless` mode
   - Check internet connection
   - Verify website structure hasn't changed

3. **Analysis Errors**
   - Verify CSV files exist in `data/raw/`
   - Check file formats and encoding
   - Ensure sufficient disk space

### Debug Mode
```bash
# Run with verbose output
python3 -v run_modular_workflow.py --analyze

# Check file structure
ls -la data/raw/payments_files/
ls -la data/analyzed/summary_files/
```

## Future Enhancements

1. **Additional Analysis Types**
   - Risk assessment
   - Monte Carlo simulations
   - Sensitivity analysis

2. **Data Sources**
   - Multiple web calculators
   - API integrations
   - Manual data entry

3. **Output Formats**
   - Excel files
   - JSON reports
   - Interactive dashboards

4. **Performance**
   - Parallel processing
   - Caching mechanisms
   - Database storage

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the test scripts
3. Examine the generated CSV files
4. Check console output for error messages 