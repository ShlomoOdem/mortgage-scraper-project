# Mortgage Analysis Usage Guide

## Quick Start - Headless Mode

### 1. Generate All Combinations
```bash
python3 generate_mortgage_combinations.py
```
This creates `mortgage_combinations_YYYYMMDD_HHMMSS.json` with all 864 combinations.

### 2. Run Full Analysis in Headless Mode
```bash
python3 run_full_analysis_headless.py
```

That's it! The script will:
- Automatically find the latest combinations file
- Run all combinations in headless mode (no browser window)
- Track progress automatically
- Save results to `payments_files/` and `summary_files/`
- Resume from where it left off if interrupted

## What You Get

### Files Created:
- **`payments_files/`** - Detailed monthly payment data with investment analysis
- **`summary_files/`** - Summary statistics for each mortgage
- **`processed_combinations.json`** - Progress tracking (can resume later)

### Example Output Files:
```
payments_files/
├── loan_פריים_int_5.04_term_60_infl_1.0_payments.csv
├── loan_קבועה_צמודה_int_3.35_term_120_infl_2.0_payments.csv
└── ...

summary_files/
├── loan_פריים_int_5.04_term_60_infl_1.0_summary.csv
├── loan_קבועה_צמודה_int_3.35_term_120_infl_2.0_summary.csv
└── ...
```

## Monitoring Progress

### Check Progress Without Running:
```bash
python3 run_comprehensive_mortgage_analysis.py --status
```

### Expected Output:
```
============================================================
TRACKING STATUS
============================================================
Total combinations: 864
Already processed: 245
Remaining to process: 619
Progress: 28.4%
```

## Interruption and Resume

### If You Need to Stop:
- Press `Ctrl+C` to stop the analysis
- Progress is automatically saved
- Run the script again to resume from where it left off

### Reset and Start Fresh:
```bash
python3 run_comprehensive_mortgage_analysis.py --reset-tracking
python3 run_full_analysis_headless.py
```

## Performance

- **Total Combinations**: 864
- **Processing Time**: ~30-45 minutes for all combinations
- **Memory Usage**: Minimal (processes one at a time)
- **Network**: Requires internet connection

## Troubleshooting

### Common Issues:
1. **"No combinations file found"** - Run `generate_mortgage_combinations.py` first
2. **"ChromeDriver not found"** - Run `pip install webdriver-manager`
3. **"Page not loading"** - Check internet connection

### Debug Mode (if needed):
```bash
python3 run_comprehensive_mortgage_analysis.py --full --no-headless
```

## Results Analysis

### Summary Files Include:
- Loan parameters (amount, interest, term, channel, amortization)
- Total mortgage interest
- Investment analysis (monthly income: 1,200 ILS)
- Total cost calculation (interest - investment profit)

### Payments Files Include:
- Monthly payment breakdown
- Investment amounts and returns
- Inflation-adjusted calculations

---

**Ready to analyze 864 mortgage scenarios with real interest rates! 🚀** 