FROM python:3.12.10-slim

WORKDIR /app
# WORKDIR /app = mkdir app and cd app

COPY . .
# Copies all files from . to /app (.) working directory

RUN pip install -r requirements.txt

# all above instructions only run once, unless something changes

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# run docker build -t plotulate . to build image