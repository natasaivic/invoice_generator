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

This will be a Flask-based web application for generating professional invoices with PDF export capabilities using ReportLab and WeasyPrint libraries.