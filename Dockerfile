FROM python:3.8.7-buster

WORKDIR /opt/harmony

RUN pip install poetry
RUN mkdir -p ./output

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

COPY Harmony.ipynb .
COPY harmony/ ./harmony/



ENV environment="uat"
ENTRYPOINT poetry run papermill Harmony.ipynb /root/output/Results.ipynb -p environment $environment
