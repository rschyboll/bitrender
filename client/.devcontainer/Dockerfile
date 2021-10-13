ARG VARIANT=3.9
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

RUN apt-get update && apt-get install -y fish

COPY . .
