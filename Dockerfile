FROM n8nio/n8n:2.24.0

USER root

# Cài Python + thư viện
RUN apk add --no-cache python3 py3-pip poppler-utils \
    && pip3 install reportlab pillow --break-system-packages

# Copy Python script vào image — tránh nhúng vào n8n command
COPY infographic_script.py /usr/local/bin/infographic_script.py
RUN chmod +x /usr/local/bin/infographic_script.py

USER node
