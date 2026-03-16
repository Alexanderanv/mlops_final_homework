import logging
import time

logger = logging.getLogger(__name__)

def extract_data():
    logger.info("run extract data")

def extract_from_clickhouse():
    logger.info("run extract from clickhouse")
    time.sleep(10)

def train():
    logger.info("run train")
    time.sleep(10)