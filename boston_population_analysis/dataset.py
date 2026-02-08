from pathlib import Path
from loguru import logger
from tqdm import tqdm
import typer
import pandas as pd  # we need pandas for data manipulation

from boston_population_analysis.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

app = typer.Typer()

@app.command()
def main(
    input_path: Path = RAW_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
):
    # ---- SIMPLE DATA CLEANING ----
    logger.info(f"Reading raw data from {input_path}...")
    df = pd.read_csv(input_path)

    # Example cleaning steps:
    # 1. Drop a column (if exists)
    if "shape_wkt" in df.columns:
        df = df.drop(columns=["shape_wkt"])

    # 2. Rename a column (if exists)
    if "name" in df.columns:
        df = df.rename(columns={"name": "boston_area_name"})

    # 3. Filter rows (optional)
    df = df[df["arealand"] > 1]  # example filter

    # Save cleaned dataset
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.success(f"Processed dataset written to {output_path}")
