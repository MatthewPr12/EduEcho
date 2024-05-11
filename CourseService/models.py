from pydantic import BaseModel


class CourseInfo(BaseModel):
    course_id: str
    course_name: str
    teacher_name: str
    number_of_students: int
    rating_sum: int = 0
    rating_count: int = 0


class CourseRate(BaseModel):
    course_id: str
    user_id: str
    rating: int
