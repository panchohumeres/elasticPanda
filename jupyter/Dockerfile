FROM jupyter/base-notebook

RUN python --version

RUN conda install --quiet --yes -c \
    conda-forge pandas


RUN pip install -U search


VOLUME /home/jovyan/work
WORKDIR /home/jovyan/work
