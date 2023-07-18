FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

COPY requirements.txt /tmp/pip-tmp/

RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp
