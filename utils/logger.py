import json
import datetime

def log_event(final_status, results):
    log = {
        "timestamp": datetime.datetime.now().isoformat(),
        "status": final_status,
        "total_files": len(results),
        "success_count": len([r for r in results if r["status"] == "SUCCESS"]),
        "failure_count": len([r for r in results if r["status"] == "FAILURE"]),
        "details": results
    }

    with open("etl_log.json", "w") as f:
        json.dump(log, f, indent=2)

    print("\nFINAL ETL LOG:")
    print(json.dumps(log, indent=2))