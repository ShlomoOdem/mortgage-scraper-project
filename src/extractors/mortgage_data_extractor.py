#!/usr/bin/env python3
"""
Hebrew Mortgage Calculator Data Extractor
This script enters values into תמהיל 1 (Mix 1) and extracts data from לוח סילוקין מלא (Full Amortization Table)
"""

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import json
import re

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

def extract_mortgage_data(loan_amount="1000000", interest_rate="3.5", loan_term="30", cpi_rate="2.0"):
    """Extract mortgage data from תמהיל 1 and לוח סילוקין מלא"""
    driver = setup_driver()
    
    try:
        print("Loading mortgage calculator page...")
        driver.get("https://mashcantaman.co.il/%D7%9E%D7%97%D7%A9%D7%91%D7%95%D7%9F-%D7%9E%D7%A9%D7%9B%D7%A0%D7%AA%D7%90/")
        
        # Wait for the page to load
        wait = WebDriverWait(driver, 15)
        
        # Wait for the calculator to be present
        calculator = wait.until(EC.presence_of_element_located((By.ID, "ma_calculator")))
        print("Calculator found!")
        
        # Wait for Vue.js to render
        time.sleep(5)
        
        # Step 1: Ensure we're on תמהיל 1 (Mix 1) tab
        print("Ensuring we're on תמהיל 1 (Mix 1) tab...")
        
        # Look for the first tab (תמהיל 1)
        first_tab = driver.find_element(By.CSS_SELECTOR, ".switcher-container.first")
        if first_tab:
            print("Found תמהיל 1 tab")
            # Click on the first tab to ensure it's active
            first_tab.click()
            time.sleep(2)
        
        # Step 2: Find and fill the visible input fields in תמהיל 1
        print("Looking for input fields in תמהיל 1...")
        
        # Wait for the first tab to be active and inputs to be visible
        time.sleep(3)
        
        # Find visible input fields in the first tab only
        visible_amount_inputs = driver.find_elements(By.CSS_SELECTOR, ".first-tab .amount-input:not([style*='display: none']):not([style*='display:none'])")
        visible_interest_inputs = driver.find_elements(By.CSS_SELECTOR, ".first-tab .interest-input:not([style*='display: none']):not([style*='display:none'])")
        visible_duration_inputs = driver.find_elements(By.CSS_SELECTOR, ".first-tab .duration-input:not([style*='display: none']):not([style*='display:none'])")
        visible_cpi_inputs = driver.find_elements(By.CSS_SELECTOR, ".first-tab .cpi-input:not([style*='display: none']):not([style*='display:none'])")
        
        print(f"Found {len(visible_amount_inputs)} visible amount inputs in תמהיל 1")
        print(f"Found {len(visible_interest_inputs)} visible interest inputs in תמהיל 1")
        print(f"Found {len(visible_duration_inputs)} visible duration inputs in תמהיל 1")
        print(f"Found {len(visible_cpi_inputs)} visible CPI inputs in תמהיל 1")
        
        # Fill in the inputs
        if visible_amount_inputs:
            print(f"Entering loan amount: {loan_amount}")
            amount_input = visible_amount_inputs[0]
            driver.execute_script("arguments[0].scrollIntoView();", amount_input)
            time.sleep(1)
            amount_input.clear()
            amount_input.send_keys(loan_amount)
            time.sleep(1)
        
        if visible_interest_inputs:
            print(f"Entering interest rate: {interest_rate}%")
            interest_input = visible_interest_inputs[0]
            driver.execute_script("arguments[0].scrollIntoView();", interest_input)
            time.sleep(1)
            interest_input.clear()
            interest_input.send_keys(interest_rate)
            time.sleep(1)
        
        if visible_duration_inputs:
            print(f"Entering loan term: {loan_term} years")
            duration_input = visible_duration_inputs[0]
            driver.execute_script("arguments[0].scrollIntoView();", duration_input)
            time.sleep(1)
            duration_input.clear()
            duration_input.send_keys(loan_term)
            time.sleep(1)
        
        if visible_cpi_inputs:
            print(f"Entering CPI rate: {cpi_rate}%")
            cpi_input = visible_cpi_inputs[0]
            driver.execute_script("arguments[0].scrollIntoView();", cpi_input)
            time.sleep(1)
            cpi_input.clear()
            cpi_input.send_keys(cpi_rate)
            time.sleep(1)
        
        # Wait for calculations to update
        print("Waiting for calculations to update...")
        time.sleep(5)
        
        # Step 3: Look for "לוח סילוקין מלא" (Full Amortization Table) link/button
        print("Looking for לוח סילוקין מלא (Full Amortization Table)...")
        
        # Try different selectors to find the amortization table link
        amortization_selectors = [
            "a[href*='amortization']",
            "a[href*='schedule']",
            "a[href*='table']",
            "button[onclick*='amortization']",
            "button[onclick*='schedule']",
            "[class*='amortization']",
            "[class*='schedule']",
            "[class*='table']",
            "a:contains('לוח סילוקין')",
            "button:contains('לוח סילוקין')",
            "[class*='full']",
            "[class*='complete']"
        ]
        
        amortization_link = None
        for selector in amortization_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for elem in elements:
                    text = elem.text.strip()
                    if "לוח סילוקין" in text or "amortization" in text.lower() or "schedule" in text.lower():
                        amortization_link = elem
                        print(f"Found amortization link with text: {text}")
                        break
                if amortization_link:
                    break
            except:
                continue
        
        # If not found by selectors, search by text content
        if not amortization_link:
            print("Searching for amortization link by text content...")
            all_links = driver.find_elements(By.TAG_NAME, "a")
            all_buttons = driver.find_elements(By.TAG_NAME, "button")
            all_elements = all_links + all_buttons
            
            for elem in all_elements:
                try:
                    text = elem.text.strip()
                    if "לוח סילוקין" in text:
                        amortization_link = elem
                        print(f"Found amortization link: {text}")
                        break
                except:
                    continue
        
        if amortization_link:
            print("Clicking on לוח סילוקין מלא...")
            driver.execute_script("arguments[0].scrollIntoView();", amortization_link)
            time.sleep(1)
            amortization_link.click()
            time.sleep(3)
            
            # Step 4: Extract data from the new tab/window
            print("Extracting data from amortization table...")
            
            # Check if a new tab/window opened
            if len(driver.window_handles) > 1:
                print("New tab detected, switching to it...")
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(3)
            
            # Extract the amortization table data
            table_data = extract_amortization_table_data(driver)
            
            return {
                "success": True,
                "loan_amount": loan_amount,
                "interest_rate": interest_rate,
                "loan_term": loan_term,
                "cpi_rate": cpi_rate,
                "amortization_data": table_data
            }
        else:
            print("Could not find לוח סילוקין מלא link")
            
            # Try to extract data from the current page
            print("Extracting data from current page...")
            current_page_data = extract_current_page_data(driver)
            
            return {
                "success": False,
                "loan_amount": loan_amount,
                "interest_rate": interest_rate,
                "loan_term": loan_term,
                "cpi_rate": cpi_rate,
                "current_page_data": current_page_data,
                "error": "Amortization table link not found"
            }
        
    except Exception as e:
        print(f"Error during data extraction: {e}")
        return {"success": False, "error": str(e)}
    
    finally:
        driver.quit()

def extract_amortization_table_data(driver):
    """Extract data from the amortization table"""
    print("Extracting amortization table data...")
    
    data = {
        "table_found": False,
        "rows": [],
        "summary": {},
        "raw_text": ""
    }
    
    try:
        # Get the page source to see what we're working with
        page_source = driver.page_source
        data["raw_text"] = driver.find_element(By.TAG_NAME, "body").text
        
        # Look for table elements
        tables = driver.find_elements(By.TAG_NAME, "table")
        print(f"Found {len(tables)} tables on the page")
        
        for i, table in enumerate(tables):
            try:
                rows = table.find_elements(By.TAG_NAME, "tr")
                print(f"Table {i+1}: {len(rows)} rows")
                
                table_data = []
                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, "td") + row.find_elements(By.TAG_NAME, "th")
                    row_data = [cell.text.strip() for cell in cells]
                    if any(row_data):  # Only add non-empty rows
                        table_data.append(row_data)
                
                if table_data:
                    data["rows"].extend(table_data)
                    data["table_found"] = True
                    
            except Exception as e:
                print(f"Error processing table {i+1}: {e}")
        
        # Look for specific data patterns in the text
        text = data["raw_text"]
        
        # Extract currency amounts
        currency_pattern = r'₪\s*[\d,]+'
        currency_matches = re.findall(currency_pattern, text)
        data["currency_amounts"] = currency_matches
        
        # Extract percentages
        percentage_pattern = r'[\d.]+%'
        percentage_matches = re.findall(percentage_pattern, text)
        data["percentages"] = percentage_matches
        
        # Look for specific Hebrew terms and their associated values
        hebrew_patterns = {
            'monthly_payment': r'החזר חודשי[:\s]*([₪\d,\s]+)',
            'total_payment': r'סה״כ תשלומים[:\s]*([₪\d,\s]+)',
            'total_interest': r'סה״כ ריבית[:\s]*([₪\d,\s]+)',
            'loan_amount': r'סכום המשכנתא[:\s]*([₪\d,\s]+)',
            'interest_rate': r'ריבית[:\s]*([\d.]+%)',
            'loan_term': r'תקופה[:\s]*([\d\s]+)'
        }
        
        for key, pattern in hebrew_patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                data["summary"][key] = matches[0].strip()
        
        print(f"Extracted {len(data['rows'])} table rows")
        print(f"Found {len(data['currency_amounts'])} currency amounts")
        print(f"Found {len(data['percentages'])} percentages")
        
        return data
        
    except Exception as e:
        print(f"Error extracting table data: {e}")
        return data

def extract_current_page_data(driver):
    """Extract data from the current calculator page"""
    print("Extracting data from current calculator page...")
    
    data = {
        "payment_results": [],
        "currency_amounts": [],
        "percentages": [],
        "summary": {}
    }
    
    try:
        # Get page text
        page_text = driver.find_element(By.TAG_NAME, "body").text
        
        # Look for payment results
        payment_elements = driver.find_elements(By.CSS_SELECTOR, "[class*='payment']")
        for elem in payment_elements:
            try:
                text = elem.text.strip()
                if text and text != "0":
                    data["payment_results"].append(text)
            except:
                pass
        
        # Extract currency amounts
        currency_pattern = r'₪\s*[\d,]+'
        currency_matches = re.findall(currency_pattern, page_text)
        data["currency_amounts"] = currency_matches
        
        # Extract percentages
        percentage_pattern = r'[\d.]+%'
        percentage_matches = re.findall(percentage_pattern, page_text)
        data["percentages"] = percentage_matches
        
        return data
        
    except Exception as e:
        print(f"Error extracting current page data: {e}")
        return data

def save_data_to_files(data, filename_prefix="mortgage_data"):
    """Save extracted data to files"""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    # Save as JSON
    json_filename = f"{filename_prefix}_{timestamp}.json"
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Data saved to {json_filename}")
    
    # Save table data as CSV if available
    if data.get("amortization_data", {}).get("rows"):
        csv_filename = f"{filename_prefix}_table_{timestamp}.csv"
        df = pd.DataFrame(data["amortization_data"]["rows"])
        df.to_csv(csv_filename, index=False, encoding="utf-8")
        print(f"Table data saved to {csv_filename}")
    
    # Save raw text
    if data.get("amortization_data", {}).get("raw_text"):
        txt_filename = f"{filename_prefix}_raw_{timestamp}.txt"
        with open(txt_filename, "w", encoding="utf-8") as f:
            f.write(data["amortization_data"]["raw_text"])
        print(f"Raw text saved to {txt_filename}")

def main():
    """Main function to run multiple mortgage calculations"""
    print("=== Hebrew Mortgage Calculator Data Extractor ===\n")
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Basic Mortgage",
            "loan_amount": "1000000",
            "interest_rate": "3.5",
            "loan_term": "30",
            "cpi_rate": "2.0"
        },
        {
            "name": "High Amount Mortgage",
            "loan_amount": "2000000",
            "interest_rate": "4.0",
            "loan_term": "25",
            "cpi_rate": "1.5"
        },
        {
            "name": "Short Term Mortgage",
            "loan_amount": "500000",
            "interest_rate": "5.0",
            "loan_term": "15",
            "cpi_rate": "3.0"
        }
    ]
    
    all_results = []
    
    for i, scenario in enumerate(test_scenarios):
        print(f"\n{'='*60}")
        print(f"Test {i+1}: {scenario['name']}")
        print(f"Loan Amount: ₪{scenario['loan_amount']}")
        print(f"Interest Rate: {scenario['interest_rate']}%")
        print(f"Loan Term: {scenario['loan_term']} years")
        print(f"CPI Rate: {scenario['cpi_rate']}%")
        print(f"{'='*60}")
        
        result = extract_mortgage_data(
            scenario["loan_amount"],
            scenario["interest_rate"],
            scenario["loan_term"],
            scenario["cpi_rate"]
        )
        
        result["scenario"] = scenario["name"]
        all_results.append(result)
        
        # Save individual result
        save_data_to_files(result, f"mortgage_{scenario['name'].replace(' ', '_')}")
        
        print(f"Test {i+1} completed: {'Success' if result['success'] else 'Failed'}")
        
        # Wait between tests
        if i < len(test_scenarios) - 1:
            print("Waiting 5 seconds before next test...")
            time.sleep(5)
    
    # Save all results
    save_data_to_files({"all_results": all_results}, "all_mortgage_results")
    
    print(f"\n=== All Tests Completed ===")
    successful_tests = sum(1 for r in all_results if r['success'])
    print(f"Successful tests: {successful_tests}/{len(test_scenarios)}")

if __name__ == "__main__":
    main() 