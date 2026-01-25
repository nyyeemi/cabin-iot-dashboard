from datetime import datetime
import time
import random
import requests
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger()

INGEST_URL = os.environ.get("INGEST_URL", "http://localhost:8000/ingest")
REGISTER_URL = os.environ.get("REGISTER_URL", "http://localhost:8000/devices/register")
DEVICE_NAME = os.environ.get("HOSTNAME", "default")

SLEEP_INTERVAL = 30
RETRY_INTERVAL = 5
NUM_RETRIES = 5


def assign_uuid():
    retries = NUM_RETRIES
    while True:
        try:
            r = requests.post(REGISTER_URL, json={"name": DEVICE_NAME})
            r.raise_for_status()
            device_id = r.json()["device_id"]
            logger.info(f"Successfully assigned id: {device_id}")
            return device_id
        except (requests.ConnectionError, requests.HTTPError) as e:
            if retries == 0:
                logger.error("Max retries exceeded. Shutting down.")
                raise e
            logger.error(
                f"Error registering device {e}, retrying in {RETRY_INTERVAL} seconds. {retries} retries remaining."
            )
            retries -= 1
            time.sleep(RETRY_INTERVAL)


DEVICE_ID = assign_uuid()


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
