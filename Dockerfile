FROM n8nio/n8n:latest

USER root

SHELL ["/bin/bash", "-c"]

RUN apt-get update -y \
    && apt-get install -y python3 python3-pip \
    && pip3 install reportlab pillow \
    && apt-get clean

USER node
