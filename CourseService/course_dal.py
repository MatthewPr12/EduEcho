import pymongo
from bson import ObjectId
from pymongo import MongoClient


class CourseDAL:
    def __init__(self, db: MongoClient):
        self.db = db
        self.course_info = self.db.course_info
        self.course_rate = self.db.course_rate
        # self.setup_collections()

    def setup_collections(self):
        # Configuring composite primary key for course_rate
        self.course_rate.create_index([("_id.course_id", 1), ("_id.user_id", 1)], unique=True)

    def add_course(self, course_info):
        # Directly inserting the document into the course_info collection
        # MongoDB will automatically assign a unique _id to each new document
        try:
            print(course_info.dict())
            result = self.course_info.insert_one(course_info.dict())
            return str(result.inserted_id)  # This will return the auto-generated _id
        except pymongo.errors.DuplicateKeyError:
            raise ValueError("An error occurred during the course insertion.")

    def get_course(self, course_id):
        # Querying by _id, which holds the course_id
        course = self.course_info.find_one({"_id": ObjectId(course_id)})
        course['_id'] = str(course['_id'])
        return course

    def get_all_courses(self):
        courses = self.course_info.find({})
        # Convert each course document's '_id' from ObjectId to string
        return [{**course, '_id': str(course['_id'])} for course in courses]

    def rate_course(self, course_rate):
        # Insert rate using composite _id from course_info's _id and user_id
        rate_document = course_rate.dict()
        rate_document['_id'] = {
            'course_id': ObjectId(rate_document.pop('course_id')),  # Remove and use as part of _id
            'user_id': rate_document.pop('user_id')  # Remove and use as part of _id
        }
        try:
            self.course_rate.insert_one(rate_document)
            # Update the corresponding course info
            self.course_info.update_one(
                {"_id": rate_document['_id']['course_id']},
                {"$inc": {"rating_sum": course_rate.rating, "rating_count": 1}}
            )
        except pymongo.errors.DuplicateKeyError:
            raise ValueError("This user has already rated this course.")