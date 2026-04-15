def generate_signals(row):

    signals = []

    if row["Amount"] < 1:
        signals.append("Card testing transaction (very low amount)")

    if row["Amount"] > 500:
        signals.append("High-value anomaly")

    if abs(row["V14"]) > 5:
        signals.append("Strong anomaly in V14")

    if abs(row["V17"]) > 5:
        signals.append("Suspicious pattern in V17")

    return signals