# syntax=docker/dockerfile:1
FROM --platform=linux/amd64 python:3.9.1
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
CMD [ "python3","app.py"]
