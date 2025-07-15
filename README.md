# Invoice Generator

Invoice Generator is a lightweight web app that lets you create professional, printable invoices in minutes through a clean and intuitive interface.

## Features

- **Clean Web Interface**: Modern, responsive design that works on desktop and mobile
- **Professional PDF Generation**: Creates high-quality PDF invoices using ReportLab
- **Dynamic Item Management**: Add/remove invoice items with real-time calculations
- **Live Preview**: See how your invoice will look before generating the PDF
- **Auto-generated Invoice Numbers**: Automatic invoice numbering with customizable prefixes
- **Client Management**: Store and manage client information
- **Form Validation**: Built-in validation to ensure data accuracy
- **Responsive Design**: Works seamlessly on all device sizes

## Quick Start

This project includes a pre-configured virtual environment for immediate use:

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd invoice_generator
   ```

2. **Activate the virtual environment**
   ```bash
   source venv/bin/activate
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   Open your browser and go to `http://127.0.0.1:5000`

## How to Use

1. **Fill out your business information** in the "From" section
2. **Add client details** in the "To" section
3. **Add invoice items** with descriptions, quantities, and rates
4. **Preview your invoice** using the Preview button
5. **Generate PDF** to download your professional invoice

The application automatically calculates totals and formats everything professionally.

## Technology Stack

- **Backend**: Python Flask web framework
- **PDF Generation**: ReportLab for high-quality PDF creation
- **Templates**: Jinja2 for dynamic HTML rendering
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Styling**: Custom CSS with responsive design
- **Configuration**: Python-dotenv for environment management

## Configuration

The application uses environment variables defined in `.env`:
- **Flask Settings**: FLASK_APP, FLASK_ENV, FLASK_DEBUG, HOST, PORT
- **Security**: SECRET_KEY for session management
- **Invoice Defaults**: DEFAULT_CURRENCY, INVOICE_NUMBER_PREFIX, TAX_RATE
- **File Paths**: UPLOAD_FOLDER, TEMP_FOLDER, STATIC_FOLDER, TEMPLATE_FOLDER

## Project Structure

```
invoice_generator/
├── app.py                    # Main Flask application
├── venv/                     # Pre-configured virtual environment
├── requirements.txt          # Python dependencies
├── .env                     # Environment configuration
├── .gitignore              # Git ignore rules
├── pytest.ini              # Test configuration
├── templates/
│   └── index.html          # Main application template
├── static/
│   ├── css/
│   │   └── style.css       # Application styling
│   └── js/
│       └── script.js       # Frontend functionality
├── tests/
│   ├── conftest.py         # Test fixtures and configuration
│   ├── test_invoice_generation.py  # Comprehensive test suite
│   └── README.md           # Testing documentation
├── reports/                 # Test reports directory
├── README.md               # This file
└── CLAUDE.md              # Development guidance
```

## Testing

The project includes a comprehensive Selenium-based test suite with pytest:

### Running Tests

```bash
# Activate environment
source venv/bin/activate

# Run all tests
pytest tests/ -v

# Run specific test categories
pytest tests/ -m ui -v          # UI tests only
pytest tests/ -m smoke -v       # Smoke tests only

# Generate HTML test report
pytest tests/ --html=reports/report.html --self-contained-html
```

### Test Coverage

- **Page Loading & Validation**: Ensures all UI elements exist and function
- **Form Filling**: Tests complete invoice form workflow
- **Real-time Calculations**: Verifies dynamic total calculations
- **Preview Functionality**: Tests live invoice preview
- **PDF Generation**: Validates PDF creation and download
- **End-to-End Workflow**: Complete smoke test from form to PDF

### Test Features

- **Headed Mode**: Visual test execution for development observation
- **3-Second Delays**: Enhanced observability between key actions
- **Consistent Fixtures**: Reliable test data for repeatable results
- **Download Verification**: Actual PDF file creation validation
- **CI-Ready**: Designed for future headless/CI environments

## Dependencies

Key dependencies include:

### Application
- **Flask**: Web framework
- **ReportLab**: PDF generation
- **WeasyPrint**: Alternative PDF generation
- **python-dotenv**: Environment variable management
- **Jinja2**: Template engine (included with Flask)

### Testing
- **Selenium**: Browser automation for UI testing
- **pytest**: Test framework and runner
- **pytest-html**: HTML test reporting
- **webdriver-manager**: Automatic WebDriver management
