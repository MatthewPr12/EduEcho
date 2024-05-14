from hazelcast import HazelcastClient
import os
from dotenv import load_dotenv

load_dotenv()

HAZELCAST_CLUSTER_NAME = os.getenv("HAZELCAST_CLUSTER_NAME")
HAZELCAST_ADDRESSES = os.getenv("HAZELCAST_ADDRESSES").split(",")


def get_hazelcast_client():
    print(f"Connecting to Hazelcast cluster: {HAZELCAST_CLUSTER_NAME} at {HAZELCAST_ADDRESSES}")
    client = HazelcastClient(cluster_name=HAZELCAST_CLUSTER_NAME, cluster_members=HAZELCAST_ADDRESSES)
    return client
