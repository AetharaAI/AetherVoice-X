FROM vllm/vllm-openai:nightly-36735fd77224467e6580f3bd48eb32d4fca8c72e

# Keep Voxtral on one coherent vLLM/Transformers build. Do not overlay a
# floating nightly `pip install vllm...` on top of this pinned base image.
RUN python3 -m pip install --no-cache-dir soxr librosa soundfile "openai==1.109.1" \
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
