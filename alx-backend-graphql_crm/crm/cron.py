import os
from datetime import datetime
import requests


def log_crm_heartbeat():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive"

    log_file = "/tmp/crm_heartbeat_log.txt"
    with open(log_file, "a") as f:
        f.write(message + "\n")

    # Optional GraphQL hello check
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=5
        )
        if response.status_code == 200 and "hello" in response.text:
            with open(log_file, "a") as f:
                f.write(f"{timestamp} GraphQL hello check OK\n")
        else:
            with open(log_file, "a") as f:
                f.write(f"{timestamp} GraphQL hello check FAILED\n")
    except Exception as e:
        with open(log_file, "a") as f:
            f.write(f"{timestamp} GraphQL hello check ERROR: {e}\n")
