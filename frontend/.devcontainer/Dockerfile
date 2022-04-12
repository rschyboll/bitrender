FROM mcr.microsoft.com/vscode/devcontainers/javascript-node:0-16

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive && apt-get -y install --no-install-recommends fish

USER node

RUN mkdir -p $HOME/.local/share/fish
