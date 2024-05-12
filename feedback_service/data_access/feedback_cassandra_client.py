from .abstract_cassandra_client import AbstractCassandraClient
from feedback_service.logging_config import *
from feedback_service.user_comment import ID, CompleteUserComment, IdentifiableUserComment


class FeedbackCassandraClient(AbstractCassandraClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.course_comments_table = "course_comments"
        self.user_assessments_table = "user_assessments"

        logging.info("Feedback Cassandra client successfully initialized")

    def get_course_comments(self, course_id: ID, replied_to_id: ID = None) -> list[CompleteUserComment]:
        query = (
            f"SELECT * FROM {self.keyspace}.{self.course_comments_table} WHERE "
            f"course_id = {course_id} AND replied_to_id = {replied_to_id}"
        )
        comments = self.execute(query).all()
        return [
            CompleteUserComment(
                course_id=str(comment.course_id),
                replied_to_id=str(comment.replied_to_id),
                comment_id=str(comment.comment_id),
                user_id=str(comment.user_id),
                comment_text=comment.comment_text,
                likes=comment.likes,
                dislikes=comment.dislikes,
                is_deleted=comment.is_deleted,
                is_edited=comment.is_edited,
                timestamp=comment.timestamp,
                current_user_assessment=None,
            )
            for comment in comments
        ]

    def mark_comment_assessment(self, comment: CompleteUserComment, current_user_id: ID) -> None:
        query = (
            f"SELECT * FROM {self.keyspace}.{self.user_assessments_table} WHERE "
            f"comment_id = {comment.comment_id} AND user_id = {current_user_id} AND course_id = {comment.course_id}"
        )

        response = self.execute(query).all()
        assert len(response) <= 1
        if len(response) == 1:
            comment.current_user_assessment = response[0].assessment_type

    def add_comment(self, comment: CompleteUserComment) -> None:
        query = (
            f"INSERT INTO {self.keyspace}.{self.course_comments_table} "
            f"(course_id, replied_to_id, comment_id, user_id, comment_text, likes, dislikes, is_deleted, is_edited, timestamp) "
            f"VALUES ({comment.course_id}, {comment.replied_to_id}, {comment.comment_id}, {comment.user_id}, "
            f"'{comment.comment_text}', {comment.likes}, {comment.dislikes}, {comment.is_deleted}, {comment.is_edited}, '{comment.timestamp}')"
        )
        self.execute(query)

    def modify_comment_text(self, identifiable_comment: IdentifiableUserComment, new_comment_text: str) -> None:
        query = (
            f"UPDATE {self.keyspace}.{self.course_comments_table} SET comment_text = '{new_comment_text}', is_edited = True "
            f"WHERE course_id = {identifiable_comment.course_id} AND replied_to_id = {identifiable_comment.replied_to_id} "
            f"AND comment_id = {identifiable_comment.comment_id}"
        )
        self.execute(query)

    def delete_comment(self, identifiable_comment: IdentifiableUserComment) -> None:
        query = (
            f"UPDATE {self.keyspace}.{self.course_comments_table} SET is_deleted = True, comment_text = '' "
            f"WHERE course_id = {identifiable_comment.course_id} AND replied_to_id = {identifiable_comment.replied_to_id} AND comment_id = {identifiable_comment.comment_id}"
        )
        self.execute(query)


if __name__ == "__main__":
    raise NotImplementedError("Is not and will not be implemented.")
