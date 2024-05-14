import psycopg2
from psycopg2.extras import RealDictCursor
import os

from user_service.logging_config import *


class PostgresClient:
    def __init__(self):
        self.conn = self.connect()

    def connect(self):
        try:
            conn = psycopg2.connect(
                dbname=os.environ["DB_NAME"], user=os.environ["DB_USER"], password=os.environ["DB_PASSWORD"], host=os.environ["DB_HOST"]
            )
            logging.info("Connected to PostgreSQL database.")
            return conn
        except psycopg2.OperationalError as e:
            logging.error(f"Unable to connect: {e}")
            return None

    def add_user(self, user_login, user_password_hash, user_faculty=None, user_program=None) -> bool:
        if not self.conn:
            logging.error("Database connection is not established.")
            return False

        if self.login_exists(user_login):
            logging.info(f"User login '{user_login}' is already taken.")
            return False

        try:
            with self.conn.cursor() as cursor:
                sql = """
                INSERT INTO "User" ("UserLogin", "UserPasswordHash", "UserFaculty", "UserProgram")
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (user_login, user_password_hash, user_faculty, user_program))
                self.conn.commit()
                logging.info("New user added successfully.")
                return True
        except psycopg2.Error as e:
            logging.error(f"Failed to add new user: {e}")
            return False

    def login_exists(self, user_login) -> bool:
        """Check if the provided user_login already exists in the database"""
        try:
            with self.conn.cursor() as cursor:
                sql = 'SELECT EXISTS(SELECT 1 FROM "User" WHERE "UserLogin" = %s)'
                cursor.execute(sql, (user_login,))
                return cursor.fetchone()[0]
        except psycopg2.Error as e:
            logging.error(f"Failed to check if login exists: {e}")
            return False

    def check_hash(self, user_login, input_password_hash) -> bool:
        if not self.conn:
            logging.error("Database connection is not established.")
            return False
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                sql = """
                SELECT "UserPasswordHash" FROM "User" WHERE "UserLogin" = %s
                """
                cursor.execute(sql, (user_login,))
                result = cursor.fetchone()
                return result and result["UserPasswordHash"] == input_password_hash
        except psycopg2.Error as e:
            logging.error(f"Failed to check password hash: {e}")
            return None

    def __del__(self):
        if self.conn:
            self.conn.close()
            logging.info("Database connection closed.")


if __name__ == "__main__":
    raise NotImplementedError("Is not and will not be implemented.")
