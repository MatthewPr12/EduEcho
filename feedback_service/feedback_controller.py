import fastapi

import os
from typing import Optional

from .user_comment import (
    CompleteUserComment,
    PublishableUserComment,
    IdentifiableUserComment,
    ID,
    generate_complete_comment,
)


from .logging_config import *

from .data_access.feedback_cassandra_client import FeedbackCassandraClient


feedback_cassandra_client = FeedbackCassandraClient(
    host=os.getenv("CASSANDRA_SEEDS"),
    port=os.getenv("CASSANDRA_PORT"),
    keyspace="user_feedbacks",
)


app = fastapi.FastAPI(title="Courses Feedback Service")


@app.get("/comments")
def retrieve_comments(
    course_id: ID,
    replied_to_id: Optional[ID] = None,
    current_user_id: Optional[ID] = None,
) -> list[CompleteUserComment]:

    comments = feedback_cassandra_client.get_course_comments(course_id=course_id, replied_to_id=replied_to_id)
    if current_user_id is None:
        return comments

    for comment in comments:
        feedback_cassandra_client.mark_comment_assessment(comment=comment, current_user_id=current_user_id)

    return comments


@app.post("/comment")
def add_comment(publishable_comment: PublishableUserComment) -> fastapi.Response:
    complete_comment = generate_complete_comment(publishable_comment=publishable_comment)

    feedback_cassandra_client.add_comment(comment=complete_comment)

    return fastapi.Response(content="Comment has been saved!", media_type="text/plain")


@app.put("/comment")
def edit_comment(comment: IdentifiableUserComment, new_comment_text: str) -> fastapi.Response:
    feedback_cassandra_client.modify_comment_text(identifiable_comment=comment, new_comment_text=new_comment_text)
    return fastapi.Response(content="Comment has been modified", media_type="text/plain")


@app.delete("/comment")
def delete_comment(comment: IdentifiableUserComment) -> fastapi.Response:
    return fastapi.Response(content="Not implemented yet", media_type="text/plain")


@app.put("/rate_comment")
def rate_comment(comment: IdentifiableUserComment, assessor_user_id: ID, is_like: bool) -> fastapi.Response:
    return fastapi.Response(content="Not implemented yet", media_type="text/plain")
