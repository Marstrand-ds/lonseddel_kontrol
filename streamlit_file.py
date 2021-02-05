import streamlit as st
import time
import numpy as np
import pandas as pd
import pdfplumber

# Use pip install pipreqs.
# Write pipreqs in the terminal to create a requirements.txt file in the folder.
# Use pipreqs --force to overwrite existing requirements.txt

data_list = []

payslip = 'https://github.com/Marstrand-ds/streamlit_test/blob/main/Lonseddel_2017.08.2020-20.09.2020.PDF'
'Lønseddel 17.08.2020-20.09.2020'
'Lønseddel 20.07.2020-16.08.2020'
with pdfplumber.open(payslip) as pdf:
    first_page = pdf.pages[0]
    text = first_page.extract_text()

uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
if uploaded_file is not None:
    df = extract_data(uploaded_file)

for row in text.split('\n'):
    #print(row.strip())

    if '1100' in row:
        products_dict = {}
        text = row.split()[1]

        products_dict["Beskrivelse"] = text
        products_dict["Enheder"] = row.split()[-3]
        products_dict["Sats"] = row.split()[-2]
        products_dict["Beløb"] = row.split()[-1]

        data_list.append(products_dict)

    if '1104' in row:
        products_dict = {}
        text_1 = row.split()[1]
        text_2 = row.split()[2]
        text = text_1 + " " + text_2

        products_dict["Beskrivelse"] = text
        products_dict["Enheder"] = row.split()[-3]
        products_dict["Sats"] = row.split()[-2]
        products_dict["Beløb"] = row.split()[-1]

        data_list.append(products_dict)

    if '1330' in row:
        products_dict = {}

        text_1 = row.split()[1]
        text_2 = row.split()[2]
        text_3 = row.split()[3]
        text_4 = row.split()[4]
        text = text_1 + " " + text_2 + " " + text_3 + " " + text_4

        products_dict["Beskrivelse"] = text
        products_dict["Enheder"] = row.split()[-3]
        products_dict["Sats"] = row.split()[-2]
        products_dict["Beløb"]  = row.split()[-1]

        data_list.append(products_dict)

    if '3992' in row:
        products_dict = {}

        text_1 = row.split()[1]
        text_2 = row.split()[2]
        text_3 = row.split()[3]
        text_4 = row.split()[4]
        text_5 = row.split()[5]
        text = text_1 + " " + text_2 + " " + text_3 + " " + text_4 + " " + text_5

        products_dict["Beskrivelse"] = text
        products_dict["Enheder"] = row.split()[-3]
        products_dict["Sats"] = row.split()[-2]
        products_dict["Beløb"]  = row.split()[-1]

        data_list.append(products_dict)

    if 'Lønseddel for perioden' in row:
        products_dict = {}
        text_1 = row.split()
        #print(text_1)

        start_dato = [''.join(text_1[3:5])]
        slut_dato = [''.join(text_1[6:8])]
        year_dato = [''.join(text_1[8:])]

        print(start_dato)
        print(slut_dato)
        print(year_dato)

st.title('My first app TEST')

st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame(data_list))

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)
chart = st.line_chart(last_rows)

for i in range(1, 101):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    status_text.text("%i%% Complete" % i)
    chart.add_rows(new_rows)
    progress_bar.progress(i)
    last_rows = new_rows
    time.sleep(0.05)

progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")