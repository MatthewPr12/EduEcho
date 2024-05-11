from fastapi import APIRouter, HTTPException, Depends
from .models import CourseInfo, CourseRate
from .dependencies import get_course_service  # Import the dependency provider function
from .course_service import CourseService

router = APIRouter()


@router.post("/")
async def create_course(course_info: CourseInfo, service: CourseService = Depends(get_course_service)):
    return service.create_course(course_info)


@router.get("/{course_id}")
async def get_course(course_id: str, service: CourseService = Depends(get_course_service)):
    course = service.retrieve_course(course_id)
    if course:
        return course
    raise HTTPException(status_code=404, detail="Course not found")


@router.get("/")
async def get_all_courses(service: CourseService = Depends(get_course_service)):
    courses = service.retrieve_all_courses()
    return {"message": "All courses retrieved successfully", "courses": courses}


@router.post("/rate")
async def rate_course(course_rate: CourseRate, service: CourseService = Depends(get_course_service)):
    service.add_rating(course_rate)
    return {"message": "Rating added successfully"}
