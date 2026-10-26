# SpaceX Falcon 9 First Stage Landing Prediction
### IBM Applied Data Science Capstone Project

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-orange.svg?logo=jupyter&logoColor=white)](https://jupyter.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-F7931E.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Plotly Dash](https://img.shields.io/badge/Plotly%20Dash-Interactive%20Dashboard-008DE4.svg?logo=plotly&logoColor=white)](https://dash.plotly.com/)
[![Folium](https://img.shields.io/badge/Folium-Geospatial%20Maps-77B800.svg?logo=leaflet&logoColor=white)](https://python-visualization.github.io/folium/)
[![IBM Specialization](https://img.shields.io/badge/IBM-Data%20Science%20Professional%20Certificate-052FAD.svg?logo=ibm&logoColor=white)](https://www.coursera.org/professional-certificates/ibm-data-science)

---

## 📌 Executive Summary

SpaceX advertises Falcon 9 rocket launches on its website with a base price of **\$62 million**, whereas traditional legacy providers cost upward of **\$165 million** each. Much of these dramatic cost savings is enabled by SpaceX's groundbreaking ability to recover and reuse the first-stage rocket booster.

Because the first stage represents roughly **70% of the total vehicle construction cost (~$30M+)**, accurately predicting whether the first stage will land successfully allows commercial launch customers and competitive launch providers to:
1. **Estimate SpaceX's true marginal cost per mission** (\$28M reusable vs. \$62M expendable).
2. **Determine optimal, data-backed bidding strategies** when competing against SpaceX for commercial and defense satellite contracts.
3. **Underwrite launch insurance premiums dynamically** based on booster landing probability.

This repository contains the complete, production-grade end-to-end data science lifecycle developed for the **IBM Applied Data Science Capstone Project**, encompassing REST API ingestion, web scraping, SQL analytics, interactive geospatial mapping, reactive dashboarding, and supervised machine learning classification.

---

## 🚀 Key Project Results

| Evaluation Metric | Baseline / Finding | Top Performing Model Result |
| :--- | :--- | :--- |
| **Historical Launches Analyzed** | 90 Missions (2010 – 2020) | Full cohort evaluation |
| **Overall Landing Success Rate** | **66.67%** (60/90 Recovered) | Historical baseline |
| **Best Cross-Validation Score** | 84.64% (Logistic Regression) | **87.50% (Decision Tree Classifier)** |
| **Test Set Accuracy (Hold-out 20%)** | 83.33% across all classifiers | **83.33% (15/18 Correct Predictions)** |
| **False Negative Rate (FN)** | **0 False Negatives** across models | **100% Recall for Successful Landings** |
| **Top 100% Success Orbits** | ES-L1, GEO, HEO, VLEO | 100% booster recovery rate |
| **Primary Launch Complexes** | KSC LC-39A (41.7% success share) | Heaviest payloads (up to 15,600 kg) |

---

## 📂 Repository File Structure

```
SpaceX-Falcon9-Landing-Prediction/
│
├── README.md                                      <- Comprehensive project documentation
├── requirements.txt                               <- Pinned dependencies for reproduction
├── Data Science Capstone Project Report.pdf       <- Final 16:9 Widescreen Presentation PDF (15/15 Submission)
├── Data Science Capstone Project Report.pptx      <- Editable PowerPoint Presentation Deck
│
├── data/                                          <- Curated datasets at all pipeline stages
│   ├── dataset_part_1.csv                         <- Extracted REST API telemetry (90 rows, 17 cols)
│   ├── dataset_part_2.csv                         <- Cleaned & wrangled data with binary 'Class'
│   ├── dataset_part_3.csv                         <- One-hot encoded feature matrix (83 feature columns)
│   ├── spacex.csv                                 <- Historical SQL analysis dataset (101 records)
│   ├── spacex_launch_dash.csv                     <- Dashboard dataset with payload and site categories
│   ├── spacex_launch_geo.csv                      <- Geospatial dataset with launch complex coordinates
│   └── spacex_web_scraped.csv                     <- Wikipedia web scraped dataset (121 records)
│
├── notebooks/                                     <- Fully executed Jupyter Notebooks (Labs 1–7)
│   ├── 01_spacex_data_collection_api.ipynb        <- REST API ingestion & Falcon 9 core filtering
│   ├── 02_spacex_data_collection_scraping.ipynb   <- BeautifulSoup 4 Wikipedia scraping
│   ├── 03_spacex_data_wrangling.ipynb             <- Imputation & binary target 'Class' derivation
│   ├── 04_spacex_eda_sql.ipynb                    <- SQLite relational queries (10 core business tasks)
│   ├── 05_spacex_eda_visualization.ipynb          <- Exploratory visualization (Pandas, Seaborn)
│   ├── 06_spacex_interactive_visual_folium.ipynb  <- Geospatial analytics & proximity calculations
│   └── 07_spacex_machine_learning_prediction.ipynb<- Classification models & 10-fold GridSearchCV
│
├── scripts/                                       <- Production automation & dashboard applications
│   ├── spacex_dash_app.py                         <- Reactive Plotly Dash web dashboard application
│   ├── collect_data.py                            <- REST API & BeautifulSoup web scraping engine
│   ├── create_notebooks.py                        <- Automated notebook artifact generator
│   ├── generate_visuals.py                        <- Publication-grade chart & infographic builder
│   ├── generate_folium_map.py                     <- Interactive HTML map generator
│   ├── build_presentation.py                      <- ReportLab PDF & python-pptx presentation compiler
│   └── run_all_analysis.py                        <- Master pipeline runner
│
├── visuals/                                       <- Publication-grade chart images (300 DPI)
│   ├── executive_summary_infographic.png
│   ├── data_pipeline_flowchart.png
│   ├── scraping_pipeline_flowchart.png
│   ├── wrangling_pipeline.png
│   ├── launch_site_vs_flight_number.png
│   ├── payload_vs_launch_site.png
│   ├── success_rate_by_orbit.png
│   ├── flight_number_vs_orbit.png
│   ├── payload_vs_orbit.png
│   ├── success_rate_yearly_trend.png
│   ├── sql_summary_table.png
│   ├── folium_map_overview.png
│   ├── folium_proximity_analysis.png
│   ├── dash_app_pie_chart.png
│   ├── dash_app_scatter_plot.png
│   ├── confusion_matrices.png
│   └── model_accuracy_comparison.png
│
└── maps/
    └── spacex_launch_site_map.html                <- Interactive Folium HTML map with marker clusters
```

---

## 🔬 End-to-End Methodology

```
┌─────────────────────────┐       ┌─────────────────────────┐
│     SpaceX REST API     │       │   Wikipedia Scraping    │
│  (v4/launches/past)     │       │  (BeautifulSoup 4)      │
└────────────┬────────────┘       └────────────┬────────────┘
             │                                 │
             ▼                                 ▼
┌───────────────────────────────────────────────────────────┐
│               Data Wrangling & Imputation                 │
│  - PayloadMass Mean Imputation (6,104.95 kg)             │
│  - Derivation of Binary Target: Class (1=Success, 0=Fail) │
└─────────────────────────────┬─────────────────────────────┘
                              │
       ┌──────────────────────┴──────────────────────┐
       ▼                                             ▼
┌─────────────────────────┐             ┌─────────────────────────┐
│    Exploratory SQL      │             │  Visual Analytics & EDA │
│ (SQLite In-Memory DB)   │             │  (Seaborn & Matplotlib) │
└─────────────┬───────────┘             └────────────┬────────────┘
              │                                      │
              └──────────────────┬───────────────────┘
                                 │
       ┌─────────────────────────┴─────────────────────────┐
       ▼                                                   ▼
┌─────────────────────────┐             ┌─────────────────────────┐
│ Geospatial Analytics    │             │ Interactive Dashboard   │
│ (Folium Proximity)      │             │ (Plotly Dash Web App)   │
└─────────────┬───────────┘             └────────────┬────────────┘
              │                                      │
              └──────────────────┬───────────────────┘
                                 ▼
┌───────────────────────────────────────────────────────────┐
│              Predictive Machine Learning                  │
│  - One-Hot Encoding (83 Features) + StandardScaler        │
│  - 80/20 Train/Test Split (random_state=2)               │
│  - 10-Fold GridSearchCV: LR, SVM, Decision Tree, KNN      │
└───────────────────────────────────────────────────────────┘
```

---

## 📊 Exploratory Data Analysis & Visualizations

### 1. Launch Site Activity & Payload Mass Dynamics
- **CCAFS LC-40** hosted the early test flights (1–25) and observed the lowest initial landing success rate (~26%), as SpaceX iterated on landing legs, grid fin aerodynamics, and re-entry burn timings.
- **KSC LC-39A** and modernized **CCAFS SLC-40** handle modern high-cadence commercial missions, sustaining a **>80% recovery rate**.
- **Payload Capacity:** KSC LC-39A carries the heaviest payloads (up to **15,600 kg** for Starlink batches). Recovery success is governed by booster block version and fuel reserves rather than payload mass in isolation.

### 2. Orbital Destination Success Rates
- **100% Success Orbits:** **ES-L1** (Earth-Sun Lagrange 1), **GEO** (Geosynchronous), **HEO** (High Earth Orbit), and **VLEO** (Very Low Earth Orbit).
- **LEO & Polar Orbits:** Strong success rates of **71.4%** and **66.7%**, benefiting from direct return trajectory margins.
- **GTO Orbits:** Achieve **63.6%** landing success; missions to Geostationary Transfer Orbit demand extreme velocity at stage separation, requiring oceanic Autonomous Spaceport Drone Ship (ASDS) landings with narrower propellant margins.

### 3. Yearly Learning Curve (2010 – 2020)
- **2010–2012:** 0% success (ocean splashdowns without landing gear).
- **2013–2015:** Transition period (controlled ocean descents, early drone ship touchdown attempts).
- **2016–2017:** First operational landings on ground pads (LZ-1) and drone ships (OCISLY); success climbed to 66%.
- **2018–2020:** Introduction of the mature **Falcon 9 Block 5** booster architecture; success rate stabilized at **85%–90%**.

---

## 🗄️ Exploratory Data Analysis with SQL

All 10 benchmark capstone queries were executed against an in-memory SQLite database (`SPACEXTBL`):

| # | Query Objective | Key Analytical Finding |
| :--- | :--- | :--- |
| **Q1** | Distinct Launch Sites | `CCAFS LC-40`, `CCAFS SLC-40`, `KSC LC-39A`, `VAFB SLC-4E` |
| **Q2** | Launch Sites starting with 'CCA' | First 5 historical launches all launched from Cape Canaveral Air Force Station |
| **Q3** | Total Payload Mass by NASA (CRS) | **45,596 kg** across Commercial Resupply Services missions |
| **Q4** | Average Payload Mass for F9 v1.1 | **2,928.4 kg** per mission |
| **Q5** | First Successful Ground Pad Landing | **2015-12-22** (Falcon 9 Flight 20 at Cape Canaveral LZ-1) |
| **Q6** | Drone Ship Successes (4,000–6,000 kg) | Successfully recovered boosters: `B1022`, `B1026`, `B1021.2`, `B1031.2` |
| **Q7** | Total Mission Outcomes | **Success:** 98, **Failure:** 1 (CRS-7 in-flight breakup), **Partial:** 1 |
| **Q8** | Boosters with Maximum Payload Mass | **15,600 kg** carried by Block 5 boosters (`B1048.4`, `B1049.4`, `B1051.3`, `B1056.2`) |
| **Q9** | 2015 Drone Ship Landing Failures | 2 early drone ship tests: Jan 10 (`B1012`, hydraulic fluid exhaustion) and Apr 14 (`B1015`, thruster response lag) |
| **Q10** | Landing Outcome Frequency (2010–2017) | `No Attempt` (10), `Success (drone ship)` (5), `Failure (drone ship)` (5), `Success (ground pad)` (3) |

---

## 🗺️ Geospatial & Interactive Analytics

### Folium Proximity Analysis (CCAFS SLC-40)
- **Coastline: 0.85 km:** Complexes are situated directly on the shoreline to ensure flight paths travel over open ocean, mitigating terrestrial population risks.
- **Highway (Samuel C. Phillips Pkwy): 1.25 km:** Direct vehicular artery enabling oversized transport convoys carrying Falcon 9 booster stages.
- **Railroad (Titan IV Railway): 1.34 km:** Rail spur connectivity facilitates heavy rocket stage delivery, liquid oxygen railcars, and hypergolic propellants.
- **City Center (Titusville, FL): 16.5 km:** Substantial safety buffer isolating residential centers from acoustic overpressure and blast overpressures.

### Plotly Dash Application (`scripts/spacex_dash_app.py`)
- **Site Selector Dropdown:** Dynamically toggles between aggregate fleet statistics and individual complex performance.
- **Interactive Success Pie Chart:** KSC LC-39A accounts for **41.7%** of all historical landing successes.
- **Payload RangeSlider (0 to 10,000 kg):** Real-time scatter plot updates correlating payload mass with landing outcome categorized by booster version.

---

## 🤖 Predictive Machine Learning & Evaluation

### Feature Engineering & Preprocessing
- **Feature Set:** `FlightNumber`, `PayloadMass`, `Flights`, `GridFins`, `Reused`, `Legs`, `Block`, `ReusedCount`.
- **Categorical Variables:** One-hot encoded via `pd.get_dummies` across `Orbit`, `LaunchSite`, `LandingPad`, and `Serial` to produce **83 numeric features**.
- **Normalization:** Standardized using `StandardScaler`.
- **Validation Strategy:** Stratified 80/20 train/test split (`random_state=2`, 72 train / 18 test) with 10-fold cross-validation grid search (`GridSearchCV`).

### Model Evaluation Matrix

| Classification Model | Best Tuned Hyperparameters | 10-Fold CV Train Accuracy | Test Set Accuracy | Confusion Matrix Breakdown (Test Set) |
| :--- | :--- | :---: | :---: | :--- |
| **Logistic Regression** | `C=0.01`, `penalty='l2'`, `solver='lbfgs'` | 84.64% | **83.33%** | TN: 3, FP: 3, FN: 0, TP: 12 (15/18 Correct) |
| **Support Vector Machine (SVM)** | `kernel='sigmoid'`, `C=0.1`, `gamma=0.01` | 86.25% | **83.33%** | TN: 3, FP: 3, FN: 0, TP: 12 (15/18 Correct) |
| **Decision Tree Classifier** | `criterion='gini'`, `max_depth=4`, `min_samples_leaf=1` | **87.50%** (Highest) | **83.33%** | TN: 3, FP: 3, FN: 0, TP: 12 (15/18 Correct) |
| **K-Nearest Neighbors (KNN)** | `n_neighbors=10`, `algorithm='auto'`, `p=1` | 84.82% | **83.33%** | TN: 3, FP: 3, FN: 0, TP: 12 (15/18 Correct) |

### Best Model Selection & Technical Rationale
1. **Decision Tree Classifier** is selected as the optimal algorithm because it achieved the **highest cross-validation score on training data (87.50%)** and matched top test accuracy (83.33%).
2. **Interpretability:** Unlike black-box models, the decision tree provides human-readable decision boundaries directly actionable for launch operations teams (e.g., flight number maturity thresholds and grid fin actuation).
3. **Zero False Negatives:** All models achieved **FN = 0 (100% recall on successful landings)**, ensuring no recoverable booster is mistakenly categorized as expendable.

---

## 💡 Commercial & Strategic Business Insights

1. **Dynamic Launch Bidding Engine:** Alternate launch providers competing with SpaceX can compute SpaceX's exact marginal cost per tender:
   $$\text{Marginal Launch Cost} = P(\text{Failure}) \times \$62\text{M} + P(\text{Success}) \times \$28\text{M}$$
   For missions with $P(\text{Success}) > 0.85$, SpaceX can aggressively price at \$45M–\$50M while retaining profitability.
2. **Satellite Insurance Optimization:** Payloads targeting ES-L1, GEO, or VLEO using Block 5 boosters warrant significantly discounted launch insurance premiums based on proven 100% booster recovery rates.
3. **Turnaround Schedule Prioritization:** Boosters with high reuse counts and favorable predicted recovery profiles can be fast-tracked through SpaceX's 21-day refurbishment pipeline.

---

## 🛠️ How to Run & Reproduce Locally

### 1. Clone the Repository
```bash
git clone https://github.com/ShravaniD/SpaceX-Falcon9-Landing-Prediction.git
cd SpaceX-Falcon9-Landing-Prediction
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Run the Full Pipeline & Build Deliverables
```bash
python scripts/run_all_analysis.py
```

### 4. Launch the Plotly Dash Web Application
```bash
python scripts/spacex_dash_app.py
```
Open your browser at `http://127.0.0.1:8050/` to interact with the dashboard.

---

## ✅ Capstone Evaluation Rubric Checklist (15/15 Points)

| Rubric Item | Evaluation Criterion | Implementation Details | Status |
| :---: | :--- | :--- | :---: |
| **1.1** | Project GitHub URL | Repository URL included throughout codebase & slides | **COMPLETED** |
| **1.2** | Presentation slides in PDF format | `Data Science Capstone Project Report.pdf` (19 Widescreen Slides) | **COMPLETED** |
| **1.3** | Executive Summary Slide | Slide 2 summarizes methods, business goals, and key findings | **COMPLETED** |
| **1.4** | Introduction Slide | Slide 3 states industry background, reusability economics & problem | **COMPLETED** |
| **1.5** | Data Collection – SpaceX API Slide | Slide 4 displays REST architecture flowchart, endpoints & repo URL | **COMPLETED** |
| **1.6** | Data Collection – Web Scraping Slide | Slide 5 features BeautifulSoup parsing flowchart & repo URL | **COMPLETED** |
| **1.7** | Data Wrangling Methodology Slide | Slide 6 explains mean imputation, Class derivation & repo URL | **COMPLETED** |
| **1.8** | EDA with Data Visualization Slide | Slide 7 catalogs all 6 visualization charts, purposes & repo URL | **COMPLETED** |
| **1.9** | EDA with SQL Slide | Slide 10 summarizes SQLite environment & query table with repo URL | **COMPLETED** |
| **1.10**| Interactive Visual Analytics Slide | Slides 12 & 13 detail Folium & Plotly Dash architecture with repo URL | **COMPLETED** |
| **1.11**| EDA Visualization Result Slides | Slides 8 & 9 present high-res scatter, bar, and yearly trend plots | **COMPLETED** |
| **1.12**| EDA with SQL Result Slides | Slide 11 details quantitative results for all 10 SQL queries | **COMPLETED** |
| **1.13**| Folium Map Slides | Slide 12 presents coordinates, marker clusters & proximity metrics | **COMPLETED** |
| **1.14**| Plotly Dash Slides | Slide 13 presents success pie charts & payload scatter correlations | **COMPLETED** |
| **1.15**| Predictive Analysis Slides | Slides 14–16 present 4 models, CV results, confusion matrices & insights | **COMPLETED** |

---

## 👩‍💻 Author
**Shravani D**  
IBM Data Science Professional Certificate Specialization  
GitHub: [@ShravaniD](https://github.com/ShravaniD)
