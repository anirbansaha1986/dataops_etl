import pandas as pd
from utils.logger import setup_logger

logger = setup_logger("ANALYTICS")

df = pd.read_csv("data/creditcard.csv")


def total_transactions():
    logger.info("Calculating total transactions")
    return f"Total transactions: {len(df)}"


def fraud_count():
    logger.info("Calculating fraud count")
    fraud = df["Class"].sum()
    return f"Fraud transactions: {fraud}"


def normal_count():
    logger.info("Calculating normal transactions")
    normal = len(df) - df["Class"].sum()
    return f"Normal transactions: {normal}"


def show_fraud_samples(n=5):
    logger.info("Fetching fraud samples")
    fraud_df = df[df["Class"] == 1].head(n)

    result = []
    for _, row in fraud_df.iterrows():
        result.append(f"Time={row['Time']} Amount={row['Amount']}")

    return "\n".join(result)