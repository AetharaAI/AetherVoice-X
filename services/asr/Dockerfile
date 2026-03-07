FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*

COPY services/asr/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app

ENV PYTHONPATH=/app/services/worker-common:/app/services/asr

CMD ["sh", "-lc", "uvicorn app.main:app --host ${ASR_HOST:-0.0.0.0} --port ${ASR_PORT:-8090}"]
