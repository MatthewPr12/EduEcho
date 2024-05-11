from pydantic import BaseModel, Field
from typing import Optional, Dict


class CourseInfo(BaseModel):
    course_name: str
    teacher_name: str
    number_of_students: int
    rating_sum: int = 0
    rating_count: int = 0
    id: Optional[str] = Field(None, alias='_id')

    class Config:
        populate_by_name = True


class CourseRate(BaseModel):
    course_id: str
    user_id: str
    rating: int
    id: Optional[Dict[str, str]] = Field(None, alias='_id')

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "course_id": "course123",
                "user_id": "user456",
                "rating": 5
            }
        }
