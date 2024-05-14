from fastapi import FastAPI, HTTPException
from consul_service.consul_utils import get_service_urls
from fastapi.responses import JSONResponse
from typing import Optional
import httpx

app = FastAPI()


@app.post("/course/")
async def create_course(course_info: dict):
    course_service_url = get_service_urls('course_service')[0]
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{course_service_url}/", json=course_info)
        return JSONResponse(content=response.json(), status_code=response.status_code)


@app.get("/course/{course_id}")
async def get_course(course_id: str):
    course_service_url = get_service_urls('course_service')[0]
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{course_service_url}/{course_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Course not found")
        return JSONResponse(content=response.json(), status_code=response.status_code)


@app.get("/course/")
async def get_all_courses():
    course_service_url = get_service_urls('course_service')[0]
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{course_service_url}/")
        return JSONResponse(content=response.json(), status_code=response.status_code)


@app.post("/course/rate")
async def rate_course(course_rate: dict):
    course_service_url = get_service_urls('course_service')[0]
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{course_service_url}/rate", json=course_rate)
        return JSONResponse(content=response.json(), status_code=response.status_code)


@app.get("/feedback/comments")
async def retrieve_comments(course_id: str, replied_to_id: Optional[str] = None, current_user_id: Optional[str] = None):
    feedback_service_url = get_service_urls('feedback_service')[0]
    params = {
        "course_id": course_id,
        "replied_to_id": replied_to_id,
        "current_user_id": current_user_id,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{feedback_service_url}/comments", params=params)
        return JSONResponse(content=response.json(), status_code=response.status_code)


@app.post("/feedback/comment")
async def add_comment(publishable_comment: dict):
    feedback_service_url = get_service_urls('feedback_service')[0]
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{feedback_service_url}/comment", json=publishable_comment)
        return JSONResponse(content=response.json(), status_code=response.status_code)


@app.put("/feedback/comment")
async def edit_comment(comment: dict, new_comment_text: str):
    feedback_service_url = get_service_urls('feedback_service')[0]
    data = {
        "comment": comment,
        "new_comment_text": new_comment_text,
    }
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{feedback_service_url}/comment", json=data)
        return JSONResponse(content=response.json(), status_code=response.status_code)


@app.delete("/feedback/comment")
async def delete_comment(comment: dict):
    feedback_service_url = get_service_urls('feedback_service')[0]
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{feedback_service_url}/comment", json=comment)
        return JSONResponse(content=response.json(), status_code=response.status_code)


@app.put("/feedback/rate_comment")
async def rate_comment(comment: dict, assessor_user_id: str, assessment: int):
    feedback_service_url = get_service_urls('feedback_service')[0]
    data = {
        "comment": comment,
        "assessor_user_id": assessor_user_id,
        "assessment": assessment,
    }
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{feedback_service_url}/rate_comment", json=data)
        return JSONResponse(content=response.json(), status_code=response.status_code)


@app.post("/user/login")
async def login(user_credentials: dict):
    user_service_url = get_service_urls('user_service')[0]
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{user_service_url}/login", json=user_credentials)
        return JSONResponse(content=response.json(), status_code=response.status_code)


@app.post("/user/signup")
async def signup(user_credentials: dict, faculty: Optional[str] = None, program: Optional[str] = None):
    user_service_url = get_service_urls('user_service')[0]
    data = {
        "user_credentials": user_credentials,
        "faculty": faculty,
        "program": program,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{user_service_url}/signup", json=data)
        return JSONResponse(content=response.json(), status_code=response.status_code)
