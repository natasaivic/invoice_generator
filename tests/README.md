# Invoice Generator Tests

This directory contains Selenium-based end-to-end tests for the Invoice Generator application.

## Test Structure

- `conftest.py`: Test fixtures and configuration
- `test_invoice_generation.py`: Main test suite with comprehensive coverage

## Test Categories

### UI Tests (`@pytest.mark.ui`)
- **Page Loading**: Verify application loads correctly
- **Form Fields**: Check all required fields exist
- **Form Filling**: Test complete form filling workflow
- **Real-time Calculations**: Verify dynamic calculations work
- **Preview Functionality**: Test invoice preview feature
- **PDF Generation**: Test PDF creation and download

### Smoke Tests (`@pytest.mark.smoke`)
- **Complete Workflow**: End-to-end test of entire invoice generation process

## Running Tests

### All Tests
```bash
source venv/bin/activate
pytest tests/ -v
```

### Specific Test Categories
```bash
# UI tests only
pytest tests/ -m ui -v

# Smoke tests only
pytest tests/ -m smoke -v

# Exclude UI tests (for CI/headless)
pytest tests/ -m "not ui" -v
```

### Generate HTML Report
```bash
pytest tests/ --html=reports/report.html --self-contained-html
```

## Test Configuration

- **Browser**: Chrome (headed mode for development)
- **Test Port**: 5001 (to avoid conflicts with development server)
- **Download Testing**: Uses temporary directories
- **Test Data**: Consistent fixtures for reliable testing

## CI/CD Considerations

Tests are designed to be CI-friendly:
- WebDriver manager handles driver installation automatically
- Configurable for headless mode
- Temporary download directories for isolation
- Comprehensive test data fixtures

## Test Data

Tests use two main fixture sets:
- `invoice_test_data`: Complete invoice data for full workflow testing
- `minimal_invoice_data`: Minimal required data for basic functionality testing