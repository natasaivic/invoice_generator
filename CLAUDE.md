# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an invoice generator project - a lightweight web app for creating professional, printable invoices through a clean and intuitive interface.

## Technology Stack

- **Backend**: Python with Flask web framework
- **PDF Generation**: ReportLab and WeasyPrint for invoice PDF creation
- **Templating**: Jinja2 for HTML templates

## Setup Instructions

This project includes a pre-configured virtual environment in the `venv/` directory for immediate use:

1. **Activate the virtual environment**
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Run the application**
   ```bash
   python app.py
   ```

## Development Commands

- **Activate Environment**: `source venv/bin/activate`
- **Run Development Server**: `python app.py`
- **Run Tests**: `pytest tests/ -v`
- **Run Smoke Tests**: `pytest tests/ -m smoke -v`
- **Generate Test Report**: `pytest tests/ --html=reports/report.html`
- **Install New Dependencies**: `pip install <package> && pip freeze > requirements.txt`

## Configuration

The application uses a `.env` file for configuration:
- Flask settings (FLASK_APP, FLASK_ENV, FLASK_DEBUG)
- Server settings (HOST, PORT)
- Invoice defaults (DEFAULT_CURRENCY, INVOICE_NUMBER_PREFIX, TAX_RATE)
- Directory paths (UPLOAD_FOLDER, TEMP_FOLDER, etc.)

## Important Notes

- The `venv/` directory is included in version control to provide a ready-to-run environment
- The `.env` file contains default settings and should be customized for production use
- Remember to update the SECRET_KEY in `.env` for production deployments

## Architecture Overview

This is a complete Flask-based web application for generating professional invoices with PDF export capabilities.

### Application Structure

- **app.py**: Main Flask application with routes and PDF generation logic
- **templates/index.html**: Single-page application interface
- **static/css/style.css**: Professional responsive styling
- **static/js/script.js**: Frontend functionality for dynamic invoice creation

### Key Features Implemented

- Dynamic item management with real-time calculations
- Live invoice preview before PDF generation
- Professional PDF generation using ReportLab
- Responsive design for desktop and mobile
- Form validation and error handling
- Auto-generated invoice numbers and dates

### PDF Generation

The application uses ReportLab to create professional PDFs with:
- Company and client information sections
- Itemized billing table with calculations
- Professional formatting and layout
- Automatic total calculations

### Frontend Functionality

JavaScript handles:
- Dynamic addition/removal of invoice items
- Real-time total calculations
- Form validation
- Live preview generation
- PDF download via AJAX

### Testing

The project includes comprehensive Selenium-based end-to-end testing:

#### Test Structure
- **conftest.py**: Test fixtures with WebDriver setup and test data
- **test_invoice_generation.py**: Complete test suite with 8 test scenarios
- **pytest.ini**: Test configuration with HTML reporting

#### Running Tests
```bash
# All tests
pytest tests/ -v

# Specific categories
pytest tests/ -m ui -v          # UI tests
pytest tests/ -m smoke -v       # Smoke tests
pytest tests/ --html=reports/report.html  # With HTML report
```

#### Test Features
- **Browser**: Chrome in headed mode for development observation
- **Delays**: 3-second pauses between actions for enhanced visibility
- **Coverage**: Page loading, form filling, calculations, preview, PDF generation
- **Fixtures**: Consistent test data (`invoice_test_data`, `minimal_invoice_data`)
- **PDF Verification**: Downloads and validates actual PDF files

### Development Workflow

1. **Start Development Server**: `python app.py`
2. **Access Application**: http://127.0.0.1:5000
3. **Run Tests**: `pytest tests/ -v` for comprehensive validation
4. **Testing**: Fill out forms and generate test invoices
5. **Styling Changes**: Edit `static/css/style.css`
6. **Logic Changes**: Edit `app.py` for backend or `static/js/script.js` for frontend
7. **Test Changes**: Use `pytest tests/ -m smoke -v` for quick workflow validation