FROM python:3.12-slim

WORKDIR /code

COPY user_service/requirements.txt /code/user_service/
RUN pip install --no-cache-dir -r user_service/requirements.txt


ENTRYPOINT uvicorn user_service.user_controller:app --host 0.0.0.0 --port $PORT --reload --reload-dir user_service