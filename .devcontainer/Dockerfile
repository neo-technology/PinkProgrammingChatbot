FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

RUN rm -f /etc/apt/sources.list.d/yarn.list
RUN apt-get update -y \
  && export DEBIAN_FRONTEND=noninteractive \
  # python module \
  && pip install --upgrade pip