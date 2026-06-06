FROM n8nio/n8n:latest
USER root
RUN apt-get update && apt-get install -y python3 python3-pip \
    && pip3 install reportlab pillow --break-system-packages \
    && rm -rf /var/lib/apt/lists/*
USER node
