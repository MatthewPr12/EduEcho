from .abstract_cassandra_client import AbstractCassandraClient
from feedback_service.logging_config import *
from feedback_service.user_comment import CompleteUserComment, IdentifiableUserComment, Assessment
import uuid


class FeedbackCassandraClient(AbstractCassandraClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.course_comments_table = f"{self.keyspace}.course_comments"
        self.user_assessments_table = f"{self.keyspace}.user_assessments"
        self.comment_assessors = f"{self.keyspace}.comment_assessors"

        logging.info("Feedback Cassandra client successfully initialized")

    def get_course_comments(self, course_id: str, replied_to_id: uuid.UUID = None) -> list[CompleteUserComment]:
        query = f"SELECT * FROM {self.course_comments_table} WHERE " f"course_id = '{course_id}' AND replied_to_id = {replied_to_id}"
        comments = self.execute(query).all()
        return [
            CompleteUserComment(
                course_id=str(comment.course_id),
                replied_to_id=comment.replied_to_id,
                comment_id=comment.comment_id,
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

    def load_comment_assessment(self, comment: CompleteUserComment, current_user_id: str) -> None:
        comment.current_user_assessment = self.get_users_comment_assessment(comment, current_user_id).value

    def add_comment(self, comment: CompleteUserComment) -> None:
        query = (
            f"INSERT INTO {self.course_comments_table} "
            f"(course_id, replied_to_id, comment_id, user_id, comment_text, likes, dislikes, is_deleted, is_edited, timestamp) "
            f"VALUES ('{comment.course_id}', {comment.replied_to_id}, {comment.comment_id}, '{comment.user_id}', "
            f"'{comment.comment_text}', {comment.likes}, {comment.dislikes}, {comment.is_deleted}, {comment.is_edited}, '{comment.timestamp}')"
        )
        self.execute(query)

    def modify_comment_text(self, identifiable_comment: IdentifiableUserComment, new_comment_text: str) -> None:
        query = (
            f"UPDATE {self.course_comments_table} SET comment_text = '{new_comment_text}', is_edited = True "
            f"WHERE course_id = '{identifiable_comment.course_id}' AND replied_to_id = {identifiable_comment.replied_to_id} "
            f"AND comment_id = {identifiable_comment.comment_id}"
        )
        self.execute(query)

    def mark_comment_deleted(self, identifiable_comment: IdentifiableUserComment) -> None:
        query = (
            f"UPDATE {self.course_comments_table} SET is_deleted = True, comment_text = '' "
            f"WHERE course_id = '{identifiable_comment.course_id}' AND replied_to_id = {identifiable_comment.replied_to_id} AND comment_id = {identifiable_comment.comment_id}"
        )
        self.execute(query)

        self.delete_comment_assessments(identifiable_comment)

    def delete_comment_assessments(self, identifiable_comment: IdentifiableUserComment) -> None:
        get_users_query = (
            f"SELECT user_id FROM {self.comment_assessors} "
            f"WHERE course_id = '{identifiable_comment.course_id}' AND comment_id = {identifiable_comment.comment_id}"
        )
        user_ids_response = self.execute(get_users_query).all()

        for user_id_row in user_ids_response:
            user_id = user_id_row.user_id

            user_assessment_deletion_query = (
                f"DELETE FROM {self.user_assessments_table} "
                f"WHERE course_id = '{identifiable_comment.course_id}' AND comment_id = {identifiable_comment.comment_id} AND user_id = '{user_id}'"
            )
            self.execute(user_assessment_deletion_query)

        comment_assessors_deletion_query = (
            f"DELETE FROM {self.comment_assessors} "
            f"WHERE course_id = '{identifiable_comment.course_id}' AND comment_id = {identifiable_comment.comment_id}"
        )
        self.execute(comment_assessors_deletion_query)

    def get_users_comment_assessment(self, comment: IdentifiableUserComment | CompleteUserComment, current_user_id: str) -> Assessment:
        query = (
            f"SELECT is_like FROM {self.user_assessments_table} WHERE "
            f"comment_id = {comment.comment_id} AND user_id = '{current_user_id}' AND course_id = '{comment.course_id}'"
        )
        response = self.execute(query).one()
        if response is None:
            return Assessment.NO_ASSESSMENT
        return Assessment.LIKE_ASSESSMENT if response.is_like else Assessment.DISLIKE_ASSESSMENT

    def get_comment_ratings(self, comment: IdentifiableUserComment | CompleteUserComment) -> tuple[int, int]:
        """
        Returns the pair (likes, dislikes) for the given comment.
        """
        query = (
            f"SELECT likes, dislikes FROM {self.course_comments_table} WHERE "
            f"course_id = '{comment.course_id}' AND replied_to_id = {comment.replied_to_id} AND comment_id = {comment.comment_id}"
        )
        response = self.execute(query).one()
        return response.likes, response.dislikes

    def rate_comment(self, identifiable_comment: IdentifiableUserComment, assessor_user_id: str, assessment: Assessment) -> bool:
        current_assessment = self.get_users_comment_assessment(identifiable_comment, assessor_user_id)
        if current_assessment == assessment:
            return False

        if current_assessment != Assessment.NO_ASSESSMENT:
            # go back to `NO ASSESSMENT`
            comment_assessor_deletion_query = (
                f"DELETE FROM {self.comment_assessors} WHERE "
                f"course_id = '{identifiable_comment.course_id}' AND comment_id = {identifiable_comment.comment_id} AND user_id = '{assessor_user_id}'"
            )
            user_assessment_deletion_query = (
                f"DELETE FROM {self.user_assessments_table} "
                f"WHERE course_id = '{identifiable_comment.course_id}' AND comment_id = {identifiable_comment.comment_id} AND user_id = '{assessor_user_id}'"
            )
            self.execute(comment_assessor_deletion_query)
            self.execute(user_assessment_deletion_query)

        likes, dislikes = self.get_comment_ratings(identifiable_comment)
        new_likes, new_dislikes = likes, dislikes
        if current_assessment == Assessment.LIKE_ASSESSMENT:
            new_likes -= 1
        elif current_assessment == Assessment.DISLIKE_ASSESSMENT:
            new_dislikes -= 1

        if assessment == Assessment.LIKE_ASSESSMENT:
            new_likes += 1
        elif assessment == Assessment.DISLIKE_ASSESSMENT:
            new_dislikes += 1

        courses_query = (
            f"UPDATE {self.course_comments_table} SET likes = {new_likes}, dislikes = {new_dislikes} "
            f"WHERE course_id = '{identifiable_comment.course_id}' AND replied_to_id = {identifiable_comment.replied_to_id} AND comment_id = {identifiable_comment.comment_id}"
        )
        self.execute(courses_query)

        if assessment == Assessment.NO_ASSESSMENT:
            return True

        assessment_query = (
            f"INSERT INTO {self.user_assessments_table} "
            f"(course_id, user_id, comment_id, is_like) "
            f"VALUES ('{identifiable_comment.course_id}', '{assessor_user_id}', {identifiable_comment.comment_id}, {True if assessment == Assessment.LIKE_ASSESSMENT else False})"
        )
        comment_assessor_query = (
            f"INSERT INTO {self.comment_assessors} "
            f"(course_id, comment_id, user_id) "
            f"VALUES ('{identifiable_comment.course_id}', {identifiable_comment.comment_id}, '{assessor_user_id}')"
        )

        self.execute(assessment_query)
        self.execute(comment_assessor_query)
        return True


if __name__ == "__main__":
    raise NotImplementedError("Is not and will not be implemented.")
