"""
clean_data.py
Author: Joseph Cho, ujcho@jacksongov.org
Purpose: Clean and filters raw data file for latest referrals, exporting an output .csv to overwrite STRIVIN' data feature layer
"""

import pandas as pd 
from datetime import datetime
from pathlib import Path

'''from arcgis.gis import GIS
from arcgis import features
from arcgis.features import FeatureLayerCollection'''

# Get current date
current_date = datetime.now().date()
print(current_date)

# Initialize dtype dict 

col_types = {
    'FirstInit': str, 
    'LastShort': str, 
    'Age': 'Int64', 
    'AgeRange': str, 
    'ReferralDate': str, 
    'ReferralYear': 'Int64', 
    'ReferralMonth': 'Int64', 
    'State': str, 
    'City': str, 
    'Zip': 'Int64', 
    'Gender': str, 
    'RaceEthnicity': str, 
    'Hispanic': 'Int64', 
    'AgencyName': str,
    'ReferralStatus': str, 
    'PersonID': 'Int64', 
    'AssessmentID': 'Int64', 
    'IncidentDate': str, 
    'Severity': str, 
    'ReferringOrg': str, 
    'RefPerson': str, 
    'ServiceNum': str, 
    'Income': 'Int64', # Social Service needs (determinants of health)
    'Employment': 'Int64', 
    'Food': 'Int64', 
    'HouseholdItems': 'Int64',
    'Education': 'Int64', 
    'SocialRelation': 'Int64', 
    'Transportation': 'Int64', 
    'Housing': 'Int64', 
    'UtilityAssistance': 'Int64', 
    'MentalHealth': 'Int64', 
    'Childcare': 'Int64', 
    'Parenting': 'Int64', 
    'SubstanceUse': 'Int64', 
    'Legal': 'Int64', 
    'Reentry': 'Int64', 
    'Trauma': 'Int64',
    'Community': 'Int64', 
    'Clothing': 'Int64', 
    'HealthInsurance': 'Int64', 
    'Healthcare': 'Int64', # end
    'ReferralType': str, 
    'LastUpdate': str, 
    'Receptive': str
}

# Initialize paths 
raw_data_path = Path("DATA/RAW")
export_path = Path("DATA/CLEANED")

# Find most recent datafile
datafiles = []

for item in raw_data_path.iterdir():
    if item.is_file() and item.suffix.upper() == ".CSV":
        datafiles.append(item.name)

print(f"Cleaning {sorted(datafiles)[-1]}...\n")
file_date = input("Press the Enter key to continue, or provide the DATE ONLY (MMDDYYYY) of the data file you would like to clean:\n")

if file_date:
    file_name = "jacksongov_export_"+file_date.strip()+".csv"
    df = pd.read_csv(raw_data_path / file_name, dtype=col_types, encoding="utf-8")
else:
    latest_file = sorted(datafiles)[-1]
    df = pd.read_csv(raw_data_path / latest_file, dtype=col_types, encoding="utf-8")

# Create 'Month_Text' column
df['ReferralDate'] = pd.to_datetime(df['ReferralDate'])
df['Month_Text'] = df['ReferralDate'].dt.strftime("%B")

# Create 'Zip2' column
df['Zip2'] = df['Zip'].astype('str')

# Filter DF by latest Referral Date on ArcGIS Service Definition
referral_date = input("Open `Strivin_ReferralReferenceList2021_2024_ExceltoTable` in ArcGIS Pro and confirm the latest `Referral Date` (MMDDYYYY) in the table:\n")
referral_date = pd.to_datetime(referral_date.strip(), format="%m%d%Y", errors="raise") # datetime.strptime(referral_date, "%m%d%Y")

# Create DF to append 
append_df = df[df['ReferralDate'] > referral_date].copy() # >=
append_df['ReferralDate'] = append_df['ReferralDate'].dt.strftime("%m/%d/%Y")

# Export df 
append_df.to_csv(export_path / f"edit_{current_date.strftime("%m%d%Y")}.csv", index=False, encoding='utf-8')
df.to_csv(export_path / f"New Data {current_date}.csv", index=False, encoding='utf-8')

print(f"Please append the newly created `edit_{current_date.strftime("%m%d%Y")}.csv` to the `Strivin_ReferralReferenceList2021_2024_ExceltoTable` in ArcGIS Pro.")
input("Please hit the Enter key to close the program...")


# Add functionality: connect to ArcGIS account, access service definition, then append with latest data (upsert with entire data file)?
'''# Connect to GIS
gis = GIS(profile="your_enterprise_profile")'''