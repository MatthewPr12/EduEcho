from CourseService.course_dal import CourseDAL
from CourseService.models import CourseInfo, CourseRate
from CourseService.setup_hazelcast import get_hazelcast_client


class CourseService:
    def __init__(self, dal):
        self.dal = dal
        try:
            self.hazelcast_client = get_hazelcast_client()
            self.course_cache = self.hazelcast_client.get_map("course_cache")
            print("Hazelcast client and course_cache map initialized successfully")
        except Exception as e:
            print(f"Error initializing Hazelcast client: {e}")
            self.hazelcast_client = None
            self.course_cache = None

    def create_course(self, course_info):
        print("CourseService: Creating course")
        course_id = self.dal.add_course(course_info)
        if self.course_cache:
            self.course_cache.set(course_id, course_info.dict())
        return course_id

    def retrieve_course(self, course_id):
        if self.course_cache:
            cached_course = self.course_cache.get(course_id).result()
            if cached_course:
                print(f"Course {course_id} found in cache")
                return cached_course
        course = self.dal.get_course(course_id)
        if course and self.course_cache:
            self.course_cache.set(course_id, course)
        return course

    def retrieve_all_courses(self):
        return self.dal.get_all_courses()

    def add_rating(self, course_rate):
        result = self.dal.rate_course(course_rate)
        if self.course_cache:
            self.course_cache.delete(course_rate.course_id)
        return result
