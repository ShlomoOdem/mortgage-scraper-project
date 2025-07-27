# Automated CP Programs Extractor

This collection of scripts automatically extracts mortgage amortization data (cp_programs) from the Hebrew mortgage calculator website.

## Quick Start

### Option 1: Simple Shell Script (Recommended)
```bash
# Run single scenario with default values
./run_automated_extraction.sh single

# Run single scenario in visible mode (show browser)
./run_automated_extraction.sh single --no-headless

# Run predefined batch scenarios
./run_automated_extraction.sh batch

# Run batch scenarios in visible mode
./run_automated_extraction.sh batch --no-headless

# Run scenarios from configuration file
./run_automated_extraction.sh config

# Run configurable scenarios in visible mode
./run_automated_extraction.sh config --no-headless

# Run with custom configuration file
./run_automated_extraction.sh custom my_scenarios.json

# Run custom scenarios in visible mode
./run_automated_extraction.sh custom my_scenarios.json --no-headless
```

### Option 2: Direct Python Scripts
```bash
# Single scenario (headless)
python3 automated_cp_programs_extractor.py

# Single scenario in visible mode
python3 automated_cp_programs_extractor.py --no-headless

# Batch scenarios (headless)
python3 batch_cp_programs_extractor.py

# Batch scenarios in visible mode
python3 batch_cp_programs_extractor.py --no-headless

# Configurable scenarios (headless)
python3 configurable_batch_extractor.py

# Configurable scenarios in visible mode
python3 configurable_batch_extractor.py --no-headless

# Configurable scenarios with custom config file
python3 configurable_batch_extractor.py my_scenarios.json

# Configurable scenarios with custom config in visible mode
python3 configurable_batch_extractor.py --no-headless my_scenarios.json
```

## Scripts Overview

### 1. `automated_cp_programs_extractor.py`
- **Purpose**: Extracts cp_programs data for a single mortgage scenario
- **Features**: 
  - Automatically navigates to the calculator
  - Injects loan parameters via JavaScript
  - Waits for calculations to complete
  - Extracts and parses cp_programs data
  - Saves data in multiple formats (JSON, CSV, TXT)

### 2. `batch_cp_programs_extractor.py`
- **Purpose**: Runs multiple predefined scenarios automatically
- **Features**:
  - Runs 5 different mortgage scenarios
  - Waits between scenarios to avoid overwhelming the server
  - Saves individual files for each scenario
  - Creates a batch summary report

### 3. `configurable_batch_extractor.py`
- **Purpose**: Runs scenarios defined in a JSON configuration file
- **Features**:
  - Reads scenarios from `scenarios_config.json`
  - Configurable settings (headless mode, wait times, etc.)
  - Flexible and easy to modify scenarios

### 4. `run_automated_extraction.sh`
- **Purpose**: Easy-to-use shell script wrapper
- **Features**:
  - Simple command-line interface
  - Error handling and validation
  - Multiple execution modes

## Configuration

### Headless vs Visible Mode
The scripts can run in two modes:

- **Headless Mode (Default)**: Runs without showing the browser window. Faster and uses less resources.
- **Visible Mode**: Shows the browser window so you can see what's happening. Useful for debugging.

To run in visible mode, add the `--no-headless` flag:
```bash
# Shell script
./run_automated_extraction.sh single --no-headless

# Python script
python3 automated_cp_programs_extractor.py --no-headless
```

### Default Values
The scripts use these default values:
- **Loan Amount**: 1,000,000
- **Interest Rate**: 3.5%
- **Loan Term**: 30 years
- **CPI Rate**: 2.0%

### Customizing Scenarios

#### Method 1: Edit scenarios_config.json
```json
{
  "scenarios": [
    {
      "name": "My_Custom_Mortgage",
      "loan_amount": "1500000",
      "interest_rate": "4.2",
      "loan_term": "25",
      "cpi_rate": "2.8"
    }
  ],
  "settings": {
    "headless": true,
    "wait_between_scenarios": 5
  }
}
```

#### Method 2: Modify the Python scripts
Edit the parameters in the `main()` function of any script.

## Output Files

For each successful extraction, the scripts create:

1. **Raw Data** (`*_raw_*.txt`)
   - The original cp_programs value as extracted from the form

2. **Parsed JSON** (`*_parsed_*.json`)
   - Structured data with input parameters and monthly payments

3. **Monthly Payments CSV** (`*_payments_*.csv`)
   - All monthly payment details in spreadsheet format

4. **Summary** (`*_summary_*.txt`)
   - Key information and statistics

5. **Batch Summary** (`batch_summary_*.json`)
   - Overview of all scenarios in a batch run

## Data Structure

The extracted data includes:

### Input Data
- Loan amount
- Interest rate
- Loan term (duration)
- CPI rate
- Channel type (קבועה צמודה, etc.)
- Amortization method (שפיצר, etc.)

### Monthly Payment Data
- Month number
- Current duration remaining
- Opening balance
- Interest payment
- Capital payment
- Monthly payment amount
- CPI adjustment
- Closing balance

## Requirements

- Python 3.6+
- Selenium
- Chrome browser
- ChromeDriver (automatically managed by webdriver-manager)

## Installation

```bash
# Install required Python packages
pip install selenium webdriver-manager

# Make shell script executable
chmod +x run_automated_extraction.sh
```

## Usage Examples

### Single Scenario
```bash
# Run with default values
./run_automated_extraction.sh single

# Or directly
python3 automated_cp_programs_extractor.py
```

### Multiple Scenarios
```bash
# Run predefined batch
./run_automated_extraction.sh batch

# Run from configuration file
./run_automated_extraction.sh config

# Run with custom config
./run_automated_extraction.sh custom my_scenarios.json
```

### Custom Configuration
Create your own `my_scenarios.json`:
```json
{
  "scenarios": [
    {
      "name": "High_Value_Mortgage",
      "loan_amount": "3000000",
      "interest_rate": "3.8",
      "loan_term": "20",
      "cpi_rate": "2.5"
    }
  ],
  "settings": {
    "headless": false,
    "wait_between_scenarios": 10
  }
}
```

## Troubleshooting

### Common Issues

1. **Chrome not found**
   - Install Google Chrome browser
   - The script will automatically download ChromeDriver

2. **Page load timeout**
   - Check internet connection
   - Increase timeout values in the configuration

3. **Form not found**
   - The website structure may have changed
   - Check if the calculator page is accessible

4. **Empty cp_programs value**
   - Calculations may not have completed
   - Try increasing the calculation timeout

### Debug Mode
Set `headless: false` in the configuration to see the browser in action.

## File Naming Convention

Files are named with timestamps to avoid conflicts:
- `automated_cp_programs_parsed_20250724_143022.json`
- `batch_summary_20250724_143022.json`
- `configurable_batch_summary_20250724_143022.json`

## Notes

- The scripts include delays between requests to be respectful to the server
- All data is saved with UTF-8 encoding to properly handle Hebrew text
- The headless mode can be disabled for debugging by setting `headless: false`
- Failed extractions are logged and reported in batch summaries 