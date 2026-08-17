import logging
import re
import pandas as pd

logger = logging.getLogger("pipeline.transform")


CATEGORY_MAP = {
    "sales": "Sales",
    "purchase": "Purchase",
    "utilties": "Utilities",
    "utilities": "Utilities",
    "rent": "Rent",
    "salary": "Salary",
}


def parse_messy_date(value):
    """Convert different date formats into a standard date."""

    if pd.isna(value):
        return pd.NaT

    value = str(value).strip()

    formats = [
        "%d-%m-%Y",
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%b %d, %Y",
    ]

    for fmt in formats:
        try:
            return pd.to_datetime(value, format=fmt)
        except (ValueError, TypeError):
            continue

    return pd.to_datetime(value, errors="coerce")


def parse_messy_amount(value):
    """Convert messy money values into numbers."""

    if pd.isna(value):
        return None

    s = str(value).strip()

    is_negative = s.startswith("(") and s.endswith(")")

    s = re.sub(r"[^\d.\-]", "", s)

    if s in ("", "-", "."):
        return None

    try:
        amount = float(s)
    except ValueError:
        return None

    if is_negative:
        return -abs(amount)

    return amount


def clean_category(value):
    """Standardize category names."""

    if pd.isna(value) or str(value).strip() == "":
        return "Uncategorized"

    key = str(value).strip().lower()

    return CATEGORY_MAP.get(
        key,
        str(value).strip().title()
    )


def transform_bank_transactions(df: pd.DataFrame):
    """Clean and standardize bank transactions."""

    logger.info("Transforming bank transactions")

    out = df.copy()

    out["date"] = out["Txn Date"].apply(parse_messy_date)
    out["amount"] = out["Amount (INR)"].apply(parse_messy_amount)
    out["category"] = out["Category"].apply(clean_category)

    out["source"] = "bank"
    out["reference"] = out["Description"]
    out["direction"] = out["Type"]

    out = out[
        [
            "date",
            "reference",
            "amount",
            "category",
            "direction",
            "source",
        ]
    ]

    return out


def transform_invoices(df: pd.DataFrame):
    """Clean and standardize invoice data."""

    logger.info("Transforming invoices")

    out = df.copy()

    out["date"] = out["InvoiceDate"].apply(parse_messy_date)
    out["amount"] = out["Total Amount"].apply(parse_messy_amount)

    out["category"] = "Sales"
    out["source"] = "invoice"
    out["reference"] = out["InvoiceNo"]

    out["direction"] = "CR"

    out = out[
        [
            "date",
            "reference",
            "amount",
            "category",
            "direction",
            "source",
        ]
    ]

    return out


def transform_expenses(df: pd.DataFrame):
    """Clean and standardize expense data."""

    logger.info("Transforming expenses")

    out = df.copy()

    out["date"] = out["date"].apply(parse_messy_date)
    out["amount"] = out["amount_inr"].apply(parse_messy_amount)
    out["category"] = out["expense_category"].apply(clean_category)

    out["source"] = "expense"
    out["reference"] = out["vendor_name"]

    out["direction"] = "DR"

    out = out[
        [
            "date",
            "reference",
            "amount",
            "category",
            "direction",
            "source",
        ]
    ]

    return out


def build_unified_transactions(
    bank_df: pd.DataFrame,
    invoice_df: pd.DataFrame,
    expense_df: pd.DataFrame,
):
    """Transform all sources and combine them into one dataset."""

    logger.info("Building unified transaction dataset")

    bank = transform_bank_transactions(bank_df)

    invoices = transform_invoices(invoice_df)

    expenses = transform_expenses(expense_df)

    unified = pd.concat(
        [bank, invoices, expenses],
        ignore_index=True
    )

    logger.info(
        f"Unified dataset contains {len(unified)} rows"
    )

    return unified