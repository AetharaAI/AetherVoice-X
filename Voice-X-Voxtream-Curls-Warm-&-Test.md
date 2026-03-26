

mkdir -p ~/tmp-models/voxtral-sentinel-4b
hf download trishtan/voxtral-sentinel-4b --local-dir ~/tmp-models/voxtral-sentinel-4b
mkdir -p /mnt/aetherpro/models/audio/trishtan/voxtral-sentinel-4b
rsync -ah --info=progress2 ~/tmp-models/voxtral-sentinel-4b/ /mnt/aetherpro/models/audio/trishtan/voxtral-sentinel-4b/


docker compose down voxtream2-provider
docker compose up -d voxtream2-provider
docker compose logs -f voxtream2-provider


curl http://127.0.0.1:8075/health


# 1. In Aether-Voice-X on the VM
git pull
docker compose build tts
docker compose up -d tts

# 2. Run the seed script once (needs httpx — should already be in your venv)
python3 scripts/seed_voxtream_voices.py

# 3. In voxtream-experiments (if you pushed new WAVs there)
git pull
docker compose restart   # picks up new audio-refs on next stream/start



docker compose up -d voxtream2-provider
docker compose logs -f voxtream2-provider
curl http://127.0.0.1:8075/health

docker compose down voxtream2-provider
docker compose build voxtream2-provider
docker compose up -d voxtream2-provider
docker compose exec voxtream2-provider ls -l /app/audio-refs


docker compose exec voxtream2-provider /app/.venv/bin/python -c "import voxtream; print(voxtream.__file__)"
docker compose exec voxtream2-provider /app/.venv/bin/python -c "from voxtream.generator import SpeechGenerator; print('ok')"



curl -X POST http://127.0.0.1:8075/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model":"voxtream2_realtime",
    "input":"Thank you for calling Aethara. I can help you with that now.",
    "voice":"reference_audio_required",
    "prompt_audio_path":"/app/audio-refs/bella_voice_ref.wav",
    "speaking_rate":3.0,
    "response_format":"wav"
  }' > voxstream2-test.json


PID=mkdir -p ~/tmp-models/voxtral-sentinel-4b
hf download trishtan/voxtral-sentinel-4b --local-dir ~/tmp-models/voxtral-sentinel-4b
mkdir -p /mnt/aetherpro/models/audio/trishtan/voxtral-sentinel-4b
rsync -ah --info=progress2 ~/tmp-models/voxtral-sentinel-4b/ /mnt/aetherpro/models/audio/trishtan/voxtral-sentinel-4b/
watch -n 2 "ps -p $PID -o pid,etime,%cpu,%mem,stat,cmd"
