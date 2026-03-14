









cd /home/cory/Aether-Voice-Platform/Aether-Voice-X
docker compose --profile kokoro up -d --build kokoro tts gateway frontend










cd /home/cory/Aether-Voice-Platform/Aether-Voice-X
docker compose --profile voxtral --profile kokoro up -d --build voxtral kokoro tts gateway frontend asr





docker compose --profile kokoro ps
docker compose --profile kokoro logs -f kokoro tts gateway frontend






curl -sf http://127.0.0.1:8018/health
curl -sf http://127.0.0.1:8010/api/health
curl -sf http://127.0.0.1:8091/internal/health
curl -sf http://127.0.0.1:8010/api/v1/models

