FROM python:3-alpine as base

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./
COPY templates ./templates
COPY .env.template .env

FROM base as production
ENV FLASK_ENV=production
CMD [ "flask", "run", "--no-reload", "--host=0.0.0.0"]

FROM base as development
CMD [ "flask", "run", "--host=0.0.0.0"]
