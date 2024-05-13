FROM python:3.9-alpine

# Install the Cassandra CQL shell
RUN apk add --no-cache bash curl \
    && pip install cqlsh

WORKDIR /code
ENTRYPOINT cqlsh -f ./ddl.cql $CASSANDRA_SEEDS $PORT
