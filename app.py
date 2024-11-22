import csv
from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flashing messages
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def process_csv(file_path):
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)

            # Initialize the sums
            gst_free_total = 0.0
            gst_applicable_total = 0.0
            total_gst = 0.0
            gst_free_details = []
            gst_applicable_details = []

            # Extract the first row and iterate over all rows
            first_row = None
            for index, row in enumerate(csv_reader):
                if index == 0:
                    first_row = row

                try:
                    expense_total_without_tax = float(row.get("Expense Total Without Tax", 0))
                    expense_tax_amount = float(row.get("Expense Tax Amount", 0))
                    expense_amount = float(row.get("Expense Amount (in Reimbursement Currency)", 0))

                    total_gst += expense_tax_amount

                    if row.get("Item Exemption Code") == "GST FREE":
                        gst_free_total += expense_amount
                        gst_free_details = [
                            f"{row.get('Report Number', 'N/A')} - {row.get('Employee Name', 'N/A')} - Expenses - GST Free"
                        ]
                    else:
                        gst_applicable_total += expense_total_without_tax
                        gst_applicable_details.append(
                            f"{row.get('Report Number', 'N/A')} - {row.get('Employee Name', 'N/A')} - Expenses - GST Applicable, {gst_applicable_total:.2f}"
                        )
                except ValueError:
                    continue

            if first_row:
                result = {
                    'employee_name': first_row.get("Employee Name", "N/A"),
                    'customer_name': first_row.get("Customer Name", "N/A"),
                    'project_name': first_row.get("Project Name", "N/A"),
                    'project_code': first_row.get("Project Code", "N/A"),
                    'reimbursable_total': first_row.get("Reimbursable Total", "N/A"),
                    'report_number': first_row.get("Report Number", "N/A"),
                    'gst_free_total': f"{gst_free_total:.2f}",
                    'gst_applicable_total': f"{gst_applicable_total:.2f}",
                    'total_gst': f"{total_gst:.2f}",
                    'gst_free_details': gst_free_details,
                    'gst_applicable_details': gst_applicable_details
                }
                return result
            else:
                return None
    except Exception as e:
        raise Exception(f"Error processing CSV: {str(e)}")

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return render_template('upload.html')
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return render_template('upload.html')

        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                result = process_csv(filepath)
                os.remove(filepath)  # Clean up the uploaded file
                
                if result:
                    return render_template('upload.html', result=result)
                else:
                    flash('The CSV file appears to be empty or invalid')
                    return render_template('upload.html')
            except Exception as e:
                flash(f'Error processing file: {str(e)}')
                return render_template('upload.html')
        else:
            flash('Please upload a CSV file')
            return render_template('upload.html')

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)