from pymongo.mongo_client import MongoClient
from CourseService.course_dal import CourseDAL
from CourseService.course_service import CourseService
import os
from consul_service.consul_utils import get_config

MONGO_USERNAME = get_config("MONGO_USERNAME")
MONGO_PASSWORD = get_config("MONGO_PASSWORD")

# uri = (
#     f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}"
#     "@clusterucu.24uib8z.mongodb.net/?retryWrites=true&w=majority&appName=ClusterUCU"
# )
uri = (
    f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@mongodb:27017/?retryWrites=true&w=majority"
)


# Create and configure MongoDB client
def get_client():
    client = MongoClient(uri)
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
        raise ConnectionError("Failed to connect to MongoDB") from e
    return client


# Function to get the database
def get_database():
    client = get_client()
    return client["сourse_db"]


# Function to provide a CourseDAL instance
def get_course_dal():
    db = get_database()
    return CourseDAL(db)


# Function to provide a CourseService instance
def get_course_service():
    dal = get_course_dal()
    return CourseService(dal)
