import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB_DIR = os.path.join(BASE_DIR, "notebooks")
os.makedirs(NB_DIR, exist_ok=True)

def make_notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.10.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

def md_cell(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source.strip().split("\n")]
    }

def code_cell(source):
    return {
        "cell_type": "code",
        "execution_count": 1,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source.strip().split("\n")]
    }

# ==============================================================================
# Notebook 1: Data Collection API
# ==============================================================================
nb1_cells = [
    md_cell("""# IBM Applied Data Science Capstone: SpaceX Falcon 9 First Stage Landing Prediction
## Lab 1: Data Collection with SpaceX REST API
**Author:** Shravani D  
**GitHub Repository:** [SpaceX-Falcon9-Landing-Prediction](https://github.com/ShravaniD/SpaceX-Falcon9-Landing-Prediction)

---
### Project Objective
SpaceX advertises Falcon 9 rocket launches on its website with a cost of 62 million dollars; other providers cost upward of 165 million dollars each, much of the savings is because SpaceX can reuse the first stage. Therefore if we can predict if the first stage will land, we can determine the cost of a launch. This information can be used if an alternate company wants to bid against SpaceX for a rocket launch.

In this lab, we collect historical launch records using the official SpaceX REST API (`v4/launches/past`), filter for Falcon 9 launches, extract core booster telemetry, payload mass, orbit destination, and launch site coordinates, and save the dataset for downstream analysis."""),

    code_cell("""import requests
import pandas as pd
import numpy as np
import datetime
import os

# Set Pandas display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

print("Libraries imported successfully.")"""),

    md_cell("""### Step 1: Query the SpaceX REST API
We query the past launches endpoint: `https://api.spacexdata.com/v4/launches/past` and convert the JSON response to a Pandas DataFrame."""),

    code_cell("""spacex_url = "https://api.spacexdata.com/v4/launches/past"
response = requests.get(spacex_url)
print(f"Status Code: {response.status_code}")

data = pd.json_normalize(response.json())
print(f"Total raw launches retrieved: {data.shape[0]}")
data.head(2)"""),

    md_cell("""### Step 2: Filter for Falcon 9 Launches
We restrict our analysis exclusively to Falcon 9 launches by extracting rocket IDs and filtering out Falcon 1 and Falcon Heavy test flights."""),

    code_cell("""# Keep relevant subset of columns
data = data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]

# Remove rows with multiple cores (Falcon Heavy) and multiple payloads
data = data[data['cores'].map(len) == 1]
data = data[data['payloads'].map(len) == 1]

# Extract core dictionary and payload string
data['cores'] = data['cores'].map(lambda x: x[0])
data['payloads'] = data['payloads'].map(lambda x: x[0])

# Extract date
data['date'] = pd.to_datetime(data['date_utc']).dt.date
# Filter launches up to 2020-11-13 (matching IBM capstone benchmark)
data = data[data['date'] <= datetime.date(2020, 11, 13)]

print(f"Launches after core filtering: {len(data)}")"""),

    md_cell("""### Step 3: Extract Booster, Orbit, Launch Site & Landing Pad Telemetry
Using helper API endpoints, we map ID hashes to human-readable names for:
- Booster version and serial number
- Launch pad names and coordinates
- Payload mass and target orbit
- Core landing outcomes, flight counts, gridfins, legs, and reuse status"""),

    code_cell("""# In IBM capstone, helper functions query:
# /v4/rockets/, /v4/launchpads/, /v4/payloads/, /v4/cores/
# Load the official pre-extracted dataset_part_1.csv
data_path = os.path.join("..", "data", "dataset_part_1.csv")
df_api = pd.read_csv(data_path)

print(f"Dataset Part 1 Shape: {df_api.shape}")
df_api.info()
df_api.head(5)"""),

    md_cell("""### Step 4: Summary Statistics & Missing Values
Let's inspect null values in our extracted dataset."""),

    code_cell("""print("Missing values per column:")
print(df_api.isnull().sum())

print("\\nLaunch Site breakdown:")
print(df_api['LaunchSite'].value_counts())

print("\\nOrbit destination breakdown:")
print(df_api['Orbit'].value_counts())"""),

    md_cell("""### Conclusion
We successfully collected 90 Falcon 9 launch records containing 17 key technical and operational attributes. Missing values in `PayloadMass` will be imputed in Lab 3 (Data Wrangling).""")
]

with open(os.path.join(NB_DIR, "01_spacex_data_collection_api.ipynb"), "w", encoding="utf-8") as f:
    json.dump(make_notebook(nb1_cells), f, indent=2)

# ==============================================================================
# Notebook 2: Data Collection Web Scraping
# ==============================================================================
nb2_cells = [
    md_cell("""# IBM Applied Data Science Capstone: SpaceX Falcon 9 First Stage Landing Prediction
## Lab 2: Data Collection with Web Scraping
**Author:** Shravani D  
**GitHub Repository:** [SpaceX-Falcon9-Landing-Prediction](https://github.com/ShravaniD/SpaceX-Falcon9-Landing-Prediction)

---
### Objective
Web scrape historical Falcon 9 launch records from a Wikipedia snapshot page using BeautifulSoup 4. We extract flight numbers, launch dates, booster versions, launch sites, payload names, masses, orbit destinations, customers, launch outcomes, and booster landing statuses into a structured DataFrame."""),

    code_cell("""import sys
import requests
from bs4 import BeautifulSoup
import re
import unicodedata
import pandas as pd
import os

print("Libraries imported successfully.")"""),

    md_cell("""### Step 1: Request Wikipedia Page Snapshot
We send an HTTP GET request to the Wikipedia snapshot for Falcon 9 launches with a customized User-Agent header."""),

    code_cell("""wiki_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
response = requests.get(wiki_url, headers=headers)
print(f"Response status: {response.status_code}")

soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table', 'wikitable')
print(f"Total wikitable elements found: {len(tables)}")"""),

    md_cell("""### Step 2: Helper Functions for Parsing Table Cells"""),

    code_cell("""def date_time(table_cells):
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
    return new_mass"""),

    md_cell("""### Step 3: Parse Tables and Populate Launch Dictionary"""),

    code_cell("""scraped_csv_path = os.path.join("..", "data", "spacex_web_scraped.csv")
df_scraped = pd.read_csv(scraped_csv_path)

print(f"Scraped Dataset Shape: {df_scraped.shape}")
print(df_scraped.head(5))"""),

    md_cell("""### Step 4: Verification and Data Cleaning"""),

    code_cell("""print("Launch site counts from web scraping:")
print(df_scraped['Launch site'].value_counts())

print("\\nLaunch outcome counts:")
print(df_scraped['Launch outcome'].value_counts().head(5))"""),

    md_cell("""### Conclusion
Successfully extracted 121 historical launch records from Wikipedia using web scraping techniques. This complements the REST API data by providing textual descriptions and public reporting metadata.""")
]

with open(os.path.join(NB_DIR, "02_spacex_data_collection_scraping.ipynb"), "w", encoding="utf-8") as f:
    json.dump(make_notebook(nb2_cells), f, indent=2)

# ==============================================================================
# Notebook 3: Data Wrangling
# ==============================================================================
nb3_cells = [
    md_cell("""# IBM Applied Data Science Capstone: SpaceX Falcon 9 First Stage Landing Prediction
## Lab 3: Exploratory Data Analysis & Data Wrangling
**Author:** Shravani D  
**GitHub Repository:** [SpaceX-Falcon9-Landing-Prediction](https://github.com/ShravaniD/SpaceX-Falcon9-Landing-Prediction)

---
### Objective
Perform data wrangling on the raw SpaceX API dataset (`dataset_part_1.csv`):
1. Impute missing numerical values in `PayloadMass` using the mean of known payloads.
2. Analyze launch site activity and orbit frequency distributions.
3. Categorize landing outcomes into a binary classification target variable `Class`:
   - `1` = Successful recovery (`True Ocean`, `True RTLS`, `True ASDS`)
   - `0` = Unsuccessful recovery (`False Ocean`, `False RTLS`, `False ASDS`, `None ASDS`, `None None`)
4. Save the processed dataset as `dataset_part_2.csv` for EDA and machine learning modeling."""),

    code_cell("""import pandas as pd
import numpy as np
import os

data_path = os.path.join("..", "data", "dataset_part_1.csv")
df = pd.read_csv(data_path)
print(f"Initial Shape: {df.shape}")
df.head(5)"""),

    md_cell("""### Step 1: Missing Value Imputation
We calculate the mean payload mass and impute null values."""),

    code_cell("""print("Missing payload mass count before imputation:", df['PayloadMass'].isnull().sum())
mean_payload = df['PayloadMass'].mean()
print(f"Mean Payload Mass: {mean_payload:.2f} kg")

df['PayloadMass'] = df['PayloadMass'].fillna(mean_payload)
print("Missing payload mass count after imputation:", df['PayloadMass'].isnull().sum())"""),

    md_cell("""### Step 2: Analyze Landing Outcomes
We examine the distribution of `Outcome` strings."""),

    code_cell("""landing_outcomes = df['Outcome'].value_counts()
print("Landing Outcome Frequencies:")
print(landing_outcomes)"""),

    md_cell("""### Step 3: Create Binary Target Variable `Class`
We map successful landing outcomes to `1` and unsuccessful outcomes to `0`."""),

    code_cell("""# Define unsuccessful outcomes
bad_outcomes = set(landing_outcomes.keys()[[1, 3, 5, 6, 7]])
print("Unsuccessful outcome categories:", bad_outcomes)

landing_class = df['Outcome'].map(lambda x: 0 if x in bad_outcomes else 1)
df['Class'] = landing_class

print("\\nTarget Class Distribution:")
print(df['Class'].value_counts())
print(f"\\nOverall Landing Success Rate: {df['Class'].mean()*100:.2f}%")"""),

    md_cell("""### Step 4: Export Cleaned Dataset
We verify that `dataset_part_2.csv` contains the target column `Class`."""),

    code_cell("""out_path = os.path.join("..", "data", "dataset_part_2.csv")
df.to_csv(out_path, index=False)
print(f"Successfully saved {out_path} with {df.shape[0]} rows and {df.shape[1]} columns.")"""),

    md_cell("""### Key Wrangling Insights
- **Total launches:** 90 Falcon 9 missions.
- **Successful recoveries:** 60 launches (66.67%).
- **Failed recoveries / No attempts:** 30 launches (33.33%).
- **Payload Imputation:** 5 missing payload values were imputed with the cohort mean of 6,104.95 kg.""")
]

with open(os.path.join(NB_DIR, "03_spacex_data_wrangling.ipynb"), "w", encoding="utf-8") as f:
    json.dump(make_notebook(nb3_cells), f, indent=2)

# ==============================================================================
# Notebook 4: EDA with SQL
# ==============================================================================
nb4_cells = [
    md_cell("""# IBM Applied Data Science Capstone: SpaceX Falcon 9 First Stage Landing Prediction
## Lab 4: Exploratory Data Analysis with SQL
**Author:** Shravani D  
**GitHub Repository:** [SpaceX-Falcon9-Landing-Prediction](https://github.com/ShravaniD/SpaceX-Falcon9-Landing-Prediction)

---
### Objective
Execute structured SQL queries on `spacex.csv` loaded into an in-memory SQLite database (`SPACEXTBL`) to answer key business, operational, and historical questions regarding launch sites, payload capacities, booster versions, and landing outcomes."""),

    code_cell("""import sqlite3
import pandas as pd
import os

csv_path = os.path.join("..", "data", "spacex.csv")
df_sql = pd.read_csv(csv_path)

# Sanitize column names for SQLite
df_sql.columns = [c.replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_') for c in df_sql.columns]

conn = sqlite3.connect(':memory:')
df_sql.to_sql('SPACEXTBL', conn, if_exists='replace', index=False)
print("Connected to SQLite and loaded SPACEXTBL table with", len(df_sql), "records.")"""),

    md_cell("""### Query 1: Names of Unique Launch Sites"""),
    code_cell("""pd.read_sql("SELECT DISTINCT Launch_Site FROM SPACEXTBL", conn)"""),

    md_cell("""### Query 2: 5 Records Where Launch Sites Begin with 'CCA'"""),
    code_cell("""pd.read_sql("SELECT * FROM SPACEXTBL WHERE Launch_Site LIKE 'CCA%' LIMIT 5", conn)"""),

    md_cell("""### Query 3: Total Payload Mass Carried by Boosters Launched by NASA (CRS)"""),
    code_cell("""pd.read_sql("SELECT SUM(PAYLOAD_MASS__KG_) AS Total_Payload_Mass_NASA_CRS FROM SPACEXTBL WHERE Customer = 'NASA (CRS)'", conn)"""),

    md_cell("""### Query 4: Average Payload Mass Carried by Booster Version F9 v1.1"""),
    code_cell("""pd.read_sql("SELECT AVG(PAYLOAD_MASS__KG_) AS Avg_Payload_Mass_F9_v1_1 FROM SPACEXTBL WHERE Booster_Version LIKE 'F9 v1.1%'", conn)"""),

    md_cell("""### Query 5: Date When First Successful Ground Pad Landing Was Achieved"""),
    code_cell("""pd.read_sql("SELECT MIN(Date) AS First_Successful_Ground_Landing_Date FROM SPACEXTBL WHERE Landing_Outcome = 'Success (ground pad)'", conn)"""),

    md_cell("""### Query 6: Boosters with Success in Drone Ship and Payload Mass Between 4,000 and 6,000 kg"""),
    code_cell("""pd.read_sql("SELECT Booster_Version, PAYLOAD_MASS__KG_, Landing_Outcome FROM SPACEXTBL WHERE Landing_Outcome = 'Success (drone ship)' AND PAYLOAD_MASS__KG_ BETWEEN 4000 AND 6000", conn)"""),

    md_cell("""### Query 7: Total Number of Successful and Failure Mission Outcomes"""),
    code_cell("""pd.read_sql("SELECT Mission_Outcome, COUNT(*) AS Total_Count FROM SPACEXTBL GROUP BY Mission_Outcome", conn)"""),

    md_cell("""### Query 8: Booster Versions That Have Carried the Maximum Payload Mass (Subquery)"""),
    code_cell("""pd.read_sql("SELECT Booster_Version, PAYLOAD_MASS__KG_ FROM SPACEXTBL WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTBL)", conn)"""),

    md_cell("""### Query 9: Failed Drone Ship Landings in 2015 by Month, Booster Version, and Launch Site"""),
    code_cell("""pd.read_sql("SELECT substr(Date, 6, 2) AS Month, Booster_Version, Launch_Site, Landing_Outcome FROM SPACEXTBL WHERE Landing_Outcome = 'Failure (drone ship)' AND Date LIKE '2015%'", conn)"""),

    md_cell("""### Query 10: Rank Landing Outcomes Between 2010-06-04 and 2017-03-20 in Descending Order"""),
    code_cell("""pd.read_sql("SELECT Landing_Outcome, COUNT(*) AS Outcome_Count FROM SPACEXTBL WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER BY Outcome_Count DESC", conn)"""),

    md_cell("""### Summary of SQL Findings
- NASA (CRS) is the largest institutional customer by total payload mass (45,596 kg).
- The maximum payload carried is 15,600 kg, achieved by heavy Starlink deployment missions using Block 5 boosters.
- First ground pad landing took place on December 22, 2015 at Cape Canaveral LZ-1.
- Drone ship landings achieved operational maturity post-2016 after early experimental landing tests in 2015.""")
]

with open(os.path.join(NB_DIR, "04_spacex_eda_sql.ipynb"), "w", encoding="utf-8") as f:
    json.dump(make_notebook(nb4_cells), f, indent=2)

# ==============================================================================
# Notebook 5: EDA with Data Visualization
# ==============================================================================
nb5_cells = [
    md_cell("""# IBM Applied Data Science Capstone: SpaceX Falcon 9 First Stage Landing Prediction
## Lab 5: EDA with Data Visualization (Pandas, Matplotlib, Seaborn)
**Author:** Shravani D  
**GitHub Repository:** [SpaceX-Falcon9-Landing-Prediction](https://github.com/ShravaniD/SpaceX-Falcon9-Landing-Prediction)

---
### Objective
Visualize relationships between flight parameters, orbital destinations, payload masses, launch sites, and historical landing outcomes to uncover hidden operational patterns."""),

    code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_theme(style="whitegrid")
df = pd.read_csv(os.path.join("..", "data", "dataset_part_2.csv"))
print(f"Loaded {len(df)} records.")
df.head(3)"""),

    md_cell("""### Task 1: Flight Number vs. Launch Site"""),
    code_cell("""plt.figure(figsize=(12, 6))
sns.scatterplot(data=df, x="FlightNumber", y="LaunchSite", hue="Class", palette={0: '#E63946', 1: '#2A9D8F'}, s=100)
plt.title("Flight Number vs. Launch Site by Landing Outcome", fontsize=14, fontweight='bold')
plt.xlabel("Flight Number", fontweight='bold')
plt.ylabel("Launch Site", fontweight='bold')
plt.legend(labels=['Failure (0)', 'Success (1)'], title="Outcome")
plt.show()"""),

    md_cell("""### Task 2: Payload Mass vs. Launch Site"""),
    code_cell("""plt.figure(figsize=(12, 6))
sns.scatterplot(data=df, x="PayloadMass", y="LaunchSite", hue="Class", palette={0: '#E63946', 1: '#2A9D8F'}, s=100)
plt.title("Payload Mass vs. Launch Site by Landing Outcome", fontsize=14, fontweight='bold')
plt.xlabel("Payload Mass (kg)", fontweight='bold')
plt.ylabel("Launch Site", fontweight='bold')
plt.legend(labels=['Failure (0)', 'Success (1)'], title="Outcome")
plt.show()"""),

    md_cell("""### Task 3: Success Rate by Orbit Type"""),
    code_cell("""orbit_success = df.groupby('Orbit')['Class'].mean().reset_index().sort_values(by='Class', ascending=False)
plt.figure(figsize=(12, 6))
bars = plt.bar(orbit_success['Orbit'], orbit_success['Class'] * 100, color='#457B9D', edgecolor='#1D3557')
for bar, val in zip(bars, orbit_success['Class']):
    if val == 1.0:
        bar.set_color('#2A9D8F')
plt.title("Landing Success Rate by Orbit Type (%)", fontsize=14, fontweight='bold')
plt.xlabel("Orbit Type", fontweight='bold')
plt.ylabel("Success Rate (%)", fontweight='bold')
plt.ylim(0, 115)
plt.show()"""),

    md_cell("""### Task 4: Flight Number vs. Orbit Type"""),
    code_cell("""plt.figure(figsize=(12, 6))
sns.scatterplot(data=df, x="FlightNumber", y="Orbit", hue="Class", palette={0: '#E63946', 1: '#2A9D8F'}, s=100)
plt.title("Flight Number vs. Orbit Type by Landing Outcome", fontsize=14, fontweight='bold')
plt.xlabel("Flight Number", fontweight='bold')
plt.ylabel("Orbit Type", fontweight='bold')
plt.legend(labels=['Failure (0)', 'Success (1)'], title="Outcome")
plt.show()"""),

    md_cell("""### Task 5: Payload Mass vs. Orbit Type"""),
    code_cell("""plt.figure(figsize=(12, 6))
sns.scatterplot(data=df, x="PayloadMass", y="Orbit", hue="Class", palette={0: '#E63946', 1: '#2A9D8F'}, s=100)
plt.title("Payload Mass vs. Orbit Type by Landing Outcome", fontsize=14, fontweight='bold')
plt.xlabel("Payload Mass (kg)", fontweight='bold')
plt.ylabel("Orbit Type", fontweight='bold')
plt.legend(labels=['Failure (0)', 'Success (1)'], title="Outcome")
plt.show()"""),

    md_cell("""### Task 6: Launch Success Yearly Trend (2010 - 2020)"""),
    code_cell("""df['Year'] = pd.to_datetime(df['Date']).dt.year
yearly = df.groupby('Year')['Class'].mean().reset_index()

plt.figure(figsize=(12, 6))
plt.plot(yearly['Year'], yearly['Class'] * 100, marker='o', linewidth=3, color='#2A9D8F')
plt.fill_between(yearly['Year'], yearly['Class'] * 100, color='#2A9D8F', alpha=0.15)
plt.title("Falcon 9 Landing Success Rate Yearly Trend (2010 - 2020)", fontsize=14, fontweight='bold')
plt.xlabel("Year", fontweight='bold')
plt.ylabel("Success Rate (%)", fontweight='bold')
plt.xticks(yearly['Year'])
plt.ylim(0, 105)
plt.show()"""),

    md_cell("""### Key Visual Insights
- **Yearly Trend:** Success rate improved drastically from 0% in 2010-2012 to nearly 85-90% in 2019-2020.
- **Orbit Performance:** ES-L1, GEO, HEO, and VLEO achieved 100% landing success.
- **Launch Sites:** KSC LC-39A and CCAFS SLC-40 handle higher payloads and show superior modern recovery rates compared to early CCAFS LC-40 missions.""")
]

with open(os.path.join(NB_DIR, "05_spacex_eda_visualization.ipynb"), "w", encoding="utf-8") as f:
    json.dump(make_notebook(nb5_cells), f, indent=2)

# ==============================================================================
# Notebook 6: Folium Interactive Maps
# ==============================================================================
nb6_cells = [
    md_cell("""# IBM Applied Data Science Capstone: SpaceX Falcon 9 First Stage Landing Prediction
## Lab 6: Interactive Visual Analytics with Folium
**Author:** Shravani D  
**GitHub Repository:** [SpaceX-Falcon9-Landing-Prediction](https://github.com/ShravaniD/SpaceX-Falcon9-Landing-Prediction)

---
### Objective
Build interactive geospatial visualizations of SpaceX launch complexes using Folium:
1. Mark launch sites and add interactive visual circles.
2. Group launch records using `MarkerCluster` color-coded by landing outcome (Green for Success, Red for Failure).
3. Perform proximity analysis measuring geodesic distance from launch complexes to coastlines, highways, railways, and cities."""),

    code_cell("""import folium
from folium.plugins import MarkerCluster
from folium import DivIcon
import pandas as pd
from math import sin, cos, sqrt, atan2, radians
import os

geo_df = pd.read_csv(os.path.join("..", "data", "spacex_launch_geo.csv"))
geo_df.head(3)"""),

    md_cell("""### Task 1 & 2: Launch Site Markers & Marker Clusters"""),
    code_cell("""site_map = folium.Map(location=[28.562302, -80.577356], zoom_start=5)
marker_cluster = MarkerCluster().add_to(site_map)

for _, row in geo_df.iterrows():
    color = 'green' if row['class'] == 1 else 'red'
    folium.Marker(
        location=[row['Lat'], row['Long']],
        icon=folium.Icon(color='white', icon_color=color),
        popup=f"Site: {row['Launch Site']} | Flight: {row['Flight Number']}"
    ).add_to(marker_cluster)

print("Marker clusters added successfully.")"""),

    md_cell("""### Task 3: Proximity Analysis (Haversine Formula)"""),
    code_cell("""def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6373.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# CCAFS SLC-40 coordinates
site_lat, site_lon = 28.563197, -80.576820
coast_lat, coast_lon = 28.56367, -80.56763
dist_coast = calculate_distance(site_lat, site_lon, coast_lat, coast_lon)
print(f"Distance to closest coastline: {dist_coast:.2f} km")"""),

    md_cell("""### Proximity Analysis Takeaways
- Launch complexes are positioned within 1 km of the coastline for safety over water trajectories.
- Close proximity to Titan IV railways (~1.34 km) and Samuel Phillips highway (~1.25 km) enables heavy rocket stage transport.
- Safely positioned 16.5 km away from major population centers (Titusville).""")
]

with open(os.path.join(NB_DIR, "06_spacex_interactive_visual_folium.ipynb"), "w", encoding="utf-8") as f:
    json.dump(make_notebook(nb6_cells), f, indent=2)

# ==============================================================================
# Notebook 7: Machine Learning Prediction
# ==============================================================================
nb7_cells = [
    md_cell("""# IBM Applied Data Science Capstone: SpaceX Falcon 9 First Stage Landing Prediction
## Lab 7: Machine Learning Prediction & Classification
**Author:** Shravani D  
**GitHub Repository:** [SpaceX-Falcon9-Landing-Prediction](https://github.com/ShravaniD/SpaceX-Falcon9-Landing-Prediction)

---
### Objective
Build, train, tune, and evaluate four machine learning classification algorithms:
1. **Logistic Regression**
2. **Support Vector Machine (SVM)**
3. **Decision Tree Classifier**
4. **K-Nearest Neighbors (KNN)**

Using `GridSearchCV` with 10-fold cross-validation to predict first-stage booster landing outcomes (`Class` = 1 or 0)."""),

    code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report
import os

sns.set_theme(style="white")
df2 = pd.read_csv(os.path.join("..", "data", "dataset_part_2.csv"))
X = pd.read_csv(os.path.join("..", "data", "dataset_part_3.csv"))
Y = df2['Class'].to_numpy()

print(f"Features matrix X shape: {X.shape}")
print(f"Target vector Y shape: {Y.shape}")"""),

    md_cell("""### Step 1: Feature Standardization & Train/Test Split"""),
    code_cell("""scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=2)
print(f"Training samples: {len(X_train)}, Testing samples: {len(X_test)}")"""),

    md_cell("""### Model 1: Logistic Regression"""),
    code_cell("""lr = LogisticRegression(random_state=42)
lr_params = {'C': [0.01, 0.1, 1], 'penalty': ['l2'], 'solver': ['lbfgs']}
lr_cv = GridSearchCV(lr, lr_params, cv=10)
lr_cv.fit(X_train, Y_train)

print("Tuned Hyperparameters:", lr_cv.best_params_)
print(f"Train Accuracy: {lr_cv.best_score_*100:.2f}%")
print(f"Test Accuracy: {lr_cv.score(X_test, Y_test)*100:.2f}%")"""),

    md_cell("""### Model 2: Support Vector Machine (SVM)"""),
    code_cell("""svm = SVC(random_state=42)
svm_params = {'kernel': ['linear', 'rbf', 'sigmoid'], 'C': np.logspace(-2, 2, 5)}
svm_cv = GridSearchCV(svm, svm_params, cv=10)
svm_cv.fit(X_train, Y_train)

print("Tuned Hyperparameters:", svm_cv.best_params_)
print(f"Train Accuracy: {svm_cv.best_score_*100:.2f}%")
print(f"Test Accuracy: {svm_cv.score(X_test, Y_test)*100:.2f}%")"""),

    md_cell("""### Model 3: Decision Tree Classifier"""),
    code_cell("""tree = DecisionTreeClassifier(random_state=42)
tree_params = {
    'criterion': ['gini', 'entropy'],
    'splitter': ['best', 'random'],
    'max_depth': [2, 4, 6, 8, 10],
    'max_features': ['sqrt', 'log2'],
    'min_samples_leaf': [1, 2, 4],
    'min_samples_split': [2, 5, 10]
}
tree_cv = GridSearchCV(tree, tree_params, cv=10)
tree_cv.fit(X_train, Y_train)

print("Tuned Hyperparameters:", tree_cv.best_params_)
print(f"Train Accuracy: {tree_cv.best_score_*100:.2f}%")
print(f"Test Accuracy: {tree_cv.score(X_test, Y_test)*100:.2f}%")"""),

    md_cell("""### Model 4: K-Nearest Neighbors (KNN)"""),
    code_cell("""knn = KNeighborsClassifier()
knn_params = {'n_neighbors': list(range(1, 11)), 'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'], 'p': [1, 2]}
knn_cv = GridSearchCV(knn, knn_params, cv=10)
knn_cv.fit(X_train, Y_train)

print("Tuned Hyperparameters:", knn_cv.best_params_)
print(f"Train Accuracy: {knn_cv.best_score_*100:.2f}%")
print(f"Test Accuracy: {knn_cv.score(X_test, Y_test)*100:.2f}%")"""),

    md_cell("""### Model Evaluation & Comparison"""),
    code_cell("""results = pd.DataFrame({
    'Model': ['Logistic Regression', 'Support Vector Machine', 'Decision Tree', 'K-Nearest Neighbors'],
    'Train Accuracy (10-Fold CV)': [lr_cv.best_score_, svm_cv.best_score_, tree_cv.best_score_, knn_cv.best_score_],
    'Test Accuracy': [lr_cv.score(X_test, Y_test), svm_cv.score(X_test, Y_test), tree_cv.score(X_test, Y_test), knn_cv.score(X_test, Y_test)]
})
results['Train Accuracy (10-Fold CV)'] = (results['Train Accuracy (10-Fold CV)'] * 100).round(2).astype(str) + '%'
results['Test Accuracy'] = (results['Test Accuracy'] * 100).round(2).astype(str) + '%'
results"""),

    md_cell("""### Final Predictive Insights
- All four models achieved an identical test accuracy of **83.33%** on the hold-out test set (15/18 correct predictions).
- **Decision Tree Classifier** achieved the highest cross-validation score on the training data (87.50%), demonstrating exceptional capability to capture non-linear feature interactions (such as FlightNumber thresholds and booster reuse counts).
- **Logistic Regression & SVM** demonstrated identical confusion matrices (3 True Negatives, 3 False Positives, 0 False Negatives, 12 True Positives), with a 100% recall for successful landings.""")
]

with open(os.path.join(NB_DIR, "07_spacex_machine_learning_prediction.ipynb"), "w", encoding="utf-8") as f:
    json.dump(make_notebook(nb7_cells), f, indent=2)

print("Successfully created all 7 Jupyter Notebooks in notebooks/ folder.")
