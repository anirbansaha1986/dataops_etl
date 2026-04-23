import pandas as pd
from rag.fraud_rules import generate_signals

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["abs_v14"] = df["V14"].abs()
    df["abs_v17"] = df["V17"].abs()

    df["is_micro_txn"] = (df["Amount"] < 1).astype(int)
    df["is_high_amount"] = (df["Amount"] > 500).astype(int)

    df["amount_bucket"] = pd.cut(
        df["Amount"],
        bins=[-1, 1, 50, 500, 1000000],
        labels=["micro", "low", "medium", "high"]
    )

    df["signal_list"] = df.apply(generate_signals, axis=1)
    df["signal_count"] = df["signal_list"].apply(len)
    df["signal_text"] = df["signal_list"].apply(
        lambda x: ", ".join(x) if x else "No strong signals"
    )

    return df