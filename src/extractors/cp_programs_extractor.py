#!/usr/bin/env python3
"""
CP Programs Extractor
Extracts the cp_programs value from the form element when clicked and stores it in a file
"""

import time
import json
import re
import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import unquote

def setup_driver():
    """Set up Chrome driver with appropriate options"""
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Comment out for debugging
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def inject_values_via_javascript(driver, loan_amount, interest_rate, loan_term, cpi_rate):
    """Inject values into the calculator using JavaScript"""
    print("Injecting values via JavaScript...")
    
    # JavaScript to set values directly
    js_script = f"""
    // Find all amount inputs in the first tab
    var amountInputs = document.querySelectorAll('.first-tab .amount-input');
    if (amountInputs.length > 0) {{
        amountInputs[0].value = '{loan_amount}';
        amountInputs[0].dispatchEvent(new Event('input', {{ bubbles: true }}));
        amountInputs[0].dispatchEvent(new Event('change', {{ bubbles: true }}));
        console.log('Set amount to: {loan_amount}');
    }}
    
    // Find all interest inputs in the first tab
    var interestInputs = document.querySelectorAll('.first-tab .interest-input');
    if (interestInputs.length > 0) {{
        interestInputs[0].value = '{interest_rate}';
        interestInputs[0].dispatchEvent(new Event('input', {{ bubbles: true }}));
        interestInputs[0].dispatchEvent(new Event('change', {{ bubbles: true }}));
        console.log('Set interest to: {interest_rate}');
    }}
    
    // Find all duration inputs in the first tab
    var durationInputs = document.querySelectorAll('.first-tab .duration-input');
    if (durationInputs.length > 0) {{
        durationInputs[0].value = '{loan_term}';
        durationInputs[0].dispatchEvent(new Event('input', {{ bubbles: true }}));
        durationInputs[0].dispatchEvent(new Event('change', {{ bubbles: true }}));
        console.log('Set duration to: {loan_term}');
    }}
    
    // Find all CPI inputs in the first tab
    var cpiInputs = document.querySelectorAll('.first-tab .cpi-input');
    if (cpiInputs.length > 0) {{
        cpiInputs[0].value = '{cpi_rate}';
        cpiInputs[0].dispatchEvent(new Event('input', {{ bubbles: true }}));
        cpiInputs[0].dispatchEvent(new Event('change', {{ bubbles: true }}));
        console.log('Set CPI to: {cpi_rate}');
    }}
    
    return {{
        amountInputs: amountInputs.length,
        interestInputs: interestInputs.length,
        durationInputs: durationInputs.length,
        cpiInputs: cpiInputs.length
    }};
    """
    
    try:
        result = driver.execute_script(js_script)
        print(f"JavaScript injection result: {result}")
        return True
    except Exception as e:
        print(f"JavaScript injection error: {e}")
        return False

def extract_cp_programs_value(driver):
    """Extract the cp_programs value from the form element"""
    print("Extracting cp_programs value...")
    
    try:
        # Wait for the form to be present
        wait = WebDriverWait(driver, 10)
        
        # Look for the form with the specific action URL
        form_selector = 'form[action*="לוח-סילוקין-מלא"]'
        form = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, form_selector)))
        
        # Find the cp_programs input field
        cp_programs_input = form.find_element(By.CSS_SELECTOR, 'input[name="cp_programs"]')
        cp_programs_value = cp_programs_input.get_attribute('value')
        
        if cp_programs_value:
            print(f"Found cp_programs value (length: {len(cp_programs_value)})")
            return cp_programs_value
        else:
            print("cp_programs value is empty")
            return None
            
    except Exception as e:
        print(f"Error extracting cp_programs value: {e}")
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

def save_cp_programs_data(cp_programs_value, parsed_data, filename_prefix="cp_programs"):
    """Save the cp_programs data to files"""
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
        'summary_file': summary_filename
    }

def extract_cp_programs(loan_amount="1000000", interest_rate="3.5", loan_term="30", cpi_rate="2.0"):
    """Main function to extract cp_programs data"""
    driver = None
    try:
        print("Starting CP Programs extraction...")
        
        # Setup driver
        driver = setup_driver()
        
        # Navigate to the calculator page
        url = "https://mashcantaman.co.il/מחשבון-משכנתא/"
        print(f"Navigating to: {url}")
        driver.get(url)
        
        # Wait for page to load
        time.sleep(3)
        
        # Inject values
        if not inject_values_via_javascript(driver, loan_amount, interest_rate, loan_term, cpi_rate):
            print("Failed to inject values")
            return None
        
        # Wait for calculations to complete
        time.sleep(2)
        
        # Extract cp_programs value
        cp_programs_value = extract_cp_programs_value(driver)
        
        if not cp_programs_value:
            print("Failed to extract cp_programs value")
            return None
        
        # Parse the data
        parsed_data = parse_cp_programs_data(cp_programs_value)
        
        # Save the data
        saved_files = save_cp_programs_data(cp_programs_value, parsed_data)
        
        print("CP Programs extraction completed successfully!")
        return saved_files
        
    except Exception as e:
        print(f"Error during extraction: {e}")
        return None
        
    finally:
        if driver:
            driver.quit()

def main():
    """Main function"""
    print("CP Programs Extractor")
    print("====================")
    
    # Default values
    loan_amount = "1000000"
    interest_rate = "3.5"
    loan_term = "30"
    cpi_rate = "2.0"
    
    # You can modify these values as needed
    print(f"Using default values:")
    print(f"  Loan Amount: {loan_amount}")
    print(f"  Interest Rate: {interest_rate}%")
    print(f"  Loan Term: {loan_term} years")
    print(f"  CPI Rate: {cpi_rate}%")
    
    # Extract the data
    result = extract_cp_programs(loan_amount, interest_rate, loan_term, cpi_rate)
    
    if result:
        print("\nExtraction successful!")
        print(f"Files saved:")
        for file_type, filename in result.items():
            if filename:
                print(f"  {file_type}: {filename}")
    else:
        print("\nExtraction failed!")

if __name__ == "__main__":
    main() 