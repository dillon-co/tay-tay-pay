import pandas as pd
import xlrd
import re
import pdftables_api
import os
import PySimpleGUI as sg

converter = pdftables_api.Client('yxej3gzmkomh')
# converter.xlsx('Invoice.pdf', 'invoice.xlsx')
# data = pd.read_excel('invoice.xlsx', header=2)
def convert_file(file_path):
    converter.xlsx(file_path, 'invoice.xlsx')
    data = pd.read_excel('invoice.xlsx', header=2)
    df = pd.DataFrame(data)
    df.fillna(0, inplace=True)
    return df

def get_amounts_paid_to_girls(df):
    girls = {}
    for _, row in df.iterrows():
        if row['Unnamed: 0'] != 0:
            a = row["Unnamed: 0"].split(' ')
            b = row["2607 Stacy Ln"]
            if '$35/hr,' in a:
                name_and_description = a[a.index('|') - 1]
                name = name_and_description.split("\n")[-1]
                
                amount = float(b.split("$")[-1]) if type(b) == str else b
                if name not in girls:
                    girls[name] = amount 
                else: 
                    girls[name] += amount
    os.remove("invoice.xlsx")
    return girls

def reformat_girls(girls):
    full_str = ""
    for key in girls.keys():
        full_str += f"{key}: {girls[key]}\n"
    return full_str
# os.remove("Invoice.pdf") 
# print(girls)
layout = [[sg.Text("Hey cutie, select the invoice you want to use" ), sg.FileBrowse(key="-IN-")], [sg.Button("Submit")], [sg.Text("", key="-OUTPUT-")]]
window = sg.Window('Damn you fine', layout, size=(800, 500))

while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event == "Submit":
        window["-OUTPUT-"].update("Processing...")    
        if values["-IN-"].lower().endswith(".pdf") == False:
            sg.popup("Please select a PDF file")
        df = convert_file(values["-IN-"])
        girls = get_amounts_paid_to_girls(df)
        # sg.popup(girls)
        window["-OUTPUT-"].update(reformat_girls(girls))
        # print(girls)
        # print(values["-IN-"])


# df = convert_file("Invoice 0000029.pdf")
# girls = get_amounts_paid_to_girls(df)
# print(girls)