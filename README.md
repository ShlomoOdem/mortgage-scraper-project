# Mortgage Scraper Project

A comprehensive mortgage analysis and scraping tool for Israeli mortgage market data.

## Project Structure

```
mortgage_scraper/
├── src/                          # Source code
│   ├── extractors/               # Data extraction modules
│   │   ├── automated_cp_programs_extractor.py
│   │   ├── batch_cp_programs_extractor.py
│   │   ├── cp_programs_extractor.py
│   │   ├── debug_cp_programs.py
│   │   ├── extract_from_sample.py
│   │   ├── final_mortgage_extractor.py
│   │   ├── comprehensive_mortgage_extractor.py
│   │   ├── targeted_amortization_extractor.py
│   │   ├── robust_mortgage_extractor.py
│   │   └── mortgage_data_extractor.py
│   ├── calculators/              # Mortgage calculation modules
│   │   ├── enhanced_mortgage_calculator.py
│   │   ├── mortgage_calculator_interaction.py
│   │   └── invesment.py
│   ├── analyzers/                # Analysis modules
│   │   ├── calculator_analyzer.py
│   │   ├── combine_summary_files.py
│   │   └── generate_mortgage_combinations.py
│   └── utils/                    # Utility functions
├── scripts/                      # Executable scripts
│   ├── run_automated_extraction.sh
│   ├── run_comprehensive_mortgage_analysis.py
│   ├── run_full_analysis_headless.py
│   └── run_multiple_scenarios.sh
├── data/                         # Data files
│   ├── raw/                      # Raw input data
│   │   ├── mashfix.xls
│   │   ├── pribmash.xls
│   │   └── sample.txt
│   ├── processed/                # Processed data
│   │   ├── all_mortgage_results_20250724_003939.json
│   │   ├── mortgage_combinations_*.json
│   │   ├── processed_combinations.json
│   │   └── test_mortgage_combinations.json
│   └── results/                  # Analysis results
│       ├── combined_mortgage_summaries_20250725_042251.csv
│       ├── payments_files/       # Payment schedule files
│       └── summary_files/        # Summary analysis files
├── docs/                         # Documentation
│   ├── README.md
│   ├── README_COMPREHENSIVE_ANALYSIS.md
│   ├── USAGE_GUIDE.md
│   ├── COMBINED_ANALYSIS_GUIDE.md
│   └── AUTOMATED_EXTRACTION_README.md
├── config/                       # Configuration files
│   └── configurable_batch_extractor.py
├── tests/                        # Test files
└── investment_module/            # Investment analysis module
    ├── __init__.py
    ├── calculator.py
    ├── models.py
    ├── utils.py
    ├── test_example.py
    ├── setup.py
    ├── requirements.txt
    ├── README.md
    ├── EXTRACTION_SUMMARY.md
    └── MIGRATION_GUIDE.md
```

## Quick Start

### Running Analysis Scripts

```bash
# Run comprehensive mortgage analysis
python scripts/run_comprehensive_mortgage_analysis.py

# Run automated extraction
bash scripts/run_automated_extraction.sh

# Run full analysis in headless mode
python scripts/run_full_analysis_headless.py
```

### Using Extractors

```bash
# Extract mortgage data
python src/extractors/final_mortgage_extractor.py

# Extract CP programs
python src/extractors/automated_cp_programs_extractor.py
```

### Using Calculators

```bash
# Enhanced mortgage calculator
python src/calculators/enhanced_mortgage_calculator.py

# Investment analysis
python src/calculators/invesment.py
```

## Data Organization

- **Raw Data**: Input files like Excel spreadsheets and sample data
- **Processed Data**: JSON files with extracted and processed mortgage data
- **Results**: CSV files with analysis results, payment schedules, and summaries

## Documentation

See the `docs/` directory for detailed documentation:
- `README_COMPREHENSIVE_ANALYSIS.md` - Comprehensive analysis guide
- `USAGE_GUIDE.md` - Usage instructions
- `COMBINED_ANALYSIS_GUIDE.md` - Combined analysis workflow
- `AUTOMATED_EXTRACTION_README.md` - Automated extraction guide

## Investment Module

The `investment_module/` contains a separate investment analysis package with its own documentation and requirements.

## Development

To add new functionality:
1. Place extractors in `src/extractors/`
2. Place calculators in `src/calculators/`
3. Place analyzers in `src/analyzers/`
4. Place utility functions in `src/utils/`
5. Place executable scripts in `scripts/`
6. Place configuration files in `config/`
7. Place test files in `tests/` 