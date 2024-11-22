import csv

# Specify the path to your CSV file
file_path = "report.csv"

# Open and read the CSV file
try:
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)  # Read as a dictionary

        # Initialize the sums for GST Free, GST Applicable, and Total GST
        gst_free_total = 0.0
        gst_applicable_total = 0.0
        total_gst = 0.0
        gst_free_details = []  # Store details for GST Free
        gst_applicable_details = []  # Store details for GST Applicable

        # Extract the first row and iterate over all rows
        first_row = None
        for index, row in enumerate(csv_reader):
            # Save the first row
            if index == 0:
                first_row = row

            # Check the "Item Exemption Code" and update totals
            try:
                expense_total_without_tax = float(row.get("Expense Total Without Tax", 0))
                expense_tax_amount = float(row.get("Expense Tax Amount", 0))
                expense_amount = float(row.get("Expense Amount (in Reimbursement Currency)", 0))

                # Sum GST amounts
                total_gst += expense_tax_amount

                # Classify as GST Free or GST Applicable
                if row.get("Item Exemption Code") == "GST FREE":
                    gst_free_total += expense_amount
                    gst_free_details.append(
                        f"{row.get('Report Number', 'N/A')} - {row.get('Employee Name', 'N/A')} - Expenses - GST Free, {gst_free_total:.2f}"
                    )
                else:
                    gst_applicable_total += expense_total_without_tax
                    gst_applicable_details.append(
                        f"{row.get('Report Number', 'N/A')} - {row.get('Employee Name', 'N/A')} - Expenses - GST Applicable, {gst_applicable_total:.2f}"
                    )
            except ValueError:
                continue

        if first_row:
            # Extract and print the first value of each specified column
            employee_name = first_row.get("Employee Name", "N/A")
            customer_name = first_row.get("Customer Name", "N/A")
            project_name = first_row.get("Project Name", "N/A")
            project_code = first_row.get("Project Code", "N/A")
            reimbursable_total = first_row.get("Reimbursable Total", "N/A")
            report_number = first_row.get("Report Number", "N/A")

            print(f"Employee Name: {employee_name}")
            print(f"Customer Name: {customer_name}")
            print(f"Project Name: {project_name}")
            print(f"Project Code: {project_code}")
            print(f"Reimbursable Total: {reimbursable_total}")
            print(f"Report Number: {report_number}")
            print(f"Total Amount GST Free: {gst_free_total:.2f}")
            print(f"Total Amount GST Applicable: {gst_applicable_total:.2f}")
            print(f"Total GST: {total_gst:.2f}")
            print("")
            print(f"Project Code: {project_code}")
            print(f"{report_number} - {employee_name} - Expenses GST Free {gst_free_total}")
            print(f"{report_number} - {employee_name} - Expenses GST Applicable {gst_applicable_total}")

            
        
        else:
            print("The file is empty or missing headers.")
except FileNotFoundError:
    print(f"File not found: {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")