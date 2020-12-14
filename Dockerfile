FROM jupyter/scipy-notebook:latest

WORKDIR /opt/harmony

# RUN curl -sSL
# https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py
        # | python -

RUN pip install poetry

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

COPY Harmony.ipynb .
COPY NASA_logo.svg .

ENV environment="uat"
ENTRYPOINT poetry run papermill Harmony.ipynb /tmp/Results.ipynb -p environment $environment
