# Selecting base image
FROM jupyter/minimal-notebook:python-3.11

# Installing required packages
USER root
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
USER jovyan
COPY --chown=${NB_UID}:${NB_GID} requirements.txt /tmp/
RUN pip install --no-cache-dir --requirement /tmp/requirements.txt
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN git clone https://github.com/MattChanTK/gym-maze /tmp/gym-maze
WORKDIR /tmp/gym-maze/
RUN python setup.py install
RUN rm -r /tmp/gym-maze/

# Additional configuration
ENV DIR="$HOME/work"
WORKDIR $DIR
ENV JUPYTER_ENABLE_LAB=yes

# Starting JupyterLab
CMD jupyter lab \
    --ip 0.0.0.0 \
    --port 8888 \
    --ServerApp.terminado_settings="shell_command=['/bin/bash']" \
    --allow-root \
    --NotebookApp.token='' \
    --NotebookApp.password='' \
