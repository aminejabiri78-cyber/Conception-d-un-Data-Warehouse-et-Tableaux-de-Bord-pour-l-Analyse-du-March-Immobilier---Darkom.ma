from sqlalchemy import text
from src.logger import get_logger

logger = get_logger("staging")

def load_to_staging(df, engine):

    try:
        sql_path = r"C:\Users\AMINE JBR\Downloads\Conception-d-un-Data-Warehouse-et-Tableaux-de-Bord-pour-l-Analyse-du-March-Immobilier---Darkom.ma-main\sql\staging.sql"
        logger.info("Loading staging SQL file...")

        with open(sql_path, "r", encoding="utf-8") as f:
            staging_sql = f.read()

        logger.info("Executing staging SQL...")

        with engine.begin() as con:
            con.execute(text(staging_sql))

        logger.info("Inserting data into staging_darkom...")

        df.to_sql(
            "staging_darkom",
            con=engine,
            schema="raw_darkom",
            if_exists="append",
            index=False
        )

        logger.info(f"STAGING load successful  Shape: {df.shape}")

        return df

    except FileNotFoundError:
        logger.error("staging.sql file not found ")
        return None

    except Exception as e:
        logger.error(f"Error while loading to staging : {e}")
        return None