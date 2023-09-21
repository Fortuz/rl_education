# Selecting base image
FROM jupyter/minimal-notebook:python-3.11

# Installing required packages
COPY --chown=${NB_UID}:${NB_GID} requirements.txt /tmp/
RUN pip install --quiet --no-cache-dir --requirement /tmp/requirements.txt

# Additional configuration
ENV DIR="$HOME/work"
WORKDIR $DIR
ENV JUPYTER_ENABLE_LAB=yes
RUN fix-permissions "$DIR"

# Starting JupyterLab
CMD jupyter lab \
    --ip 0.0.0.0 \
    --port 8888 \
    --ServerApp.terminado_settings="shell_command=['/bin/bash']" \
    --allow-root \
    --NotebookApp.token='' \
    --NotebookApp.password='' \
