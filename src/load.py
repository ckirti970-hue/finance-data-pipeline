
import os
import logging
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("pipeline.load")


def get_engine():

    db_url = os.getenv("DB_URL")
    print(db_url,'?????????')
    if db_url:
        logger.info("Connecting to configured database")
        return create_engine(db_url)

    logger.info(
        "No DB_URL set - falling back to local SQLite "
        "(data/processed/finance.db)"
    )

    return create_engine("sqlite:///data/processed/finance.db")


def load_transactions(df, table_name="transactions", if_exists="replace"):
    engine = get_engine()

    logger.info(
        f"Loading {len(df)} rows into table '{table_name}'"
    )

    df.to_sql(
        table_name,
        engine,
        if_exists=if_exists,
        index=False
    )

    logger.info("Load complete")

    return engine
