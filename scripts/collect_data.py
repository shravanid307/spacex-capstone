import os
import urllib.request
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# 1. Download Spacex.csv for SQL lab
spacex_sql_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv"
spacex_sql_path = os.path.join(DATA_DIR, "spacex.csv")
if not os.path.exists(spacex_sql_path):
    print("Downloading spacex.csv for SQL analysis...")
    urllib.request.urlretrieve(spacex_sql_url, spacex_sql_path)
print(f"Saved spacex.csv: {len(pd.read_csv(spacex_sql_path))} records.")

# 2. Web Scraping Falcon 9 and Falcon Heavy launches from Wikipedia
print("Scraping Falcon 9 launches from Wikipedia snapshot...")
wiki_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
response = requests.get(wiki_url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

def date_time(table_cells):
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]

def booster_version(table_cells):
    out = ''.join([bv for j, bv in enumerate(table_cells.strings) if j % 2 == 0][0:1])
    return out.strip()

def landing_status(table_cells):
    out = [i for i in table_cells.strings][0]
    return out.strip()

def get_mass(table_cells):
    mass = unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        new_mass = mass[0:mass.find("kg")]
        new_mass = re.sub(r'[^0-9.]', '', new_mass)
    else:
        new_mass = 0
    return new_mass

html_tables = soup.find_all('table', "wikitable")

launch_dict = {
    'Flight No.': [],
    'Launch site': [],
    'Payload': [],
    'Payload mass': [],
    'Orbit': [],
    'Customer': [],
    'Launch outcome': [],
    'Version Booster': [],
    'Booster landing': [],
    'Date': [],
    'Time': []
}

extracted_row = 0
for table_number, table in enumerate(html_tables):
    for rows in table.find_all("tr"):
        flight_number = None
        if rows.th:
            txt = rows.th.text.strip()
            if txt.isdigit():
                flight_number = txt
        
        row = rows.find_all('td')
        if flight_number and len(row) >= 8:
            extracted_row += 1
            launch_dict['Flight No.'].append(flight_number)
            
            datatimelist = date_time(row[0])
            date = datatimelist[0].strip(',') if len(datatimelist) > 0 else None
            time = datatimelist[1] if len(datatimelist) > 1 else None
            launch_dict['Date'].append(date)
            launch_dict['Time'].append(time)
            
            bv = booster_version(row[1])
            if not(bv):
                bv = row[1].a.string if row[1].a else None
            launch_dict['Version Booster'].append(bv)
            
            launch_site = row[2].a.string if row[2].a else (row[2].string or "Unknown")
            launch_dict['Launch site'].append(launch_site)
            
            payload = row[3].a.string if row[3].a else (row[3].string or "Unknown")
            launch_dict['Payload'].append(payload)
            
            payload_mass = get_mass(row[4])
            launch_dict['Payload mass'].append(payload_mass)
            
            orbit = row[5].a.string if row[5].a else (row[5].string or "Unknown")
            launch_dict['Orbit'].append(orbit)
            
            customer = row[6].a.string if row[6].a else (row[6].string or "Unknown")
            launch_dict['Customer'].append(customer)
            
            launch_outcome = list(row[7].strings)[0] if len(list(row[7].strings)) > 0 else "Unknown"
            launch_dict['Launch outcome'].append(launch_outcome.strip())
            
            booster_landing = landing_status(row[8]) if len(row) > 8 else "Unknown"
            launch_dict['Booster landing'].append(booster_landing)

df_scraped = pd.DataFrame(launch_dict)
scraped_path = os.path.join(DATA_DIR, "spacex_web_scraped.csv")
df_scraped.to_csv(scraped_path, index=False)
print(f"Scraped {len(df_scraped)} launches successfully saved to {scraped_path}")
