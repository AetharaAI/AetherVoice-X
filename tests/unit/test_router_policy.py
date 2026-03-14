from aether_common.model_aliases import normalize_asr_model_name, normalize_tts_model_name
from aether_common.settings import Settings

from services.gateway.app.services.router_policy import choose_asr_model, choose_tts_model


def test_choose_batch_asr_defaults_to_faster_whisper():
    settings = Settings()
    selected = choose_asr_model("auto", streaming=False, language="auto", settings=settings)
    assert selected == "faster_whisper"


def test_choose_streaming_asr_prefers_default_realtime():
    settings = Settings()
    selected = choose_asr_model("auto", streaming=True, language="auto", settings=settings)
    assert selected == normalize_asr_model_name(settings.default_asr_model)


def test_choose_tts_stream_prefers_stream_model():
    settings = Settings()
    selected = choose_tts_model("auto", streaming=True, context_mode="conversation", settings=settings)
    assert selected == normalize_tts_model_name(settings.default_stream_tts_model)


def test_normalize_tts_model_name_maps_kokoro_aliases():
    assert normalize_tts_model_name("kokoro") == "kokoro_realtime"
    assert normalize_tts_model_name("kokoro-realtime") == "kokoro_realtime"
