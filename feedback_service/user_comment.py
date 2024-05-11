from pydantic import BaseModel
from datetime import datetime


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


class IdentifiableUserComment(BaseModel):
    course_id: str
    replied_to_id: str
    comment_id: str


class PublishableUserComment(BaseModel):
    course_id: str
    replied_to_id: str
    user_id: str

    comment_text: str