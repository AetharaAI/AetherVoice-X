FROM vllm/vllm-openai:nightly

RUN python3 -m pip install --no-cache-dir --upgrade --pre "vllm[audio]" \
    --extra-index-url https://wheels.vllm.ai/nightly \
    && python3 -m pip install --no-cache-dir soxr librosa soundfile "openai>=1.109.1" \
    && python3 - <<'PY'
from pathlib import Path

target = Path("/usr/local/lib/python3.12/dist-packages/vllm/entrypoints/openai/server_utils.py")
source = target.read_text()
needle = 'if scope["type"] not in ("http", "websocket") or scope["method"] == "OPTIONS":'
replacement = 'if scope["type"] not in ("http", "websocket") or (scope["type"] == "http" and scope.get("method") == "OPTIONS"):'
if needle not in source:
    raise SystemExit("expected vLLM websocket middleware guard not found")
target.write_text(source.replace(needle, replacement))
print(f"patched {target}")
PY
