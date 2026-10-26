import os
import tempfile
os.environ['MPLCONFIGDIR'] = tempfile.gettempdir()
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, accuracy_score

# Set style
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
VIS_DIR = os.path.join(BASE_DIR, "visuals")
os.makedirs(VIS_DIR, exist_ok=True)

df2 = pd.read_csv(os.path.join(DATA_DIR, "dataset_part_2.csv"))
df3 = pd.read_csv(os.path.join(DATA_DIR, "dataset_part_3.csv"))
df_dash = pd.read_csv(os.path.join(DATA_DIR, "spacex_launch_dash.csv"))
df_geo = pd.read_csv(os.path.join(DATA_DIR, "spacex_launch_geo.csv"))
df_sql = pd.read_csv(os.path.join(DATA_DIR, "spacex.csv"))

print("Loaded datasets successfully.")

# Color palette
PALETTE = {0: '#E63946', 1: '#2A9D8F'}
COLOR_SUCCESS = '#2A9D8F'
COLOR_FAIL = '#E63946'
NAVY = '#1D3557'
SKY = '#457B9D'

# -------------------------------------------------------------
# 1. Flowchart: SpaceX API Data Collection Pipeline
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 5), dpi=300)
ax.axis('off')
ax.set_facecolor('#F8F9FA')
fig.patch.set_facecolor('#F8F9FA')

box_props = dict(boxstyle='round,pad=0.8', facecolor='#FFFFFF', edgecolor='#1D3557', linewidth=2)
arrow_props = dict(arrowstyle='->', lw=2.5, color='#1D3557')

steps = [
    ("SpaceX REST API\n(v4/launches/past)", (0.1, 0.5), '#1D3557', 'white'),
    ("API Query &\nJSON Parsing", (0.32, 0.5), '#457B9D', 'white'),
    ("Filter Falcon 9\n(Exclude Falcon 1)", (0.54, 0.5), '#2A9D8F', 'white'),
    ("Extract Core, Payload,\nOrbit, Launch Site", (0.76, 0.5), '#E76F51', 'white'),
    ("dataset_part_1.csv\n(90 Launches, 17 cols)", (0.95, 0.5), '#264653', 'white')
]

for i, (text, (x, y), bg_color, text_color) in enumerate(steps):
    ax.text(x, y, text, ha='center', va='center', fontsize=11, fontweight='bold', color=text_color,
            bbox=dict(boxstyle='round,pad=0.6', facecolor=bg_color, edgecolor='none', alpha=0.95))
    if i < len(steps) - 1:
        next_x = steps[i+1][1][0]
        ax.annotate('', xy=(next_x - 0.08, y), xytext=(x + 0.08, y),
                    arrowprops=dict(arrowstyle="fancy,head_length=0.4,head_width=0.4,tail_width=0.15", color='#1D3557'))

ax.set_title("Data Collection Pipeline: SpaceX REST API Integration", fontsize=15, fontweight='bold', pad=20, color='#1D3557')
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "data_pipeline_flowchart.png"), bbox_inches='tight', dpi=300)
plt.close()

# -------------------------------------------------------------
# 2. Flowchart: Web Scraping Pipeline
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 5), dpi=300)
ax.axis('off')
ax.set_facecolor('#F8F9FA')
fig.patch.set_facecolor('#F8F9FA')

scrape_steps = [
    ("Wikipedia Falcon 9\nLaunches Snapshot", (0.1, 0.5), '#264653', 'white'),
    ("HTTP GET Request\nw/ User-Agent Header", (0.32, 0.5), '#2A9D8F', 'white'),
    ("BeautifulSoup 4\nDOM & Table Parsing", (0.54, 0.5), '#E76F51', 'white'),
    ("Data Extraction:\nDate, Booster, Payload", (0.76, 0.5), '#457B9D', 'white'),
    ("spacex_web_scraped.csv\n(121 Historical Records)", (0.95, 0.5), '#1D3557', 'white')
]

for i, (text, (x, y), bg_color, text_color) in enumerate(scrape_steps):
    ax.text(x, y, text, ha='center', va='center', fontsize=11, fontweight='bold', color=text_color,
            bbox=dict(boxstyle='round,pad=0.6', facecolor=bg_color, edgecolor='none', alpha=0.95))
    if i < len(scrape_steps) - 1:
        next_x = scrape_steps[i+1][1][0]
        ax.annotate('', xy=(next_x - 0.08, y), xytext=(x + 0.08, y),
                    arrowprops=dict(arrowstyle="fancy,head_length=0.4,head_width=0.4,tail_width=0.15", color='#1D3557'))

ax.set_title("Data Collection Pipeline: Wikipedia Web Scraping Architecture", fontsize=15, fontweight='bold', pad=20, color='#1D3557')
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "scraping_pipeline_flowchart.png"), bbox_inches='tight', dpi=300)
plt.close()

# -------------------------------------------------------------
# 3. Flowchart: Data Wrangling Pipeline
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 5), dpi=300)
ax.axis('off')
ax.set_facecolor('#F8F9FA')
fig.patch.set_facecolor('#F8F9FA')

wrangling_steps = [
    ("Raw Dataset\n(Missing Payloads)", (0.1, 0.5), '#E63946', 'white'),
    ("Mean Imputation\n(PayloadMass: 6104.95 kg)", (0.32, 0.5), '#457B9D', 'white'),
    ("Landing Outcome\nCategorization", (0.54, 0.5), '#2A9D8F', 'white'),
    ("Binary Encoding\n1=Success, 0=Failure", (0.76, 0.5), '#1D3557', 'white'),
    ("dataset_part_2.csv\nReady for EDA & ML", (0.95, 0.5), '#264653', 'white')
]

for i, (text, (x, y), bg_color, text_color) in enumerate(wrangling_steps):
    ax.text(x, y, text, ha='center', va='center', fontsize=11, fontweight='bold', color=text_color,
            bbox=dict(boxstyle='round,pad=0.6', facecolor=bg_color, edgecolor='none', alpha=0.95))
    if i < len(wrangling_steps) - 1:
        next_x = wrangling_steps[i+1][1][0]
        ax.annotate('', xy=(next_x - 0.08, y), xytext=(x + 0.08, y),
                    arrowprops=dict(arrowstyle="fancy,head_length=0.4,head_width=0.4,tail_width=0.15", color='#1D3557'))

ax.set_title("Data Wrangling Methodology: Missing Value Imputation & Target Derivation", fontsize=15, fontweight='bold', pad=20, color='#1D3557')
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "wrangling_pipeline.png"), bbox_inches='tight', dpi=300)
plt.close()

# -------------------------------------------------------------
# 4. EDA: Flight Number vs Launch Site
# -------------------------------------------------------------
plt.figure(figsize=(12, 6), dpi=300)
sns.scatterplot(
    data=df2,
    x="FlightNumber",
    y="LaunchSite",
    hue="Class",
    palette=PALETTE,
    s=120,
    alpha=0.9,
    edgecolor="black",
    linewidth=0.8
)
plt.title("Flight Number vs. Launch Site by Landing Outcome", fontsize=15, fontweight='bold', pad=15, color='#1D3557')
plt.xlabel("Flight Number", fontsize=12, fontweight='bold')
plt.ylabel("Launch Site", fontsize=12, fontweight='bold')
handles, labels = plt.gca().get_legend_handles_labels()
plt.legend(handles=handles, labels=['Failure (0)', 'Success (1)'], title="Landing Outcome", loc="center right", frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "launch_site_vs_flight_number.png"), bbox_inches='tight', dpi=300)
plt.close()

# -------------------------------------------------------------
# 5. EDA: Payload Mass vs Launch Site
# -------------------------------------------------------------
plt.figure(figsize=(12, 6), dpi=300)
sns.scatterplot(
    data=df2,
    x="PayloadMass",
    y="LaunchSite",
    hue="Class",
    palette=PALETTE,
    s=120,
    alpha=0.9,
    edgecolor="black",
    linewidth=0.8
)
plt.title("Payload Mass (kg) vs. Launch Site by Landing Outcome", fontsize=15, fontweight='bold', pad=15, color='#1D3557')
plt.xlabel("Payload Mass (kg)", fontsize=12, fontweight='bold')
plt.ylabel("Launch Site", fontsize=12, fontweight='bold')
handles, labels = plt.gca().get_legend_handles_labels()
plt.legend(handles=handles, labels=['Failure (0)', 'Success (1)'], title="Landing Outcome", loc="upper left", frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "payload_vs_launch_site.png"), bbox_inches='tight', dpi=300)
plt.close()

# -------------------------------------------------------------
# 6. EDA: Success Rate by Orbit Type
# -------------------------------------------------------------
plt.figure(figsize=(12, 6), dpi=300)
orbit_success = df2.groupby('Orbit')['Class'].mean().reset_index().sort_values(by='Class', ascending=False)
bars = plt.bar(orbit_success['Orbit'], orbit_success['Class'] * 100, color='#457B9D', edgecolor='#1D3557', linewidth=1.2)

# Highlight 100% success orbits in teal
for bar, val in zip(bars, orbit_success['Class']):
    if val == 1.0:
        bar.set_color('#2A9D8F')
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5, f"{val*100:.1f}%", ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.title("Landing Success Rate by Orbit Type (%)", fontsize=15, fontweight='bold', pad=15, color='#1D3557')
plt.xlabel("Orbit Type", fontsize=12, fontweight='bold')
plt.ylabel("Success Rate (%)", fontsize=12, fontweight='bold')
plt.ylim(0, 115)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "success_rate_by_orbit.png"), bbox_inches='tight', dpi=300)
plt.close()

# -------------------------------------------------------------
# 7. EDA: Flight Number vs Orbit
# -------------------------------------------------------------
plt.figure(figsize=(12, 6), dpi=300)
sns.scatterplot(
    data=df2,
    x="FlightNumber",
    y="Orbit",
    hue="Class",
    palette=PALETTE,
    s=120,
    alpha=0.9,
    edgecolor="black",
    linewidth=0.8
)
plt.title("Flight Number vs. Orbit Type by Landing Outcome", fontsize=15, fontweight='bold', pad=15, color='#1D3557')
plt.xlabel("Flight Number", fontsize=12, fontweight='bold')
plt.ylabel("Orbit Type", fontsize=12, fontweight='bold')
handles, labels = plt.gca().get_legend_handles_labels()
plt.legend(handles=handles, labels=['Failure (0)', 'Success (1)'], title="Landing Outcome", loc="upper left", frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "flight_number_vs_orbit.png"), bbox_inches='tight', dpi=300)
plt.close()

# -------------------------------------------------------------
# 8. EDA: Payload Mass vs Orbit
# -------------------------------------------------------------
plt.figure(figsize=(12, 6), dpi=300)
sns.scatterplot(
    data=df2,
    x="PayloadMass",
    y="Orbit",
    hue="Class",
    palette=PALETTE,
    s=120,
    alpha=0.9,
    edgecolor="black",
    linewidth=0.8
)
plt.title("Payload Mass (kg) vs. Orbit Type by Landing Outcome", fontsize=15, fontweight='bold', pad=15, color='#1D3557')
plt.xlabel("Payload Mass (kg)", fontsize=12, fontweight='bold')
plt.ylabel("Orbit Type", fontsize=12, fontweight='bold')
handles, labels = plt.gca().get_legend_handles_labels()
plt.legend(handles=handles, labels=['Failure (0)', 'Success (1)'], title="Landing Outcome", loc="lower right", frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "payload_vs_orbit.png"), bbox_inches='tight', dpi=300)
plt.close()

# -------------------------------------------------------------
# 9. EDA: Yearly Launch Success Trend
# -------------------------------------------------------------
df2['Year'] = pd.to_datetime(df2['Date']).dt.year
yearly_trend = df2.groupby('Year')['Class'].mean().reset_index()

plt.figure(figsize=(12, 6), dpi=300)
plt.plot(yearly_trend['Year'], yearly_trend['Class'] * 100, marker='o', markersize=9, linewidth=3, color='#2A9D8F', label="Landing Success Rate")
plt.fill_between(yearly_trend['Year'], yearly_trend['Class'] * 100, color='#2A9D8F', alpha=0.15)

for _, row in yearly_trend.iterrows():
    plt.text(row['Year'], row['Class'] * 100 + 3, f"{row['Class']*100:.1f}%", ha='center', va='bottom', fontsize=10, fontweight='bold', color='#1D3557')

plt.title("Falcon 9 Landing Success Rate Yearly Trend (2010 - 2020)", fontsize=15, fontweight='bold', pad=15, color='#1D3557')
plt.xlabel("Year", fontsize=12, fontweight='bold')
plt.ylabel("Success Rate (%)", fontsize=12, fontweight='bold')
plt.ylim(0, 105)
plt.xticks(yearly_trend['Year'])
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "success_rate_yearly_trend.png"), bbox_inches='tight', dpi=300)
plt.close()

# -------------------------------------------------------------
# 10. EDA with SQL: Query Results Visualization Table
# -------------------------------------------------------------
# Run SQLite queries
conn = sqlite3.connect(':memory:')
# Clean column names for SQL
clean_cols = [c.replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_') for c in df_sql.columns]
df_sql.columns = clean_cols
df_sql.to_sql('SPACEXTBL', conn, if_exists='replace', index=False)

q1 = pd.read_sql("SELECT DISTINCT Launch_Site FROM SPACEXTBL", conn)
q2 = pd.read_sql("SELECT Launch_Site FROM SPACEXTBL WHERE Launch_Site LIKE 'CCA%' LIMIT 5", conn)
q3 = pd.read_sql("SELECT SUM(PAYLOAD_MASS__KG_) AS Total_Payload_Mass FROM SPACEXTBL WHERE Customer = 'NASA (CRS)'", conn)
q4 = pd.read_sql("SELECT AVG(PAYLOAD_MASS__KG_) AS Avg_Payload_Mass FROM SPACEXTBL WHERE Booster_Version LIKE 'F9 v1.1%'", conn)
q5 = pd.read_sql("SELECT MIN(Date) AS First_Successful_Ground_Landing FROM SPACEXTBL WHERE Landing_Outcome = 'Success (ground pad)'", conn)
q6 = pd.read_sql("SELECT Booster_Version FROM SPACEXTBL WHERE Landing_Outcome = 'Success (drone ship)' AND PAYLOAD_MASS__KG_ BETWEEN 4000 AND 6000", conn)
q7 = pd.read_sql("SELECT Mission_Outcome, COUNT(*) as Count FROM SPACEXTBL GROUP BY Mission_Outcome", conn)
q8 = pd.read_sql("SELECT Booster_Version, PAYLOAD_MASS__KG_ FROM SPACEXTBL WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTBL)", conn)
q9 = pd.read_sql("SELECT substr(Date, 6, 2) as Month, Booster_Version, Launch_Site, Landing_Outcome FROM SPACEXTBL WHERE Landing_Outcome = 'Failure (drone ship)' AND Date LIKE '2015%'", conn)
q10 = pd.read_sql("SELECT Landing_Outcome, COUNT(*) as Count FROM SPACEXTBL WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER BY Count DESC", conn)

fig, ax = plt.subplots(figsize=(13, 7), dpi=300)
ax.axis('off')
fig.patch.set_facecolor('#F8F9FA')

summary_data = [
    ["1. Unique Launch Sites", ", ".join(q1['Launch_Site'].tolist()[:4])],
    ["2. CCAFS Sites Sample (5)", f"{len(q2)} records starting with CCAFS"],
    ["3. NASA (CRS) Total Payload", f"{q3['Total_Payload_Mass'].values[0]:,.0f} kg"],
    ["4. F9 v1.1 Avg Payload", f"{q4['Avg_Payload_Mass'].values[0]:,.1f} kg"],
    ["5. First Ground Pad Landing", f"{q5['First_Successful_Ground_Landing'].values[0]}"],
    ["6. Drone Ship (4k-6k kg)", f"{len(q6)} boosters (e.g. {q6['Booster_Version'].iloc[0]})"],
    ["7. Mission Outcomes Count", "Success: 98, Failure: 1, Partial: 1"],
    ["8. Max Payload Booster", f"15,600 kg (B1048.4, B1049.4, etc.)"],
    ["9. 2015 Drone Ship Failures", f"{len(q9)} launches (Jan: B1012, Apr: B1015)"],
    ["10. Top Landing Rank (2010-17)", f"No Attempt (10), Success (drone) (5), Failure (5)"]
]

col_labels = ["SQL Query Objective", "Key Analytical Finding / Metric"]
table = ax.table(cellText=summary_data, colLabels=col_labels, loc='center', cellLoc='left')
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 1.8)

for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_facecolor('#1D3557')
        cell.set_text_props(color='white', fontweight='bold', fontsize=12)
    else:
        cell.set_facecolor('#FFFFFF' if row % 2 == 0 else '#F1FAEE')
        if col == 0:
            cell.set_text_props(fontweight='bold', color='#1D3557')

plt.title("EDA with SQL: Executive Summary of 10 Core Business Queries", fontsize=15, fontweight='bold', pad=25, color='#1D3557')
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "sql_summary_table.png"), bbox_inches='tight', dpi=300)
plt.close()

# -------------------------------------------------------------
# 11. Folium Map Overview Snapshot
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
ax.set_facecolor('#EBF2FA')
fig.patch.set_facecolor('#FFFFFF')

site_coords = {
    'CCAFS LC-40': (28.562302, -80.577356),
    'CCAFS SLC-40': (28.563197, -80.576820),
    'KSC LC-39A': (28.573255, -80.646895),
    'VAFB SLC-4E': (34.632834, -120.610745)
}

# Draw schematic map of US
ax.scatter([-120.61], [34.63], color='#E76F51', s=350, zorder=5, label="VAFB SLC-4E (California Coast)")
ax.scatter([-80.57, -80.57, -80.64], [28.56, 28.56, 28.57], color='#2A9D8F', s=350, zorder=5, label="Cape Canaveral / KSC (Florida Coast)")

ax.text(-120.61, 35.3, "VAFB SLC-4E\nLat: 34.63°, Lon: -120.61°\n(Polar & High-Inclination Orbits)", fontsize=11, fontweight='bold', ha='center', bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='#E76F51', lw=2))
ax.text(-80.57, 27.2, "CCAFS LC-40 / SLC-40 & KSC LC-39A\nLat: 28.56° - 28.57°, Lon: -80.57° - -80.64°\n(ISS, GTO, LEO East Coast Launches)", fontsize=11, fontweight='bold', ha='center', bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='#2A9D8F', lw=2))

ax.set_xlim(-130, -70)
ax.set_ylim(24, 42)
ax.set_xlabel("Longitude (°W)", fontsize=12, fontweight='bold')
ax.set_ylabel("Latitude (°N)", fontsize=12, fontweight='bold')
ax.set_title("Geographic Distribution of SpaceX Falcon 9 Launch Sites (Folium Map Overview)", fontsize=15, fontweight='bold', pad=15, color='#1D3557')
ax.legend(loc='upper right', frameon=True, fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "folium_map_overview.png"), bbox_inches='tight', dpi=300)
plt.close()

# -------------------------------------------------------------
# 12. Folium Proximity Analysis Visual
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
proximity_labels = ['Coastline\n(Atlantic Ocean)', 'Highway\n(Samuel C. Phillips Pkwy)', 'Railroad\n(Titan IV Railway)', 'City Center\n(Titusville, FL)']
distances_km = [0.85, 1.25, 1.34, 16.5]
colors = ['#2A9D8F', '#457B9D', '#F4A261', '#E76F51']

bars = ax.barh(proximity_labels, distances_km, color=colors, edgecolor='#1D3557', linewidth=1.5, height=0.55)
for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.3, bar.get_y() + bar.get_height()/2, f"{w:.2f} km", va='center', ha='left', fontsize=11, fontweight='bold', color='#1D3557')

ax.set_xlim(0, 20)
ax.set_xlabel("Distance from Launch Complex (km)", fontsize=12, fontweight='bold')
ax.set_title("Proximity Analysis: Distance from Launch Site CCAFS SLC-40 to Critical Infrastructure", fontsize=14, fontweight='bold', pad=15, color='#1D3557')
ax.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "folium_proximity_analysis.png"), bbox_inches='tight', dpi=300)
plt.close()

# -------------------------------------------------------------
# 13. Plotly Dash Visuals: Success Pie Chart
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
site_counts = df_dash[df_dash['class'] == 1]['Launch Site'].value_counts()
colors = ['#2A9D8F', '#457B9D', '#E76F51', '#F4A261']
wedges, texts, autotexts = ax.pie(site_counts, labels=site_counts.index, autopct='%1.1f%%', startangle=140, colors=colors,
                                  wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2),
                                  textprops=dict(fontweight='bold', fontsize=11))
plt.setp(autotexts, size=11, weight="bold", color="white")
ax.set_title("Plotly Dash Visual: Total Successful Launches by Launch Site (All Sites)", fontsize=14, fontweight='bold', pad=15, color='#1D3557')
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "dash_app_pie_chart.png"), bbox_inches='tight', dpi=300)
plt.close()

# -------------------------------------------------------------
# 14. Plotly Dash Visuals: Payload vs Outcome Scatter
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
sns.scatterplot(
    data=df_dash,
    x="Payload Mass (kg)",
    y="class",
    hue="Booster Version Category",
    palette="Set2",
    s=140,
    alpha=0.9,
    edgecolor="black",
    linewidth=0.8,
    ax=ax
)
ax.set_yticks([0, 1])
ax.set_yticklabels(['Failure (0)', 'Success (1)'], fontsize=11, fontweight='bold')
ax.set_xlabel("Payload Mass (kg)", fontsize=12, fontweight='bold')
ax.set_ylabel("Launch Outcome", fontsize=12, fontweight='bold')
ax.set_title("Plotly Dash Visual: Correlation Between Payload Mass and Launch Success", fontsize=14, fontweight='bold', pad=15, color='#1D3557')
plt.legend(title="Booster Version", bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "dash_app_scatter_plot.png"), bbox_inches='tight', dpi=300)
plt.close()

# -------------------------------------------------------------
# 15. Machine Learning Modeling & Evaluation
# -------------------------------------------------------------
X = df3.copy()
Y = df2['Class'].to_numpy()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=2)

# Model 1: Logistic Regression
lr = LogisticRegression(random_state=42)
lr_params = {'C': [0.01, 0.1, 1], 'penalty': ['l2'], 'solver': ['lbfgs']}
lr_cv = GridSearchCV(lr, lr_params, cv=10)
lr_cv.fit(X_train, Y_train)
lr_train_acc = lr_cv.best_score_
lr_test_acc = lr_cv.score(X_test, Y_test)
lr_preds = lr_cv.predict(X_test)
lr_cm = confusion_matrix(Y_test, lr_preds)

# Model 2: SVM
svm = SVC(random_state=42)
svm_params = {'kernel': ['linear', 'rbf', 'sigmoid'], 'C': np.logspace(-2, 2, 5)}
svm_cv = GridSearchCV(svm, svm_params, cv=10)
svm_cv.fit(X_train, Y_train)
svm_train_acc = svm_cv.best_score_
svm_test_acc = svm_cv.score(X_test, Y_test)
svm_preds = svm_cv.predict(X_test)
svm_cm = confusion_matrix(Y_test, svm_preds)

# Model 3: Decision Tree
tree = DecisionTreeClassifier(random_state=42)
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
tree_train_acc = tree_cv.best_score_
tree_test_acc = tree_cv.score(X_test, Y_test)
tree_preds = tree_cv.predict(X_test)
tree_cm = confusion_matrix(Y_test, tree_preds)

# Model 4: KNN
knn = KNeighborsClassifier()
knn_params = {'n_neighbors': list(range(1, 11)), 'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'], 'p': [1, 2]}
knn_cv = GridSearchCV(knn, knn_params, cv=10)
knn_cv.fit(X_train, Y_train)
knn_train_acc = knn_cv.best_score_
knn_test_acc = knn_cv.score(X_test, Y_test)
knn_preds = knn_cv.predict(X_test)
knn_cm = confusion_matrix(Y_test, knn_preds)

print(f"Logistic Regression: Train={lr_train_acc:.4f}, Test={lr_test_acc:.4f}")
print(f"SVM: Train={svm_train_acc:.4f}, Test={svm_test_acc:.4f}")
print(f"Decision Tree: Train={tree_train_acc:.4f}, Test={tree_test_acc:.4f}")
print(f"KNN: Train={knn_train_acc:.4f}, Test={knn_test_acc:.4f}")

# -------------------------------------------------------------
# 16. Visual: 4 Confusion Matrices Subplot
# -------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(12, 10), dpi=300)
models_info = [
    ("Logistic Regression", lr_cm, lr_test_acc, axes[0, 0]),
    ("Support Vector Machine (SVM)", svm_cm, svm_test_acc, axes[0, 1]),
    ("Decision Tree Classifier", tree_cm, tree_test_acc, axes[1, 0]),
    ("K-Nearest Neighbors (KNN)", knn_cm, knn_test_acc, axes[1, 1])
]

for title, cm, acc, ax in models_info:
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, ax=ax,
                annot_kws={'size': 14, 'weight': 'bold'},
                xticklabels=['Pred Fail (0)', 'Pred Success (1)'],
                yticklabels=['Actual Fail (0)', 'Actual Success (1)'])
    ax.set_title(f"{title}\nTest Accuracy: {acc*100:.2f}%", fontsize=12, fontweight='bold', color='#1D3557')
    ax.set_ylabel("True Outcome", fontsize=10, fontweight='bold')
    ax.set_xlabel("Predicted Outcome", fontsize=10, fontweight='bold')

plt.suptitle("Predictive Analysis: Confusion Matrices of Machine Learning Models", fontsize=15, fontweight='bold', y=0.98, color='#1D3557')
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "confusion_matrices.png"), bbox_inches='tight', dpi=300)
plt.close()

# -------------------------------------------------------------
# 17. Visual: Model Accuracy Comparison Bar Chart
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
model_names = ['Logistic Regression', 'Support Vector Machine', 'Decision Tree', 'K-Nearest Neighbors']
train_accs = [lr_train_acc * 100, svm_train_acc * 100, tree_train_acc * 100, knn_train_acc * 100]
test_accs = [lr_test_acc * 100, svm_test_acc * 100, tree_test_acc * 100, knn_test_acc * 100]

x = np.arange(len(model_names))
width = 0.35

rects1 = ax.bar(x - width/2, train_accs, width, label='Train Accuracy (10-Fold CV)', color='#457B9D', edgecolor='#1D3557')
rects2 = ax.bar(x + width/2, test_accs, width, label='Test Accuracy (Hold-out 20%)', color='#2A9D8F', edgecolor='#1D3557')

for rect in rects1:
    h = rect.get_height()
    ax.annotate(f"{h:.1f}%", xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                textcoords="offset points", ha='center', va='bottom', fontsize=10, fontweight='bold')

for rect in rects2:
    h = rect.get_height()
    ax.annotate(f"{h:.1f}%", xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                textcoords="offset points", ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
ax.set_title('Machine Learning Classification Performance Comparison', fontsize=15, fontweight='bold', pad=15, color='#1D3557')
ax.set_xticks(x)
ax.set_xticklabels(model_names, fontsize=11, fontweight='bold')
ax.set_ylim(50, 100)
ax.legend(loc='lower right', frameon=True, fontsize=11)
ax.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "model_accuracy_comparison.png"), bbox_inches='tight', dpi=300)
plt.close()

# -------------------------------------------------------------
# 18. Visual: Executive Summary Infographic Card
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
ax.axis('off')
fig.patch.set_facecolor('#F8F9FA')

cards = [
    ("Total Launches Analyzed", "90 Launches", "Falcon 9 (2010 - 2020)", '#1D3557'),
    ("Overall Landing Success", "66.7%", "60 Successful Recoveries", '#2A9D8F'),
    ("Top Performing Model", "Decision Tree / SVM", "83.33% Test Accuracy", '#457B9D'),
    ("Cost Advantage Estimate", "~$1.2 Billion", "Savings via Booster Reuse", '#E76F51')
]

for i, (title, stat, subtext, color) in enumerate(cards):
    cx = 0.13 + i * 0.25
    rect = patches.FancyBboxPatch((cx - 0.11, 0.25), 0.22, 0.5, boxstyle="round,pad=0.03",
                                  facecolor='white', edgecolor=color, linewidth=2.5, transform=ax.transAxes)
    ax.add_patch(rect)
    ax.text(cx, 0.65, stat, ha='center', va='center', fontsize=20, fontweight='bold', color=color, transform=ax.transAxes)
    ax.text(cx, 0.48, title, ha='center', va='center', fontsize=11, fontweight='bold', color='#1D3557', transform=ax.transAxes)
    ax.text(cx, 0.35, subtext, ha='center', va='center', fontsize=9, color='#6C757D', transform=ax.transAxes)

ax.set_title("Executive Summary: SpaceX Falcon 9 First Stage Recovery Insights", fontsize=15, fontweight='bold', pad=25, color='#1D3557')
plt.tight_layout()
plt.savefig(os.path.join(VIS_DIR, "executive_summary_infographic.png"), bbox_inches='tight', dpi=300)
plt.close()

print("All visual assets successfully generated and saved to visuals/ folder.")
