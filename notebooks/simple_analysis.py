import sys
from pathlib import Path

import pandas as pd
from loguru import logger

# Add the project root to sys.path so Python can find boston_population_analysis
sys.path.append(str(Path(__file__).resolve().parents[1]))

from boston_population_analysis.config import PROCESSED_DATA_DIR

# Load processed dataset
df = pd.read_csv(PROCESSED_DATA_DIR / "dataset.csv")
logger.info(f"Dataset loaded with {len(df)} rows and {len(df.columns)} columns")

# Simple analysis: calculate the average of 'arealand_sqmi' column
if "arealand_sqmi" in df.columns:
    avg_arealand = df["arealand_sqmi"].mean()
    # Print to console
    print(f"Average arealand: {avg_arealand}")
    # Log it
    logger.info(f"Average arealand: {avg_arealand}")
else:
    print("Column 'arealand_sqmi' not found in dataset")
    logger.warning("Column 'arealand_sqmi' not found in dataset")

