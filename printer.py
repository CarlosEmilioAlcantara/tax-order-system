import jinja2
import pdfkit

last_name = "Doe"
date = "7/07/77"
first_name = "John"
middle_name = "Jones"
address = "Somewhere"
profession = "Doctor"
type_of_payment = "New"
amount = "Php 100.00"
receipt_no = "1010101"
penalty = "Php 50.00"

context = {'last_name': last_name, 'date': date, 'first_name': first_name,
           'middle_name': middle_name, 'address': address, 
           'profession': profession, 'type_of_payment': type_of_payment,
           'amount': amount, 'receipt_no': receipt_no, 'penalty': penalty}

template_loader = jinja2.FileSystemLoader('./')
template_env = jinja2.Environment(loader=template_loader)

template = template_env.get_template("tax_order_receipt.html")
output_text = template.render(context)

config = pdfkit.configuration(wkhtmltopdf='D:/apps2/wkhtmltopdf/bin/wkhtmltopdf.exe')
pdfkit.from_string(output_text, 'generated.pdf', configuration=config)