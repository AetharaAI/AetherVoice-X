FROM vllm/vllm-openai:nightly

RUN python3 -m pip install --no-cache-dir --upgrade --pre "vllm[audio]" \
    --extra-index-url https://wheels.vllm.ai/nightly \
    && python3 -m pip install --no-cache-dir soxr librosa soundfile "openai>=1.109.1"

ENV VLLM_USE_V1=1
