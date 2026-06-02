import pandas as pd
from src.logger import get_logger

logger = get_logger("extract")

def extract_data():
    try:
        path = r"C:\Users\AMINE JBR\Downloads\Conception-d-un-Data-Warehouse-et-Tableaux-de-Bord-pour-l-Analyse-du-March-Immobilier---Darkom.ma-main\data\raw\darkom-annonces.csv"

        logger.info(f"Loading data from {path}")

        df = pd.read_csv(path)

        logger.info(f"Data loaded successfully  Shape: {df.shape}")

        return df

    except FileNotFoundError:
        logger.error("CSV file not found ")
        return None

    except Exception as e:
        logger.error(f"Error while loading data : {e}")
        return None