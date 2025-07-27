#!/usr/bin/env python3
"""
Hebrew Mortgage Calculator Interaction Script
This script interacts with the mortgage calculator on mashcantaman.co.il
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

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

def interact_with_calculator():
    """Main function to interact with the mortgage calculator"""
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
        
        # Look for input fields that might be rendered by Vue.js
        print("Looking for calculator input fields...")
        
        # Try to find input fields by common selectors
        input_selectors = [
            "input[type='text']",
            "input[type='number']",
            ".amount-input",
            ".loan-amount",
            ".interest-rate",
            ".loan-term",
            "input[name*='amount']",
            "input[name*='rate']",
            "input[name*='term']",
            "input[name*='years']"
        ]
        
        found_inputs = []
        for selector in input_selectors:
            try:
                inputs = driver.find_elements(By.CSS_SELECTOR, selector)
                if inputs:
                    found_inputs.extend(inputs)
                    print(f"Found {len(inputs)} inputs with selector: {selector}")
            except Exception as e:
                print(f"Error with selector {selector}: {e}")
        
        print(f"Total input fields found: {len(found_inputs)}")
        
        # Look for any visible input fields in the calculator
        calculator_inputs = calculator.find_elements(By.TAG_NAME, "input")
        print(f"Input fields within calculator: {len(calculator_inputs)}")
        
        for i, inp in enumerate(calculator_inputs):
            try:
                input_type = inp.get_attribute("type")
                input_name = inp.get_attribute("name")
                input_id = inp.get_attribute("id")
                input_class = inp.get_attribute("class")
                input_value = inp.get_attribute("value")
                
                print(f"Input {i+1}:")
                print(f"  Type: {input_type}")
                print(f"  Name: {input_name}")
                print(f"  ID: {input_id}")
                print(f"  Class: {input_class}")
                print(f"  Value: {input_value}")
                print(f"  Visible: {inp.is_displayed()}")
                print()
            except Exception as e:
                print(f"Error getting input {i+1} details: {e}")
        
        # Look for select dropdowns
        selects = calculator.find_elements(By.TAG_NAME, "select")
        print(f"Select dropdowns in calculator: {len(selects)}")
        
        # Look for buttons
        buttons = calculator.find_elements(By.TAG_NAME, "button")
        print(f"Buttons in calculator: {len(buttons)}")
        
        # Try to find Vue.js components
        vue_components = driver.find_elements(By.CSS_SELECTOR, "[class*='loan-tab'], [class*='calculator']")
        print(f"Vue.js components found: {len(vue_components)}")
        
        # Get page source to see what's actually rendered
        print("\nGetting page source to analyze rendered content...")
        page_source = driver.page_source
        
        # Look for specific calculator elements in the rendered HTML
        if "amount" in page_source.lower():
            print("Found 'amount' in page source")
        
        if "ריבית" in page_source:  # Hebrew word for interest
            print("Found Hebrew 'interest' in page source")
        
        if "תשלום" in page_source:  # Hebrew word for payment
            print("Found Hebrew 'payment' in page source")
        
        # Try to interact with any visible input field
        visible_inputs = [inp for inp in calculator_inputs if inp.is_displayed()]
        if visible_inputs:
            print(f"\nFound {len(visible_inputs)} visible input fields")
            
            # Try to interact with the first visible input
            first_input = visible_inputs[0]
            try:
                print("Attempting to interact with first visible input...")
                first_input.clear()
                first_input.send_keys("1000000")  # Enter 1 million
                print("Successfully entered value in first input")
                
                # Wait a moment to see if anything updates
                time.sleep(2)
                
                # Check if the value was accepted
                new_value = first_input.get_attribute("value")
                print(f"New value in input: {new_value}")
                
            except Exception as e:
                print(f"Error interacting with input: {e}")
        else:
            print("No visible input fields found")
        
        # Look for any calculation results or output areas
        output_selectors = [
            ".result",
            ".calculation",
            ".payment",
            ".monthly-payment",
            ".total-payment",
            "[class*='result']",
            "[class*='payment']"
        ]
        
        for selector in output_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"Found {len(elements)} elements with selector: {selector}")
                    for elem in elements:
                        print(f"  Text: {elem.text}")
            except Exception as e:
                pass
        
        print("\nCalculator interaction completed!")
        
    except Exception as e:
        print(f"Error during calculator interaction: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    interact_with_calculator() 