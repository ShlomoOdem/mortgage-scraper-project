#!/usr/bin/env python3
"""
Extract CP Programs from Sample Data
Extracts and parses the cp_programs value from the provided sample data
"""

import json
import re
import html
from urllib.parse import unquote

def extract_cp_programs_from_html(html_content):
    """Extract cp_programs value from HTML content"""
    print("Extracting cp_programs from HTML...")
    
    # Look for the cp_programs input field
    pattern = r'name="cp_programs"\s+value="([^"]*)"'
    match = re.search(pattern, html_content)
    
    if match:
        cp_programs_value = match.group(1)
        print(f"Found cp_programs value (length: {len(cp_programs_value)})")
        return cp_programs_value
    else:
        print("cp_programs value not found in HTML")
        return None

def parse_cp_programs_data(cp_programs_value):
    """Parse the cp_programs value into structured data"""
    print("Parsing cp_programs data...")
    
    try:
        # URL decode the value
        decoded_value = unquote(cp_programs_value)
        
        # Convert HTML entities to actual characters
        decoded_value = html.unescape(decoded_value)
        
        # Parse the JSON structure
        data = json.loads(decoded_value)
        
        # Extract the programs array (first element of the outer array)
        if isinstance(data, list) and len(data) > 0:
            programs = data[0]
            
            # Extract input data and monthly payments
            if len(programs) > 0:
                first_program = programs[0]
                
                input_data = first_program.get('input_data', {})
                monthly_payments = programs
                
                return {
                    'input_data': input_data,
                    'monthly_payments': monthly_payments,
                    'total_payments': len(monthly_payments)
                }
        
        return data
        
    except Exception as e:
        print(f"Error parsing cp_programs data: {e}")
        return None

def save_cp_programs_data(cp_programs_value, parsed_data, filename_prefix="cp_programs_sample"):
    """Save the cp_programs data to files"""
    import time
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    # Save raw value
    raw_filename = f"{filename_prefix}_raw_{timestamp}.txt"
    with open(raw_filename, 'w', encoding='utf-8') as f:
        f.write(cp_programs_value)
    print(f"Saved raw cp_programs value to: {raw_filename}")
    
    # Save parsed data as JSON
    if parsed_data:
        json_filename = f"{filename_prefix}_parsed_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=2)
        print(f"Saved parsed cp_programs data to: {json_filename}")
        
        # Save monthly payments as CSV
        csv_filename = f"{filename_prefix}_payments_{timestamp}.csv"
        if 'monthly_payments' in parsed_data:
            import csv
            with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
                if parsed_data['monthly_payments']:
                    fieldnames = parsed_data['monthly_payments'][0].keys()
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    for payment in parsed_data['monthly_payments']:
                        writer.writerow(payment)
            print(f"Saved monthly payments to: {csv_filename}")
    
    # Save summary
    summary_filename = f"{filename_prefix}_summary_{timestamp}.txt"
    with open(summary_filename, 'w', encoding='utf-8') as f:
        f.write(f"CP Programs Data Summary\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Raw value length: {len(cp_programs_value)}\n")
        if parsed_data:
            f.write(f"Input data: {json.dumps(parsed_data.get('input_data', {}), ensure_ascii=False, indent=2)}\n")
            f.write(f"Total monthly payments: {parsed_data.get('total_payments', 0)}\n")
    print(f"Saved summary to: {summary_filename}")
    
    return {
        'raw_file': raw_filename,
        'json_file': json_filename if parsed_data else None,
        'csv_file': csv_filename if parsed_data and 'monthly_payments' in parsed_data else None,
        'summary_file': summary_filename
    }

def main():
    """Main function"""
    print("CP Programs Sample Extractor")
    print("============================")
    
    # Read the sample data
    try:
        with open('sample.txt', 'r', encoding='utf-8') as f:
            html_content = f.read()
        print("Loaded sample.txt")
    except FileNotFoundError:
        print("sample.txt not found. Please make sure the file exists.")
        return
    
    # Extract cp_programs value
    cp_programs_value = extract_cp_programs_from_html(html_content)
    
    if not cp_programs_value:
        print("Failed to extract cp_programs value")
        return
    
    # Parse the data
    parsed_data = parse_cp_programs_data(cp_programs_value)
    
    if not parsed_data:
        print("Failed to parse cp_programs data")
        return
    
    # Save the data
    saved_files = save_cp_programs_data(cp_programs_value, parsed_data)
    
    print("\nExtraction completed successfully!")
    print(f"Files saved:")
    for file_type, filename in saved_files.items():
        if filename:
            print(f"  {file_type}: {filename}")
    
    # Print some key information
    if 'input_data' in parsed_data:
        input_data = parsed_data['input_data']
        print(f"\nKey Information:")
        print(f"  Loan Amount: {input_data.get('amount', 'N/A')}")
        print(f"  Interest Rate: {input_data.get('interest', 'N/A')}")
        print(f"  Duration: {input_data.get('duration', 'N/A')} months")
        print(f"  Channel: {input_data.get('chanel', 'N/A')}")
        print(f"  Amortization: {input_data.get('amortization', 'N/A')}")
        print(f"  Total Payments: {parsed_data.get('total_payments', 'N/A')}")

if __name__ == "__main__":
    main() 