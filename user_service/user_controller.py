import fastapi

from typing import Optional
from user_service.data_access.postgres_client import PostgresClient
from user_service.user_credentials import UserCredentials
from consul_service.consul_utils import register_service

import os

postgres_client = PostgresClient()

app = fastapi.FastAPI(title="User Authorization Service")


@app.on_event("startup")
def startup_event():
    register_service("user_service", "user_service-1", int(os.getenv("PORT")))


@app.get("/health")
async def health() -> fastapi.Response:
    return fastapi.Response(content="Healthy", status_code=200)


@app.post("/login")
def login(user_credentials: UserCredentials) -> fastapi.Response:
    if postgres_client.check_hash(user_credentials.username, user_credentials.password_hash):
        return fastapi.Response(content="Login successful", status_code=200)
    return fastapi.Response(content="Login failed", status_code=401)


@app.post("/signup")
def signup(user_credentials: UserCredentials, faculty: Optional[str] = None, program: Optional[str] = None) -> fastapi.Response:
    if postgres_client.add_user(user_credentials.username, user_credentials.password_hash, faculty, program):
        return fastapi.Response(content="Signup successful", status_code=200)
    return fastapi.Response(content="Signup failed", status_code=400)
