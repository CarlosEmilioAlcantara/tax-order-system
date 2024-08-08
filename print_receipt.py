from fpdf import FPDF

import sys
import os
sys.path.append(os.path.join(sys.path[0]))

from create_directories import create_directory

def create_pdf():
    pdf = FPDF("P", "mm", "A5")
    pdf.add_page()

    return pdf

def create_header(pdf):
    pdf.set_font('Times', '', 8)
    pdf.cell(40, 10, '', align='C')
    pdf.cell(40, 10, 'REPUBLIKA NG PILIPINAS', align='C')
    pdf.ln(4)
    pdf.set_font('Times', 'B', 10)
    pdf.cell(40, 10, '', align='C')
    pdf.cell(40, 10, 'LUNSOD NG SAN PABLO', align='C')
    pdf.ln(4)
    pdf.set_font('Times', '', 8)
    pdf.cell(40, 10, '', align='C')
    pdf.cell(40, 10, 'Tanggapan ng Ingat-Yaman', align='C')
    pdf.ln(4)
    pdf.set_font('Times', '', 8)
    pdf.cell(40, 10, '', align='C')
    pdf.cell(40, 10, 'Business Tax Division', align='C')

def create_body_top(pdf, last_name, date, first_name, middle_name):
    pdf.ln(15)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 10, '', align='C')
    pdf.cell(40, 10, 'TAX ORDER', align='C')
    pdf.ln(10)
    pdf.set_font('Arial', '', 10)
    pdf.cell(40, 10, f'SURNAME: {last_name}')
    pdf.cell(40, 10, f'DATE: {date}', 0, 0, align="R")
    pdf.ln(5)
    pdf.cell(40, 10, f'GIVEN NAME: {first_name}')
    pdf.ln(5)
    pdf.cell(40, 10, f'MIDDLE NAME: {middle_name}')

def create_body_bottom(pdf, address, profession, license_no, type_of_payment,
                       amount, penalty, receipt_no, verified_by):
    pdf.ln(15)
    pdf.set_font('Arial', '', 10)
    pdf.cell(40, 10, f'ADDRESS: {address}')
    pdf.ln(5)
    pdf.cell(40, 10, f'PROFESSION: {profession}')
    pdf.ln(5)
    pdf.cell(40, 10, f'LICENSE NO: {license_no}')

    pdf.ln(15)
    pdf.set_font('Arial', '', 10)
    pdf.cell(40, 10, f'STATUS: {type_of_payment}')
    pdf.ln(5)
    pdf.cell(40, 10, f'AMOUNT: {amount}')
    pdf.cell(40, 10, f'OR NO: {receipt_no}', 0, 0, align="R")
    pdf.ln(5)
    pdf.cell(40, 10, f'PENALTY: {penalty}')
    pdf.cell(40, 10, f'VERIFIED BY: {verified_by}', 0, 0, align="R")

def print_receipt(professional_record, receipt_record):
    pdf = create_pdf()
    create_header(pdf)

    last_name = professional_record[0][1]
    first_name = professional_record[0][2]
    middle_name = professional_record[0][3]
    date = receipt_record[0][3]

    create_body_top(pdf, last_name, date, first_name, middle_name)

    address = professional_record[0][4]
    profession = professional_record[0][5]
    license_no = professional_record[0][0]

    type_of_payment = receipt_record[0][2]
    amount = receipt_record[0][4]
    penalty = receipt_record[0][5]
    receipt_no = receipt_record[0][1]
    verified_by = receipt_record[0][7]

    create_body_bottom(pdf, address, profession, license_no, type_of_payment, amount, 
                    penalty, receipt_no, verified_by)

    create_directory(license_no, last_name)
    directory = f'./receipts/{license_no}_{last_name}/'

    pdf.output(f"{directory}{license_no}_{last_name}_{receipt_no}.pdf", "F")