#!/usr/bin/env python3
"""
Enhanced Hebrew Mortgage Calculator Interaction Script
This script performs complete mortgage calculations on mashcantaman.co.il
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

def setup_driver():
    """Set up Chrome driver with appropriate options"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def perform_mortgage_calculation(loan_amount="1000000", interest_rate="3.5", loan_term="30", cpi_rate="2.0"):
    """Perform a complete mortgage calculation"""
    driver = setup_driver()
    
    try:
        print("Loading mortgage calculator page...")
        driver.get("https://mashcantaman.co.il/%D7%9E%D7%97%D7%A9%D7%91%D7%95%D7%9F-%D7%9E%D7%A9%D7%9B%D7%A0%D7%AA%D7%90/")
        
        # Wait for the page to load
        wait = WebDriverWait(driver, 10)
        
        # Wait for the calculator to be present
        calculator = wait.until(EC.presence_of_element_located((By.ID, "ma_calculator")))
        print("Calculator found!")
        
        # Wait a bit more for Vue.js to render
        time.sleep(3)
        
        # Find visible input fields in the first tab
        visible_amount_inputs = driver.find_elements(By.CSS_SELECTOR, ".amount-input:not([style*='display: none']):not([style*='display:none'])")
        visible_interest_inputs = driver.find_elements(By.CSS_SELECTOR, ".interest-input:not([style*='display: none']):not([style*='display:none'])")
        visible_duration_inputs = driver.find_elements(By.CSS_SELECTOR, ".duration-input:not([style*='display: none']):not([style*='display:none'])")
        visible_cpi_inputs = driver.find_elements(By.CSS_SELECTOR, ".cpi-input:not([style*='display: none']):not([style*='display:none'])")
        
        print(f"Found {len(visible_amount_inputs)} visible amount inputs")
        print(f"Found {len(visible_interest_inputs)} visible interest inputs")
        print(f"Found {len(visible_duration_inputs)} visible duration inputs")
        print(f"Found {len(visible_cpi_inputs)} visible CPI inputs")
        
        # Fill in the first set of visible inputs
        if visible_amount_inputs:
            print(f"Entering loan amount: {loan_amount}")
            amount_input = visible_amount_inputs[0]
            amount_input.clear()
            amount_input.send_keys(loan_amount)
            time.sleep(1)
        
        if visible_interest_inputs:
            print(f"Entering interest rate: {interest_rate}%")
            interest_input = visible_interest_inputs[0]
            interest_input.clear()
            interest_input.send_keys(interest_rate)
            time.sleep(1)
        
        if visible_duration_inputs:
            print(f"Entering loan term: {loan_term} years")
            duration_input = visible_duration_inputs[0]
            duration_input.clear()
            duration_input.send_keys(loan_term)
            time.sleep(1)
        
        if visible_cpi_inputs:
            print(f"Entering CPI rate: {cpi_rate}%")
            cpi_input = visible_cpi_inputs[0]
            cpi_input.clear()
            cpi_input.send_keys(cpi_rate)
            time.sleep(1)
        
        # Wait for calculations to update
        print("Waiting for calculations to update...")
        time.sleep(3)
        
        # Look for calculation results
        print("Looking for calculation results...")
        
        # Find payment results
        payment_elements = driver.find_elements(By.CSS_SELECTOR, "[class*='payment']")
        print(f"Found {len(payment_elements)} payment-related elements")
        
        results = {}
        
        for i, elem in enumerate(payment_elements):
            try:
                text = elem.text.strip()
                if text and text != "0" and "החזר" in text:  # Hebrew word for payment
                    print(f"Payment result {i+1}: {text}")
                    results[f"payment_{i+1}"] = text
            except Exception as e:
                pass
        
        # Look for total payment amounts
        total_elements = driver.find_elements(By.CSS_SELECTOR, "[class*='total'], [class*='sum'], [class*='amount']")
        print(f"Found {len(total_elements)} total/sum elements")
        
        for i, elem in enumerate(total_elements):
            try:
                text = elem.text.strip()
                if text and text != "0" and any(word in text for word in ["סה״כ", "סהכ", "total", "sum"]):
                    print(f"Total result {i+1}: {text}")
                    results[f"total_{i+1}"] = text
            except Exception as e:
                pass
        
        # Look for monthly payment amounts
        monthly_elements = driver.find_elements(By.CSS_SELECTOR, "[class*='monthly'], [class*='חודשי']")
        print(f"Found {len(monthly_elements)} monthly payment elements")
        
        for i, elem in enumerate(monthly_elements):
            try:
                text = elem.text.strip()
                if text and text != "0":
                    print(f"Monthly payment {i+1}: {text}")
                    results[f"monthly_{i+1}"] = text
            except Exception as e:
                pass
        
        # Get all text content to search for numbers that might be results
        page_text = driver.find_element(By.TAG_NAME, "body").text
        print("\nSearching for calculation results in page text...")
        
        # Look for Hebrew currency patterns (₪ followed by numbers)
        import re
        currency_pattern = r'₪\s*[\d,]+'
        currency_matches = re.findall(currency_pattern, page_text)
        if currency_matches:
            print("Found currency amounts:")
            for match in currency_matches[:10]:  # Show first 10
                print(f"  {match}")
            results["currency_amounts"] = currency_matches[:10]
        
        # Look for percentage patterns
        percentage_pattern = r'[\d.]+%'
        percentage_matches = re.findall(percentage_pattern, page_text)
        if percentage_matches:
            print("Found percentages:")
            for match in percentage_matches[:10]:  # Show first 10
                print(f"  {match}")
            results["percentages"] = percentage_matches[:10]
        
        # Try to find specific calculation result areas
        result_areas = driver.find_elements(By.CSS_SELECTOR, ".result, .calculation, .summary, [class*='result'], [class*='calculation']")
        print(f"Found {len(result_areas)} result/calculation areas")
        
        for i, area in enumerate(result_areas):
            try:
                text = area.text.strip()
                if text and len(text) > 10:  # Only show substantial text
                    print(f"Result area {i+1}: {text[:200]}...")
                    results[f"result_area_{i+1}"] = text[:200]
            except Exception as e:
                pass
        
        print("\nCalculation completed!")
        return results
        
    except Exception as e:
        print(f"Error during calculation: {e}")
        return {}
    
    finally:
        driver.quit()

def main():
    """Main function to run different calculation scenarios"""
    print("=== Hebrew Mortgage Calculator Interaction ===\n")
    
    # Test case 1: Basic calculation
    print("Test Case 1: Basic mortgage calculation")
    print("Loan Amount: ₪1,000,000")
    print("Interest Rate: 3.5%")
    print("Loan Term: 30 years")
    print("CPI Rate: 2.0%")
    print("-" * 50)
    
    results1 = perform_mortgage_calculation("1000000", "3.5", "30", "2.0")
    
    print("\n" + "="*60 + "\n")
    
    # Test case 2: Different loan amount
    print("Test Case 2: Higher loan amount")
    print("Loan Amount: ₪2,000,000")
    print("Interest Rate: 4.0%")
    print("Loan Term: 25 years")
    print("CPI Rate: 1.5%")
    print("-" * 50)
    
    results2 = perform_mortgage_calculation("2000000", "4.0", "25", "1.5")
    
    print("\n" + "="*60 + "\n")
    
    # Test case 3: Short term loan
    print("Test Case 3: Short term loan")
    print("Loan Amount: ₪500,000")
    print("Interest Rate: 5.0%")
    print("Loan Term: 15 years")
    print("CPI Rate: 3.0%")
    print("-" * 50)
    
    results3 = perform_mortgage_calculation("500000", "5.0", "15", "3.0")
    
    print("\n=== All Calculations Completed ===")
    print(f"Test 1 results: {len(results1)} items found")
    print(f"Test 2 results: {len(results2)} items found")
    print(f"Test 3 results: {len(results3)} items found")

if __name__ == "__main__":
    main() 