consul agent -dev -server -ui -node=server -bootstrap-expect=1 -client=0.0.0.0 &

echo "Waiting for consul initialization..."

while true; do
    result=$(curl -sf http://localhost:${CONSUL_PORT}/v1/status/leader)
    if [ $? -eq 0 ]; then
        echo "Leader found: $result"
        break
    else
        echo "No leader yet. Response: $result"
    fi
    sleep 0.1
done


echo "Starting KV Population"

consul kv put MONGO_USERNAME "${MONGO_USERNAME}"
consul kv put MONGO_PASSWORD "${MONGO_PASSWORD}"

consul kv put POSTGRES_DB_NAME "${POSTGRES_DB_NAME}"
consul kv put POSTGRES_HOST "${POSTGRES_HOST}"
consul kv put POSTGRES_USER "${POSTGRES_USER}"
consul kv put POSTGRES_PASSWORD "${POSTGRES_PASSWORD}"

consul kv put CASSANDRA_CLUSTER_NAME "${CASSANDRA_CLUSTER_NAME}"
consul kv put CASSANDRA_SEEDS "${CASSANDRA_SEEDS}"
consul kv put CASSANDRA_PORT "${CASSANDRA_PORT}"

consul kv put HZ_CLUSTER_NAME "${HZ_CLUSTER_NAME}"
consul kv put HAZELCAST_ADDRESSES "${HAZELCAST_ADDRESSES}"

consul kv put ${CONSUL_ESSENTIAL_KEY} TRUE



echo "KV Population Ended!"


# let the container run
wait