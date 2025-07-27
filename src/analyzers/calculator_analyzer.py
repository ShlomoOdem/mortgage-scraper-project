#!/usr/bin/env python3
"""
Hebrew Mortgage Calculator Analyzer
This script analyzes the structure and functionality of the mortgage calculator
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json

def setup_driver():
    """Set up Chrome driver with appropriate options"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def analyze_calculator():
    """Analyze the calculator structure and functionality"""
    driver = setup_driver()
    
    try:
        print("Loading mortgage calculator page...")
        driver.get("https://mashcantaman.co.il/%D7%9E%D7%97%D7%A9%D7%91%D7%95%D7%9F-%D7%9E%D7%A9%D7%9B%D7%A0%D7%AA%D7%90/")
        
        # Wait for the page to load
        wait = WebDriverWait(driver, 10)
        
        # Wait for the calculator to be present
        calculator = wait.until(EC.presence_of_element_located((By.ID, "ma_calculator")))
        print("Calculator found!")
        
        # Wait for Vue.js to render
        time.sleep(5)
        
        print("\n=== Calculator Structure Analysis ===")
        
        # Analyze the calculator HTML structure
        calculator_html = calculator.get_attribute('innerHTML')
        print(f"Calculator HTML length: {len(calculator_html)} characters")
        
        # Look for Vue.js components
        vue_components = driver.find_elements(By.CSS_SELECTOR, "[class*='loan-tab'], [class*='switcher'], [class*='calculator']")
        print(f"\nVue.js components found: {len(vue_components)}")
        
        for i, comp in enumerate(vue_components[:10]):  # Show first 10
            try:
                class_name = comp.get_attribute("class")
                print(f"Component {i+1}: {class_name}")
            except:
                pass
        
        # Analyze input fields by type
        print("\n=== Input Field Analysis ===")
        
        input_types = {
            'amount-input': 'Loan amount inputs',
            'interest-input': 'Interest rate inputs', 
            'duration-input': 'Loan term inputs',
            'cpi-input': 'CPI rate inputs',
            'payoff-amount': 'Payoff amount inputs'
        }
        
        for class_name, description in input_types.items():
            inputs = driver.find_elements(By.CSS_SELECTOR, f".{class_name}")
            visible_inputs = [inp for inp in inputs if inp.is_displayed()]
            print(f"{description}: {len(inputs)} total, {len(visible_inputs)} visible")
        
        # Look for calculation results
        print("\n=== Result Analysis ===")
        
        # Find all elements that might contain results
        result_selectors = [
            "[class*='payment']",
            "[class*='result']", 
            "[class*='calculation']",
            "[class*='total']",
            "[class*='monthly']",
            "[class*='sum']"
        ]
        
        for selector in result_selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                print(f"Elements with '{selector}': {len(elements)}")
                for i, elem in enumerate(elements[:3]):  # Show first 3
                    try:
                        text = elem.text.strip()
                        if text:
                            print(f"  {i+1}. {text[:100]}...")
                    except:
                        pass
        
        # Analyze the page text for Hebrew mortgage terms
        print("\n=== Hebrew Content Analysis ===")
        
        page_text = driver.find_element(By.TAG_NAME, "body").text
        
        hebrew_terms = {
            'משכנתא': 'Mortgage',
            'ריבית': 'Interest rate',
            'תשלום': 'Payment',
            'החזר': 'Repayment',
            'חודשי': 'Monthly',
            'סה״כ': 'Total',
            'סהכ': 'Total (alternative)',
            'שנים': 'Years',
            'חודשים': 'Months'
        }
        
        for hebrew, english in hebrew_terms.items():
            count = page_text.count(hebrew)
            if count > 0:
                print(f"'{hebrew}' ({english}): {count} occurrences")
        
        # Look for currency amounts
        import re
        currency_pattern = r'₪\s*[\d,]+'
        currency_matches = re.findall(currency_pattern, page_text)
        if currency_matches:
            print(f"\nCurrency amounts found: {len(currency_matches)}")
            unique_amounts = list(set(currency_matches))
            for amount in unique_amounts[:10]:  # Show first 10 unique amounts
                print(f"  {amount}")
        
        # Look for percentage values
        percentage_pattern = r'[\d.]+%'
        percentage_matches = re.findall(percentage_pattern, page_text)
        if percentage_matches:
            print(f"\nPercentage values found: {len(percentage_matches)}")
            unique_percentages = list(set(percentage_matches))
            for percentage in unique_percentages[:10]:  # Show first 10 unique percentages
                print(f"  {percentage}")
        
        # Analyze calculator tabs
        print("\n=== Tab Analysis ===")
        
        tabs = driver.find_elements(By.CSS_SELECTOR, "[class*='tab'], [class*='switcher']")
        print(f"Found {len(tabs)} tab/switcher elements")
        
        for i, tab in enumerate(tabs[:5]):  # Show first 5
            try:
                text = tab.text.strip()
                class_name = tab.get_attribute("class")
                if text:
                    print(f"Tab {i+1}: '{text}' (class: {class_name})")
            except:
                pass
        
        # Look for any JavaScript data or configuration
        print("\n=== JavaScript Data Analysis ===")
        
        scripts = driver.find_elements(By.TAG_NAME, "script")
        calculator_scripts = []
        
        for script in scripts:
            try:
                script_content = script.get_attribute("innerHTML")
                if script_content and ("calculator" in script_content.lower() or "mortgage" in script_content.lower()):
                    calculator_scripts.append(script_content[:500])  # First 500 chars
            except:
                pass
        
        print(f"Found {len(calculator_scripts)} scripts with calculator content")
        
        # Look for any forms or submission mechanisms
        print("\n=== Form Analysis ===")
        
        forms = driver.find_elements(By.TAG_NAME, "form")
        print(f"Found {len(forms)} forms on the page")
        
        for i, form in enumerate(forms):
            try:
                action = form.get_attribute("action")
                method = form.get_attribute("method")
                form_id = form.get_attribute("id")
                print(f"Form {i+1}: action='{action}', method='{method}', id='{form_id}'")
            except:
                pass
        
        print("\n=== Analysis Complete ===")
        
        # Save the page source for further analysis
        with open("calculator_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("Page source saved to calculator_page_source.html")
        
        return {
            "calculator_found": True,
            "input_fields": len(driver.find_elements(By.TAG_NAME, "input")),
            "vue_components": len(vue_components),
            "currency_amounts": len(currency_matches),
            "percentage_values": len(percentage_matches)
        }
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        return {"error": str(e)}
    
    finally:
        driver.quit()

def main():
    """Main function"""
    print("=== Hebrew Mortgage Calculator Analyzer ===\n")
    
    results = analyze_calculator()
    
    print(f"\nSummary:")
    for key, value in results.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    main() 