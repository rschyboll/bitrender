FROM mcr.microsoft.com/vscode/devcontainers/python:3.10

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8 LANGUAGE=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update && apt-get install -y fish

USER vscode

RUN curl -sSL "https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py" | python3 -
RUN $HOME/.local/bin/poetry config virtualenvs.create false

