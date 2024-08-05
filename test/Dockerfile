FROM mambaorg/micromamba:1.5.8-jammy
USER root

ARG sub_dir
ARG notebook
ENV env_sub_dir=$sub_dir
ENV env_notebook=$notebook

ENV AWS_SECRET_ACCESS_KEY=no-access
ENV AWS_ACCESS_KEY_ID=no-access
ENV AWS_SESSION_TOKEN=no-access
ENV AWS_REGION=us-west-2

ENV PYTHONDONTWRITEBYTECODE=true

WORKDIR /workdir

COPY build-netrc.sh notebook-entrypoint.sh ./

RUN mkdir ./${sub_dir}
COPY ${sub_dir}/environment.yaml ./${sub_dir}

RUN micromamba create -y -f ${sub_dir}/environment.yaml \
    && micromamba clean --all --force-pkgs-dirs --yes

COPY ${sub_dir} ./${sub_dir}

ENTRYPOINT /bin/bash ./notebook-entrypoint.sh
