#!/usr/bin/env python3
"""
Combination Loader Utility
Loads mortgage combinations from various file formats
"""

import json
import csv
import yaml
import os
from typing import List, Dict, Any

def load_combinations_from_json(file_path: str) -> List[Dict[str, Any]]:
    """Load combinations from JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle different JSON structures
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and 'combinations' in data:
            return data['combinations']
        else:
            raise ValueError("Invalid JSON structure. Expected list or dict with 'combinations' key")
            
    except Exception as e:
        raise Exception(f"Error loading JSON file {file_path}: {e}")

def load_combinations_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """Load combinations from CSV file"""
    try:
        combinations = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert string values to appropriate types
                combination = {}
                for key, value in row.items():
                    if key.lower() in ['loan_amount', 'interest_rate', 'loan_term_months', 'cpi_rate']:
                        try:
                            combination[key] = str(float(value))
                        except:
                            combination[key] = value
                    else:
                        combination[key] = value
                combinations.append(combination)
        
        return combinations
        
    except Exception as e:
        raise Exception(f"Error loading CSV file {file_path}: {e}")

def load_combinations_from_yaml(file_path: str) -> List[Dict[str, Any]]:
    """Load combinations from YAML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        # Handle different YAML structures
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and 'combinations' in data:
            return data['combinations']
        else:
            raise ValueError("Invalid YAML structure. Expected list or dict with 'combinations' key")
            
    except Exception as e:
        raise Exception(f"Error loading YAML file {file_path}: {e}")

def load_combinations(file_path: str) -> List[Dict[str, Any]]:
    """Load combinations from file based on file extension"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Combination file not found: {file_path}")
    
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.json':
        return load_combinations_from_json(file_path)
    elif file_extension == '.csv':
        return load_combinations_from_csv(file_path)
    elif file_extension in ['.yml', '.yaml']:
        return load_combinations_from_yaml(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}. Supported formats: .json, .csv, .yml, .yaml")

def validate_combination(combination: Dict[str, Any]) -> bool:
    """Validate a single combination"""
    required_fields = ['loan_amount', 'interest_rate', 'loan_term_months', 'cpi_rate', 'channel', 'amortization']
    
    for field in required_fields:
        if field not in combination:
            print(f"Warning: Missing required field '{field}' in combination: {combination}")
            return False
    
    # Validate numeric fields
    try:
        float(combination['loan_amount'])
        float(combination['interest_rate'])
        int(combination['loan_term_months'])
        float(combination['cpi_rate'])
    except (ValueError, TypeError):
        print(f"Warning: Invalid numeric values in combination: {combination}")
        return False
    
    return True

def validate_combinations(combinations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Validate all combinations and return valid ones"""
    valid_combinations = []
    invalid_count = 0
    
    for i, combination in enumerate(combinations):
        if validate_combination(combination):
            valid_combinations.append(combination)
        else:
            invalid_count += 1
            print(f"Invalid combination {i+1}: {combination}")
    
    if invalid_count > 0:
        print(f"Warning: {invalid_count} invalid combinations were skipped")
    
    return valid_combinations

def create_sample_combination_file(file_path: str, format_type: str = 'json'):
    """Create a sample combination file"""
    sample_combinations = [
        {
            'loan_amount': '1000000',
            'interest_rate': '3.5',
            'loan_term_months': '360',
            'cpi_rate': '2.0',
            'channel': 'קבועה צמודה',
            'amortization': 'שפיצר'
        },
        {
            'loan_amount': '1000000',
            'interest_rate': '3.5',
            'loan_term_months': '360',
            'cpi_rate': '2.0',
            'channel': 'קבועה לא צמודה',
            'amortization': 'שפיצר'
        },
        {
            'loan_amount': '1000000',
            'interest_rate': '4.0',
            'loan_term_months': '360',
            'cpi_rate': '2.0',
            'channel': 'פריים',
            'amortization': 'שפיצר'
        }
    ]
    
    if format_type == 'json':
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(sample_combinations, f, ensure_ascii=False, indent=2)
    
    elif format_type == 'csv':
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['loan_amount', 'interest_rate', 'loan_term_months', 'cpi_rate', 'channel', 'amortization']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for combo in sample_combinations:
                writer.writerow(combo)
    
    elif format_type == 'yaml':
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(sample_combinations, f, default_flow_style=False, allow_unicode=True)
    
    print(f"Sample combination file created: {file_path}")

def main():
    """Test the combination loader"""
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        try:
            combinations = load_combinations(file_path)
            valid_combinations = validate_combinations(combinations)
            
            print(f"Loaded {len(combinations)} combinations, {len(valid_combinations)} valid")
            
            for i, combo in enumerate(valid_combinations[:3]):  # Show first 3
                print(f"  {i+1}. {combo['loan_amount']} @ {combo['interest_rate']}% for {combo['loan_term_months']} months")
                print(f"     Channel: {combo['channel']}, Amortization: {combo['amortization']}, CPI: {combo['cpi_rate']}%")
            
            if len(valid_combinations) > 3:
                print(f"  ... and {len(valid_combinations) - 3} more")
                
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Usage: python3 combination_loader.py <file_path>")
        print("Supported formats: .json, .csv, .yml, .yaml")

if __name__ == "__main__":
    main() 