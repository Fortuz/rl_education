FROM jupyter/minimal-notebook:python-3.11

COPY --chown=${NB_UID}:${NB_GID} requirements.txt /tmp/

WORKDIR "${HOME}/work"

RUN pip install --quiet --no-cache-dir --requirement /tmp/requirements.txt && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

EXPOSE 8888

ENV JUPYTER_ENABLE_LAB=yes

CMD jupyter lab \
    --ip 0.0.0.0 \
    --port 8888 \
    --ServerApp.terminado_settings="shell_command=['/bin/bash']" \
    --allow-root \
    --NotebookApp.token='' \
    --NotebookApp.password='' \
