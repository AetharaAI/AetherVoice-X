# TTS Module - Registry System & Model Architecture

The TTS module uses a **hybrid registry pattern** that combines local model loading with microservice proxying to handle dependency conflicts and optimize performance.

## 🏗️ Architecture Overview

The TTS registry manages three models with different loading strategies:

```
┌─────────────────────────────────────────────────────────────┐
│                    Gateway Service (Port 8000)               │
│                                                                │
│  ┌────────────────────────────────────────────────────┐     │
│  │            TTS Registry                             │     │
│  │                                                    │     │
│  │  Local Models (Loaded in Gateway):                 │     │
│  │  ┌──────────────┐                                  │     │
│  │  │   Kokoro     │ 82M params, 24kHz, 7 voices      │     │
│  │  │   (Fast TTS) │ Direct method calls              │     │
│  │  └──────────────┘                                  │     │
│  │                                                    │     │
│  │  Remote Proxies (Microservices):                   │     │
│  │  ┌──────────────┐     ┌──────────────────┐        │     │
│  │  │  F5-TTS      │────▶│ Microservice     │        │     │
│  │  │  (Cloning)   │     │ Port 8001        │        │     │
│  │  └──────────────┘     └──────────────────┘        │     │
│  │                                                    │     │
│  │  ┌──────────────┐     ┌──────────────────┐        │     │
│  │  │ StyleTTS2    │────▶│ Microservice     │        │     │
│  │  │  (Fallback)  │     │ Port 8002        │        │     │
│  │  └──────────────┘     └──────────────────┘        │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Current TTS Models

### 1. Kokoro-82M (Default & Fast TTS)

**Location:** Loaded locally in gateway container
**File:** `backend/tts/kokoro.py`
**Provider ID:** `"kokoro"`

**Characteristics:**
- Model Size: 82M parameters
- Sample Rate: 24kHz
- Built-in Voices: 7 voices
  - `af_sky` - Female, sky tone
  - `af_bella` - Female, bell-like
  - `af_heart` - Female, heart tone
  - `am_adam` - Male, Adam
  - `am_michael` - Male, Michael
  - `bf_emma` - Female, Emma
  - `bm_george` - Male, George
- Latency: ~100-300ms TTFB
- Supports streaming: Yes
- Supports cloning: No
- Best for: Realtime conversations, interactive applications

**Usage:**
```json
{
  "text": "Hello, how can I help you?",
  "voice": "af_sky",
  "provider": "kokoro",
  "speed": 1.0
}
```

**Meter Type:** `tts_fast`

---

### 2. F5-TTS (Voice Cloning)

**Location:** Isolated microservice (Port 8001)
**Service Directory:** `backend/services/f5/`
**Provider ID:** `"f5-tts"`

**Characteristics:**
- Model: F5-TTS with DiT architecture
- Model Size: ~1B parameters
- Sample Rate: 24kHz
- Latency: ~500-1000ms TTFB
- Supports streaming: Yes (emulated)
- Supports cloning: Yes (zero-shot)
- Best for: Voice cloning, custom voice synthesis

**Cloning Process:**
1. Client sends base64-encoded reference audio to gateway
2. Gateway converts audio and saves to shared volume (`/mnt/aetherpro/models/voice/temp_shared/`)
3. Gateway sends request to F5-TTS microservice with:
   - Text to synthesize
   - Path to reference audio (on shared volume)
   - Reference text (for alignment)
4. Microservice processes and returns audio
5. Gateway streams audio back to client
6. Gateway cleans up temporary reference file

**Usage (Voice Cloning):**
```json
{
  "text": "Hello, this is my cloned voice!",
  "reference_audio": "<base64_encoded_audio>",
  "reference_text": "This is a sample of my voice",
  "provider": "f5-tts",
  "speed": 1.0
}
```

**Dependencies:**
- PyTorch 2.4.0
- CUDA 12.1
- F5-TTS (git+https://github.com/SWivid/F5-TTS.git)

**Meter Type:** `tts_hq`

**Docker Configuration:**
- Base Image: `pytorch/pytorch:2.4.0-cuda12.1-cudnn9-runtime`
- Port: 8001
- Shared Volume: `/mnt/aetherpro/models/voice/temp_shared`

---

### 3. StyleTTS2 (Fallback)

**Location:** Isolated microservice (Port 8002)
**Service Directory:** `backend/services/style/`
**Provider ID:** `"styletts2"`

**Characteristics:**
- Model: StyleTTS2
- Model Size: ~1B parameters
- Sample Rate: 24kHz
- Latency: ~500-1000ms TTFB
- Supports streaming: Yes (emulated)
- Supports cloning: Yes
- Best for: Fallback/backup TTS service

**Note:** This model is rarely used and acts as a fallback. It exists because:
1. It requires PyTorch 2.1.0 (conflicts with F5-TTS's PyTorch 2.4.0)
2. It's kept for backward compatibility
3. Only used when explicitly requested via provider parameter

**Dependencies:**
- PyTorch 2.1.0
- CUDA 12.1
- StyleTTS2 0.1.6
- accelerate<0.26.0 (older version requirement)

**Meter Type:** `tts_hq`

**Docker Configuration:**
- Base Image: `pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime`
- Port: 8002
- PyTorch patch applied for compatibility with newer model files

---

## 🔄 TTS Registry System

### Registry Architecture

The `TTSRegistry` class (in `backend/tts/registry.py`) manages all TTS models:

```python
class TTSRegistry:
    def __init__(self):
        self.models = {}

    def load_all(self, device_id="0"):
        # 1. Load local models (fast, lightweight)
        self.models["kokoro"] = KokoroTTS(settings.tts_path, device_id)

        # 2. Create proxy objects for microservices
        self.models["f5-tts"] = RemoteTTSProxy(
            settings.tts_f5_url,  # http://tts-f5:8001
            "f5-tts",
            "Zero-Shot Cloning Service (F5)"
        )

        self.models["styletts2"] = RemoteTTSProxy(
            settings.tts_style_url,  # http://tts-style:8002
            "styletts2",
            "High-Fidelity Service (StyleTTS2)"
        )
```

### RemoteTTSProxy

The `RemoteTTSProxy` class wraps microservice calls:

```python
class RemoteTTSProxy(BaseTTS):
    """
    Proxy that forwards requests to isolated microservice containers.
    """
    def __init__(self, service_url: str, name: str, description: str):
        self.url = service_url
        self.name = name
        self.description = description
        # Long timeout because F5/Style can take a moment to start generating
        self.client = httpx.AsyncClient(timeout=120.0)

    async def synthesize_stream(self, text: str, voice: str = "default",
                                speed: float = 1.0, ref_text: str = "") -> AsyncGenerator[bytes, None]:
        # Forwards request to microservice /generate_stream endpoint
        async with self.client.stream("POST", f"{self.url}/generate_stream", json={
            "text": text, "voice": voice, "speed": speed, "ref_text": ref_text
        }) as response:
            async for chunk in response.aiter_bytes():
                yield chunk
```

**Key Features:**
- HTTPX async client with 120-second timeout
- Forwards requests to microservice endpoints
- Streams audio bytes back to caller
- Handles errors gracefully

### Registry API

The registry provides these methods:

```python
# Get a specific model
model = tts_registry.get("kokoro")
model = tts_registry.get("f5-tts")
model = tts_registry.get("styletts2")

# Get default model (kokoro)
default_model = tts_registry.get_default()

# List all loaded models
models = tts_registry.list_loaded()  # ["kokoro", "f5-tts", "styletts2"]

# Get info for all models
info = tts_registry.get_all_info()

# Check if model is loaded
is_loaded = tts_registry.is_loaded("kokoro")

# Cleanup all models
tts_registry.cleanup_all()
```

### BaseTTS Interface

All TTS models implement the `BaseTTS` abstract class:

```python
class BaseTTS(ABC):
    name: str = "base"
    description: str = "Base TTS"
    sample_rate: int = 24000
    supports_cloning: bool = False
    supports_streaming: bool = True

    @abstractmethod
    async def synthesize_stream(
        self,
        text: str,
        voice: str = "default",
        speed: float = 1.0
    ) -> AsyncGenerator[bytes, None]:
        pass

    @abstractmethod
    def get_voices(self) -> List[Dict]:
        pass

    @abstractmethod
    def cleanup(self) -> None:
        pass
```

## 🔌 Gateway Integration

The gateway service uses the registry in `backend/main.py`:

```python
from tts.registry import tts_registry

@app.on_event("startup")
async def lifespan():
    # Load all TTS models
    tts_registry.load_all(device_id=settings.gpu_device)
    default_tts = tts_registry.get("kokoro")

@app.post("/v1/tts/stream")
async def tts_stream(request: TTSRequest):
    # Get model from registry
    engine = tts_registry.get(request.provider)
    if not engine:
        raise HTTPException(503, detail="Provider not available")

    # Use the model
    async for chunk in engine.synthesize_stream(request.text, request.voice, request.speed):
        yield chunk

@app.post("/v1/tts/clone")
async def tts_clone(request: VoiceCloneRequest):
    # For cloning, gateway handles shared volume
    # and forwards path to microservice
    engine = tts_registry.get(request.provider)
    # ... process reference audio ...
    wav = await engine.synthesize(request.text, voice=str(shared_path),
                                   speed=request.speed, ref_text=request.reference_text)
```

## 📊 Model Selection Guide

| Use Case | Recommended Model | Reason |
|----------|-------------------|--------|
| Realtime conversation | **Kokoro** | Fast TTFB (~100-300ms), 7 built-in voices |
| Voice cloning | **F5-TTS** | Zero-shot cloning, high quality |
| Batch narration | **Kokoro** or **F5-TTS** | Kokoro for speed, F5 for quality |
| Fallback | **StyleTTS2** | Backup service, rarely needed |
| Interactive chatbot | **Kokoro** | Low latency critical |
| Podcast/dictation | **Kokoro** | Speed over quality |

## 🛠️ Configuration

### Environment Variables (backend/config.py)

```python
# Local TTS model path
tts_path: Path = Path("/mnt/aetherpro/models/voice/tts/kokoro-v1")

# Microservice URLs
tts_f5_url: str = "http://tts-f5:8001"
tts_style_url: str = "http://tts-style:8002"

# Shared volume for cloning reference files
shared_vol_path: Path = Path("/mnt/aetherpro/models/voice/temp_shared")
```

### Docker Compose Configuration

Services are defined in `docker-compose.yml`:

```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - tts-f5
      - tts-style

  tts-f5:
    build: ./backend/services/f5
    ports:
      - "8001:8001"
    volumes:
      - /mnt/aetherpro/models:/mnt/aetherpro/models:ro
      - voice-temp:/mnt/aetherpro/models/voice/temp_shared

  tts-style:
    build: ./backend/services/style
    ports:
      - "8002:8002"
    volumes:
      - /mnt/aetherpro/models:/mnt/aetherpro/models:ro

volumes:
  voice-temp:
```

## 🔍 Health Check

The `/v1/health` endpoint shows TTS model status:

```json
{
  "status": "ok",
  "services": {
    "tts_f5": true,
    "tts_style": true,
    "tts_kokoro": true
  }
}
```

## 📚 Endpoint Reference

### GET /v1/tts/voices

Lists all available TTS providers and voices:

```json
{
  "providers": {
    "kokoro": {
      "name": "kokoro",
      "description": "Fast TTS (82M params)",
      "sample_rate": 24000,
      "supports_cloning": false,
      "supports_streaming": true,
      "voices": [
        {"id": "af_sky", "name": "Sky"},
        {"id": "af_bella", "name": "Bella"},
        ...
      ],
      "loaded": true
    },
    "f5-tts": {
      "name": "f5-tts",
      "description": "Zero-Shot Cloning Service (F5)",
      "type": "microservice",
      "status": "online",
      "voices": [{"id": "default", "name": "f5-tts Remote"}],
      "loaded": true
    },
    "styletts2": {
      "name": "styletts2",
      "description": "High-Fidelity Service (StyleTTS2)",
      "type": "microservice",
      "status": "online",
      "voices": [{"id": "default", "name": "styletts2 Remote"}],
      "loaded": true
    }
  },
  "available": ["kokoro", "styletts2", "f5-tts"],
  "default": "kokoro"
}
```

## 🚀 Development

### Adding a New TTS Model

**Option 1: Local Model (if lightweight)**
1. Create `backend/tts/your_model.py` implementing `BaseTTS`
2. Add to `backend/tts/registry.py` in `load_all()`
3. Add config path to `backend/config.py`

**Option 2: Microservice (if heavy/has conflicts)**
1. Create `backend/services/your_service/` directory
2. Create `main.py` with FastAPI app
3. Create `Dockerfile` with proper dependencies
4. Add `RemoteTTSProxy` entry in `registry.py`
5. Add service to `docker-compose.yml`

### Testing

```bash
# Test Kokoro (local)
curl -X POST http://localhost:8000/v1/tts/stream \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "provider": "kokoro"}' --output test.wav

# Test F5-TTS (microservice)
curl -X POST http://localhost:8000/v1/tts/clone \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "reference_audio": "BASE64", "provider": "f5-tts"}' --output clone.wav
```

## 🐛 Troubleshooting

**F5-TTS not responding:**
- Check if `tts-f5` container is running: `docker ps`
- Check logs: `docker compose logs tts-f5`
- Verify shared volume is mounted
- Check network connectivity: `docker exec backend curl http://tts-f5:8001/generate`

**StyleTTS2 errors:**
- PyTorch version mismatch (needs 2.1.0)
- Check `weights_only` compatibility (patched in main.py)
- Verify model files exist at configured path

**Kokoro loading failures:**
- Check model path exists
- Verify GPU device ID in config
- Check available VRAM
