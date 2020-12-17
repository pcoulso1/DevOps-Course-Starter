FROM python:3-alpine as base

WORKDIR /usr/src/app

ENV POETRY_HOME=/etc/poetry 
ENV PORT=5000

RUN wget -q -O- https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python && \
    chmod -R 755 ${POETRY_HOME}

ENV PATH=${POETRY_HOME}/bin:${PATH}

################## 
# Production stage
FROM base as production

# Only copy the files to be deployed on Production
COPY *.py *.lock *.toml *.md ./
COPY templates ./templates

# Install dependencies
RUN poetry config virtualenvs.create false --local &&\
    poetry install --no-dev -n

RUN chmod -R 777 poetry.toml

# Setup run command 
CMD [ "sh", "-c", "poetry run gunicorn -w 4 -b 0.0.0.0:$PORT 'app:create_app()'" ]

################## 
# Development stage
FROM base as development

# Copy the pyproject.toml from production stage
COPY --from=production /usr/src/app/pyproject.toml pyproject.toml

# Install dependencies
RUN poetry config virtualenvs.create false --local &&\
    poetry install -n

# Setup run command 
CMD [ "poetry", "run", "flask", "run", "--host=0.0.0.0"]

################## 
# Testing stage
FROM python:3-buster as test

WORKDIR /usr/src/app

ENV POETRY_HOME=/etc/poetry 

RUN wget -q -O- https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python && \
    chmod -R 755 ${POETRY_HOME}

ENV PATH=${POETRY_HOME}/bin:${PATH}/usr/src/app

# Install Chrome and WebDriver
RUN apt-get update && \
 wget -q -O- https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python &&\
 curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb &&\
 apt-get install ./chrome.deb -y &&\
 rm ./chrome.deb &&\
 LATEST=`curl -sSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE` &&\
 echo "Installing chromium webdriver version ${LATEST}" &&\
 curl -sSL https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip -o chromedriver_linux64.zip &&\
 apt-get install unzip -y &&\
 unzip ./chromedriver_linux64.zip &&\
 apt-get clean

# Copy all files
COPY ./ ./

# Install dependencies
RUN poetry config virtualenvs.create false --local &&\
    poetry install -n

# Setup the entry point
ENTRYPOINT ["poetry", "run", "pytest"]
