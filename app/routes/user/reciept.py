from app import app
from flask import render_template, send_file
from datetime import datetime
import os
import pdfkit

# Set the UPLOAD_FOLDER to the desired path
app.config['UPLOAD_FOLDER'] = r'C:\Users\Lawal Adam Gangara\Downloads'

# Define the path to the wkhtmltopdf executable
wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

# Create a configuration object for pdfkit
config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

@app.route('/download_reciept/<filename>')
def download_receipt(filename):
    # Provide the receipt file for downloading
    return send_file(filename, as_attachment=True)

@app.route('/success/<filename>')
def payment(filename):
    return render_template('user/payment.html', filename=filename)

@app.route('/success/<filename>/download')
def download_success_receipt(filename):
    # Provide the receipt for downloading
    return send_file(filename, as_attachment=True)

def generate_receipt(receipt_data):
    # Define the path to the HTML template
    html_template_path = "app/templates/user/receipt_template.html"

    # Read HTML content from the separate file
    with open(html_template_path, "r") as file:
        receipt_content = file.read()

        # Format the HTML content with receipt data
        receipt_content = receipt_content.format(**receipt_data)

        # Generate a unique filename for the receipt using timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f'receipt_{timestamp}.pdf'

        # Generate PDF directly from HTML string
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        pdfkit.from_string(receipt_content, pdf_path, configuration=config)

        return pdf_path
