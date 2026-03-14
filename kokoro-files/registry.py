import httpx
import logging
from typing import AsyncGenerator, Dict, Optional, List
from config import settings
from tts.kokoro import KokoroTTS
from tts.base import BaseTTS

logger = logging.getLogger(__name__)

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

    async def synthesize_stream(self, text: str, voice: str = "default", speed: float = 1.0, ref_text: str = "") -> AsyncGenerator[bytes, None]:
        try:
            # Connect to microservice /generate_stream
            async with self.client.stream("POST", f"{self.url}/generate_stream", json={
                "text": text, "voice": voice, "speed": speed, "ref_text": ref_text
            }) as response:
                if response.status_code != 200:
                    logger.error(f"Remote {self.name} returned {response.status_code}")
                    return
                async for chunk in response.aiter_bytes():
                    yield chunk
        except Exception as e:
            logger.error(f"Remote {self.name} connection failed: {e}")

    async def synthesize(self, text: str, voice: str = "default", speed: float = 1.0, ref_text: str = "") -> bytes:
        try:
            # Connect to microservice /generate
            resp = await self.client.post(f"{self.url}/generate", json={
                "text": text, "voice": voice, "speed": speed, "ref_text": ref_text
            })
            resp.raise_for_status()
            return resp.content
        except Exception as e:
            logger.error(f"Remote {self.name} failed: {e}")
            raise

    def get_voices(self) -> List[Dict]:
        return [{"id": "default", "name": f"{self.name} Remote"}]

    def get_info(self) -> Dict:
        return {
            "name": self.name, 
            "description": self.description, 
            "type": "microservice", 
            "status": "online",
            "voices": self.get_voices(),
            "loaded": True
        }
    
    def cleanup(self):
        pass

class TTSRegistry:
    def __init__(self):
        self.models = {}

    def load_all(self, device_id="0"):
        # 1. Local Models (Fast/Light) - Kept in main container
        try:
            self.models["kokoro"] = KokoroTTS(settings.tts_path, device_id)
            logger.info("Local Kokoro Loaded")
        except Exception as e:
            logger.error(f"Kokoro load failed: {e}")

        # 2. Remote Microservices (Isolated Containers)
        self.models["f5-tts"] = RemoteTTSProxy(
            settings.tts_f5_url, 
            "f5-tts", 
            "Zero-Shot Cloning Service (F5)"
        )
        self.models["styletts2"] = RemoteTTSProxy(
            settings.tts_style_url, 
            "styletts2", 
            "High-Fidelity Service (StyleTTS2)"
        )
        logger.info("Remote proxies registered")

    def get(self, name):
        return self.models.get(name)

    def get_default(self):
        return self.models.get("kokoro")
    
    def list_loaded(self):
        return list(self.models.keys())
    
    def get_all_info(self):
        return {k: v.get_info() for k, v in self.models.items()}
    
    def is_loaded(self, name):
        return name in self.models
    
    def cleanup_all(self):
        if "kokoro" in self.models:
            self.models["kokoro"].cleanup()

tts_registry = TTSRegistry()