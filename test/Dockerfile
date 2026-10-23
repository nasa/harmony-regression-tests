FROM mambaorg/micromamba:2.5.0-ubuntu22.04
USER root

ARG sub_dir
ARG notebook
ARG shared_utils=false
ENV env_sub_dir=$sub_dir
ENV env_notebook=$notebook

ENV PYTHONDONTWRITEBYTECODE=true

WORKDIR /workdir

COPY build-netrc.sh notebook-entrypoint.sh fetch-edl-credentials.py report.py requirements-astra.txt ./

RUN mkdir ./${sub_dir}
COPY ${sub_dir}/environment.yaml ./${sub_dir}

RUN micromamba create -y -f ${sub_dir}/environment.yaml \
    && micromamba clean --all --force-pkgs-dirs --yes

# fetch-edl-credentials.py/report.py's dependencies, needed when ASTRA=true.
# Installed unconditionally here, rather than per-suite environment.yaml, so every
# suite image supports ASTRA=true regardless of its own notebook dependencies.
RUN micromamba run -n papermill-${sub_dir} pip install -r requirements-astra.txt

# Include shared utility functions if requested.  This is a bit awkward, it
# always copies the shared utils directory to the image, but then deletes it if
# you didn't want it.
COPY shared_utils ./shared_utils
RUN if [ "$shared_utils" = "false" ]; then \
        rm -rf ./shared_utils; \
    fi

COPY ${sub_dir} ./${sub_dir}

ENTRYPOINT /bin/bash ./notebook-entrypoint.sh
