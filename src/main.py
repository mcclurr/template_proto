import random
import time
import uuid

from log import init_logging

from common import common_pb2
from example1 import test1_pb2


def random_position() -> common_pb2.Position:
    return common_pb2.Position(
        x=random.uniform(-1000, 1000),
        y=random.uniform(-1000, 1000),
        z=random.uniform(0, 10000),
    )


def random_timestamp() -> common_pb2.Timestamp:
    return common_pb2.Timestamp(
        epoch=time.time()
    )


def random_track() -> test1_pb2.Track:
    return test1_pb2.Track(
        id=str(uuid.uuid4()),
        position=random_position(),
        time=random_timestamp(),
    )


if __name__ == "__main__":
    logger = init_logging("python-dev")

    logger.info("Starting random proto generator...")

    try:
        while True:
            track = random_track()

            # Option 1: readable string
            logger.info(f"Track generated:\n{track}")

            # Option 2 (alternative): serialized size
            # logger.info(f"Serialized size: {len(track.SerializeToString())} bytes")

            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")