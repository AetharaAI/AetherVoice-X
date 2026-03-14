FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg espeak-ng libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

COPY services/kokoro/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cu128 torch==2.8.0 torchaudio==2.8.0 \
    && pip install --no-cache-dir -r /tmp/requirements.txt

COPY services/kokoro /app

CMD ["sh", "-lc", "python3 -m uvicorn app.main:app --host 0.0.0.0 --port ${KOKORO_RUNTIME_PORT:-8026}"]
