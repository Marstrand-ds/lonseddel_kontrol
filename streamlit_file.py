import streamlit as st
import numpy as np
import pandas as pd
import pdfplumber

# Use pip install pipreqs.
# Write pipreqs in the terminal to create a requirements.txt file in the folder.
# Use pipreqs --force to overwrite existing requirements.txt

# Markdown emoji's: https://raw.githubusercontent.com/omnidan/node-emoji/master/lib/emoji.json

st.title('Kontrol af lønseddel')

my_slot1 = st.empty()

def extract_data_lonseddel(feed):
    data_list = []
    with pdfplumber.load(feed) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()

        for row in text.split('\n'):
            #st.write(row)
            if '1100' in row:
                global timer
                products_dict = {}
                text = row.split()[1]

                products_dict["Beskrivelse"] = text
                products_dict["Enheder"] = row.split()[-3]
                timer = row.split()[-3]
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
                products_dict["Beløb"] = row.split()[-1]

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
                products_dict["Beløb"] = row.split()[-1]

                data_list.append(products_dict)


            if 'Overført til reg./konto' in row:
                global udbetaling
                if '8100' in row:
                    timer = row.split()[-2]

                products_dict = {}

                text_1 = row.split()[0]
                text_2 = row.split()[1]
                text_3 = row.split()[2]
                text = text_1 + " " + text_2 + " " + text_3

                products_dict["Beskrivelse"] = text
                products_dict["Enheder"] = timer
                products_dict["Sats"] = " "
                udbetaling = row.split()[-1]
                products_dict["Beløb"] = udbetaling

                data_list.append(products_dict)

            if 'Lønseddel for perioden' in row:
                text_1 = row.split()
                #print(text_1)

                global start_dato, slut_dato,year_dato
                start_dato = str([' '.join(text_1[3:5])])[2:-2]
                slut_dato = str([' '.join(text_1[-3:-1])])[2:-2]
                year_dato = str([''.join(text_1[-1:])])[2:-2]

    return data_list  # build more code to return a dataframe


def extract_data_geofency(feed):

    data = pd.read_csv(feed,sep=";")

    data_list = data.loc[:, ['Location', 'EntryDate', 'EntryTime', 'ExitTime', 'Hours']]

    global total_hours
    total_hours = 0.00
    for row in data.itertuples():
        total_hours = float(total_hours)+ float(row[7].replace(',','.'))

    #data_list.loc['Total',:] = round(total_hours,2)

    return data_list

# File picker for lønseddel
uploaded_file_pdf = st.sidebar.file_uploader('Vælg din lønseddel.pdf', type="pdf")
if uploaded_file_pdf is not None:
    df_lonseddel = extract_data_lonseddel(uploaded_file_pdf)
    df_lonseddel = pd.DataFrame(df_lonseddel)

    st.header("Data fra lønseddel")
    st.table(df_lonseddel.assign(hack='').set_index('hack'))
else:
    #https://docs.streamlit.io/en/stable/api.html
    st.markdown(':arrow_left: ' + '**Vælg din lønseddel.**')

# File picker for geofency data
uploaded_file_csv = st.sidebar.file_uploader('Vælg din geofency.csv', type="csv", )
if uploaded_file_csv is not None:
    df_geofency = extract_data_geofency(uploaded_file_csv)
    geofency = pd.DataFrame(df_geofency)

    st.header("Data fra Geofency")
    st.table(geofency.assign(hack='').set_index('hack'))

    #option = st.sidebar.selectbox(
    #    'Which number do you like best?',
    #    pd.DataFrame(df_geofency)['EntryDate'])
    #
    #'You selected:', option
else:
    #https://docs.streamlit.io/en/stable/api.html
    st.markdown(':arrow_left: ' + '**Indsæt din Geofency data.**')

if uploaded_file_csv and uploaded_file_pdf is not None:
    timer = timer.replace(",",".")
    timer = float(timer)
    my_slot1.write(f":calendar: Lønperioden: {start_dato} til {slut_dato} ({year_dato})  "
                   f"\n:clock3: Der udbetales løn for **{timer}** og **{round(total_hours,2)}** er registreret i Geofency.  "
                   f"\n:moneybag: Udbetaling på {udbetaling} kr.")

st.sidebar.button("Re-run")


