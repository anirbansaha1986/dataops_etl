from etl.pipeline import run_pipeline
import sys
import json

if __name__ == "__main__":
    run_pipeline()

    with open("etl_log.json") as f:
        log = json.load(f)

    if log["status"] == "SUCCESS":
        sys.exit(0)
    else:
        sys.exit(1)