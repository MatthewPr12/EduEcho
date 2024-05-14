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


consul kv put ${CONSUL_ESSENTIAL_KEY} TRUE

echo "KV Population Ended!"


# let the container run
wait