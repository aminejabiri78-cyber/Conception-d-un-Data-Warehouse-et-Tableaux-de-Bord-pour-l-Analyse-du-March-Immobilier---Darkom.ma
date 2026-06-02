from sqlalchemy import create_engine, text
import pandas as pd

from src.load_db import get_engine
from src.logger import get_logger


# ENGINE + LOGGER

def load_power_bi():
    engine = get_engine()
    logger = get_logger(__name__)
    
    
    # EXECUTE STAR SCHEMA SQL
    
    
    with engine.begin() as con:
    
        path_file = r"C:\Users\AMINE JBR\Downloads\Conception-d-un-Data-Warehouse-et-Tableaux-de-Bord-pour-l-Analyse-du-March-Immobilier---Darkom.ma-main\sql\star_schema.sql"
    
        with open(path_file, "r", encoding="utf-8") as f:
            sql_script = f.read()
    
        con.exec_driver_sql(sql_script)
    
    logger.info("Star schema créé avec succès")
    
    
    # READ CLEAN DATA
    
    
    df = pd.read_sql(
        "SELECT * FROM schema_clean_darkom.darkom_clean",
        engine
    )
    
    df.columns = df.columns.str.lower()
    
    logger.info("Données chargées depuis darkom_clean")
    
    
    # FIX DATE TYPE
    
    
    df["date_publication"] = pd.to_datetime(
        df["date_publication"]
    )
    
    
    # CREATE DIM_DATE
    
    
    dim_date = df[
        [
            "date_publication",
            "annee_publication",
            "mois_publication",
            "trimestre_publication"
        ]
    ].drop_duplicates()
    
    dim_date.to_sql(
        con=engine,
        schema="star_schema_darkom",
        name="dim_date",
        if_exists="append",
        index=False
    )
    
    logger.info("dim_date chargée")
    
    # CREATE DIM_LOCATION
    
    
    dim_location = df[
        [
            "quartier",
            "ville"
        ]
    ].drop_duplicates()
    
    dim_location.to_sql(
        con=engine,
        schema="star_schema_darkom",
        name="dim_location",
        if_exists="append",
        index=False
    )
    
    logger.info("dim_location chargée")
    
    
    # CREATE DIM_PROPERTY
    
    
    dim_property = df[
        [
            "titre",
            "type_bien",
            "transaction",
            "categorie_prix",
            "categorie_surface",
            "annee_construction"
        ]
    ].drop_duplicates()
    
    dim_property.to_sql(
        con=engine,
        schema="star_schema_darkom",
        name="dim_property",
        if_exists="append",
        index=False
    )
    
    logger.info("dim_property chargée")
    
    
    # READ DIMENSIONS FROM DB
    
    
    dim_date_db = pd.read_sql(
        "SELECT * FROM star_schema_darkom.dim_date",
        engine
    )
    
    dim_location_db = pd.read_sql(
        "SELECT * FROM star_schema_darkom.dim_location",
        engine
    )
    
    dim_property_db = pd.read_sql(
        "SELECT * FROM star_schema_darkom.dim_property",
        engine
    )
    
    
    # FIX DATE TYPE AGAIN
    
    
    dim_date_db["date_publication"] = pd.to_datetime(
        dim_date_db["date_publication"]
    )
    
    
    # MERGE DATE DIMENSION
    
    
    df = df.merge(
        dim_date_db,
        on=[
            "date_publication",
            "annee_publication",
            "mois_publication",
            "trimestre_publication"
        ],
        how="left"
    )
    
    
    # MERGE LOCATION DIMENSION
    
    df = df.merge(
        dim_location_db,
        on=[
            "quartier",
            "ville"
        ],
        how="left"
    )
    
    # MERGE PROPERTY DIMENSION
    
    df = df.merge(
        dim_property_db,
        on=[
            "titre",
            "type_bien",
            "transaction",
            "categorie_prix",
            "categorie_surface",
            "annee_construction"
        ],
        how="left"
    )
    
    logger.info("Merges terminés")
    
    # CREATE FACT TABLE
    
    fact_darkom = df[
        [
            "annonce_id",
            "date_id",
            "location_id",
            "property_id",
            "prix",
            "surface",
            "prix_m2",
            "age_bien",
            "nb_chambres",
            "nb_salles_bain",
            "etage"
        ]
    ].drop_duplicates()
    
    # LOAD FACT TABLE
    
    fact_darkom.to_sql(
        con=engine,
        schema="star_schema_darkom",
        name="fact_darkom_listings",
        if_exists="append",
        index=False
    )
    
    logger.info("fact_darkom_listing chargée avec succès")
    
    print("Pipeline Star Schema terminé avec succès")