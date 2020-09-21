FROM python:3-alpine as base

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

FROM base as production
COPY ./ ./
ENV FLASK_ENV=production
RUN pip install --no-cache-dir  gunicorn
CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]

FROM base as development
CMD [ "flask", "run", "--host=0.0.0.0"]
