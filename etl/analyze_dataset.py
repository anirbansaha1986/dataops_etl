import pandas as pd
import json


def analyze_dataset():

    df = pd.read_csv("data/creditcard.csv")

    summary = {}

    summary["row_count"] = len(df)
    summary["fraud_transactions"] = int(df["Class"].sum())
    summary["fraud_ratio"] = float(df["Class"].mean())
    summary["max_transaction"] = float(df["Amount"].max())
    summary["avg_transaction"] = float(df["Amount"].mean())

    summary["alerts"] = []

    if summary["fraud_ratio"] < 0.001:
        summary["alerts"].append("Fraud ratio unusually low")

    if summary["max_transaction"] > 10000:
        summary["alerts"].append("Very large transaction detected")

    with open("dataset_summary.json", "w") as f:
        json.dump(summary, f, indent=4)

    print("Dataset analysis completed")