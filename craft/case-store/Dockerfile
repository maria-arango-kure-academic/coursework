FROM python:3.12-alpine

WORKDIR /app
COPY blob.py /app/blob.py

RUN mkdir -p /data
ENV BLOB_DATA_DIR=/data \
    BLOB_PORT=8088 \
    BLOB_ALLOW_ORIGIN=* \
    BLOB_MAX_BYTES=262144

EXPOSE 8088

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget -qO- http://localhost:8088/healthz >/dev/null || exit 1

CMD ["python", "/app/blob.py"]
