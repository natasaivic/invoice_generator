import pytest
import os
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import threading
import time
from flask import Flask

# Import the Flask app
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app as flask_app

@pytest.fixture(scope="session")
def flask_server():
    """Start Flask server in a separate thread for testing"""
    # Use a different port for testing to avoid conflicts
    test_port = 5001
    
    def run_server():
        flask_app.config['TESTING'] = True
        flask_app.run(host='127.0.0.1', port=test_port, debug=False, use_reloader=False)
    
    # Start server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Give server time to start
    time.sleep(2)
    
    yield f"http://127.0.0.1:{test_port}"
    
    # Server will be cleaned up automatically due to daemon thread

@pytest.fixture(scope="function")
def chrome_driver():
    """Create Chrome WebDriver instance for each test"""
    # Set up Chrome options
    chrome_options = Options()
    
    # For local development, run in headed mode
    # chrome_options.add_argument("--headless")  # Commented out for headed mode
    
    # Set up download directory
    download_dir = tempfile.mkdtemp()
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Additional options for stability
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Set up ChromeDriver service
    service = Service(ChromeDriverManager().install())
    
    # Create driver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    
    yield driver, download_dir
    
    # Cleanup
    driver.quit()

@pytest.fixture
def invoice_test_data():
    """Provide consistent test data for invoice creation"""
    return {
        "invoice_details": {
            "invoice_number": "TEST-001",
            "date": "2024-01-15",
            "due_date": "2024-02-15"
        },
        "from_info": {
            "name": "John Doe",
            "company": "Test Company Inc.",
            "address": "123 Test Street",
            "city": "Test City, TC 12345",
            "email": "john@testcompany.com",
            "phone": "+1-555-123-4567"
        },
        "to_info": {
            "name": "Jane Smith",
            "company": "Client Corp",
            "address": "456 Client Avenue",
            "city": "Client City, CC 67890",
            "email": "jane@clientcorp.com"
        },
        "items": [
            {
                "description": "Web Development Services",
                "quantity": "40",
                "rate": "75.00"
            },
            {
                "description": "Design Consultation",
                "quantity": "10", 
                "rate": "100.00"
            }
        ],
        "notes": "Payment due within 30 days. Thank you for your business!"
    }

@pytest.fixture
def minimal_invoice_data():
    """Provide minimal test data for basic testing"""
    return {
        "invoice_details": {
            "invoice_number": "MIN-001",
            "date": "2024-01-15",
            "due_date": "2024-02-15"
        },
        "from_info": {
            "name": "Test User"
        },
        "to_info": {
            "name": "Test Client"
        },
        "items": [
            {
                "description": "Test Service",
                "quantity": "1",
                "rate": "100.00"
            }
        ]
    }