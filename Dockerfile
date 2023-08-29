FROM jupyter/minimal-notebook:python-3.11

COPY --chown=${NB_UID}:${NB_GID} requirements.txt /tmp/

RUN pip install --quiet --no-cache-dir --requirement /tmp/requirements.txt && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

ENV JUPYTER_ENABLE_LAB=yes
