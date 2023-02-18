FROM python:3.7.3-alpine3.9

COPY src /app
WORKDIR /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 5000
