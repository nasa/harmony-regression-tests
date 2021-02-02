FROM python:3.8.7-buster

WORKDIR /opt/harmony

RUN pip install poetry
RUN mkdir -p ./output

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

COPY notebooks ./notebooks
COPY harmony ./harmony
COPY run_notebooks.sh .

ENTRYPOINT ./run_notebooks.sh -p harmony_host_url $harmony_host_url
