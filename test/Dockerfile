FROM continuumio/miniconda3:latest

ARG sub_dir
ARG notebook
ENV env_sub_dir=$sub_dir
ENV env_notebook=$notebook

WORKDIR /root

RUN conda config --add channels conda-forge
RUN pip install conda-lock
RUN conda install conda-lock

COPY .netrc .netrc
RUN mkdir ./${sub_dir}
COPY ${sub_dir}/conda-linux-64.lock ./${sub_dir}

RUN conda create --name papermill --file ./${sub_dir}/conda-linux-64.lock

ENTRYPOINT export PATH=/opt/conda/envs/papermill/bin:$PATH; mkdir /root/output/${env_sub_dir}; papermill --cwd ${env_sub_dir} ${env_sub_dir}/${env_notebook} /root/output/${env_sub_dir}/Results.ipynb -p harmony_host_url $harmony_host_url