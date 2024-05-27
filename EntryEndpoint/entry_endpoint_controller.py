from fastapi import FastAPI, HTTPException, Request
from consul_service.consul_utils import get_service_urls
from fastapi.responses import JSONResponse, RedirectResponse
from typing import Optional
import random

import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(levelname)s (%(asctime)s): %(message)s (Line %(lineno)d [%(filename)s])", datefmt="%d/%m/%Y %H:%M:%S"
)

import httpx
from consul_service.consul_utils import register_service

app = FastAPI()
register_service("entry_endpoint", "entry_endpoint-01", 8000)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.api_route("/course/{path:path}", methods=["GET", "POST"])
async def handle_courses(request: Request, path: str):
    service_URL = random.choice(get_service_urls("course_service"))
    logging.debug(f"{service_URL = }")

    url = f"{service_URL}/{path}"
    query_params = request.query_params
    if query_params:
        url = f"{url}?{query_params}"

    async with httpx.AsyncClient() as client:
        response = await client.request(method=request.method, url=url, headers=request.headers.raw, content=await request.body())
    return response.json()


@app.api_route("/feedback/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def handle_courses(request: Request, path: str):
    service_URL = random.choice(get_service_urls("feedback_service"))
    logging.debug(f"{service_URL = }")

    url = f"{service_URL}/{path}"
    query_params = request.query_params
    if query_params:
        url = f"{url}?{query_params}"

    async with httpx.AsyncClient() as client:
        response = await client.request(method=request.method, url=url, headers=request.headers.raw, content=await request.body())
    return response.json()


@app.api_route("/user/{path:path}", methods=["POST"])
async def handle_courses(request: Request, path: str):
    service_URL = random.choice(get_service_urls("user_service"))
    logging.debug(f"{service_URL = }")

    url = f"{service_URL}/{path}"
    query_params = request.query_params
    if query_params:
        url = f"{url}?{query_params}"

    async with httpx.AsyncClient() as client:
        response = await client.request(method=request.method, url=url, headers=request.headers.raw, content=await request.body())
    return response.text
