import time
import random
import requests
import argparse
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger()


INGEST_URL = os.environ.get("INGEST_URL", "http://localhost:8000/ingest")


parser = argparse.ArgumentParser(description="Run mock IoT device")
parser.add_argument(
    "--device-id",
    "-d",
    type=str,
    default="cabin_node_1",
    help="ID of the device (defaults to 'cabin_node_1')",
)
args = parser.parse_args()
DEVICE_ID = args.device_id

print(f"Using device ID: {DEVICE_ID}")

SLEEP_INTERVAL = 10
RETRY_DELAY = 5


def generate_payload():
    payload = {
        "device_id": "cabin_node_1",
        "temperature": random.normalvariate(20, 5),
        "light": random.randint(200, 500),
    }

    return payload


def ingest_server(payload: dict):
    try:
        logger.info(f"Sending payload: {payload}")
        r = requests.post(INGEST_URL, json=payload)
        if r.status_code != 200:
            logger.error(f"Failed POST - status: {r.status_code}, response: {r.json()}")
        else:
            logger.info(f"Successfully ingested payload, server response: {r.json()}")
    except requests.ConnectionError as ce:
        logger.error(f"Connection error: {ce}, will retry after {RETRY_DELAY}s")
        time.sleep(RETRY_DELAY)
    except requests.Timeout as te:
        logger.error(f"Request timed out: {te}")
    except Exception as e:
        logger.error(f"Error making request: {e}")


if __name__ == "__main__":
    try:
        logger.info(f"Starting mock iot device {DEVICE_ID}.")
        while True:
            payload = generate_payload()
            ingest_server(payload)
            time.sleep(SLEEP_INTERVAL)
    except KeyboardInterrupt:
        logger.info("CTRL+C received, shutting down.")
        exit()
