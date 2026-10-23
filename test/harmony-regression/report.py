"""Submit harmony-regression results to ASTRA's reporting service."""

import os
import sys
from datetime import datetime

import requests


def main() -> None:
    reporting_url = os.getenv("ETQ_REPORTING_URL")
    if not reporting_url:
        print("ETQ_REPORTING_URL is not set; skipping results submission.")
        return

    status, start_raw, end_raw = sys.argv[1], sys.argv[2], sys.argv[3]
    start = datetime.strptime(start_raw, "%Y-%m-%dT%H:%M:%S.%f%z")
    end = datetime.strptime(end_raw, "%Y-%m-%dT%H:%M:%S.%f%z")
    duration = (end - start).total_seconds()

    response = requests.post(
        url=f"{reporting_url}/v1/results",
        json={
            "title": "Harmony Regression",
            "start": start.isoformat(),
            "end": end.isoformat(),
            "duration": duration,
            "tests": [
                {
                    "title": "HarmonyRegression.ipynb",
                    "status": status,
                    "duration": duration,
                }
            ],
        },
    )
    response.raise_for_status()
    print(f"Results submitted with ID {response.json()['id']}.")


if __name__ == "__main__":
    main()
