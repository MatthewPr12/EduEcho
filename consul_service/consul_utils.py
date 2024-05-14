import consul
import os
import socket

c = consul.Consul(host=os.getenv("CONSUL_HOST"), port=os.getenv("CONSUL_PORT"))


def register_service(service_name, service_id, port):
    c.agent.service.register(name=service_name, service_id=service_id, address=socket.gethostname(), port=port, tags=["microservice"])


def get_service_urls(service_name):
    _, services = c.health.service(service_name, passing=True)
    if services:
        return [f"http://{service['Service']['Address']}:{service['Service']['Port']}" for service in services if service["Service"]]

    raise Exception("No available services found")


def set_config(key, value):
    c.kv.put(key, value)


def get_config(key):
    _, data = c.kv.get(key)
    if data:
        return data["Value"].decode("utf-8")
    return None
