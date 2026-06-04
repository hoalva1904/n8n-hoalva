FROM n8nio/n8n:latest

USER root

RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-pillow \
    freetype \
    freetype-dev \
    jpeg-dev \
    zlib-dev \
    && pip3 install reportlab --break-system-packages

USER node
