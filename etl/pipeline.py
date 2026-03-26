from etl.extract import extract
from etl.transform import transform
from etl.load import load
from utils.logger import log_event


def run_pipeline():
    results = []

    data_list = extract()

    for df, file_path in data_list:
        try:
            print(f"\nProcessing file: {file_path}")

            transformed = transform([(df, file_path)])

            for t_df, _ in transformed:
                load(t_df)

            results.append({
                "file": file_path,
                "status": "SUCCESS",
                "errors": None
            })

        except Exception as e:
            error_list = e.args[0] if isinstance(e.args[0], list) else [str(e)]

            results.append({
                "file": file_path,
                "status": "FAILURE",
                "errors": error_list
            })

    # Final status
    if all(r["status"] == "SUCCESS" for r in results):
        final_status = "SUCCESS"
    elif all(r["status"] == "FAILURE" for r in results):
        final_status = "FAILURE"
    else:
        final_status = "PARTIAL_SUCCESS"

    log_event(final_status, results)