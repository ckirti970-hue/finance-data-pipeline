import logging
import pandas as pd

logger = logging.getLogger("pipeline.extract")

def extract_bank_transactions(path="data/raw/bank_transactions.csv") :
    logger.info(f"Extracting bank transactions from {path}")
    df = pd.read_csv(path)
    logger.info(f"Extracted {len(df)} raw bank transaction rows")
    return df


def extract_invoices(path="data/raw/invoices.xlsx") :
    logger.info(f"Extracting invoices from {path}")
    df = pd.read_excel(path)
    logger.info(f"Extracted {len(df)} raw invoice rows")
    return df


def extract_expenses(path="data/raw/expenses.csv") :
    logger.info(f"Extracting expenses from {path}")
    df = pd.read_csv(path)
    logger.info(f"Extracted {len(df)} raw expense rows")
    return df 
    
