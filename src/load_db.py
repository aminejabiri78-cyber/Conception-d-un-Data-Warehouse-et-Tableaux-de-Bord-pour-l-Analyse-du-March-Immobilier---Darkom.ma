from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
from src.logger import get_logger  

logger = get_logger("db")

def get_engine():
    load_dotenv()

    DB_USER = os.getenv("DB_USER")
    DB_NAME = os.getenv("DB_NAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")

    if not all([DB_USER, DB_NAME, DB_PASSWORD, DB_HOST, DB_PORT]):
        logger.error("Missing DB environment variables")
        return None

    try:
        db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

        engine = create_engine(db_url)

        logger.info("Database connection created successfully")

        return engine

    except Exception as e:
        logger.error(f"Database connection error : {e}")
        return None