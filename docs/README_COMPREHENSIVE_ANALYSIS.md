# Comprehensive Mortgage Analysis System

This system generates and analyzes all possible mortgage combinations based on real interest rate data from the Bank of Israel.

## 🎯 **What This System Does**

1. **Generates 864 mortgage combinations** based on:
   - Fixed loan amount: 100,000 ILS
   - 6 loan terms: 60, 120, 180, 240, 300, 360 months (5-30 years)
   - 4 inflation rates: 1%, 2%, 3%, 4%
   - 12 channel types (loan types)
   - 3 amortization methods
   - Real interest rates from Bank of Israel tables

2. **Automatically scrapes** mortgage calculator data for each combination
3. **Calculates investment analysis** for each mortgage scenario
4. **Saves results** in organized CSV files

## 📊 **Interest Rate Tables Used**

### No Inflation Loans (Prime, Fixed Unlinked, Variable Unlinked Every 5)
| Loan Term | Interest Rate |
|-----------|---------------|
| 5 years   | 5.04%         |
| 10 years  | 4.83%         |
| 15 years  | 4.96%         |
| 20 years  | 4.97%         |
| 25 years  | 4.97%         |
| 30 years  | 5.05%         |

### Inflation-Adjusted Loans (Fixed Linked, Variable Linked, etc.)
| Loan Term | Interest Rate |
|-----------|---------------|
| 5 years   | 3.83%         |
| 10 years  | 3.35%         |
| 15 years  | 3.67%         |
| 20 years  | 3.63%         |
| 25 years  | 3.63%         |
| 30 years  | 3.55%         |

## 🚀 **How to Use**

### Step 1: Generate All Combinations
```bash
python3 generate_mortgage_combinations.py
```
This creates:
- `mortgage_combinations_YYYYMMDD_HHMMSS.json` (all 864 combinations)
- `test_mortgage_combinations.json` (first 20 combinations for testing)

### Step 2: Run Analysis

#### Test with small subset (recommended first):
```bash
python3 run_comprehensive_mortgage_analysis.py --max 10 --no-headless
```

#### Run full analysis:
```bash
python3 run_comprehensive_mortgage_analysis.py --full --no-headless
```

#### Run in headless mode (faster):
```bash
python3 run_comprehensive_mortgage_analysis.py --full
```

### Step 3: Check Results
Results are saved in:
- `payments_files/` - Detailed monthly payment data with investment analysis
- `summary_files/` - Summary statistics for each mortgage

## 📁 **File Structure**

```
mortgage_scraper/
├── generate_mortgage_combinations.py          # Generate all combinations
├── run_comprehensive_mortgage_analysis.py     # Run the analysis
├── automated_cp_programs_extractor.py         # Core scraper
├── invesment.py                              # Investment calculations
├── processed_combinations.json               # Progress tracking file
├── payments_files/                           # Monthly payment data
│   ├── loan_פריים_int_5.04_term_60_infl_1.0_payments.csv
│   ├── loan_קבועה_צמודה_int_3.35_term_120_infl_2.0_payments.csv
│   └── ...
├── summary_files/                            # Summary statistics
│   ├── loan_פריים_int_5.04_term_60_infl_1.0_summary.csv
│   ├── loan_קבועה_צמודה_int_3.35_term_120_infl_2.0_summary.csv
│   └── ...
└── mortgage_combinations_*.json              # Generated combinations
```

## 📈 **Investment Analysis**

For each mortgage, the system calculates:
- **Monthly Income**: Fixed at 1,200 ILS
- **Monthly Investment**: (1,200 - monthly mortgage payment)
- **Investment Growth**: 7% annual return, 3% inflation, 25% tax
- **Total Cost**: Mortgage interest - Investment profit after tax

## 🔄 **Progress Tracking**

The system automatically tracks which combinations have been processed to avoid recomputation:

### Tracking Features:
- **Automatic Tracking**: Each successful combination is marked as processed
- **Resume Capability**: Can stop and resume analysis from where it left off
- **Status Checking**: Check progress without running analysis
- **Reset Option**: Start fresh by resetting the tracking file

### Tracking File (`processed_combinations.json`):
```json
{
  "last_updated": "2025-07-24T22:30:09.247094",
  "total_processed": 5,
  "processed_combinations": [
    "100000_5.04_60_1.0_פריים_שפיצר",
    "100000_5.04_60_1.0_פריים_קרן שווה",
    ...
  ]
}
```

### Usage Examples:
```bash
# Check current progress
python3 run_comprehensive_mortgage_analysis.py --status

# Reset tracking and start fresh
python3 run_comprehensive_mortgage_analysis.py --reset-tracking

# Use custom tracking file
python3 run_comprehensive_mortgage_analysis.py --tracking my_tracking.json
```

## 🔧 **Command Line Options**

### `run_comprehensive_mortgage_analysis.py`:
- `--combinations, -c`: Specify combinations file (default: test_mortgage_combinations.json)
- `--no-headless, -n`: Run in visible mode (show browser)
- `--max, -m`: Maximum combinations to process (for testing)
- `--full, -f`: Use full combinations file (all 864 combinations)
- `--tracking, -t`: Specify tracking file (default: processed_combinations.json)
- `--status, -s`: Show tracking status without running analysis
- `--reset-tracking, -r`: Reset tracking file (start fresh)

### Examples:
```bash
# Test with 5 combinations, visible mode
python3 run_comprehensive_mortgage_analysis.py --max 5 --no-headless

# Run full analysis in headless mode
python3 run_comprehensive_mortgage_analysis.py --full

# Use specific combinations file
python3 run_comprehensive_mortgage_analysis.py --combinations my_combinations.json

# Check progress without running analysis
python3 run_comprehensive_mortgage_analysis.py --status

# Reset tracking and start fresh
python3 run_comprehensive_mortgage_analysis.py --reset-tracking
```

## 📊 **Sample Results**

### Summary File Example:
```csv
Parameter,Value
Loan Type,פריים
Interest Rate (%),5.04
Loan Term (months),60
Inflation Rate (%),1.0
Loan Amount,100000
Channel,פריים
Amortization Method,שפיצר
Total Monthly Payments,60
Total Mortgage Interest,2520.00
Total Investment Amount,46800.00
Total Investment Final Value,74520.00
Total Investment Profit,13860.00
Total Investment Taxes,3465.00
Total Investment Profit After Tax,10395.00
Total Cost (Interest - Investment Profit),-7875.00
```

### Payments File Example:
```csv
month,monthly_income,monthly_investment,investment_final_value,investment_profit_after_tax
1,1200,780,1087.84,139.37
2,1200,780,1081.72,136.45
...
```

## ⚡ **Performance**

- **864 total combinations** generated
- **~2-3 seconds per combination** (depending on website response)
- **Full analysis time**: ~30-45 minutes for all combinations
- **Memory usage**: Minimal (processes one combination at a time)

## 🎯 **Key Features**

✅ **Real Interest Rates**: Based on actual Bank of Israel data  
✅ **Complete Coverage**: All channel types and amortization methods  
✅ **Investment Analysis**: Comprehensive investment calculations  
✅ **Progress Tracking**: Automatically tracks processed combinations to avoid recomputation  
✅ **Error Handling**: Continues processing even if some combinations fail  
✅ **Organized Output**: Clear file structure and naming  
✅ **Flexible Testing**: Can test subsets before running full analysis  
✅ **Resume Capability**: Can stop and resume analysis from where it left off  

## 🚨 **Important Notes**

1. **Internet Required**: The scraper needs to access the mortgage calculator website
2. **Rate Limiting**: The system includes delays to be respectful to the website
3. **Browser Dependencies**: Requires Chrome and ChromeDriver
4. **Hebrew Support**: Full support for Hebrew channel names and text

## 🔍 **Troubleshooting**

### Common Issues:
- **"ChromeDriver not found"**: Run `pip install webdriver-manager`
- **"Page not loading"**: Check internet connection
- **"Element not found"**: Website structure may have changed

### Debug Mode:
Use `--no-headless` to see the browser and debug issues visually.

---

**Ready to analyze 864 mortgage scenarios with real interest rates and investment analysis! 🚀** 