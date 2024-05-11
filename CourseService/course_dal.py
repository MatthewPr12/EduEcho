# course_dal.py
import pymongo


class CourseDAL:
    def __init__(self, db):
        self.db = db

    def add_course(self, course_info):
        return self.db.course_info.insert_one(course_info.dict()).inserted_id

    def get_course(self, course_id):
        return self.db.course_info.find_one({"course_id": course_id})

    def get_all_courses(self):
        return list(self.db.course_info.find({}))

    def rate_course(self, course_rate):
        self.db.course_rate.insert_one(course_rate.dict())
        self.db.course_info.update_one(
            {"course_id": course_rate.course_id},
            {"$inc": {"rating_sum": course_rate.rating, "rating_count": 1}}
        )
