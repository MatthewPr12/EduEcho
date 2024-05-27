# Project Objective & Description

**EduEcho**:

 A project designed to create a comprehensive feedback system for university courses.

**Features**:
- **Leave Feedback**: 

  Students can leave detailed reviews on courses.
- **Rate Courses**: 
  
  Students can rate courses on various parameters.
- **Respond to Comments**: 

  Engage in discussions by responding to comments.
- **Promote Comments**: 

  Highlight useful feedback through upvotes or downvotes.
- **Anonymous Feedback**: 

  Option to leave feedback anonymously, ensuring honest opinions.



## Running the services
```bash
docker compose up -d
```

## Stopping the services
```bash
docker compose down
```


## Services Docs
- [Feedback Service](feedback_service/README.md)

- [User Service](user_service/README.md)


# Gateway Commands:

## GET

- ### /course/
  Retrieves all registered courses.

  **HTTP Request**
  ```http request
  GET http://localhost:8000/course/
  ```

  **Curl Command**
  ```bash
  curl -X 'GET' \
    'http://localhost:8000/course/' \
    -H 'accept: application/json'
  ```

  **Expected Response**
  ```json
  {
    "message": "All courses retrieved successfully",
    "courses": [
      {
        "_id": "665390d3d5d5b4445e98df53",
        "course_name": "Introduction to Programming",
        "teacher_name": "Andrii Romanyuk",
        "number_of_students": 100,
        "rating_sum": 0,
        "rating_count": 0,
        "id": null
      }
    ]
  }
  ```

- ### /course/{id}
  Retrieves details of a specific course by its ID.

  **HTTP Request**
  ```http request
  GET http://localhost:8000/course/{id}
  ```

  **Curl Command**
  ```bash
  curl -X 'GET' \
    'http://localhost:8000/course/665390d3d5d5b4445e98df53' \
    -H 'accept: application/json'
  ```

  **Expected Response**
  ```json
  {
    "course_name": "Introduction to Programming",
    "teacher_name": "Andrii Romanyuk",
    "number_of_students": 100,
    "rating_sum": 0,
    "rating_count": 0,
    "id": null
  }
  ```

- ### /feedback/comments
  Retrieves feedback on a course, replies to a specific comment, or comments on a course by a specific user.

  **HTTP Request**
  ```http request
  GET http://localhost:8000/feedback/comments?course_id=66539e7d40eb9b6a4f306bea&replied_to_id=0148d81d-2c0e-43e6-b222-1fbcc1c9d14c
  ```

  **Curl Command**
  ```bash
  curl -X 'GET' \
    'http://localhost:8000/feedback/comments?course_id=66539e7d40eb9b6a4f306bea&replied_to_id=0148d81d-2c0e-43e6-b222-1fbcc1c9d14c' \
    -H 'accept: application/json'
  ```

  **Expected Response**
  ```json
  [
    {
      "course_id": "66539e7d40eb9b6a4f306bea",
      "replied_to_id": "0148d81d-2c0e-43e6-b222-1fbcc1c9d14c",
      "user_id": "user_abc",
      "comment_text": "i did not like it",
      "comment_id": "921e03f2-8b9b-4e01-9195-ee0d9e1789f1",
      "likes": 0,
      "dislikes": 0,
      "is_deleted": false,
      "is_edited": false,
      "timestamp": "2024-05-27T03:10:35.223000",
      "current_user_assessment": null
    }
  ]
  ```

## POST

- ### /course/
  Adds a new course to the database.

  **Curl Command**
  ```bash
  curl -X 'POST' \
    'http://localhost:8000/course/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
      "course_name": "Introduction to Programming",
      "teacher_name": "Andrii Romanyuk",
      "number_of_students": 100
    }'
  ```

  **Expected Response**
  ```json
  "66539e7d40eb9b6a4f306bea"
  ```

- ### /user/signup/
  Signs up a user.

  **Curl Command**
  ```bash
  curl -X 'POST' \
    'http://localhost:8000/user/signup?faculty=apps&program=ba' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
      "username": "user1234",
      "password_hash": "123"
    }'
  ```

  **Expected Response**
  ```json
  "Signup successful"
  ```

- ### /user/login
  Logs a user into the system.

  **Curl Command**
  ```bash
  curl -X 'POST' \
    'http://localhost:8000/user/login' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
      "username": "user1234",
      "password_hash": "123"
    }'
  ```

  **Expected Response**
  ```json
  "Login successful"
  ```

- ### /course/rate
  Allows a user to rate a course.

  **Curl Command**
  ```bash
  curl -X 'POST' \
    'http://localhost:8000/course/rate' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
      "course_id": "66539e7d40eb9b6a4f306bea",
      "rating": 5,
      "user_id": "user1234"
    }'
  ```

  **Expected Response**
  ```json
  {
    "message": "Rating added successfully"
  }
  ```

- ### /feedback/comments

  1. Leave a comment.

  **Curl Command**
  ```bash
  curl -X 'POST' \
    'http://localhost:8000/feedback/comment' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
      "course_id": "66539e7d40eb9b6a4f306bea",
      "replied_to_id": null,
      "user_id": "user1234",
      "comment_text": "amazing"
    }'
  ```

  **Expected Response**
  ```json
  {
    "course_id": "66539e7d40eb9b6a4f306bea",
    "replied_to_id": null,
    "user_id": "user1234",
    "comment_text": "amazing",
    "comment_id": "0148d81d-2c0e-43e6-b222-1fbcc1c9d14c",
    "likes": 0,
    "dislikes": 0,
    "is_deleted": false,
    "is_edited": false,
    "timestamp": "2024-05-27T03:09:01.060704",
    "current_user_assessment": 0
  }
  ```

  2. Reply to a comment.

  **Curl Command**
  ```bash
  curl -X 'POST' \
    'http://localhost:8000/feedback/comment' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
      "course_id": "66539e7d40eb9b6a4f306bea",
      "replied_to_id": "0148d81d-2c0e-43e6-b222-1fbcc1c9d14c",
      "user_id": "user_abc",
      "comment_text": "i did not like it"
    }'
  ```

  **Expected Response**
  ```json
  {
    "course_id": "66539e7d40eb9b6a4f306bea",
    "replied_to_id": "0148d81d-2c0e-43e6-b222-1fbcc1c9d14c",
    "user_id": "user_abc",
    "comment_text": "i did not like it",
    "comment_id": "921e03f2-8b9b-4e01-9195-ee0d9e1789f1",
    "likes": 0,
    "dislikes": 0,
    "is_deleted": false,
    "is_edited": false,
    "timestamp": "2024-05-27T03:10:35.223194",
    "current_user_assessment": 0
  }
  ```

## PUT

- ### /feedback/comment
  Edits a comment.

  **Curl Command**
  ```bash
  curl -X 'PUT' \
    'http://localhost:8000/feedback/comment?new_comment_text=truly%20awesome' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
      "course_id": "66539e7d40eb9b6a4f306bea",
      "replied_to_id": null,
      "comment_id": "0148d81d-2c0e-43e6-b222-1fbcc1c9d14c"
    }'
  ```

  **Expected Response**
  ```json
  "Comment has been modified"
  ```

- ### /feedback/rate_comment
  Rates a comment.
  
  - 0 - NO_ASSESSMENT
  - 1 - LIKE_ASSESSMENT
  - 2 - DISLIKE_ASSESSMENT

  **Curl Command**
  ```bash
  curl -X 'PUT' \
    'http://localhost:8000/feedback/rate_comment?assessor_user_id=user1234&assessment=2' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
      "course_id": "66539e7d40eb9b6a4f306bea",
      "replied_to_id": null,
      "comment_id": "0148d81d-2c0e-43e6-b222-1fbcc1c9d14c"
    }'
  ```

  **Expected Response**
  ```json
  "The comment assessment was successful"
  ```

## DELETE

- ### /feedback/comment
  Marks a comment as deleted.

  **Curl Command**
  ```bash
  curl -X 'DELETE' \
    'http://localhost:8000/feedback/comment' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
      "course_id": "66539e7d40eb9b6a4f306bea",
      "replied_to_id": null,
      "comment_id": "0148d81d-2c0e-43e6-b222-1fbcc1c9d14c"
    }'
  ```

  **Expected Response**
  ```json
  "Comment has been marked deleted."
  ```
