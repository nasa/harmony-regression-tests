FROM python:3.8.7-buster

WORKDIR /opt/harmony

RUN pip install poetry

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

COPY Harmony.ipynb .
COPY NASA_logo.svg .
COPY harmony/ ./harmony/

ENV environment="uat"
ENTRYPOINT poetry run papermill Harmony.ipynb Results.ipynb -p environment $environment
