FROM python:3.7-alpine3.8

WORKDIR /app
COPY requirements.txt /app/

RUN \
  apk add --no-cache libxml2-dev libxslt-dev gcc libc-dev libxml2  && \
  pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python",  "low_hanging.py"]
