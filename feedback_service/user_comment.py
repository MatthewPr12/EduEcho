from pydantic import BaseModel
import datetime
import uuid

from enum import Enum
from typing import Optional


class Assessment(Enum):
    NO_ASSESSMENT = 0
    LIKE_ASSESSMENT = 1
    DISLIKE_ASSESSMENT = 2


class IdentifiableUserComment(BaseModel):
    course_id: str
    replied_to_id: uuid.UUID
    comment_id: uuid.UUID


class PublishableUserComment(BaseModel):
    course_id: str
    replied_to_id: uuid.UUID
    user_id: str

    comment_text: str


class CompleteUserComment(PublishableUserComment):
    course_id: str
    replied_to_id: uuid.UUID
    comment_id: uuid.UUID
    user_id: str

    comment_text: str

    likes: int
    dislikes: int

    is_deleted: bool
    is_edited: bool

    timestamp: datetime.datetime

    current_user_assessment: Optional[Assessment]


def generate_complete_comment(
    publishable_comment: PublishableUserComment,
) -> CompleteUserComment:
    return CompleteUserComment(
        course_id=publishable_comment.course_id,
        replied_to_id=publishable_comment.replied_to_id,
        comment_id=uuid.uuid4(),
        user_id=publishable_comment.user_id,
        comment_text=publishable_comment.comment_text,
        likes=0,
        dislikes=0,
        is_deleted=False,
        is_edited=False,
        timestamp=datetime.datetime.now(),
        current_user_assessment=None,
    )
