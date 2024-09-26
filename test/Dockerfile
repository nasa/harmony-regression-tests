FROM mambaorg/micromamba:1.5.8-jammy
USER root

ARG sub_dir
ARG notebook
ARG shared_utils=false
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

# Include shared utility functions if requested.  This is a bit awkward, it
# always copies the shared utils directory to the image, but then deletes it if
# you didn't want it.
COPY shared_utils ./shared_utils
RUN if [ "$shared_utils" = "false" ]; then \
        rm -rf ./shared_utils; \
    fi

COPY ${sub_dir} ./${sub_dir}

ENTRYPOINT /bin/bash ./notebook-entrypoint.sh
