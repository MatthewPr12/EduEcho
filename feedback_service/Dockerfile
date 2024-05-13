FROM python:3.12-slim
LABEL authors="mrkorch"

RUN apt-get update
RUN pip install --upgrade pip

EXPOSE $PORT

WORKDIR /code

COPY feedback_service/requirements.txt /code/feedback_service/requirements.txt
RUN pip install -r feedback_service/requirements.txt

ENTRYPOINT uvicorn feedback_service.feedback_controller:app --host 0.0.0.0 --port $PORT --reload --reload-dir feedback_service