FROM continuumio/miniconda3:latest

ARG sub_dir
ARG notebook
ENV env_sub_dir=$sub_dir
ENV env_notebook=$notebook

ENV AWS_SECRET_ACCESS_KEY=no-access
ENV AWS_ACCESS_KEY_ID=no-access
ENV AWS_REGION=us-west-2

WORKDIR /root

RUN conda install --channel=conda-forge --name=base conda-lock -q -y

COPY build-netrc.sh notebook-entrypoint.sh ./
RUN mkdir ./${sub_dir}
COPY ${sub_dir}/conda-lock.yml ./${sub_dir}
RUN conda-lock install -n papermill ./${sub_dir}/conda-lock.yml


ENTRYPOINT /bin/bash ./notebook-entrypoint.sh
