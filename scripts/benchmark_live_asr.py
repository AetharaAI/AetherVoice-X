#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import base64
import json
import time
import uuid
import wave
from pathlib import Path
from urllib import request as urllib_request

import websockets


def encode_pcm16(payload: bytes) -> str:
    return base64.b64encode(payload).decode("utf-8")


def post_json(url: str, payload: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib_request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib_request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


async def run() -> int:
    parser = argparse.ArgumentParser(description="Benchmark the ASR live websocket path with a WAV file.")
    parser.add_argument("--api-base", default="http://127.0.0.1:8010/v1")
    parser.add_argument("--ws-base", default="ws://127.0.0.1:8010/v1")
    parser.add_argument("--file", required=True, help="Path to a mono PCM WAV file.")
    parser.add_argument("--model", default="voxtral_realtime")
    parser.add_argument("--chunk-ms", type=int, default=320)
    parser.add_argument("--realtime", action="store_true", help="Sleep between chunks to simulate a live microphone.")
    args = parser.parse_args()

    wav_path = Path(args.file)
    if not wav_path.exists():
        raise SystemExit(f"File not found: {wav_path}")

    with wave.open(str(wav_path), "rb") as handle:
        channels = handle.getnchannels()
        sample_rate = handle.getframerate()
        sample_width = handle.getsampwidth()
        if sample_width != 2:
            raise SystemExit("Only 16-bit PCM WAV files are supported")
        frames = handle.readframes(handle.getnframes())

    frames_per_chunk = max(int(sample_rate * args.chunk_ms / 1000), 1)
    bytes_per_chunk = frames_per_chunk * channels * sample_width
    start_payload = {
        "model": args.model,
        "language": "auto",
        "sample_rate": sample_rate,
        "encoding": "pcm_s16le",
        "channels": channels,
        "triage_enabled": False,
        "metadata": {"source": "benchmark_live_asr", "benchmark_id": f"bench_{uuid.uuid4().hex[:12]}"},
    }
    stream = post_json(f"{args.api_base}/asr/stream/start", start_payload)
    session_id = stream["session_id"]
    started_at = time.perf_counter()
    first_partial_at = None
    final_at = None
    partials = 0
    final_text = ""

    async with websockets.connect(f"{args.ws_base}/asr/stream/{session_id}", max_size=None) as socket:
        for index, offset in enumerate(range(0, len(frames), bytes_per_chunk), start=1):
            chunk = frames[offset : offset + bytes_per_chunk]
            timestamp_ms = int((offset / (channels * sample_width)) / sample_rate * 1000)
            await socket.send(
                json.dumps(
                    {
                        "type": "audio_frame",
                        "seq": index,
                        "timestamp_ms": timestamp_ms,
                        "sample_rate": sample_rate,
                        "encoding": "pcm_s16le",
                        "channels": channels,
                        "payload_b64": encode_pcm16(chunk),
                    }
                )
            )
            while True:
                try:
                    message = await asyncio.wait_for(socket.recv(), timeout=0.01)
                except TimeoutError:
                    break
                payload = json.loads(message)
                if payload.get("type") == "partial_transcript":
                    partials += 1
                    if first_partial_at is None:
                        first_partial_at = time.perf_counter()
                elif payload.get("type") == "final_transcript":
                    final_text = payload.get("text", "")
                    final_at = time.perf_counter()
            if args.realtime:
                await asyncio.sleep(args.chunk_ms / 1000)

        await socket.send(json.dumps({"type": "end_stream"}))
        while True:
            payload = json.loads(await socket.recv())
            if payload.get("type") == "partial_transcript":
                partials += 1
                if first_partial_at is None:
                    first_partial_at = time.perf_counter()
            elif payload.get("type") == "final_transcript":
                final_text = payload.get("text", "")
                final_at = time.perf_counter()
                break

    first_partial_ms = round((first_partial_at - started_at) * 1000) if first_partial_at else None
    final_ms = round((final_at - started_at) * 1000) if final_at else None
    print(
        json.dumps(
            {
                "session_id": session_id,
                "model": args.model,
                "chunk_ms": args.chunk_ms,
                "realtime": args.realtime,
                "first_partial_ms": first_partial_ms,
                "final_ms": final_ms,
                "partial_events": partials,
                "final_chars": len(final_text),
                "final_text_preview": final_text[:240],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(run()))
