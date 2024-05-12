from .abstract_cassandra_client import AbstractCassandraClient
from feedback_service.logging_config import *


class FeedbackCassandraClient(AbstractCassandraClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        logging.info("Feedback Cassandra client successfully initialized")


if __name__ == "__main__":
    raise NotImplementedError("Is and will not be implemented.")
