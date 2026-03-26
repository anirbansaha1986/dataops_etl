import os
import pandas as pd
import csv

DATA_DIR = "data"


def detect_delimiter(file_path):
    with open(file_path, 'r') as f:
        sample = f.read(1024)
        sniffer = csv.Sniffer()
        try:
            return sniffer.sniff(sample).delimiter
        except:
            return ","


def read_file(file_path):
    ext = file_path.split(".")[-1].lower()

    if ext in ["csv", "txt"]:
        delimiter = detect_delimiter(file_path)
        return pd.read_csv(file_path, delimiter=delimiter)

    elif ext == "json":
        return pd.read_json(file_path)

    elif ext in ["xlsx", "xls"]:
        return pd.read_excel(file_path)

    else:
        raise Exception(f"Unsupported format: {ext}")


def extract():
    data_list = []

    files = [f for f in os.listdir(DATA_DIR) if not f.startswith(".")]

    if not files:
        raise Exception("No files found in data directory")

    for file in files:
        #file_path = os.path.join(DATA_DIR, file)
        file_path = os.path.normpath(os.path.join(DATA_DIR, file)).replace("\\", "/")

        print(f"\nReading file: {file_path}")

        df = read_file(file_path)

        print("Columns:", list(df.columns))

        data_list.append((df, file_path))

    return data_list