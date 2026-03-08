FROM nvidia/cuda:12.8.1-cudnn-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip git ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY services/moss/requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache-dir --upgrade pip \
    && python3 -m pip install --no-cache-dir -r /tmp/requirements.txt \
    && git clone --depth=1 https://github.com/OpenMOSS/MOSS-TTS.git /opt/MOSS-TTS \
    && python3 -m pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cu128 -e "/opt/MOSS-TTS[torch-runtime]"

COPY services/moss /app

ENV PYTHONUNBUFFERED=1

CMD ["sh", "-lc", "python3 -m uvicorn app.main:app --host 0.0.0.0 --port ${MOSS_RUNTIME_PORT:-8021}"]
