import pandas as pd
import glob
from fpdf import FPDF
import re
import datetime
import os
#redo using pathlip and Path


def pdf_hdr_maker(filestring):
    pdf_title = f"{filestring.strip("invoices//")}"
    pdf_title = f"{pdf_title.strip(".xlsx")}"
    pdf_title = pdf_title.strip('\\')

    filenames = re.split(pattern='[-]' , string=pdf_title)
    pdf_title = f"Invoice Num. {filenames[0]}"
    return pdf_title


def pdf_date_hdr():
    date_header = str(datetime.datetime.now())
    date_header = (date_header.split(" "))[0]
    date_header = f"Date: {date_header}"
    return date_header


filenames = glob.glob("invoices/*.xlsx")

#This for loop iterates through the excel files that were located by glob
for i, filename in enumerate(filenames):

    #create the pdf object that we will add information from the excel file to
    invoice_pdf = FPDF(orientation='P', unit= 'mm', format='A4')
    invoice_pdf.add_page()

    #extract the strings that will be displayed in the PDF
    #will move to function pdf_hdr_maker
    pdf_header = pdf_hdr_maker(filename)
    date = pdf_date_hdr()

    #Create strings for the text that needs to be printed in the pdf
    invoice_pdf.set_font(family='Times', style='B', size=24)
    invoice_pdf.set_text_color(100,100,100)

    invoice_pdf.cell(w=50, h=12, txt=pdf_header, align='L', ln=1)
    invoice_pdf.cell(w=50, h=12, txt=date, align='L', ln=1)
    
    #make the table for the pdf invoice
    #first make the header
    # print(f"{invoices_df[:0]}")
    # invoice_headers = str(invoices_df.columns)
    # invoice_pdf.cell(w=0, h=12, txt=invoice_headers, align='L', ln=1)

    invoices_df = pd.read_excel(filename, sheet_name='Sheet 1')
    
    #using nested for loops to create header for invoice PDF and the table
    #values- high time complexity (n^3)

    #change Dataframe columns into list, then take values from list and output
    #to a pdf cell, to create a header for the table
    table_headlist = list(invoices_df.columns)
    for table_head in table_headlist:
        table_head = table_head.title()
        invoice_pdf.set_font(family="times", style="B", size=12)
        invoice_pdf.set_text_color(80, 80, 80)
        invoice_pdf.cell(w=40, h=12, txt=table_head, border=1)

    invoice_pdf.cell(w=50, h=12, txt=" ", align='L', ln=1)

    total = 0

    #create table entries for the invoice PDF. Using a nested for loop going 
    #through each row in the DataFrame and setting it to text of cell
    for index, row in invoices_df.iterrows():
        invoice_pdf.set_font(family="times", size=10)
        invoice_pdf.set_text_color(80, 80, 80)
        invoice_pdf.cell(w=40, h=12, txt=str(row["product_id"]), border=1)
        invoice_pdf.cell(w=40, h=12, txt=str(row["product_name"]), border=1)
        invoice_pdf.cell(w=40, h=12, txt=str(row["amount_purchased"]), border=1)
        invoice_pdf.cell(w=40, h=12, txt=str(row["price_per_unit"])+" CAD", border=1)
        invoice_pdf.cell(w=40, h=12, txt=str(row["total_price"])+" CAD", border=1, ln=1)

        total = total + float(row["total_price"])

    #Spaces before the final total
    invoice_pdf.cell(w=40, h=12, txt=" ", ln=1)
    invoice_pdf.cell(w=40, h=12, txt=" ", ln=1)
    invoice_pdf.cell(w=40, h=12, txt=" ", ln=1)

    #output final total to PDF
    invoice_pdf.set_font(family="times", style="B", size=14)
    invoice_pdf.set_text_color(80, 80, 80)
    invoice_pdf.cell(w=100, h=12, txt= f"The total due amount is: {total} CAD", align='L', ln=1)

    #add company name and logo
    invoice_pdf.cell(w=40, h=10, txt=" ", ln=1)
    invoice_pdf.cell(w=60, h=12, txt= f"Skyview Industrial Supply", align='L')

    if os.path.exists("logo/pythonhow.png"):
        print(os.path.exists("logo/pythonhow.png"))
        invoice_pdf.image("logo/pythonhow.png", w=20, h=20)

    if not os.path.exists("final_invoices/"):
        os.mkdir("final_invoices/")

    invoice_pdf.output(f"final_invoices/invoice{i+1}.pdf")


