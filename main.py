import os
import pandas as pd
import glob
from fpdf import FPDF

filenames = glob.glob("invoices/*.xlsx")

for filename in filenames:
    invoices_df = pd.read_excel(filename, sheet_name='Sheet 1')

