FROM n8nio/n8n:1.94.1

USER root

RUN apk add --no-cache python3 py3-pip \
    && pip3 install reportlab pillow --break-system-packages

USER node
