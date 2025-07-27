#!/bin/bash

# Hebrew Mortgage Calculator - Multiple Scenarios Runner
# This script runs multiple mortgage scenarios quickly

echo "=== Hebrew Mortgage Calculator - Multiple Scenarios Runner ==="
echo ""

# Scenario 1: Basic Mortgage
echo "Running Scenario 1: Basic Mortgage"
python3 final_mortgage_extractor.py 1000000 3.5 30 2.0 Basic_Mortgage
echo ""

# Scenario 2: High Amount Mortgage
echo "Running Scenario 2: High Amount Mortgage"
python3 final_mortgage_extractor.py 2000000 4.0 25 1.5 High_Amount_Mortgage
echo ""

# Scenario 3: Short Term Mortgage
echo "Running Scenario 3: Short Term Mortgage"
python3 final_mortgage_extractor.py 500000 5.0 15 3.0 Short_Term_Mortgage
echo ""

# Scenario 4: Medium Mortgage
echo "Running Scenario 4: Medium Mortgage"
python3 final_mortgage_extractor.py 1500000 4.2 20 2.5 Medium_Mortgage
echo ""

# Scenario 5: Low Interest Mortgage
echo "Running Scenario 5: Low Interest Mortgage"
python3 final_mortgage_extractor.py 800000 2.8 25 1.8 Low_Interest_Mortgage
echo ""

# Scenario 6: High Interest Mortgage
echo "Running Scenario 6: High Interest Mortgage"
python3 final_mortgage_extractor.py 1200000 6.5 20 4.0 High_Interest_Mortgage
echo ""

echo "=== All scenarios completed! ==="
echo "Check the generated files for results:"
echo "- JSON files: final_mortgage_*_*.json"
echo "- CSV files: final_mortgage_*_table_*.csv"
echo "- Text files: final_mortgage_*_raw_*.txt" 