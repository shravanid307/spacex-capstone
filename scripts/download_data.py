import os
import urllib.request
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(DATA_DIR, exist_ok=True)

DATASETS = {
    "dataset_part_1.csv": "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv",
    "dataset_part_2.csv": "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv",
    "dataset_part_3.csv": "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv",
    "spacex.csv": "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex.csv",
    "spacex_launch_dash.csv": "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv",
    "spacex_launch_geo.csv": "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv",
}

print("Starting dataset download...")
for filename, url in DATASETS.items():
    dest_path = os.path.join(DATA_DIR, filename)
    try:
        print(f"Downloading {filename} from {url}...")
        urllib.request.urlretrieve(url, dest_path)
        df = pd.read_csv(dest_path)
        print(f" -> Successfully saved {filename} ({len(df)} rows, {len(df.columns)} columns)")
    except Exception as e:
        print(f" -> Error downloading {filename}: {e}")

print("Dataset download completed.")
