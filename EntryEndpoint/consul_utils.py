import consul


def register_service(service_name, service_id, port):
    c = consul.Consul(host='localhost', port=8500)
    c.agent.service.register(
        name=service_name,
        service_id=service_id,
        address='localhost',
        port=port,
        tags=['microservice']
    )


def get_service_urls(service_name):
    c = consul.Consul()
    index, services = c.health.service(service_name, passing=True)
    if services:
        return [f"http://{service['Service']['Address']}:{service['Service']['Port']}"
                for service in services if service['Service']]

    raise Exception("No available services found")


def set_config(key, value):
    c = consul.Consul()
    c.kv.put(key, value)


def get_config(key):
    c = consul.Consul()
    index, data = c.kv.get(key)
    if data:
        return data['Value'].decode('utf-8')
    return None