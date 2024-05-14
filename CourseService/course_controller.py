from fastapi import FastAPI, HTTPException, Depends
from CourseService.models import CourseInfo, CourseRate
from CourseService.dependencies import get_course_service  # Import the dependency provider function
from CourseService.course_service import CourseService
from consul_service.consul_utils import register_service
import os

app = FastAPI()


@app.on_event("startup")
def startup_event():
    register_service("course_service", "course_service-01", os.getenv("PORT"))


@app.post("/")
async def create_course(course_info: CourseInfo, service: CourseService = Depends(get_course_service)):
    print("Request received to create a new course")
    return service.create_course(course_info)


@app.get("/{course_id}")
async def get_course(course_id: str, service: CourseService = Depends(get_course_service)):
    course = service.retrieve_course(course_id)
    if course:
        return course
    raise HTTPException(status_code=404, detail="Course not found")


@app.get("/")
async def get_all_courses(service: CourseService = Depends(get_course_service)):
    courses = service.retrieve_all_courses()
    return {"message": "All courses retrieved successfully", "courses": courses}


@app.post("/rate")
async def rate_course(course_rate: CourseRate, service: CourseService = Depends(get_course_service)):
    service.add_rating(course_rate)
    return {"message": "Rating added successfully"}
