#!/usr/bin/env python3
"""
Comprehensive Hebrew Mortgage Calculator Extractor
This script handles the complex Vue.js interface and extracts amortization data
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
import json
import re

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

def find_amortization_link_comprehensive(driver):
    """Find the amortization link using multiple strategies"""
    print("Looking for amortization link using comprehensive search...")
    
    # Strategy 1: Look for the exact text in any element
    js_find_exact = """
    var links = [];
    var allElements = document.querySelectorAll('*');
    
    for (var i = 0; i < allElements.length; i++) {
        var elem = allElements[i];
        var text = elem.textContent || elem.innerText || '';
        
        if (text.includes('לוח סילוקין מלא')) {
            links.push({
                element: elem,
                text: text.trim(),
                tagName: elem.tagName,
                className: elem.className,
                id: elem.id,
                href: elem.getAttribute('href'),
                onclick: elem.getAttribute('onclick'),
                style: elem.getAttribute('style')
            });
        }
    }
    
    return links;
    """
    
    try:
        links = driver.execute_script(js_find_exact)
        print(f"Found {len(links)} elements containing 'לוח סילוקין מלא'")
        
        for i, link in enumerate(links[:3]):  # Show first 3
            print(f"Link {i+1}: {link['text'][:100]}... (tag: {link['tagName']}, class: {link['className']})")
        
        # Strategy 2: Look for clickable elements near the text
        if links:
            js_click_nearby = """
            var allElements = document.querySelectorAll('*');
            for (var i = 0; i < allElements.length; i++) {
                var elem = allElements[i];
                var text = elem.textContent || elem.innerText || '';
                
                if (text.includes('לוח סילוקין מלא')) {
                    // Try to find a clickable parent or child
                    var clickable = elem;
                    
                    // Check if this element is clickable
                    if (elem.tagName === 'A' || elem.tagName === 'BUTTON' || 
                        elem.onclick || elem.getAttribute('onclick') || 
                        elem.getAttribute('href') || elem.getAttribute('role') === 'button') {
                        elem.click();
                        return { clicked: true, element: 'direct' };
                    }
                    
                    // Look for clickable parent
                    var parent = elem.parentElement;
                    while (parent && parent !== document.body) {
                        if (parent.tagName === 'A' || parent.tagName === 'BUTTON' || 
                            parent.onclick || parent.getAttribute('onclick') || 
                            parent.getAttribute('href') || parent.getAttribute('role') === 'button') {
                            parent.click();
                            return { clicked: true, element: 'parent' };
                        }
                        parent = parent.parentElement;
                    }
                    
                    // Look for clickable child
                    var children = elem.querySelectorAll('a, button, [onclick], [href], [role="button"]');
                    if (children.length > 0) {
                        children[0].click();
                        return { clicked: true, element: 'child' };
                    }
                }
            }
            return { clicked: false };
            """
            
            click_result = driver.execute_script(js_click_nearby)
            print(f"Click result: {click_result}")
            
            if click_result.get('clicked'):
                time.sleep(3)
                return True
        
        # Strategy 3: Look for elements with specific patterns
        js_pattern_search = """
        var patterns = [
            'a[href*="amortization"]',
            'a[href*="schedule"]',
            'a[href*="table"]',
            'button[onclick*="amortization"]',
            'button[onclick*="schedule"]',
            '[class*="amortization"]',
            '[class*="schedule"]',
            '[class*="table"]',
            '[id*="amortization"]',
            '[id*="schedule"]',
            '[id*="table"]'
        ];
        
        for (var i = 0; i < patterns.length; i++) {
            var elements = document.querySelectorAll(patterns[i]);
            for (var j = 0; j < elements.length; j++) {
                var elem = elements[j];
                var text = elem.textContent || elem.innerText || '';
                if (text.includes('לוח') || text.includes('סילוקין') || text.includes('amortization') || text.includes('schedule')) {
                    elem.click();
                    return { clicked: true, pattern: patterns[i] };
                }
            }
        }
        return { clicked: false };
        """
        
        pattern_result = driver.execute_script(js_pattern_search)
        print(f"Pattern search result: {pattern_result}")
        
        if pattern_result.get('clicked'):
            time.sleep(3)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error in comprehensive search: {e}")
        return False

def extract_amortization_table_data(driver):
    """Extract data from the amortization table"""
    print("Extracting amortization table data...")
    
    # JavaScript to extract table data
    js_extract = """
    var data = {
        tables: [],
        text: document.body.innerText,
        currencyAmounts: [],
        percentages: [],
        summary: {},
        pageTitle: document.title,
        url: window.location.href
    };
    
    // Extract all tables
    var tables = document.querySelectorAll('table');
    for (var i = 0; i < tables.length; i++) {
        var table = tables[i];
        var rows = table.querySelectorAll('tr');
        var tableData = [];
        
        for (var j = 0; j < rows.length; j++) {
            var cells = rows[j].querySelectorAll('td, th');
            var rowData = [];
            for (var k = 0; k < cells.length; k++) {
                rowData.push(cells[k].textContent.trim());
            }
            if (rowData.some(function(cell) { return cell.length > 0; })) {
                tableData.push(rowData);
            }
        }
        
        if (tableData.length > 0) {
            data.tables.push(tableData);
        }
    }
    
    // Extract currency amounts
    var currencyRegex = /₪\\s*[\\d,]+/g;
    var currencyMatches = data.text.match(currencyRegex);
    if (currencyMatches) {
        data.currencyAmounts = currencyMatches;
    }
    
    // Extract percentages
    var percentageRegex = /[\\d.]+%/g;
    var percentageMatches = data.text.match(percentageRegex);
    if (percentageMatches) {
        data.percentages = percentageMatches;
    }
    
    // Look for specific Hebrew terms and their associated values
    var hebrewPatterns = {
        'monthly_payment': /החזר חודשי[:\s]*([₪\d,\s]+)/,
        'total_payment': /סה״כ תשלומים[:\s]*([₪\d,\s]+)/,
        'total_interest': /סה״כ ריבית[:\s]*([₪\d,\s]+)/,
        'loan_amount': /סכום המשכנתא[:\s]*([₪\d,\s]+)/,
        'interest_rate': /ריבית[:\s]*([\d.]+%)/,
        'loan_term': /תקופה[:\s]*([\d\s]+)/
    };
    
    for (var key in hebrewPatterns) {
        var match = data.text.match(hebrewPatterns[key]);
        if (match) {
            data.summary[key] = match[1].trim();
        }
    }
    
    return data;
    """
    
    try:
        data = driver.execute_script(js_extract)
        print(f"Extracted {len(data['tables'])} tables")
        print(f"Found {len(data['currencyAmounts'])} currency amounts")
        print(f"Found {len(data['percentages'])} percentages")
        print(f"Page title: {data['pageTitle']}")
        print(f"URL: {data['url']}")
        
        return data
    except Exception as e:
        print(f"Error extracting data: {e}")
        return {"tables": [], "text": "", "currencyAmounts": [], "percentages": [], "summary": {}, "pageTitle": "", "url": ""}

def extract_mortgage_data(loan_amount="1000000", interest_rate="3.5", loan_term="30", cpi_rate="2.0"):
    """Extract mortgage data using comprehensive approach"""
    driver = setup_driver()
    
    try:
        print("Loading mortgage calculator page...")
        driver.get("https://mashcantaman.co.il/%D7%9E%D7%97%D7%A9%D7%91%D7%95%D7%9F-%D7%9E%D7%A9%D7%9B%D7%A0%D7%AA%D7%90/")
        
        # Wait for the page to load
        wait = WebDriverWait(driver, 15)
        calculator = wait.until(EC.presence_of_element_located((By.ID, "ma_calculator")))
        print("Calculator found!")
        
        # Wait for Vue.js to render
        time.sleep(5)
        
        # Ensure we're on תמהיל 1 tab
        print("Ensuring we're on תמהיל 1 tab...")
        js_click_first_tab = """
        var firstTab = document.querySelector('.switcher-container.first');
        if (firstTab) {
            firstTab.click();
            return true;
        }
        return false;
        """
        driver.execute_script(js_click_first_tab)
        time.sleep(3)
        
        # Inject values via JavaScript
        success = inject_values_via_javascript(driver, loan_amount, interest_rate, loan_term, cpi_rate)
        if not success:
            print("Failed to inject values")
            return {"success": False, "error": "Failed to inject values"}
        
        # Wait for calculations to update
        print("Waiting for calculations to update...")
        time.sleep(5)
        
        # Find and click amortization link using comprehensive search
        if find_amortization_link_comprehensive(driver):
            # Switch to new tab if opened
            if len(driver.window_handles) > 1:
                print("New tab detected, switching to it...")
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(3)
            
            # Extract data
            amortization_data = extract_amortization_table_data(driver)
            
            return {
                "success": True,
                "loan_amount": loan_amount,
                "interest_rate": interest_rate,
                "loan_term": loan_term,
                "cpi_rate": cpi_rate,
                "amortization_data": amortization_data
            }
        else:
            print("Could not click amortization link")
            
            # Extract data from current page
            current_data = extract_amortization_table_data(driver)
            
            return {
                "success": False,
                "loan_amount": loan_amount,
                "interest_rate": interest_rate,
                "loan_term": loan_term,
                "cpi_rate": cpi_rate,
                "current_page_data": current_data,
                "error": "Could not access amortization table"
            }
        
    except Exception as e:
        print(f"Error during extraction: {e}")
        return {"success": False, "error": str(e)}
    
    finally:
        driver.quit()

def save_data_to_files(data, filename_prefix="mortgage_data"):
    """Save extracted data to files"""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    # Save as JSON
    json_filename = f"{filename_prefix}_{timestamp}.json"
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Data saved to {json_filename}")
    
    # Save table data as CSV if available
    if data.get("amortization_data", {}).get("tables"):
        for i, table in enumerate(data["amortization_data"]["tables"]):
            csv_filename = f"{filename_prefix}_table_{i}_{timestamp}.csv"
            df = pd.DataFrame(table)
            df.to_csv(csv_filename, index=False, encoding="utf-8")
            print(f"Table {i} saved to {csv_filename}")
    
    # Save raw text
    if data.get("amortization_data", {}).get("text"):
        txt_filename = f"{filename_prefix}_raw_{timestamp}.txt"
        with open(txt_filename, "w", encoding="utf-8") as f:
            f.write(data["amortization_data"]["text"])
        print(f"Raw text saved to {txt_filename}")

def main():
    """Main function to run mortgage data extraction"""
    print("=== Comprehensive Hebrew Mortgage Calculator Extractor ===\n")
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Basic_Mortgage",
            "loan_amount": "1000000",
            "interest_rate": "3.5",
            "loan_term": "30",
            "cpi_rate": "2.0"
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
        save_data_to_files(result, f"comprehensive_mortgage_{scenario['name']}")
        
        print(f"Test {i+1} completed: {'Success' if result['success'] else 'Failed'}")
    
    # Save all results
    save_data_to_files({"all_results": all_results}, "comprehensive_all_mortgage_results")
    
    print(f"\n=== All Tests Completed ===")
    successful_tests = sum(1 for r in all_results if r['success'])
    print(f"Successful tests: {successful_tests}/{len(test_scenarios)}")

if __name__ == "__main__":
    main() 