from datetime import datetime
import time
import random
import uuid
import requests
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger()

INGEST_URL = os.environ.get("INGEST_URL", "http://localhost:8000/ingest")

DEVICE_ID = str(uuid.uuid4())
print(f"Using device ID: {DEVICE_ID}")
SLEEP_INTERVAL = 10
RETRY_INTERVAL = 1
NUM_RETRIES = 5


def generate_payload():
    payload = {
        "device_id": DEVICE_ID,
        "temp": random.normalvariate(20, 5),
        "ts": str(datetime.now()),
    }

    return payload


def ingest_server(payload: dict):
    retries = NUM_RETRIES
    while True:
        try:
            logger.info(f"Sending payload: {payload}")
            r = requests.post(INGEST_URL, json=payload)
            if r.status_code != 200:
                logger.error(
                    f"Failed POST - status: {r.status_code}, response: {r.text}"
                )
            else:
                logger.info(f"Successfully ingested payload, server response: {r.text}")
            return
        except requests.ConnectionError as ce:
            if retries == 0:
                logger.error("Max retries exceeded. Shutting down.")
                raise ce
            logger.error(
                f"Error connecting to {INGEST_URL}, retrying in {RETRY_INTERVAL} seconds. {retries} retries remaining."
            )
            retries -= 1
            time.sleep(RETRY_INTERVAL)


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
