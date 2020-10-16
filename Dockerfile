FROM python:3-alpine as base

WORKDIR /usr/src/app

RUN wget -q -O- https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH=/root/.poetry/bin:${PATH}

FROM base as production
COPY ./ ./
RUN poetry install --no-dev -n
CMD [ "poetry", "run", "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]

FROM base as development
COPY --from=production /usr/src/app/pyproject.toml pyproject.toml
RUN poetry install -n
CMD [ "poetry", "run", "flask", "run", "--host=0.0.0.0"]
