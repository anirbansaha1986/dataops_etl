from utils.validation_rules import validate_data

def transform(data_list):
    transformed_data = []

    for df, file_path in data_list:
        errors = validate_data(df)

        if errors:
            raise Exception(errors)

        df["amount"] = df["amount"].astype(float)
        df["tax"] = df["amount"] * 0.1

        transformed_data.append((df, file_path))

    return transformed_data