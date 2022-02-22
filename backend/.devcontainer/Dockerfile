FROM mcr.microsoft.com/vscode/devcontainers/python:0-3.10

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive && apt-get -y install --no-install-recommends fish

RUN mkdir /data

RUN chown vscode /data && chmod 777 /data

USER vscode

RUN mkdir -p $HOME/.local/share/fish

RUN curl -sSL "https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py" | python3 -
RUN $HOME/.local/bin/poetry config virtualenvs.create false

