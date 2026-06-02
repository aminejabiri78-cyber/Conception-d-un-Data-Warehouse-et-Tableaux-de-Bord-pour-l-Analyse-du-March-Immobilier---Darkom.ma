import logging
import pandas as pd

from src.load_db import get_engine
from src.logger import get_logger

logger = get_logger(__name__)
logger = logging.getLogger(__name__)


def etl_darkom_clean():

    logger.info("Début ETL Clean Layer")

    engine = get_engine()

    try:

        # LOAD DATA
        df = pd.read_sql(
            "SELECT * FROM raw_darkom.staging_darkom",
            engine
        )

        logger.info(f"Données chargées : {df.shape[0]} lignes")

        # CLEAN COLUMNS
        df.columns = df.columns.str.strip().str.lower()

        # =========================
        # FIX TEXT (IMPORTANT)
        # =========================
        df["ville"] = (
            df["ville"]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        df["type_bien"] = (
            df["type_bien"]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        # VILLE STANDARDISATION (FIX CASA ISSUE)
        mapping_ville = {
        # Casablanca
        "casa": "Casablanca",
        "casablanca": "Casablanca",
        "casa blanca": "Casablanca",
        "dar el beida": "Casablanca",

        # Rabat
        "rabat": "Rabat",

        # Marrakech
        "marrakech": "Marrakech",
        "marrakesh": "Marrakech",

        # Fès
        "fes": "Fès",
        "fès": "Fès",
        "fez": "Fès",

        # Tanger
        "tanger": "Tanger",
        "tanja": "Tanger",
        "tangier": "Tanger",

        # Agadir
        "agadir": "Agadir",

        # Meknès
        "meknes": "Meknès",
        "meknès": "Meknès",

        # Oujda
        "oujda": "Oujda",

        # Kénitra
        "kenitra": "Kénitra",
        "kénitra": "Kénitra",

        # Tétouan
        "tetouan": "Tétouan",
        "tétouan": "Tétouan",

        # Beni Mellal
        "beni mellal": "Beni Mellal",
        "benimellal": "Beni Mellal",

        # Safi
        "safi": "Safi",

        # El Jadida
        "el jadida": "El Jadida",

        # Nador
        "nador": "Nador",

        # Al Hoceima
        "alhoceima": "Al Hoceima",
        "al hoceima": "Al Hoceima",

        # Khouribga
        "khouribga": "Khouribga",

        # Settat
        "settat": "Settat",

        # Berrechid
        "berrechid": "Berrechid",

        # Mohammedia
        "mohammedia": "Mohammedia",

        # Laayoune
        "laayoune": "Laâyoune",
        "layoune": "Laâyoune",

        # Dakhla
        "dakhla": "Dakhla",

        # Errachidia
        "errachidia": "Errachidia",

        # Ouarzazate
        "ouarzazate": "Ouarzazate"
        }   

        df["ville"] = df["ville"].replace(mapping_ville)

        # TYPE BIEN MAPPING
        mapping_type = {
            "appt": "Appartement",
            "appartement": "Appartement",
            "villa": "Villa",
            "terrain": "Terrain",
            "bureau": "Bureau"
        }

        df["type_bien"] = df["type_bien"].replace(mapping_type)

        # DROP DUPLICATES
        before = df.shape[0]
        df.drop_duplicates(subset="annonce_id", inplace=True)
        after = df.shape[0]

        logger.info(f"Doublons supprimés : {before - after}")

        # DATE
        df["date_publication"] = pd.to_datetime(
            df["date_publication"],
            errors="coerce"
        )

        # =========================
        # NUMERIC
        # =========================
        numeric_cols = [
            "prix",
            "surface",
            "nb_chambres",
            "nb_salles_bain",
            "etage",
            "annee_construction"
        ]

        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # FILL DATE
        df = df.sort_values("date_publication")
        df["date_publication"] = df["date_publication"].ffill()

        # FILL CATEGORICAL
        cat_cols = ["quartier", "type_bien", "transaction", "ville"]

        for col in cat_cols:
            mode_val = df[col].mode()
            df[col] = df[col].fillna(mode_val[0] if not mode_val.empty else "inconnu")

        # FILL NUMERIC
        for col in numeric_cols:
            df[col] = df[col].fillna(df[col].median())

        # OUTLIERS
        def remove_outliers(df, col):
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1

            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR

            return df[(df[col] >= lower) & (df[col] <= upper)]

        for col in ["prix", "surface", "nb_chambres", "nb_salles_bain"]:
            df = remove_outliers(df, col)

        # FEATURES
        df["prix_m2"] = df["prix"] / df["surface"].replace(0, pd.NA)

        current_year = pd.Timestamp.now().year
        df["age_bien"] = current_year - df["annee_construction"]
        df.loc[df["age_bien"] < 0, "age_bien"] = pd.NA

        df["categorie_prix"] = df["prix"].apply(
            lambda x: "Economique" if x < 500000 else
                      "Moyen" if x < 1500000 else
                      "Haut Standing" if x < 3000000 else
                      "Luxe"
        )

        df["categorie_surface"] = df["surface"].apply(
            lambda x: "Petit" if x < 80 else
                      "Moyen" if x <= 150 else
                      "Grand"
        )

        df["annee_publication"] = df["date_publication"].dt.year
        df["mois_publication"] = df["date_publication"].dt.month
        df["trimestre_publication"] = df["date_publication"].dt.quarter

        # INT CAST
        for col in ["nb_chambres", "nb_salles_bain", "etage", "annee_construction"]:
            df[col] = df[col].astype("Int64")

        # CREATE SCHEMA (IMPORTANT FIX)
            file_path=r"C:\Users\AMINE JBR\Downloads\Conception-d-un-Data-Warehouse-et-Tableaux-de-Bord-pour-l-Analyse-du-March-Immobilier---Darkom.ma-main\sql\clean.sql"
            with open(file_path,"r") as f :
                exe_query=f.read()
            with engine.begin() as con:
                con.exec_driver_sql(exe_query)

        # LOAD
        df.to_sql(
            name="darkom_clean",
            con=engine,
            schema="schema_clean_darkom",
            if_exists="append",
            index=False
        )

        logger.info(f"ETL terminé : {df.shape[0]} lignes")

        return df

    except Exception as e:
        logger.error(f"Erreur ETL Clean Layer : {e}")
        raise