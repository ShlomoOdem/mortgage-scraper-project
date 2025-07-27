#!/usr/bin/env python3
"""
Debug CP Programs Data
Examine the raw cp_programs value to understand its structure
"""

import re
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

def debug_cp_programs_value(cp_programs_value):
    """Debug the cp_programs value"""
    print("Debugging cp_programs value...")
    
    # Save raw value for inspection
    with open('debug_raw_cp_programs.txt', 'w', encoding='utf-8') as f:
        f.write(cp_programs_value)
    print("Saved raw value to debug_raw_cp_programs.txt")
    
    # Show first 500 characters
    print(f"\nFirst 500 characters:")
    print(cp_programs_value[:500])
    
    # Show last 500 characters
    print(f"\nLast 500 characters:")
    print(cp_programs_value[-500:])
    
    # Try URL decoding
    try:
        decoded_value = unquote(cp_programs_value)
        print(f"\nURL decoded (first 500 chars):")
        print(decoded_value[:500])
        
        # Save decoded value
        with open('debug_decoded_cp_programs.txt', 'w', encoding='utf-8') as f:
            f.write(decoded_value)
        print("Saved decoded value to debug_decoded_cp_programs.txt")
        
        return decoded_value
    except Exception as e:
        print(f"URL decode error: {e}")
        return cp_programs_value

def main():
    """Main function"""
    print("CP Programs Debug")
    print("================")
    
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
    
    # Debug the value
    decoded_value = debug_cp_programs_value(cp_programs_value)
    
    print("\nDebug completed. Check the debug files for more details.")

if __name__ == "__main__":
    main() 