from src.extract import extract_data
from src.load_db import get_engine
from src.staging import load_to_staging
from src.clean import etl_darkom_clean
from src.warhouse import load_power_bi

def main():

    df = extract_data()

    engine = get_engine()

    load_to_staging(df, engine)

    df=etl_darkom_clean()
    
    df=load_power_bi()

if __name__ == "__main__":
    main()