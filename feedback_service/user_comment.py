from pydantic import BaseModel
from datetime import datetime
from enum import Enum


type ID = str


class Assessment(Enum):
    NO_ASSESSMENT = 0
    LIKE_ASSESSMENT = 1
    DISLIKE_ASSESSMENT = 2


class CompleteUserComment(BaseModel):
    course_id: ID
    replied_to_id: ID
    comment_id: ID
    user_id: ID

    comment_text: str

    likes: int
    dislikes: int

    is_deleted: bool

    date: datetime

    current_user_assessment: Assessment


class IdentifiableUserComment(BaseModel):
    course_id: ID
    replied_to_id: ID
    comment_id: ID


class PublishableUserComment(BaseModel):
    course_id: ID
    replied_to_id: ID
    user_id: ID

    comment_text: str
