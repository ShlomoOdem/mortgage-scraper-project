# Mortgage Scraper - Core Components

A streamlined mortgage analysis tool that scrapes web data, calculates investments, and generates summaries.

## Core Components

### 1. Web Scraping
- **`src/extractors/final_mortgage_extractor.py`** - Main mortgage data extractor
- **`src/extractors/automated_cp_programs_extractor.py`** - Automated CP programs extractor

### 2. Investment Calculations
- **`src/calculators/invesment.py`** - Investment calculator for remaining money
- **`investment_module/calculator.py`** - Advanced investment calculations with tax/inflation

### 3. Data Processing
- **`src/analyzers/combine_summary_files.py`** - Combines summary files into comprehensive reports

### 4. Main Scripts
- **`scripts/run_comprehensive_mortgage_analysis.py`** - Main analysis runner

## Project Structure

```
mortgage_scraper/
├── src/
│   ├── extractors/               # Web scraping modules
│   │   ├── final_mortgage_extractor.py
│   │   └── automated_cp_programs_extractor.py
│   ├── calculators/              # Investment calculations
│   │   └── invesment.py
│   └── analyzers/                # Data analysis
│       └── combine_summary_files.py
├── scripts/                      # Main execution scripts
│   └── run_comprehensive_mortgage_analysis.py
├── investment_module/            # Advanced investment module
│   ├── calculator.py
│   ├── models.py
│   ├── utils.py
│   └── __init__.py
├── data/
│   ├── raw/                      # Raw input data
│   └── results/                  # Generated results (CSV files preserved)
│       ├── summary_files/        # Individual summary files
│       ├── payments_files/       # Payment schedule files
│       └── combined_mortgage_summaries_*.csv
├── requirements.txt
├── setup.py
└── .gitignore
```

## Quick Start

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Analysis
```bash
python scripts/run_comprehensive_mortgage_analysis.py
```

### Extract Single Mortgage
```bash
python src/extractors/final_mortgage_extractor.py
```

### Combine Summary Files
```bash
python src/analyzers/combine_summary_files.py
```

## Data Files Preserved

All existing CSV files in `data/results/` have been preserved, including:
- Summary files for different mortgage combinations
- Payment schedule files
- Combined analysis results

## Core Functionality

1. **Web Scraping**: Extracts mortgage data from online calculators
2. **Investment Analysis**: Calculates returns on remaining money after mortgage payments
3. **Data Export**: Saves results to CSV files
4. **Summary Generation**: Creates comprehensive mortgage summaries 