import pandas as pd


def validate_data(df):
    errors = []

    # 1. Required Columns Check
    required_columns = ["id", "amount"]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        errors.append({
            "type": "SCHEMA_ERROR",
            "message": f"Missing columns: {missing_columns}"
        })
        return errors  # Stop further validation

    # 2. Data Type Validation (ROOT CAUSE CHECK)
    # Convert safely: invalid values become NaN
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    if df["amount"].isnull().any():
        errors.append({
            "type": "DATA_TYPE_ERROR",
            "message": "Invalid datatype in 'amount'"
        })
        return errors  # Stop further checks to avoid cascading errors

    # 3. Negative Value Check
    if (df["amount"] < 0).any():
        errors.append({
            "type": "VALUE_ERROR",
            "message": "Negative values found in 'amount'"
        })

    # 4. Duplicate ID Check
    if df["id"].duplicated().any():
        errors.append({
            "type": "DUPLICATE_ERROR",
            "message": "Duplicate IDs found"
        })

    return errors