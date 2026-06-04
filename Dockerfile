FROM n8nio/n8n:latest

USER root

RUN apk add --no-cache \
    python3 \
    py3-pip \
    && python3 -m pip install --upgrade pip setuptools \
    && python3 -m pip install reportlab pillow \
    && ln -sf python3 /usr/bin/python

USER node
