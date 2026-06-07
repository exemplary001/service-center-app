from openpyxl import Workbook


def generate_excel(customers):

    workbook = Workbook()

    worksheet = workbook.active

    worksheet.title = "Customer Report"

    headers = [
        "ID",
        "Customer Name",
        "Address",
        "Phone Number",
        "Call Date",
        "Total Calls",
        "Closed Calls",
        "Pending Calls"
    ]

    worksheet.append(headers)

    for customer in customers:

        worksheet.append([
            customer.id,
            customer.customer_name,
            customer.address,
            customer.phone_number,
            str(customer.call_date),
            customer.total_calls,
            customer.closed_calls,
            customer.total_calls - customer.closed_calls
        ])

    filename = "customer_report.xlsx"

    workbook.save(filename)

    return filename