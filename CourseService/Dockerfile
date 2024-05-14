# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY CourseService/requirements.txt /app/CourseService/requirements.txt
#COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r CourseService/requirements.txt

# Expose the port the app runs on
EXPOSE 8001

# Define environment variable
ENV MONGO_USERNAME=admin
ENV MONGO_PASSWORD=password
ENV PYTHONPATH=/app

# Run app.py when the container launches
ENTRYPOINT uvicorn CourseService.course_controller:app --host 0.0.0.0 --port $PORT --reload
