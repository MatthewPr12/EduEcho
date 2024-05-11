from .course_dal import CourseDAL
from .models import CourseInfo, CourseRate


class CourseService:
    def __init__(self, dal):
        self.dal = dal

    def create_course(self, course_info):
        return self.dal.add_course(course_info)

    def retrieve_course(self, course_id):
        return self.dal.get_course(course_id)

    def retrieve_all_courses(self):
        return self.dal.get_all_courses()

    def add_rating(self, course_rate):
        return self.dal.rate_course(course_rate)
