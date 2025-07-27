#!/usr/bin/env python3
"""
Final Hebrew Mortgage Calculator Extractor
This script can be run multiple times quickly to extract mortgage data from תמהיל 1 and לוח סילוקין מלא
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
import sys

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

def find_and_click_amortization_link(driver):
    """Find and click the amortization link with multiple strategies"""
    print("Looking for amortization link...")
    
    # Store the current window handle
    original_window = driver.current_window_handle
    
    # Strategy 1: Look for the form and submit it
    js_find_and_submit_form = """
    var forms = document.querySelectorAll('form');
    for (var i = 0; i < forms.length; i++) {
        var form = forms[i];
        var action = form.getAttribute('action') || '';
        var target = form.getAttribute('target') || '';
        
        // Check if this form is for the amortization table
        if (action.includes('לוח') && action.includes('סילוקין') && target === '_blank') {
            console.log('Found amortization form:', action);
            
            // Check if form is disabled
            if (form.classList.contains('disabled')) {
                console.log('Form is disabled, trying to enable it...');
                form.classList.remove('disabled');
            }
            
            // Submit the form
            form.submit();
            return { submitted: true, method: 'form_submit', action: action };
        }
    }
    
    // Strategy 2: Look for the exact text and try to click
    var allElements = document.querySelectorAll('*');
    for (var i = 0; i < allElements.length; i++) {
        var elem = allElements[i];
        var text = elem.textContent || elem.innerText || '';
        
        if (text.includes('לוח סילוקין מלא')) {
            // Try to click this element directly
            if (elem.tagName === 'A' || elem.tagName === 'BUTTON' || 
                elem.onclick || elem.getAttribute('onclick') || 
                elem.getAttribute('href') || elem.getAttribute('role') === 'button') {
                elem.click();
                return { clicked: true, method: 'direct', element: elem.tagName };
            }
            
            // Look for clickable parent
            var parent = elem.parentElement;
            while (parent && parent !== document.body) {
                if (parent.tagName === 'A' || parent.tagName === 'BUTTON' || 
                    parent.onclick || parent.getAttribute('onclick') || 
                    parent.getAttribute('href') || parent.getAttribute('role') === 'button') {
                    parent.click();
                    return { clicked: true, method: 'parent', element: parent.tagName };
                }
                parent = parent.parentElement;
            }
            
            // Look for clickable child
            var children = elem.querySelectorAll('a, button, [onclick], [href], [role="button"]');
            if (children.length > 0) {
                children[0].click();
                return { clicked: true, method: 'child', element: children[0].tagName };
            }
        }
    }
    return { clicked: false, submitted: false };
    """
    
    try:
        result = driver.execute_script(js_find_and_submit_form)
        print(f"Form submission result: {result}")
        
        if result.get('submitted'):
            print(f"Form submitted using method: {result.get('method')}")
            time.sleep(3)
            
            # Check if a new tab/window opened
            new_window_handles = [handle for handle in driver.window_handles if handle != original_window]
            if new_window_handles:
                print(f"New tab detected! Switching to new tab...")
                driver.switch_to.window(new_window_handles[0])
                time.sleep(5)  # Wait for the new page to load
                return True
            else:
                print("No new tab opened after form submission")
                return False
        
        elif result.get('clicked'):
            print(f"Clicked element using method: {result.get('method')}")
            time.sleep(3)
            
            # Check if a new tab/window opened
            new_window_handles = [handle for handle in driver.window_handles if handle != original_window]
            if new_window_handles:
                print(f"New tab detected! Switching to new tab...")
                driver.switch_to.window(new_window_handles[0])
                time.sleep(5)  # Wait for the new page to load
                return True
            else:
                print("No new tab opened, staying on current page")
                return True
        
        return False
        
    except Exception as e:
        print(f"Error clicking amortization link: {e}")
        return False

def prepare_amortization_form_data(driver, loan_amount, interest_rate, loan_term, cpi_rate):
    """Prepare the amortization form with the mortgage data"""
    print("Preparing amortization form data...")
    
    js_prepare_form = f"""
    // Get the current mortgage data from the calculator
    var mortgageData = {{
        active_tab: 1,
        programs: [],
        loan_details: {{}}
    }};
    
    // Try to extract current program data
    var programInputs = document.querySelectorAll('.program-input');
    var programs = [];
    
    for (var i = 0; i < programInputs.length; i++) {{
        var input = programInputs[i];
        var value = input.value;
        if (value && value !== '0' && value !== '') {{
            programs.push({{
                amount: value,
                interest: '{interest_rate}',
                duration: '{loan_term}',
                cpi: '{cpi_rate}'
            }});
        }}
    }}
    
    // If no programs found, create a default one
    if (programs.length === 0) {{
        programs.push({{
            amount: '{loan_amount}',
            interest: '{interest_rate}',
            duration: '{loan_term}',
            cpi: '{cpi_rate}'
        }});
    }}
    
    mortgageData.programs = programs;
    
    // Update form fields
    var forms = document.querySelectorAll('form');
    for (var i = 0; i < forms.length; i++) {{
        var form = forms[i];
        var action = form.getAttribute('action') || '';
        
        if (action.includes('לוח') && action.includes('סילוקין')) {{
            // Update hidden fields
            var activeTabInput = form.querySelector('input[name="cp_active_tab"]');
            if (activeTabInput) {{
                activeTabInput.value = mortgageData.active_tab;
            }}
            
            var programsInput = form.querySelector('input[name="cp_programs"]');
            if (programsInput) {{
                programsInput.value = JSON.stringify(mortgageData.programs);
            }}
            
            var loanDetailsInput = form.querySelector('input[name="cp_loan_details"]');
            if (loanDetailsInput) {{
                loanDetailsInput.value = JSON.stringify(mortgageData.loan_details);
            }}
            
            // Remove disabled class if present
            if (form.classList.contains('disabled')) {{
                form.classList.remove('disabled');
            }}
            
            console.log('Form prepared with data:', mortgageData);
            return {{ prepared: true, data: mortgageData }};
        }}
    }}
    
    return {{ prepared: false, error: 'Form not found' }};
    """
    
    try:
        result = driver.execute_script(js_prepare_form)
        print(f"Form preparation result: {result}")
        return result.get('prepared', False)
    except Exception as e:
        print(f"Error preparing form data: {e}")
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
        url: window.location.href,
        html: document.documentElement.outerHTML,
        structuredData: {
            monthlyPayments: [],
            principalPayments: [],
            interestPayments: [],
            remainingBalance: [],
            paymentDates: [],
            totalPayments: 0,
            totalInterest: 0,
            totalPrincipal: 0
        }
    };
    
    // Extract all tables with better structure detection
    var tables = document.querySelectorAll('table');
    for (var i = 0; i < tables.length; i++) {
        var table = tables[i];
        var rows = table.querySelectorAll('tr');
        var tableData = [];
        var tableHeaders = [];
        
        // Extract headers from first row
        if (rows.length > 0) {
            var headerCells = rows[0].querySelectorAll('th, td');
            for (var h = 0; h < headerCells.length; h++) {
                tableHeaders.push(headerCells[h].textContent.trim());
            }
        }
        
        // Extract all rows
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
            data.tables.push({
                index: i,
                headers: tableHeaders,
                data: tableData,
                rowCount: tableData.length,
                columnCount: tableHeaders.length > 0 ? tableHeaders.length : (tableData[0] ? tableData[0].length : 0)
            });
        }
    }
    
    // Extract currency amounts with better regex
    var currencyRegex = /₪\\s*[\\d,]+(?:\\.[\\d]{2})?/g;
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
    
    // Look for specific Hebrew terms and their associated values with improved patterns
    var hebrewPatterns = {
        'monthly_payment': /החזר חודשי[:\s]*([₪\d,\s]+)/,
        'total_payment': /סה״כ תשלומים[:\s]*([₪\d,\s]+)/,
        'total_interest': /סה״כ ריבית[:\s]*([₪\d,\s]+)/,
        'loan_amount': /סכום המשכנתא[:\s]*([₪\d,\s]+)/,
        'interest_rate': /ריבית[:\s]*([\d.]+%)/,
        'loan_term': /תקופה[:\s]*([\d\s]+)/,
        'monthly_principal': /קרן חודשית[:\s]*([₪\d,\s]+)/,
        'monthly_interest': /ריבית חודשית[:\s]*([₪\d,\s]+)/,
        'remaining_balance': /יתרה[:\s]*([₪\d,\s]+)/
    };
    
    for (var key in hebrewPatterns) {
        var match = data.text.match(hebrewPatterns[key]);
        if (match) {
            data.summary[key] = match[1].trim();
        }
    }
    
    // Try to extract structured payment data from tables
    for (var t = 0; t < data.tables.length; t++) {
        var table = data.tables[t];
        var headers = table.headers;
        
        // Look for payment schedule table
        if (headers.some(function(h) { return h.includes('תשלום') || h.includes('Payment'); })) {
            console.log('Found payment schedule table');
            
            for (var r = 1; r < table.data.length; r++) { // Skip header row
                var row = table.data[r];
                var paymentData = {};
                
                for (var c = 0; c < Math.min(headers.length, row.length); c++) {
                    var header = headers[c];
                    var value = row[c];
                    
                    if (header.includes('תשלום') || header.includes('Payment')) {
                        paymentData.payment = value;
                    } else if (header.includes('קרן') || header.includes('Principal')) {
                        paymentData.principal = value;
                    } else if (header.includes('ריבית') || header.includes('Interest')) {
                        paymentData.interest = value;
                    } else if (header.includes('יתרה') || header.includes('Balance')) {
                        paymentData.balance = value;
                    } else if (header.includes('תאריך') || header.includes('Date')) {
                        paymentData.date = value;
                    }
                }
                
                if (Object.keys(paymentData).length > 0) {
                    data.structuredData.monthlyPayments.push(paymentData);
                }
            }
        }
    }
    
    // Calculate totals from structured data
    if (data.structuredData.monthlyPayments.length > 0) {
        data.structuredData.totalPayments = data.structuredData.monthlyPayments.length;
        
        // Sum up totals (assuming currency format like "₪ 1,234.56")
        var totalInterest = 0;
        var totalPrincipal = 0;
        
        for (var p = 0; p < data.structuredData.monthlyPayments.length; p++) {
            var payment = data.structuredData.monthlyPayments[p];
            
            if (payment.interest) {
                var interestValue = payment.interest.replace(/[₪,\s]/g, '');
                if (!isNaN(parseFloat(interestValue))) {
                    totalInterest += parseFloat(interestValue);
                }
            }
            
            if (payment.principal) {
                var principalValue = payment.principal.replace(/[₪,\s]/g, '');
                if (!isNaN(parseFloat(principalValue))) {
                    totalPrincipal += parseFloat(principalValue);
                }
            }
        }
        
        data.structuredData.totalInterest = totalInterest;
        data.structuredData.totalPrincipal = totalPrincipal;
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
        print(f"Structured payment data: {data['structuredData']['totalPayments']} payments")
        
        return data
    except Exception as e:
        print(f"Error extracting data: {e}")
        return {"tables": [], "text": "", "currencyAmounts": [], "percentages": [], "summary": {}, "pageTitle": "", "url": "", "structuredData": {"monthlyPayments": [], "totalPayments": 0, "totalInterest": 0, "totalPrincipal": 0}}

def extract_mortgage_data(loan_amount="1000000", interest_rate="3.5", loan_term="30", cpi_rate="2.0"):
    """Extract mortgage data from תמהיל 1 and לוח סילוקין מלא"""
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
        
        # Store original window handle
        original_window = driver.current_window_handle
        print(f"Original window handle: {original_window}")
        
        # Find and click amortization link
        if find_and_click_amortization_link(driver):
            print("Successfully clicked amortization link")
            
            # Check if we're now on a new tab
            current_window = driver.current_window_handle
            print(f"Current window handle: {current_window}")
            
            if current_window != original_window:
                print("Successfully switched to new tab!")
                print(f"New tab URL: {driver.current_url}")
                print(f"New tab title: {driver.title}")
                
                # Wait for the new page to fully load
                time.sleep(5)
                
                # Extract data from the new tab
                amortization_data = extract_amortization_table_data(driver)
                
                return {
                    "success": True,
                    "loan_amount": loan_amount,
                    "interest_rate": interest_rate,
                    "loan_term": loan_term,
                    "cpi_rate": cpi_rate,
                    "amortization_data": amortization_data,
                    "data_source": "new_tab",
                    "new_tab_url": driver.current_url,
                    "new_tab_title": driver.title
                }
            else:
                print("No new tab opened, extracting from current page")
                
                # Extract data from current page
                current_data = extract_amortization_table_data(driver)
                
                return {
                    "success": True,
                    "loan_amount": loan_amount,
                    "interest_rate": interest_rate,
                    "loan_term": loan_term,
                    "cpi_rate": cpi_rate,
                    "amortization_data": current_data,
                    "data_source": "current_page"
                }
        else:
            print("Could not click amortization link, trying form preparation...")
            
            # Try to prepare and submit the form
            if prepare_amortization_form_data(driver, loan_amount, interest_rate, loan_term, cpi_rate):
                print("Form prepared, trying to submit again...")
                time.sleep(2)
                
                if find_and_click_amortization_link(driver):
                    print("Successfully submitted form after preparation")
                    
                    # Check if we're now on a new tab
                    current_window = driver.current_window_handle
                    if current_window != original_window:
                        print("Successfully switched to new tab after form preparation!")
                        print(f"New tab URL: {driver.current_url}")
                        print(f"New tab title: {driver.title}")
                        
                        # Wait for the new page to fully load
                        time.sleep(5)
                        
                        # Extract data from the new tab
                        amortization_data = extract_amortization_table_data(driver)
                        
                        return {
                            "success": True,
                            "loan_amount": loan_amount,
                            "interest_rate": interest_rate,
                            "loan_term": loan_term,
                            "cpi_rate": cpi_rate,
                            "amortization_data": amortization_data,
                            "data_source": "new_tab_after_preparation",
                            "new_tab_url": driver.current_url,
                            "new_tab_title": driver.title
                        }
            
            # Extract data from current page as fallback
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
    
    # Save structured payment data as CSV if available
    if data.get("amortization_data", {}).get("structuredData", {}).get("monthlyPayments"):
        payments = data["amortization_data"]["structuredData"]["monthlyPayments"]
        if payments:
            # Create a DataFrame from the payment data
            payment_rows = []
            for i, payment in enumerate(payments):
                row = {
                    "Payment_Number": i + 1,
                    "Payment_Amount": payment.get("payment", ""),
                    "Principal": payment.get("principal", ""),
                    "Interest": payment.get("interest", ""),
                    "Remaining_Balance": payment.get("balance", ""),
                    "Payment_Date": payment.get("date", "")
                }
                payment_rows.append(row)
            
            df_payments = pd.DataFrame(payment_rows)
            payments_csv_filename = f"{filename_prefix}_payments_{timestamp}.csv"
            df_payments.to_csv(payments_csv_filename, index=False, encoding="utf-8")
            print(f"Payment schedule saved to {payments_csv_filename}")
    
    # Save table data as CSV if available
    if data.get("amortization_data", {}).get("tables"):
        for i, table in enumerate(data["amortization_data"]["tables"]):
            if isinstance(table, dict) and "data" in table:
                # New structured table format
                table_data = table["data"]
                headers = table.get("headers", [])
                
                if headers:
                    df = pd.DataFrame(table_data[1:], columns=headers)  # Skip header row
                else:
                    df = pd.DataFrame(table_data)
                
                csv_filename = f"{filename_prefix}_table_{i}_{timestamp}.csv"
                df.to_csv(csv_filename, index=False, encoding="utf-8")
                print(f"Table {i} saved to {csv_filename}")
            else:
                # Old format
                df = pd.DataFrame(table)
                csv_filename = f"{filename_prefix}_table_{i}_{timestamp}.csv"
                df.to_csv(csv_filename, index=False, encoding="utf-8")
                print(f"Table {i} saved to {csv_filename}")
    
    # Save raw text
    if data.get("amortization_data", {}).get("text"):
        txt_filename = f"{filename_prefix}_raw_{timestamp}.txt"
        with open(txt_filename, "w", encoding="utf-8") as f:
            f.write(data["amortization_data"]["text"])
        print(f"Raw text saved to {txt_filename}")
    
    # Save HTML if available
    if data.get("amortization_data", {}).get("html"):
        html_filename = f"{filename_prefix}_page_{timestamp}.html"
        with open(html_filename, "w", encoding="utf-8") as f:
            f.write(data["amortization_data"]["html"])
        print(f"HTML page saved to {html_filename}")
    
    # Save summary data
    if data.get("amortization_data", {}).get("summary"):
        summary_filename = f"{filename_prefix}_summary_{timestamp}.txt"
        with open(summary_filename, "w", encoding="utf-8") as f:
            f.write("=== Mortgage Summary ===\n\n")
            summary = data["amortization_data"]["summary"]
            for key, value in summary.items():
                f.write(f"{key}: {value}\n")
            
            # Add structured data summary
            structured_data = data["amortization_data"].get("structuredData", {})
            if structured_data:
                f.write(f"\n=== Structured Data Summary ===\n")
                f.write(f"Total Payments: {structured_data.get('totalPayments', 0)}\n")
                f.write(f"Total Interest: {structured_data.get('totalInterest', 0)}\n")
                f.write(f"Total Principal: {structured_data.get('totalPrincipal', 0)}\n")
        
        print(f"Summary saved to {summary_filename}")

def main():
    """Main function to run mortgage data extraction"""
    print("=== Final Hebrew Mortgage Calculator Extractor ===\n")
    
    # Check if command line arguments are provided
    if len(sys.argv) >= 5:
        loan_amount = sys.argv[1]
        interest_rate = sys.argv[2]
        loan_term = sys.argv[3]
        cpi_rate = sys.argv[4]
        scenario_name = sys.argv[5] if len(sys.argv) > 5 else "Custom_Mortgage"
        
        print(f"Using command line arguments:")
        print(f"Loan Amount: ₪{loan_amount}")
        print(f"Interest Rate: {interest_rate}%")
        print(f"Loan Term: {loan_term} years")
        print(f"CPI Rate: {cpi_rate}%")
        print(f"Scenario: {scenario_name}")
        
        result = extract_mortgage_data(loan_amount, interest_rate, loan_term, cpi_rate)
        result["scenario"] = scenario_name
        
        # Save result
        save_data_to_files(result, f"final_mortgage_{scenario_name}")
        
        print(f"Extraction completed: {'Success' if result['success'] else 'Failed'}")
        
    else:
        # Default test scenarios
        test_scenarios = [
            {
                "name": "Basic_Mortgage",
                "loan_amount": "1000000",
                "interest_rate": "3.5",
                "loan_term": "30",
                "cpi_rate": "2.0"
            },
            {
                "name": "High_Amount_Mortgage",
                "loan_amount": "2000000",
                "interest_rate": "4.0",
                "loan_term": "25",
                "cpi_rate": "1.5"
            },
            {
                "name": "Short_Term_Mortgage",
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
            save_data_to_files(result, f"final_mortgage_{scenario['name']}")
            
            print(f"Test {i+1} completed: {'Success' if result['success'] else 'Failed'}")
            
            # Wait between tests
            if i < len(test_scenarios) - 1:
                print("Waiting 3 seconds before next test...")
                time.sleep(3)
        
        # Save all results
        save_data_to_files({"all_results": all_results}, "final_all_mortgage_results")
        
        print(f"\n=== All Tests Completed ===")
        successful_tests = sum(1 for r in all_results if r['success'])
        print(f"Successful tests: {successful_tests}/{len(test_scenarios)}")

if __name__ == "__main__":
    main() 