ARG VARIANT=3.9
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

SHELL ["/bin/fish", "-c"]

ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get update && apt-get install -y fish
RUN apt-get -y install meson cmake fuse3 libfuse3-dev libglib2.0-dev

RUN apt-get update && apt-get install -y     wget     libopenexr-dev     bzip2     build-essential     zlib1g-dev     libxmu-dev     libxi-dev     libxxf86vm-dev     libfontconfig1     libxrender1     libgl1-mesa-glx     xz-utils     tzdata   && apt-get clean -y   && rm -rf /var/lib/apt/lists/*.* # buildkit

USER vscode

RUN mkdir -p $HOME/.local/share/rendering_server_worker && chown vscode -R $HOME

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

RUN source $HOME/.poetry/env && poetry config virtualenvs.create false
