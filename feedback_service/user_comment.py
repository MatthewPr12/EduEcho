from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class Assessment(Enum):
    NO_ASSESSMENT = 0
    LIKE_ASSESSMENT = 1
    DISLIKE_ASSESSMENT = 2


class CompleteUserComment(BaseModel):
    course_id: str
    replied_to_id: str
    comment_id: str
    user_id: str

    comment_text: str

    likes: int
    dislikes: int

    is_deleted: bool

    date: datetime

    current_user_assessment: Assessment


class IdentifiableUserComment(BaseModel):
    course_id: str
    replied_to_id: str
    comment_id: str


class PublishableUserComment(BaseModel):
    course_id: str
    replied_to_id: str
    user_id: str

    comment_text: str
