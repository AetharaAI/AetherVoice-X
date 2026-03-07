FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*

COPY services/tts/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app

ENV PYTHONPATH=/app/services/worker-common:/app/services/tts

CMD ["sh", "-lc", "uvicorn app.main:app --host ${TTS_HOST:-0.0.0.0} --port ${TTS_PORT:-8091}"]
