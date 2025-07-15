import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from dotenv import load_dotenv
import tempfile

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    try:
        # Get form data
        data = request.get_json()
        
        # Create temporary PDF file
        temp_dir = tempfile.mkdtemp()
        pdf_path = os.path.join(temp_dir, f"invoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
        
        # Generate PDF
        create_pdf_invoice(data, pdf_path)
        
        return send_file(pdf_path, as_attachment=True, download_name=f"invoice_{data.get('invoice_number', 'unknown')}.pdf")
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def create_pdf_invoice(data, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Header
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "INVOICE")
    
    # Company info (from)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 100, "FROM:")
    c.setFont("Helvetica", 10)
    y_pos = height - 120
    
    from_info = [
        data.get('from_name', ''),
        data.get('from_company', ''),
        data.get('from_address', ''),
        data.get('from_city', ''),
        data.get('from_email', ''),
        data.get('from_phone', '')
    ]
    
    for line in from_info:
        if line:
            c.drawString(50, y_pos, line)
            y_pos -= 15
    
    # Client info (to)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(350, height - 100, "TO:")
    c.setFont("Helvetica", 10)
    y_pos = height - 120
    
    to_info = [
        data.get('to_name', ''),
        data.get('to_company', ''),
        data.get('to_address', ''),
        data.get('to_city', ''),
        data.get('to_email', '')
    ]
    
    for line in to_info:
        if line:
            c.drawString(350, y_pos, line)
            y_pos -= 15
    
    # Invoice details
    c.setFont("Helvetica-Bold", 10)
    c.drawString(350, height - 250, f"Invoice #: {data.get('invoice_number', '')}")
    c.drawString(350, height - 270, f"Date: {data.get('date', '')}")
    c.drawString(350, height - 290, f"Due Date: {data.get('due_date', '')}")
    
    # Items table
    y_pos = height - 350
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y_pos, "Description")
    c.drawString(300, y_pos, "Quantity")
    c.drawString(380, y_pos, "Rate")
    c.drawString(450, y_pos, "Amount")
    
    # Draw line under headers
    y_pos -= 5
    c.line(50, y_pos, 500, y_pos)
    
    # Items
    c.setFont("Helvetica", 9)
    y_pos -= 20
    total = 0
    
    items = data.get('items', [])
    for item in items:
        description = item.get('description', '')
        quantity = float(item.get('quantity', 0))
        rate = float(item.get('rate', 0))
        amount = quantity * rate
        total += amount
        
        c.drawString(50, y_pos, description)
        c.drawString(300, y_pos, str(quantity))
        c.drawString(380, y_pos, f"${rate:.2f}")
        c.drawString(450, y_pos, f"${amount:.2f}")
        y_pos -= 20
    
    # Total
    y_pos -= 20
    c.line(400, y_pos, 500, y_pos)
    y_pos -= 15
    c.setFont("Helvetica-Bold", 12)
    c.drawString(400, y_pos, f"Total: ${total:.2f}")
    
    # Notes
    if data.get('notes'):
        y_pos -= 50
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y_pos, "Notes:")
        c.setFont("Helvetica", 9)
        y_pos -= 15
        c.drawString(50, y_pos, data.get('notes', ''))
    
    c.save()

if __name__ == '__main__':
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)