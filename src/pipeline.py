import logging
import sys
from datetime import datetime

from extract import extract_bank_transactions, extract_invoices, extract_expenses
from transform import build_unified_transactions
from load import load_transactions


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler("logs/pipeline.log"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def run():
    setup_logging()
    logger = logging.getLogger("pipeline")
    start = datetime.now()
    logger.info("=== Pipeline run started ===")

    try:
        bank_df = extract_bank_transactions()
        invoice_df = extract_invoices()
        expense_df = extract_expenses()

        unified_df = build_unified_transactions(bank_df, invoice_df, expense_df)

        unified_df.to_csv("data/processed/unified_transactions.csv", index=False)

        load_transactions(unified_df)

        duration = (datetime.now() - start).total_seconds()
        logger.info(
            f"=== Pipeline run finished successfully in {duration:.2f}s | "
            f"{len(unified_df)} rows loaded ==="
        )

    except Exception:
        logger.exception("Pipeline run FAILED")
        raise


if __name__ == "__main__":
    run()