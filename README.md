# Invoice Generator

Invoice Generator is a lightweight web app that lets you create professional, printable invoices in minutes through a clean and intuitive interface.

## Features

- Clean and intuitive web interface
- Professional PDF invoice generation
- Customizable invoice templates
- Support for multiple currencies
- Auto-generated invoice numbering

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

## Technology Stack

- **Backend**: Python Flask
- **PDF Generation**: ReportLab and WeasyPrint
- **Templates**: Jinja2
- **Frontend**: HTML/CSS/JavaScript

## Configuration

The application uses environment variables defined in `.env`:
- Flask settings (debug mode, host, port)
- Invoice defaults (currency, numbering prefix, tax rate)
- File path configurations

## Project Structure

```
invoice_generator/
├── venv/                 # Pre-configured virtual environment
├── requirements.txt      # Python dependencies
├── .env                 # Environment configuration
├── .gitignore          # Git ignore rules
├── README.md           # This file
└── CLAUDE.md          # Development guidance
```
