FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.12.23 /uv /usr/local/bin/uv

ARG sub_dir
ARG notebook
ARG shared_utils=false
ENV env_sub_dir=$sub_dir
ENV env_notebook=$notebook

ENV PYTHONDONTWRITEBYTECODE=true

WORKDIR /workdir

COPY build-netrc.sh notebook-entrypoint.sh ./

RUN mkdir ./${sub_dir}
COPY ${sub_dir}/requirements.txt ./${sub_dir}

RUN uv pip install --system --no-cache -r ${sub_dir}/requirements.txt

# Include shared utility functions if requested.  This is a bit awkward, it
# always copies the shared utils directory to the image, but then deletes it if
# you didn't want it.
COPY shared_utils ./shared_utils
RUN if [ "$shared_utils" = "false" ]; then \
        rm -rf ./shared_utils; \
    fi

COPY ${sub_dir} ./${sub_dir}

ENTRYPOINT ["/bin/bash", "./notebook-entrypoint.sh"]
