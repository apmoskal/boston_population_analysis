from pathlib import Path
from loguru import logger
from tqdm import tqdm
import typer
import pandas as pd  # for data manipulation

from boston_population_analysis.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

app = typer.Typer()

@app.command()
def main(
    input_path: Path = RAW_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
):
    # ---- DEBUG LOGGING ----
    logger.info(f"Project root: {PROCESSED_DATA_DIR.parent.resolve()}")
    logger.info(f"Reading raw data from: {input_path.resolve()}")
    
    # ---- READ RAW DATA ----
    if not input_path.exists():
        logger.error(f"Input file not found: {input_path.resolve()}")
        raise FileNotFoundError(f"Cannot find raw dataset at {input_path}")
    
    df = pd.read_csv(input_path)
    logger.info(f"Raw dataset loaded with shape: {df.shape}")

    # ---- SIMPLE DATA CLEANING ----
    # 1. Drop a column (if exists)
    if "shape_wkt" in df.columns:
        df = df.drop(columns=["shape_wkt"])
        logger.info("Dropped column 'shape_wkt'")

    # 2. Rename a column (if exists)
    if "name" in df.columns:
        df = df.rename(columns={"name": "boston_area_name"})
        logger.info("Renamed column 'name' -> 'boston_area_name'")

    # 3. Filter rows (optional)
    if "arealand" in df.columns:
        original_rows = df.shape[0]
        df = df[df["arealand"] > 1]
        logger.info(f"Filtered rows on 'arealand'>1: {original_rows} -> {df.shape[0]}")

    # ---- WRITE CLEANED DATA ----
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.success(f"Processed dataset written to: {output_path.resolve()}")

if __name__ == "__main__":
    app()
