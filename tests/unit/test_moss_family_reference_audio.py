from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import torch
import torchaudio

from services.moss.app.family import RuntimeAssets, SynthesizeRequest, _build_conversations


class FakeProcessor:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def build_user_message(self, **kwargs: object) -> dict[str, object]:
        self.calls.append(kwargs)
        return {"kwargs": kwargs}


def _runtime(*, kind: str, sample_rate: int = 24000) -> RuntimeAssets:
    return RuntimeAssets(
        kind=kind,
        device=torch.device("cpu"),
        dtype=torch.float32,
        model_source="test-model",
        codec_source=None,
        sample_rate=sample_rate,
        max_new_tokens=16,
        temperature=0.8,
        top_p=0.6,
        top_k=50,
        repetition_penalty=1.2,
        processor=FakeProcessor(),
        model=SimpleNamespace(),
    )


def _write_wav(path: Path, *, sample_rate: int, channels: int) -> None:
    seconds = 0.1
    frames = int(sample_rate * seconds)
    wav = torch.linspace(-0.2, 0.2, frames, dtype=torch.float32).repeat(channels, 1)
    torchaudio.save(path.as_posix(), wav, sample_rate)


def test_build_conversations_normalizes_tts_reference_audio(tmp_path: Path) -> None:
    runtime = _runtime(kind="tts")
    reference_path = tmp_path / "voice_ref.wav"
    _write_wav(reference_path, sample_rate=44100, channels=2)

    request = SynthesizeRequest(
        text="test",
        metadata={
            "extra": {
                "reference_audio_path": reference_path.as_posix(),
                "resolved_voice": {
                    "voice_id": "voice_a",
                    "reference_audio_path": reference_path.as_posix(),
                },
            }
        },
    )

    conversations, mode, artifacts = _build_conversations(runtime, request, temp_dir=tmp_path / "normalized")

    assert mode == "generation"
    assert conversations
    assert runtime.processor.calls[0]["reference"] != [reference_path.as_posix()]
    normalized_path = Path(runtime.processor.calls[0]["reference"][0])
    assert normalized_path.exists()
    normalized_wav, normalized_sr = torchaudio.load(normalized_path.as_posix())
    assert normalized_sr == runtime.sample_rate
    assert normalized_wav.shape[0] == 1
    assert artifacts["original_reference_audio_path"] == reference_path.as_posix()
    assert artifacts["normalized_reference_audio_path"] == normalized_path.as_posix()
    assert artifacts["reference_audio_source_sample_rate"] == 44100
    assert artifacts["reference_audio_target_sample_rate"] == runtime.sample_rate
    assert artifacts["reference_audio_source_channels"] == 2
    assert artifacts["reference_audio_resampled"] is True
    assert artifacts["reference_audio_mono_mixed"] is True
    assert artifacts["actual_runtime_conditioning_source"] == normalized_path.as_posix()


def test_build_conversations_normalizes_ttsd_speaker_references(tmp_path: Path) -> None:
    runtime = _runtime(kind="ttsd")
    speaker_path = tmp_path / "speaker_ref.wav"
    _write_wav(speaker_path, sample_rate=48000, channels=2)

    request = SynthesizeRequest(
        text="[S1] hello there",
        metadata={
            "extra": {
                "speaker_references": [
                    {
                        "speaker": "S1",
                        "audio_path": speaker_path.as_posix(),
                    }
                ]
            }
        },
    )

    _conversations, _mode, artifacts = _build_conversations(runtime, request, temp_dir=tmp_path / "normalized_speakers")

    assert runtime.processor.calls[0]["text"] == "[S1] hello there"
    assert "reference" not in runtime.processor.calls[0]

    normalized_path = Path(artifacts["normalized_speaker_reference_paths"][0])
    assert normalized_path.exists()
    normalized_wav, normalized_sr = torchaudio.load(normalized_path.as_posix())
    assert normalized_sr == runtime.sample_rate
    assert normalized_wav.shape[0] == 1
    assert artifacts["original_speaker_reference_paths"] == [speaker_path.as_posix()]
    assert artifacts["speaker_reference_normalization"][0]["reference_audio_resampled"] is True
    assert artifacts["speaker_reference_normalization"][0]["reference_audio_mono_mixed"] is True
    assert artifacts["actual_runtime_conditioning_source"] == normalized_path.as_posix()
