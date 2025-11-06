import pandas as pd
# import xlwings as xw - if with windows
import openpyxl #with ubuntu
from openpyxl.utils.dataframe import dataframe_to_rows
import os
import sys
import functools as ft
from datetime import date
from pathlib import Path

#Path settings
if '__file__' in locals():
    current_dir = Path(__file__).parent
else:
    current_dir = Path.cwd()

#open ba_charges template
input_dir = current_dir/"INPUT"
output_dir = current_dir/"OUTPUT"
excel_template = str(input_dir) + '/BA_CHARGES_TEMPLATE.xlsx'

# Load the Excel workbook
workbook = pd.ExcelFile('Analytique_Asso.xlsx')

today = date.today()
year = today.year
#print(year)

#Creating the 3 first column
str1 = "BALANCE RECAPITULATIVE SELON NOUVEAU PLAN COMPTABLE ANALYTIQUE"
str2 = f'Exercice : {year}'
str3 = today.strftime('%d/%m/%Y')

#print(str3)

# Feuil4: Read in the sheets you want to merge
df1 = pd.read_excel(workbook, sheet_name="Feuil4", skiprows=[0,1,2,3])
# Feuil6: Read in the sheets you want to merge
df2 = pd.read_excel(workbook, sheet_name="Feuil6", skiprows=[0,1,2,3])

#split df1
df11 = df1.iloc[:1]
df12 = df1.iloc[3:14]
cni_df12 = df12.loc[df12['LIBELLE'] == 'Charges non incorporables']
ci_df12 = df12[df12['LIBELLE'] != 'Charges non incorporables']
header = df1.columns


#create sum for each splitted dataframe
NRP = df11['SOLDE'].sum()
RCMOD = ci_df12['SOLDE'].sum() 

#split df2
df21 = df2.iloc[:2]
df22 = df2.iloc[2:5]
df23 = df2.iloc[5:8]
df24 = df2.iloc[8:10]
df28 = df2.iloc[10:13]
df25 = df2.iloc[13:15]
df26 = df2.iloc[15:18]
df27 = df2.iloc[18:21]

#create sum for each splitted dataframe
RPCO = df21['SOLDE'].sum()
RPGF = df22['SOLDE'].sum()
RPME = df23['SOLDE'].sum()
RPMH = df24['SOLDE'].sum()
RPGOT= df25['SOLDE'].sum()
RPPA = df26['SOLDE'].sum()
RPSIPSE = df27['SOLDE'].sum()
RPMT = df28['SOLDE'].sum()

#insert data in dataframe for sub-sum
CINRP_id = '9A15IGE101000'
CINRP_label = 'CI - NRP'
CDRCMOD_id = '9D'
CDRCMOD_label = 'CD - RCMOD'
CIRPCO_label = 'CI - RP CO'
CIRPGF_label = 'CI - RP-GF'
CIRPME_label = 'CI - RPME'
CIRPMT_label = 'CI - RP-MT'
CIRPGOT_label = 'CI - RP-GOT'
CIRPPA_label = 'CI - RP-PA'
CIRPSISPE_label = 'CI - RP-SISPE'
CIRPMH_label = 'CI - RP-MH'
CIRQE_label = 'CI - RQE'

# Define a list of dictionaries containing row data for each DataFrame
rows = [
    {'COMPTE': CINRP_id, 'LIBELLE': CINRP_label , 'SOLDE': NRP},
    {'COMPTE': CDRCMOD_id, 'LIBELLE': CDRCMOD_label , 'SOLDE': RCMOD},
    {'LIBELLE': CIRPCO_label , 'SOLDE': RPCO},
    {'LIBELLE': CIRPGF_label , 'SOLDE': RPGF},
    {'LIBELLE': CIRPME_label , 'SOLDE': RPME},
    {'LIBELLE': CIRPMT_label , 'SOLDE': RPMT},
    {'LIBELLE': CIRPGOT_label , 'SOLDE': RPGOT},
    {'LIBELLE': CIRPPA_label , 'SOLDE': RPPA},
    {'LIBELLE': CIRPSISPE_label , 'SOLDE': RPSIPSE},
    {'LIBELLE': CIRPMH_label , 'SOLDE': RPMH},
    {'LIBELLE': CIRQE_label}
]

# Define a list of DataFrame names
df_names = ['nrp_df', 'cmod_df', 'CIRPCO_df', 'CIRPGF_df', 'CIRPME_df',
            'CIRPMT_df', 'CIRPGOT_df', 'CIRPPA_df', 'CIRPSISPE_df', 'CIRPMH_df', 'CIRQE_df']

# Iterate over the rows and create a DataFrame for each
for i, row in enumerate(rows):
    df = pd.DataFrame(columns=['COMPTE', 'LIBELLE', 'DEBIT', 'CREDIT', 'SOLDE'])
    df.loc[len(df)] = row
    globals()[df_names[i]] = df

results = pd.concat([df11, nrp_df,
                     ci_df12,
                     cmod_df,cni_df12,
                     CIRPCO_df,df21,
                     CIRPGF_df,df22,
                     CIRPME_df,df23,
                     CIRPMT_df,df28,
                     CIRPGOT_df,df25,
                     CIRPPA_df,df26,
                     CIRPSISPE_df,df27,
                     CIRPMH_df,df24,
                     CIRQE_df
                    ], ignore_index=True)
#print(results)


# Open the Excel file
workbook = openpyxl.load_workbook(excel_template)
worksheet = workbook['Balance_details']

# Write data to the worksheet
worksheet['A1'] = str1
worksheet['A2'] = str2
worksheet['E2'] = str3

# Write the dataframe to the worksheet
for r_idx, row in enumerate(dataframe_to_rows(results, index=False, header=True)):
    for c_idx, value in enumerate(row):
        worksheet.cell(row=4+r_idx, column=1+c_idx, value=value)

# Save the changes to the Excel file
workbook.save(output_dir/'BA_Charges.xlsx')