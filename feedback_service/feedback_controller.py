import fastapi
from typing import Optional

from .user_comment import (
    CompleteUserComment,
    PublishableUserComment,
    IdentifiableUserComment,
    ID,
)

from .logging_config import *

# from .data_access.feedback_cassandra_client import FeedbackCassandraClient


app = fastapi.FastAPI(title="Courses Feedback Service")


@app.get("/comments")
def retrieve_comments(
    course_id: ID,
    replied_to_id: Optional[ID] = None,
    current_user_id: Optional[ID] = None,
) -> list[CompleteUserComment]:
    return fastapi.Response(content="Not implemented yet", media_type="text/plain")


@app.post("/comment")
def add_comment(comment: PublishableUserComment) -> fastapi.Response:
    return fastapi.Response(content="Not implemented yet", media_type="text/plain")


@app.put("/comment")
def edit_comment(
    comment: IdentifiableUserComment, new_comment_text: str
) -> fastapi.Response:
    return fastapi.Response(content="Not implemented yet", media_type="text/plain")


@app.delete("/comment")
def delete_comment(comment: IdentifiableUserComment) -> fastapi.Response:
    return fastapi.Response(content="Not implemented yet", media_type="text/plain")


@app.put("/rate_comment")
def rate_comment(
    comment: IdentifiableUserComment, assessor_user_id: ID, is_like: bool
) -> fastapi.Response:
    return fastapi.Response(content="Not implemented yet", media_type="text/plain")
