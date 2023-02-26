ARG VARIANT=3.9
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

RUN apt-get update && apt-get install -y fish

RUN mkdir /data_dev && chown -R vscode /data_dev && chmod 775 /data_dev

RUN mkdir /data_test && chown -R vscode /data_test && chmod 775 /data_test

COPY . .
