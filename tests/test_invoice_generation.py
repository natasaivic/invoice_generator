import pytest
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

@pytest.mark.ui
class TestInvoiceGeneration:
    
    def test_page_loads_successfully(self, chrome_driver, flask_server):
        """Test that the invoice generator page loads successfully"""
        driver, download_dir = chrome_driver
        
        driver.get(flask_server)
        time.sleep(3)  # Pause to observe page load
        
        # Check page title
        assert "Invoice Generator" in driver.title
        
        # Check that main elements are present
        header = driver.find_element(By.TAG_NAME, "h1")
        assert "Invoice Generator" in header.text
        time.sleep(3)  # Pause to observe header validation
        
        # Check form is present
        form = driver.find_element(By.ID, "invoiceForm")
        assert form.is_displayed()
        time.sleep(3)  # Pause to observe form validation
    
    def test_form_fields_exist(self, chrome_driver, flask_server):
        """Test that all required form fields are present"""
        driver, download_dir = chrome_driver
        driver.get(flask_server)
        time.sleep(3)  # Pause to observe page load
        
        # Check invoice details fields
        assert driver.find_element(By.ID, "invoice_number").is_displayed()
        assert driver.find_element(By.ID, "date").is_displayed()
        assert driver.find_element(By.ID, "due_date").is_displayed()
        time.sleep(3)  # Pause to observe invoice fields
        
        # Check from fields
        assert driver.find_element(By.ID, "from_name").is_displayed()
        assert driver.find_element(By.ID, "from_company").is_displayed()
        time.sleep(3)  # Pause to observe from fields
        
        # Check to fields
        assert driver.find_element(By.ID, "to_name").is_displayed()
        assert driver.find_element(By.ID, "to_company").is_displayed()
        time.sleep(3)  # Pause to observe to fields
        
        # Check action buttons
        assert driver.find_element(By.ID, "add-item").is_displayed()
        assert driver.find_element(By.ID, "preview-btn").is_displayed()
        time.sleep(3)  # Pause to observe action buttons
        
        # Check submit button
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        assert submit_btn.is_displayed()
        time.sleep(3)  # Pause to observe submit button
    
    def test_fill_complete_invoice_form(self, chrome_driver, flask_server, invoice_test_data):
        """Test filling out the complete invoice form"""
        driver, download_dir = chrome_driver
        driver.get(flask_server)
        time.sleep(3)  # Pause to observe page load
        
        # Fill invoice details
        driver.find_element(By.ID, "invoice_number").clear()
        driver.find_element(By.ID, "invoice_number").send_keys(invoice_test_data["invoice_details"]["invoice_number"])
        driver.find_element(By.ID, "date").send_keys(invoice_test_data["invoice_details"]["date"])
        driver.find_element(By.ID, "due_date").send_keys(invoice_test_data["invoice_details"]["due_date"])
        time.sleep(3)  # Pause to observe invoice details filled
        
        # Fill from information
        driver.find_element(By.ID, "from_name").send_keys(invoice_test_data["from_info"]["name"])
        driver.find_element(By.ID, "from_company").send_keys(invoice_test_data["from_info"]["company"])
        driver.find_element(By.ID, "from_address").send_keys(invoice_test_data["from_info"]["address"])
        driver.find_element(By.ID, "from_city").send_keys(invoice_test_data["from_info"]["city"])
        driver.find_element(By.ID, "from_email").send_keys(invoice_test_data["from_info"]["email"])
        driver.find_element(By.ID, "from_phone").send_keys(invoice_test_data["from_info"]["phone"])
        time.sleep(3)  # Pause to observe from info filled
        
        # Fill to information
        driver.find_element(By.ID, "to_name").send_keys(invoice_test_data["to_info"]["name"])
        driver.find_element(By.ID, "to_company").send_keys(invoice_test_data["to_info"]["company"])
        driver.find_element(By.ID, "to_address").send_keys(invoice_test_data["to_info"]["address"])
        driver.find_element(By.ID, "to_city").send_keys(invoice_test_data["to_info"]["city"])
        driver.find_element(By.ID, "to_email").send_keys(invoice_test_data["to_info"]["email"])
        time.sleep(3)  # Pause to observe to info filled
        
        # Fill first item (should already exist)
        first_item = driver.find_element(By.CSS_SELECTOR, ".item-row")
        first_item.find_element(By.CSS_SELECTOR, "input[name^='description_']").send_keys(invoice_test_data["items"][0]["description"])
        first_item.find_element(By.CSS_SELECTOR, "input[name^='quantity_']").clear()
        first_item.find_element(By.CSS_SELECTOR, "input[name^='quantity_']").send_keys(invoice_test_data["items"][0]["quantity"])
        first_item.find_element(By.CSS_SELECTOR, "input[name^='rate_']").send_keys(invoice_test_data["items"][0]["rate"])
        time.sleep(3)  # Pause to observe first item filled
        
        # Add second item
        driver.find_element(By.ID, "add-item").click()
        time.sleep(3)  # Pause to observe item addition
        
        # Fill second item
        items = driver.find_elements(By.CSS_SELECTOR, ".item-row")
        second_item = items[1]
        second_item.find_element(By.CSS_SELECTOR, "input[name^='description_']").send_keys(invoice_test_data["items"][1]["description"])
        second_item.find_element(By.CSS_SELECTOR, "input[name^='quantity_']").clear()
        second_item.find_element(By.CSS_SELECTOR, "input[name^='quantity_']").send_keys(invoice_test_data["items"][1]["quantity"])
        second_item.find_element(By.CSS_SELECTOR, "input[name^='rate_']").send_keys(invoice_test_data["items"][1]["rate"])
        time.sleep(3)  # Pause to observe second item filled
        
        # Fill notes
        driver.find_element(By.ID, "notes").send_keys(invoice_test_data["notes"])
        time.sleep(3)  # Pause to observe notes filled
        
        # Verify form is filled
        assert driver.find_element(By.ID, "invoice_number").get_attribute("value") == invoice_test_data["invoice_details"]["invoice_number"]
        assert driver.find_element(By.ID, "from_name").get_attribute("value") == invoice_test_data["from_info"]["name"]
        assert driver.find_element(By.ID, "to_name").get_attribute("value") == invoice_test_data["to_info"]["name"]

@pytest.mark.ui
class TestInvoiceCalculations:
    
    def test_real_time_calculations(self, chrome_driver, flask_server):
        """Test that calculations update in real time"""
        driver, download_dir = chrome_driver
        driver.get(flask_server)
        time.sleep(3)  # Pause to observe page load
        
        # Fill first item
        first_item = driver.find_element(By.CSS_SELECTOR, ".item-row")
        qty_input = first_item.find_element(By.CSS_SELECTOR, "input[name^='quantity_']")
        rate_input = first_item.find_element(By.CSS_SELECTOR, "input[name^='rate_']")
        amount_span = first_item.find_element(By.CSS_SELECTOR, ".amount")
        
        # Clear existing values and enter test values
        qty_input.clear()
        qty_input.send_keys("5")
        time.sleep(3)  # Pause to observe quantity entry
        rate_input.clear()
        rate_input.send_keys("100")
        time.sleep(3)  # Pause to observe rate entry and calculation
        
        # Check item amount
        assert "$500.00" in amount_span.text
        
        # Check total
        total_element = driver.find_element(By.ID, "total-amount")
        assert "500.00" in total_element.text
    
    def test_multiple_items_calculation(self, chrome_driver, flask_server):
        """Test calculations with multiple items"""
        driver, download_dir = chrome_driver
        driver.get(flask_server)
        time.sleep(3)  # Pause to observe page load
        
        # Fill first item
        first_item = driver.find_element(By.CSS_SELECTOR, ".item-row")
        first_item.find_element(By.CSS_SELECTOR, "input[name^='quantity_']").clear()
        first_item.find_element(By.CSS_SELECTOR, "input[name^='quantity_']").send_keys("2")
        first_item.find_element(By.CSS_SELECTOR, "input[name^='rate_']").send_keys("50")
        time.sleep(3)  # Pause to observe first item calculation
        
        # Add second item
        driver.find_element(By.ID, "add-item").click()
        time.sleep(3)  # Pause to observe item addition
        
        # Fill second item
        items = driver.find_elements(By.CSS_SELECTOR, ".item-row")
        second_item = items[1]
        second_item.find_element(By.CSS_SELECTOR, "input[name^='quantity_']").clear()
        second_item.find_element(By.CSS_SELECTOR, "input[name^='quantity_']").send_keys("3")
        second_item.find_element(By.CSS_SELECTOR, "input[name^='rate_']").send_keys("75")
        time.sleep(3)  # Pause to observe second item calculation
        
        # Check individual amounts
        first_amount = items[0].find_element(By.CSS_SELECTOR, ".amount")
        second_amount = items[1].find_element(By.CSS_SELECTOR, ".amount")
        
        assert "$100.00" in first_amount.text
        assert "$225.00" in second_amount.text
        
        # Check total (100 + 225 = 325)
        total_element = driver.find_element(By.ID, "total-amount")
        assert "325.00" in total_element.text

@pytest.mark.ui
class TestInvoicePreview:
    
    def test_preview_functionality(self, chrome_driver, flask_server, minimal_invoice_data):
        """Test the invoice preview functionality"""
        driver, download_dir = chrome_driver
        driver.get(flask_server)
        time.sleep(3)  # Pause to observe page load
        
        # Fill minimal form data
        driver.find_element(By.ID, "invoice_number").clear()
        driver.find_element(By.ID, "invoice_number").send_keys(minimal_invoice_data["invoice_details"]["invoice_number"])
        driver.find_element(By.ID, "from_name").send_keys(minimal_invoice_data["from_info"]["name"])
        driver.find_element(By.ID, "to_name").send_keys(minimal_invoice_data["to_info"]["name"])
        time.sleep(3)  # Pause to observe form filling
        
        # Fill item
        first_item = driver.find_element(By.CSS_SELECTOR, ".item-row")
        first_item.find_element(By.CSS_SELECTOR, "input[name^='description_']").send_keys(minimal_invoice_data["items"][0]["description"])
        first_item.find_element(By.CSS_SELECTOR, "input[name^='rate_']").send_keys(minimal_invoice_data["items"][0]["rate"])
        time.sleep(3)  # Pause to observe item filling
        
        # Click preview button
        preview_btn = driver.find_element(By.ID, "preview-btn")
        preview_btn.click()
        time.sleep(3)  # Pause to observe preview generation
        
        # Wait for preview to appear
        wait = WebDriverWait(driver, 10)
        preview_section = wait.until(EC.visibility_of_element_located((By.ID, "preview-section")))
        
        # Check preview content
        assert preview_section.is_displayed()
        
        # Check that preview contains our data
        preview_content = driver.find_element(By.ID, "invoice-preview")
        assert minimal_invoice_data["invoice_details"]["invoice_number"] in preview_content.text
        assert minimal_invoice_data["from_info"]["name"] in preview_content.text
        assert minimal_invoice_data["to_info"]["name"] in preview_content.text
        assert minimal_invoice_data["items"][0]["description"] in preview_content.text

@pytest.mark.ui
class TestPDFGeneration:
    
    def test_pdf_generation_and_download(self, chrome_driver, flask_server, minimal_invoice_data):
        """Test PDF generation and download"""
        driver, download_dir = chrome_driver
        driver.get(flask_server)
        time.sleep(3)  # Pause to observe page load
        
        # Fill required fields
        driver.find_element(By.ID, "invoice_number").clear()
        driver.find_element(By.ID, "invoice_number").send_keys(minimal_invoice_data["invoice_details"]["invoice_number"])
        driver.find_element(By.ID, "from_name").send_keys(minimal_invoice_data["from_info"]["name"])
        driver.find_element(By.ID, "to_name").send_keys(minimal_invoice_data["to_info"]["name"])
        time.sleep(3)  # Pause to observe form filling
        
        # Fill item
        first_item = driver.find_element(By.CSS_SELECTOR, ".item-row")
        first_item.find_element(By.CSS_SELECTOR, "input[name^='description_']").send_keys(minimal_invoice_data["items"][0]["description"])
        first_item.find_element(By.CSS_SELECTOR, "input[name^='rate_']").send_keys(minimal_invoice_data["items"][0]["rate"])
        time.sleep(3)  # Pause to observe item filling
        
        # Get initial file count in download directory
        initial_files = os.listdir(download_dir)
        initial_count = len(initial_files)
        
        # Submit form to generate PDF
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        time.sleep(3)  # Pause to observe PDF generation start
        
        # Wait for download to complete (up to 10 seconds)
        download_completed = False
        for _ in range(20):  # Check every 0.5 seconds for 10 seconds
            time.sleep(0.5)
            current_files = os.listdir(download_dir)
            current_count = len(current_files)
            
            if current_count > initial_count:
                # Check if it's a PDF file
                new_files = [f for f in current_files if f not in initial_files]
                pdf_files = [f for f in new_files if f.endswith('.pdf')]
                if pdf_files:
                    download_completed = True
                    downloaded_file = pdf_files[0]
                    break
        
        # Verify download completed
        assert download_completed, "PDF download did not complete within expected time"
        
        # Verify the downloaded file
        file_path = os.path.join(download_dir, downloaded_file)
        assert os.path.exists(file_path), "Downloaded PDF file does not exist"
        assert os.path.getsize(file_path) > 0, "Downloaded PDF file is empty"
        
        # Verify filename contains invoice number
        assert minimal_invoice_data["invoice_details"]["invoice_number"] in downloaded_file

@pytest.mark.ui
@pytest.mark.smoke
class TestSmokeTests:
    
    def test_complete_invoice_workflow(self, chrome_driver, flask_server, invoice_test_data):
        """Complete end-to-end smoke test of invoice generation workflow"""
        driver, download_dir = chrome_driver
        driver.get(flask_server)
        time.sleep(3)  # Pause to observe page load
        
        # Step 1: Fill complete form
        self._fill_complete_form(driver, invoice_test_data)
        time.sleep(3)  # Pause to observe completed form
        
        # Step 2: Test preview
        preview_btn = driver.find_element(By.ID, "preview-btn")
        preview_btn.click()
        time.sleep(3)  # Pause to observe preview generation
        
        wait = WebDriverWait(driver, 10)
        preview_section = wait.until(EC.visibility_of_element_located((By.ID, "preview-section")))
        assert preview_section.is_displayed()
        
        # Step 3: Generate PDF
        initial_files = os.listdir(download_dir)
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        time.sleep(3)  # Pause to observe PDF generation start
        
        # Step 4: Verify download
        download_completed = False
        for _ in range(20):
            time.sleep(0.5)
            current_files = os.listdir(download_dir)
            new_files = [f for f in current_files if f not in initial_files and f.endswith('.pdf')]
            if new_files:
                download_completed = True
                break
        
        assert download_completed, "Complete workflow test failed - PDF not downloaded"
    
    def _fill_complete_form(self, driver, test_data):
        """Helper method to fill the complete form"""
        # Invoice details
        driver.find_element(By.ID, "invoice_number").clear()
        driver.find_element(By.ID, "invoice_number").send_keys(test_data["invoice_details"]["invoice_number"])
        time.sleep(3)  # Pause to observe invoice details
        
        # From info
        driver.find_element(By.ID, "from_name").send_keys(test_data["from_info"]["name"])
        driver.find_element(By.ID, "from_company").send_keys(test_data["from_info"]["company"])
        time.sleep(3)  # Pause to observe from info
        
        # To info
        driver.find_element(By.ID, "to_name").send_keys(test_data["to_info"]["name"])
        driver.find_element(By.ID, "to_company").send_keys(test_data["to_info"]["company"])
        time.sleep(3)  # Pause to observe to info
        
        # First item
        first_item = driver.find_element(By.CSS_SELECTOR, ".item-row")
        first_item.find_element(By.CSS_SELECTOR, "input[name^='description_']").send_keys(test_data["items"][0]["description"])
        first_item.find_element(By.CSS_SELECTOR, "input[name^='quantity_']").clear()
        first_item.find_element(By.CSS_SELECTOR, "input[name^='quantity_']").send_keys(test_data["items"][0]["quantity"])
        first_item.find_element(By.CSS_SELECTOR, "input[name^='rate_']").send_keys(test_data["items"][0]["rate"])
        time.sleep(3)  # Pause to observe item and calculation
        
        # Notes
        driver.find_element(By.ID, "notes").send_keys(test_data["notes"])
        time.sleep(3)  # Pause to observe notes