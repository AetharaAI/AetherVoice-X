FROM nvidia/cuda:12.8.1-cudnn-runtime-ubuntu24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip python3-venv git ffmpeg \
    && python3 -m venv "${VIRTUAL_ENV}" \
    && rm -rf /var/lib/apt/lists/*

COPY services/moss/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && git clone --depth=1 https://github.com/OpenMOSS/MOSS-TTS.git /opt/MOSS-TTS \
    && pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cu128 -e "/opt/MOSS-TTS[torch-runtime]"

COPY services/moss /app

CMD ["sh", "-lc", "python3 -m uvicorn app.main:app --host 0.0.0.0 --port ${MOSS_RUNTIME_PORT:-8021}"]
