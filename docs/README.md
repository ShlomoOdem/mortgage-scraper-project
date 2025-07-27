# Hebrew Mortgage Calculator Data Extractor

This project contains scripts to automatically extract mortgage data from the Hebrew mortgage calculator at [mashcantaman.co.il](https://mashcantaman.co.il/%D7%9E%D7%97%D7%A9%D7%91%D7%95%D7%9F-%D7%9E%D7%A9%D7%9B%D7%A0%D7%AA%D7%90/).

## Features

- ✅ **Automated interaction** with the Hebrew mortgage calculator
- ✅ **JavaScript injection** to handle complex Vue.js interface
- ✅ **Targets תמהיל 1 (Mix 1)** specifically
- ✅ **Extracts data from לוח סילוקין מלא (Full Amortization Table)**
- ✅ **Multiple output formats**: JSON, CSV, and raw text
- ✅ **Batch processing** for multiple scenarios
- ✅ **Command-line interface** for custom parameters

## Requirements

```bash
pip install selenium webdriver-manager pandas
```

## Usage

### Single Scenario

```bash
python3 final_mortgage_extractor.py <loan_amount> <interest_rate> <loan_term> <cpi_rate> <scenario_name>
```

**Example:**
```bash
python3 final_mortgage_extractor.py 1000000 3.5 30 2.0 Basic_Mortgage
```

### Multiple Scenarios (Batch)

```bash
./run_multiple_scenarios.sh
```

This will run 6 different mortgage scenarios automatically.

### Default Test Scenarios

If no command-line arguments are provided, the script runs 3 default scenarios:

1. **Basic Mortgage**: ₪1,000,000 at 3.5% for 30 years
2. **High Amount Mortgage**: ₪2,000,000 at 4.0% for 25 years  
3. **Short Term Mortgage**: ₪500,000 at 5.0% for 15 years

## Output Files

For each scenario, the script generates:

- **JSON file**: `final_mortgage_<scenario>_<timestamp>.json` - Complete structured data
- **CSV files**: `final_mortgage_<scenario>_table_<index>_<timestamp>.csv` - Table data in spreadsheet format
- **Text file**: `final_mortgage_<scenario>_raw_<timestamp>.txt` - Raw extracted text

## Scripts Overview

### Main Scripts

1. **`final_mortgage_extractor.py`** - Main extraction script with command-line interface
2. **`run_multiple_scenarios.sh`** - Batch runner for multiple scenarios
3. **`comprehensive_mortgage_extractor.py`** - Advanced version with comprehensive search
4. **`targeted_amortization_extractor.py`** - Targeted version for amortization table
5. **`robust_mortgage_extractor.py`** - Robust version with JavaScript injection

### Analysis Scripts

1. **`calculator_analyzer.py`** - Analyzes calculator structure
2. **`enhanced_mortgage_calculator.py`** - Enhanced interaction version
3. **`mortgage_calculator_interaction.py`** - Basic interaction script

## How It Works

1. **Page Loading**: Loads the mortgage calculator page
2. **Tab Selection**: Ensures we're on תמהיל 1 (Mix 1) tab
3. **Value Injection**: Uses JavaScript to inject loan parameters:
   - Loan amount (סכום)
   - Interest rate (ריבית)
   - Loan term (תקופה)
   - CPI rate (מדד)
4. **Calculation Wait**: Waits for calculations to update
5. **Amortization Link**: Finds and clicks "לוח סילוקין מלא" (Full Amortization Table)
6. **Data Extraction**: Extracts all table data and text content
7. **File Saving**: Saves data in multiple formats

## Extracted Data

The script extracts:

- **Table data**: All HTML tables found on the page
- **Currency amounts**: All ₪ amounts found in the text
- **Percentages**: All percentage values
- **Summary data**: Specific Hebrew terms and their associated values:
  - Monthly payment (החזר חודשי)
  - Total payments (סה״כ תשלומים)
  - Total interest (סה״כ ריבית)
  - Loan amount (סכום המשכנתא)
  - Interest rate (ריבית)
  - Loan term (תקופה)

## Troubleshooting

### Common Issues

1. **"Element not interactable"**: The script uses JavaScript injection to handle this
2. **"Amortization link not found"**: The script uses multiple search strategies
3. **"No tables found"**: The amortization table might be in a new tab/window

### Solutions

- The script automatically handles most interaction issues
- Multiple search strategies ensure the amortization link is found
- Automatic tab switching handles new window scenarios

## Performance

- **Single scenario**: ~30-45 seconds
- **Multiple scenarios**: ~3-5 minutes for 6 scenarios
- **Headless mode**: Runs without browser UI for faster execution

## Notes

- The script runs in headless mode for faster execution
- All data is saved with timestamps to avoid overwrites
- The script handles Hebrew text and currency symbols properly
- Multiple fallback strategies ensure reliable data extraction 