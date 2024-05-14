import fastapi

import os
from typing import Optional
import uuid

from .user_comment import (
    CompleteUserComment,
    PublishableUserComment,
    IdentifiableUserComment,
    generate_complete_comment,
    assessment_value_to_assessment_type_map,
)

from consul_service.consul_utils import register_service

from .data_access.feedback_cassandra_client import FeedbackCassandraClient


feedback_cassandra_client = FeedbackCassandraClient(
    host=os.getenv("CASSANDRA_SEEDS"),
    port=os.getenv("CASSANDRA_PORT"),
    keyspace="user_feedbacks",
)


app = fastapi.FastAPI(title="Courses Feedback Service")


@app.on_event("startup")
def startup_event():
    register_service("feedback_service", "feedback_service-1", 8080)


@app.get("/comments")
def retrieve_comments(
    course_id: str,
    replied_to_id: Optional[uuid.UUID] = None,
    current_user_id: Optional[str] = None,
) -> list[CompleteUserComment]:

    comments = feedback_cassandra_client.get_course_comments(course_id=course_id, replied_to_id=replied_to_id)
    if current_user_id is None:
        return comments

    for comment in comments:
        feedback_cassandra_client.load_comment_assessment(comment=comment, current_user_id=current_user_id)

    return comments


@app.post("/comment")
def add_comment(publishable_comment: PublishableUserComment) -> CompleteUserComment:
    complete_comment = generate_complete_comment(publishable_comment=publishable_comment)
    feedback_cassandra_client.add_comment(comment=complete_comment)
    return complete_comment


@app.put("/comment")
def edit_comment(comment: IdentifiableUserComment, new_comment_text: str) -> fastapi.Response:
    feedback_cassandra_client.modify_comment_text(identifiable_comment=comment, new_comment_text=new_comment_text)
    return fastapi.Response(content="Comment has been modified", media_type="text/plain")


@app.delete("/comment")
def delete_comment(comment: IdentifiableUserComment) -> fastapi.Response:
    feedback_cassandra_client.mark_comment_deleted(identifiable_comment=comment)
    return fastapi.Response(content="Comment has been marked deleted.", media_type="text/plain")


@app.put("/rate_comment")
def rate_comment(comment: IdentifiableUserComment, assessor_user_id: str, assessment: int) -> fastapi.Response:
    assessment_type = assessment_value_to_assessment_type_map.get(assessment)
    if assessment_type is None:
        return fastapi.Response(content=f"Invalid assessment value. Got: {assessment}", media_type="text/plain")

    is_success = feedback_cassandra_client.rate_comment(identifiable_comment=comment, assessor_user_id=assessor_user_id, assessment=assessment_type)

    if not is_success:
        return fastapi.Response(content="The comment assessment was not successful", media_type="text/plain")
    return fastapi.Response(content=f"The comment assessment was successful", media_type="text/plain")
