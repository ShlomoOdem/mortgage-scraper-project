#!/usr/bin/env python3
"""
Modular Mortgage Data Extractor
Extracts mortgage data to CSV files without any analysis
"""

import time
import json
import re
import html
import csv
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import unquote

def get_combination_key(combination):
    """Generate a unique key for a mortgage combination"""
    return f"{combination['loan_amount']}_{combination['interest_rate']}_{combination['loan_term_months']}_{combination['cpi_rate']}_{combination['channel']}_{combination['amortization']}"

def load_processed_combinations(tracking_file="processed_combinations.json"):
    """Load the list of already processed combinations"""
    if os.path.exists(tracking_file):
        try:
            with open(tracking_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return set(data.get('processed_combinations', []))
        except (json.JSONDecodeError, FileNotFoundError):
            return set()
    return set()

def save_processed_combinations(processed_combinations, tracking_file="processed_combinations.json"):
    """Save the list of processed combinations"""
    data = {
        'last_updated': datetime.now().isoformat(),
        'total_processed': len(processed_combinations),
        'processed_combinations': list(processed_combinations)
    }
    with open(tracking_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def filter_unprocessed_combinations(combinations, tracking_file="processed_combinations.json"):
    """Filter out combinations that have already been processed"""
    processed = load_processed_combinations(tracking_file)
    unprocessed = []
    
    for combo in combinations:
        combo_key = get_combination_key(combo)
        if combo_key not in processed:
            unprocessed.append(combo)
    
    return unprocessed, len(combinations) - len(unprocessed)

def mark_combination_as_processed(combination, tracking_file="processed_combinations.json"):
    """Mark a combination as processed"""
    processed = load_processed_combinations(tracking_file)
    combo_key = get_combination_key(combination)
    processed.add(combo_key)
    save_processed_combinations(processed, tracking_file)

def setup_driver(headless=True):
    """Set up Chrome driver with appropriate options"""
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def wait_for_page_load(driver, timeout=5):
    """Wait for the page to be fully loaded and the calculator form to be ready"""
    print("Waiting for page to load...")
    try:
        # Wait for the specific amount input element to be present and visible
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.amount-input[placeholder='הזן סכום']"))
        )
        
        # Also wait for it to be visible
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input.amount-input[placeholder='הזן סכום']"))
        )
        
        print("Page loaded successfully - calculator form is ready")
        return True
    except Exception as e:
        print(f"Error waiting for page load: {e}")
        return False

def close_dialog_if_present(driver):
    """Close any dialog/lightbox that might be blocking the page"""
    print("Checking for dialogs/lightboxes to close...")
    
    try:
        # Look for the close button
        close_button = driver.find_element(By.CSS_SELECTOR, '.dialog-close-button.dialog-lightbox-close-button')
        if close_button:
            print("Found dialog close button, clicking it...")
            close_button.click()
            time.sleep(1)  # Wait for dialog to close
            print("Dialog closed successfully")
            return True
    except:
        # No dialog found, which is fine
        print("No dialog found to close")
        pass
    
    # Also try to close any other common dialog types
    try:
        # Look for any close button with similar classes
        close_buttons = driver.find_elements(By.CSS_SELECTOR, '.dialog-close-button, .lightbox-close, .modal-close, .close-button')
        for button in close_buttons:
            if button.is_displayed():
                print("Found visible close button, clicking it...")
                button.click()
                time.sleep(1)
                print("Additional dialog closed")
                return True
    except:
        pass
    
    return False

def try_trigger_calculations(driver):
    """Try to trigger calculations by clicking on the amortization form"""
    print("Trying to trigger calculations...")
    
    try:
        # Wait a moment for any dynamic content to load
        time.sleep(2)
        
        # Store the original window handle
        original_window = driver.current_window_handle
        
        # Look for the specific amortization form with class "monthly-return-btn"
        try:
            amortization_form = driver.find_element(By.CSS_SELECTOR, 'form.monthly-return-btn')
            if amortization_form.is_displayed():
                print("Found amortization form, clicking it...")
                amortization_form.click()
                print("Clicked amortization form successfully")
                
                # Wait a moment for the new tab to open
                time.sleep(2)
                
                # Check if a new tab/window opened
                all_windows = driver.window_handles
                if len(all_windows) > 1:
                    print(f"New tab detected. Closing {len(all_windows) - 1} additional tab(s)...")
                    
                    # Close all tabs except the original one
                    for window_handle in all_windows:
                        if window_handle != original_window:
                            driver.switch_to.window(window_handle)
                            driver.close()
                    
                    # Switch back to the original tab
                    driver.switch_to.window(original_window)
                    print("Returned to original tab")
                else:
                    print("No new tab opened")
                
                return True
        except Exception as e:
            print(f"Amortization form not found or not clickable: {e}")
        
        # Fallback: Look for any form with cp_programs input
        try:
            forms_with_cp = driver.find_elements(By.CSS_SELECTOR, 'form input[name="cp_programs"]')
            if forms_with_cp:
                print(f"Found {len(forms_with_cp)} forms with cp_programs input")
                for form_input in forms_with_cp:
                    try:
                        form = form_input.find_element(By.XPATH, './..')  # Get parent form
                        if form.is_displayed():
                            print("Clicking form with cp_programs input...")
                            form.click()
                            time.sleep(2)
                            
                            # Check for new tabs and close them
                            all_windows = driver.window_handles
                            if len(all_windows) > 1:
                                print(f"New tab detected. Closing {len(all_windows) - 1} additional tab(s)...")
                                for window_handle in all_windows:
                                    if window_handle != original_window:
                                        driver.switch_to.window(window_handle)
                                        driver.close()
                                driver.switch_to.window(original_window)
                                print("Returned to original tab")
                            
                            return True
                    except Exception as e:
                        print(f"Failed to click form: {e}")
        except Exception as e:
            print(f"Error looking for forms with cp_programs: {e}")
        
        # Additional fallback: Look for elements containing "לוח סילוקין"
        try:
            elements_with_text = driver.find_elements(By.XPATH, "//*[contains(text(), 'לוח סילוקין')]")
            for element in elements_with_text:
                if element.is_displayed() and element.is_enabled():
                    print("Found element with 'לוח סילוקין' text, clicking it...")
                    element.click()
                    time.sleep(2)
                    
                    # Check for new tabs and close them
                    all_windows = driver.window_handles
                    if len(all_windows) > 1:
                        print(f"New tab detected. Closing {len(all_windows) - 1} additional tab(s)...")
                        for window_handle in all_windows:
                            if window_handle != original_window:
                                driver.switch_to.window(window_handle)
                                driver.close()
                        driver.switch_to.window(original_window)
                        print("Returned to original tab")
                    
                    return True
        except Exception as e:
            print(f"Error looking for elements with text: {e}")
        
        print("No calculation triggers found")
        return False
        
    except Exception as e:
        print(f"Error trying to trigger calculations: {e}")
        return False

def inject_values_via_javascript(driver, loan_amount, interest_rate, loan_term_months, cpi_rate, channel, amortization):
    """Inject values into the calculator using JavaScript"""
    print("Injecting values via JavaScript...")
    
    # JavaScript to set values directly using the correct selectors
    js_script = f"""
    console.log('Setting values using correct selectors...');
    
    // Set amount in the amount input field
    var amountInput = document.querySelector('input.amount-input[placeholder="הזן סכום"]');
    if (amountInput) {{
        amountInput.value = '{loan_amount}';
        amountInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
        amountInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
        console.log('Set amount to: {loan_amount}');
    }} else {{
        console.log('Amount input not found');
    }}
    
    // Set interest rate in the interest input field
    var interestInput = document.querySelector('input.interest-input[placeholder="הזן"]');
    if (interestInput) {{
        interestInput.value = '{interest_rate}';
        interestInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
        interestInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
        console.log('Set interest to: {interest_rate}');
    }} else {{
        console.log('Interest input not found');
    }}
    
    // Handle duration selection in custom dropdown
    var durationContainer = document.querySelector('.container-custom-select.duration');
    if (durationContainer) {{
        // Click to open the dropdown
        var selectorFace = durationContainer.querySelector('.selector-face');
        if (selectorFace) {{
            selectorFace.click();
            console.log('Opened duration dropdown');
            
            // Wait a moment for dropdown to open
            setTimeout(function() {{
                // Look for the duration option with the specific number of months
                var durationOptions = durationContainer.querySelectorAll('li');
                var targetDuration = '{loan_term_months}';
                
                for (var i = 0; i < durationOptions.length; i++) {{
                    var option = durationOptions[i];
                    var text = option.textContent.trim();
                    if (text.includes(targetDuration)) {{
                        option.click();
                        console.log('Selected duration:', text);
                        break;
                    }}
                }}
            }}, 500);
        }}
    }} else {{
        console.log('Duration container not found');
    }}
    
    // Handle channel selection (מסלול)
    var channelContainer = document.querySelector('.container-custom-select.chanel');
    if (channelContainer) {{
        // Click to open the dropdown
        var selectorFace = channelContainer.querySelector('.selector-face');
        if (selectorFace) {{
            selectorFace.click();
            console.log('Opened channel dropdown');
            
            // Wait a moment for dropdown to open
            setTimeout(function() {{
                // Look for the specified channel option
                var channelOptions = channelContainer.querySelectorAll('li');
                var targetChannel = '{channel}';
                
                for (var i = 0; i < channelOptions.length; i++) {{
                    var option = channelOptions[i];
                    var text = option.textContent.trim();
                    if (text.includes(targetChannel)) {{
                        option.click();
                        console.log('Selected channel:', text);
                        break;
                    }}
                }}
            }}, 500);
        }}
    }} else {{
        console.log('Channel container not found');
    }}
    
    // Handle amortization method selection (שיטת החזר)
    var amortizationContainer = document.querySelector('.container-custom-select.amortization');
    if (amortizationContainer) {{
        // Click to open the dropdown
        var selectorFace = amortizationContainer.querySelector('.selector-face');
        if (selectorFace) {{
            selectorFace.click();
            console.log('Opened amortization dropdown');
            
            // Wait a moment for dropdown to open
            setTimeout(function() {{
                // Look for the specified amortization option
                var amortizationOptions = amortizationContainer.querySelectorAll('li');
                var targetAmortization = '{amortization}';
                
                for (var i = 0; i < amortizationOptions.length; i++) {{
                    var option = amortizationOptions[i];
                    var text = option.textContent.trim();
                    if (text.includes(targetAmortization)) {{
                        option.click();
                        console.log('Selected amortization:', text);
                        break;
                    }}
                }}
            }}, 500);
        }}
    }} else {{
        console.log('Amortization container not found');
    }}
    
    // Set CPI rate in the CPI input field (if it exists)
    var cpiInput = document.querySelector('input.cpi-input[placeholder="הזן מדד"]');
    if (cpiInput) {{
        cpiInput.value = '{cpi_rate}';
        cpiInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
        cpiInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
        console.log('Set CPI to: {cpi_rate}');
    }} else {{
        console.log('CPI input not found (may be disabled)');
    }}
    
    // Trigger any additional events that might be needed
    setTimeout(function() {{
        // Trigger blur events to ensure the calculator recognizes the changes
        if (amountInput) {{
            amountInput.dispatchEvent(new Event('blur', {{ bubbles: true }}));
            amountInput.dispatchEvent(new Event('focusout', {{ bubbles: true }}));
        }}
        if (interestInput) {{
            interestInput.dispatchEvent(new Event('blur', {{ bubbles: true }}));
            interestInput.dispatchEvent(new Event('focusout', {{ bubbles: true }}));
        }}
        console.log('Triggered blur and focusout events');
        
        // Try to trigger any calculation buttons or forms
        var calculateButtons = document.querySelectorAll('button[type="submit"], input[type="submit"], .calculate-button, .submit-button');
        if (calculateButtons.length > 0) {{
            console.log('Found', calculateButtons.length, 'potential calculate buttons');
            calculateButtons[0].click();
        }}
        
        // Try to submit any forms
        var forms = document.querySelectorAll('form');
        if (forms.length > 0) {{
            console.log('Found', forms.length, 'forms');
            // Don't actually submit, just trigger events
            forms[0].dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}
    }}, 1000);
    
    return {{
        amountInput: amountInput ? 1 : 0,
        interestInput: interestInput ? 1 : 0,
        durationContainer: durationContainer ? 1 : 0,
        channelContainer: channelContainer ? 1 : 0,
        amortizationContainer: amortizationContainer ? 1 : 0,
        cpiInput: cpiInput ? 1 : 0
    }};
    """
    
    try:
        close_dialog_if_present(driver)
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
        # Try multiple strategies to find the cp_programs input
        wait = WebDriverWait(driver, 10)
        
        # Strategy 1: Look for cp_programs input anywhere on the page
        try:
            cp_programs_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="cp_programs"]')))
            cp_programs_value = cp_programs_input.get_attribute('value')
            if cp_programs_value:
                print(f"Found cp_programs value (length: {len(cp_programs_value)})")
                print(f"Value preview: {cp_programs_value[:100]}...")
                return cp_programs_value
        except:
            pass
        
        # Strategy 2: Look for the form with the specific action URL
        try:
            form_selector = 'form[action*="לוח-סילוקין-מלא"]'
            form = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, form_selector)))
            cp_programs_input = form.find_element(By.CSS_SELECTOR, 'input[name="cp_programs"]')
            cp_programs_value = cp_programs_input.get_attribute('value')
            if cp_programs_value:
                print(f"Found cp_programs value in form (length: {len(cp_programs_value)})")
                return cp_programs_value
        except:
            pass
        
        # Strategy 3: Look for any hidden input with a long value (likely cp_programs)
        try:
            hidden_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="hidden"]')
            for input_elem in hidden_inputs:
                value = input_elem.get_attribute('value')
                if value and len(value) > 1000:  # cp_programs values are very long
                    print(f"Found long hidden input value (length: {len(value)})")
                    return value
        except:
            pass
        
        print("cp_programs value not found")
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

def save_raw_mortgage_data(cp_programs_value, parsed_data, loan_type="Fixed_Linked", interest_rate="3.5", loan_term_months="360", inflation_rate="2.0", amortization="שפיצר"):
    """Save the raw mortgage data to CSV files without any analysis"""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    # Create filename with loan parameters
    base_filename = f"loan_{loan_type}_int_{interest_rate}_term_{loan_term_months}_infl_{inflation_rate}_amort_{amortization}"
    
    # Save monthly payments as CSV in payments_files folder
    payments_filename = os.path.join("data", "raw", "payments_files", f"{base_filename}_payments.csv")
    os.makedirs(os.path.dirname(payments_filename), exist_ok=True)
    
    if parsed_data and 'monthly_payments' in parsed_data and parsed_data['monthly_payments']:
        with open(payments_filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = parsed_data['monthly_payments'][0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for payment in parsed_data['monthly_payments']:
                writer.writerow(payment)
        print(f"Saved monthly payments to: {payments_filename}")
    else:
        payments_filename = None
        print("No monthly payments data to save")
    
    # Save basic summary as CSV in summary_files folder
    summary_filename = os.path.join("data", "raw", "summary_files", f"{base_filename}_summary.csv")
    os.makedirs(os.path.dirname(summary_filename), exist_ok=True)
    
    if parsed_data:
        with open(summary_filename, 'w', newline='', encoding='utf-8') as f:
            # Create summary data
            summary_data = []
            
            # Add input parameters
            if 'input_data' in parsed_data:
                input_data = parsed_data['input_data']
                summary_data.append({
                    'Parameter': 'Loan Type',
                    'Value': loan_type
                })
                summary_data.append({
                    'Parameter': 'Interest Rate (%)',
                    'Value': interest_rate
                })
                summary_data.append({
                    'Parameter': 'Loan Term (months)',
                    'Value': loan_term_months
                })
                summary_data.append({
                    'Parameter': 'Inflation Rate (%)',
                    'Value': inflation_rate
                })
                summary_data.append({
                    'Parameter': 'Loan Amount',
                    'Value': input_data.get('amount', 'N/A')
                })
                summary_data.append({
                    'Parameter': 'Channel',
                    'Value': input_data.get('chanel', 'N/A')
                })
                summary_data.append({
                    'Parameter': 'Amortization Method',
                    'Value': input_data.get('amortization', 'N/A')
                })
            
            # Add basic mortgage calculation results
            summary_data.append({
                'Parameter': 'Total Monthly Payments',
                'Value': parsed_data.get('total_payments', 'N/A')
            })
            
            # Calculate total mortgage interest
            total_mortgage_interest = 0
            if 'monthly_payments' in parsed_data:
                for payment in parsed_data['monthly_payments']:
                    total_mortgage_interest += payment.get('interest', 0)
            
            summary_data.append({
                'Parameter': 'Total Mortgage Interest',
                'Value': f"{total_mortgage_interest:.2f}"
            })
            
            summary_data.append({
                'Parameter': 'Extraction Timestamp',
                'Value': timestamp
            })
            
            # Write summary CSV
            fieldnames = ['Parameter', 'Value']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in summary_data:
                writer.writerow(row)
        print(f"Saved summary to: {summary_filename}")
    else:
        summary_filename = None
        print("No parsed data to save summary")
    
    return {
        'payments_file': payments_filename,
        'summary_file': summary_filename
    }

def extract_single_mortgage(driver, loan_amount="1000000", interest_rate="3.5", loan_term_months="360", cpi_rate="2.0", channel="קבועה צמודה", amortization="שפיצר"):
    """Extract mortgage data for a single loan combination"""
    try:
        print(f"\n{'='*60}")
        print(f"Processing: {loan_amount} @ {interest_rate}% for {loan_term_months} months (CPI: {cpi_rate}%)")
        print(f"Channel: {channel}, Amortization: {amortization}")
        print(f"{'='*60}")
        
        # Check for and close any dialog/lightbox that might appear
        close_dialog_if_present(driver)
        
        # Inject values
        if not inject_values_via_javascript(driver, loan_amount, interest_rate, loan_term_months, cpi_rate, channel, amortization):
            print("Failed to inject values")
            return None
        
        # Wait for the JavaScript to complete and calculations to start
        print("Waiting for calculations to process...")
        
        # Check for dialogs again after setting values
        close_dialog_if_present(driver)
        
        # Try to trigger calculations by clicking on the amortization link
        try_trigger_calculations(driver)
        
        # Extract cp_programs value
        cp_programs_value = extract_cp_programs_value(driver)
        
        if not cp_programs_value:
            print("Failed to extract cp_programs value")
            return None
        
        # Parse the data
        parsed_data = parse_cp_programs_data(cp_programs_value)
        
        if not parsed_data:
            print("Failed to parse cp_programs data")
            return None
        
        # Save the raw data (no analysis)
        saved_files = save_raw_mortgage_data(
            cp_programs_value, 
            parsed_data, 
            loan_type=channel,  # Use channel as loan type
            interest_rate=interest_rate,
            loan_term_months=loan_term_months,
            inflation_rate=cpi_rate,
            amortization=amortization
        )
        
        print("Extraction completed successfully!")
        return saved_files
        
    except Exception as e:
        print(f"Error during extraction: {e}")
        return None

def extract_multiple_mortgages(loan_combinations, headless=True, tracking_file="processed_combinations.json"):
    """Extract data for multiple loan combinations using a single driver"""
    driver = None
    results = []
    
    try:
        print("Starting batch extraction...")
        print(f"Total combinations to process: {len(loan_combinations)}")
        
        # # Filter out already processed combinations
        # unprocessed_combinations, already_processed_count = filter_unprocessed_combinations(loan_combinations, tracking_file)
        
        # if already_processed_count > 0:
        #     print(f"Found {already_processed_count} already processed combinations, skipping them...")
        #     print(f"Remaining combinations to process: {len(unprocessed_combinations)}")
        
        # if not unprocessed_combinations:
        #     print("All combinations have already been processed!")
        #     return []
        
        # Setup driver once
        driver = setup_driver(headless)
        
        # Navigate to the calculator page
        url = "https://mashcantaman.co.il/מחשבון-משכנתא/"
        print(f"Navigating to: {url}")
        driver.get(url)
        
        # Process each combination
        for i, combo in enumerate(loan_combinations , 1):
            print(f"\nProcessing combination {i}/{len(loan_combinations)}")
            
            loan_amount = combo.get('loan_amount', '1000000')
            interest_rate = combo.get('interest_rate', '3.5')
            loan_term_months = combo.get('loan_term_months', '360')
            cpi_rate = combo.get('cpi_rate', '2.0')
            channel = combo.get('channel', 'קבועה צמודה')
            amortization = combo.get('amortization', 'שפיצר')
            
            result = extract_single_mortgage(
                driver, loan_amount, interest_rate, loan_term_months, cpi_rate, channel, amortization
            )
            
            if result:
                results.append({
                    'combination': combo,
                    'files': result,
                    'status': 'success'
                })
                print(f"✓ Success: {loan_amount} @ {interest_rate}% for {loan_term_months} months")
                # Mark as processed only if successful
                # mark_combination_as_processed(combo, tracking_file)
            else:
                results.append({
                    'combination': combo,
                    'files': None,
                    'status': 'failed'
                })
                print(f"✗ Failed: {loan_amount} @ {interest_rate}% for {loan_term_months} months")
                # Don't mark failed combinations as processed so they can be retried
            
            # Small delay between combinations
            time.sleep(0.1)
        
        print(f"\nBatch extraction completed!")
        print(f"Successful: {sum(1 for r in results if r['status'] == 'success')}")
        print(f"Failed: {sum(1 for r in results if r['status'] == 'failed')}")
        # print(f"Skipped (already processed): {already_processed_count}")
        
        return results
        
    except Exception as e:
        print(f"Error during batch extraction: {e}")
        return results
        
    finally:
        if driver:
            driver.quit()

def main():
    """Main function for modular extraction"""
    import sys
    
    print("Modular Mortgage Data Extractor")
    print("=================================")
    
    # Check for command line arguments
    headless = True  # Default to headless
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ['--no-headless', '-n', '--visible', '-v']:
            headless = False
            print("Running in visible mode (non-headless)")
        elif sys.argv[1].lower() in ['--help', '-h']:
            print("Usage: python3 modular_extractor.py [OPTION]")
            print("Options:")
            print("  --no-headless, -n    Run in visible mode (show browser)")
            print("  --visible, -v        Run in visible mode (show browser)")
            print("  --help, -h           Show this help message")
            return
    
    # Define loan combinations for testing
    loan_combinations = [
        {'loan_amount': '1000000', 'interest_rate': '3.5', 'loan_term_months': '360', 'cpi_rate': '2.0', 'channel': 'קבועה צמודה', 'amortization': 'שפיצר'},
        {'loan_amount': '1000000', 'interest_rate': '3.5', 'loan_term_months': '360', 'cpi_rate': '2.0', 'channel': 'קבועה לא צמודה', 'amortization': 'שפיצר'},
    ]
    
    print(f"Processing {len(loan_combinations)} loan combinations:")
    for i, combo in enumerate(loan_combinations, 1):
        print(f"  {i}. {combo['loan_amount']} @ {combo['interest_rate']}% for {combo['loan_term_months']} months (CPI: {combo['cpi_rate']}%)")
        print(f"     Channel: {combo['channel']}, Amortization: {combo['amortization']}")
    
    print(f"\nHeadless Mode: {headless}")
    print(f"Files will be saved in:")
    print(f"  Payments: data/raw/payments_files/")
    print(f"  Summaries: data/raw/summary_files/")
    
    # Extract data for all combinations
    results = extract_multiple_mortgages(loan_combinations, headless)
    
    if results:
        print(f"\n{'='*60}")
        print(f"EXTRACTION SUMMARY")
        print(f"{'='*60}")
        
        successful = [r for r in results if r['status'] == 'success']
        failed = [r for r in results if r['status'] == 'failed']
        
        print(f"Total combinations: {len(results)}")
        print(f"Successful: {len(successful)}")
        print(f"Failed: {len(failed)}")
        
        if successful:
            print(f"\nSuccessful extractions:")
            for result in successful:
                combo = result['combination']
                files = result['files']
                print(f"  ✓ {combo['loan_amount']} @ {combo['interest_rate']}% for {combo['loan_term_months']} months")
                print(f"    Channel: {combo['channel']}, Amortization: {combo['amortization']}, CPI: {combo['cpi_rate']}%")
                if files:
                    if files.get('payments_file'):
                        print(f"    Payments: {files['payments_file']}")
                    if files.get('summary_file'):
                        print(f"    Summary: {files['summary_file']}")
        
        if failed:
            print(f"\nFailed extractions:")
            for result in failed:
                combo = result['combination']
                print(f"  ✗ {combo['loan_amount']} @ {combo['interest_rate']}% for {combo['loan_term_months']} months")
                print(f"    Channel: {combo['channel']}, Amortization: {combo['amortization']}, CPI: {combo['cpi_rate']}%")
    else:
        print("\nExtraction failed!")

if __name__ == "__main__":
    main() 