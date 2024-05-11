from fastapi import FastAPI, HTTPException
from typing import Optional

from CourseService.course_controller import router as course_router
from FeedbackService.feedback_controller import router as feedback_router
from UserService.user_controller import router as user_router

app = FastAPI()

# Including routers from each service
app.include_router(course_router, prefix="/course")
app.include_router(feedback_router, prefix="/feedback")
app.include_router(user_router, prefix="/user")


# # Dummy functions to simulate other service calls
# def handle_user_request(user_action: str, data: dict):
#     return {"action": user_action, "data": data}
#
#
# def handle_course_request(course_action: str, data: dict):
#     return {"action": course_action, "data": data}
#
#
# def handle_feedback_request(feedback_action: str, data: dict):
#     return {"action": feedback_action, "data": data}
#
#
# @app.post("/user/{action}")
# async def user_service(action: str, data: dict):
#     # Here you would handle different user actions like login, register, etc.
#     return handle_user_request(action, data)
#
#
# @app.post("/course/{action}")
# async def course_service(action: str, data: dict):
#     # Here you would handle actions related to courses like adding a new course, retrieving course info, etc.
#     return handle_course_request(action, data)
#
#
# @app.post("/feedback/{action}")
# async def feedback_service(action: str, data: dict):
#     # This would handle feedback-related actions such as submitting or deleting comments
#     return handle_feedback_request(action, data)

# Add additional routes as needed for other functionalities
