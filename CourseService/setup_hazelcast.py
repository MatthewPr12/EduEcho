from hazelcast import HazelcastClient
import os
from consul_service.consul_utils import get_config


HAZELCAST_CLUSTER_NAME = get_config("HAZELCAST_CLUSTER_NAME")
HAZELCAST_ADDRESSES = get_config("HAZELCAST_ADDRESSES").split(",")

# load_dotenv()


def get_hazelcast_client():
    print(f"Connecting to Hazelcast cluster: {HAZELCAST_CLUSTER_NAME} at {HAZELCAST_ADDRESSES}")
    client = HazelcastClient(cluster_name=HAZELCAST_CLUSTER_NAME, cluster_members=HAZELCAST_ADDRESSES)
    return client
