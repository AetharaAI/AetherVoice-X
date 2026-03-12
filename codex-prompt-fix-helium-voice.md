# Codex Task: Fix "Helium Man" Voice — MOSS Conditioning Audio Sample Rate Mismatch

## Context

We have a confirmed hypothesis for why all MOSS TTS output (both `moss_realtime` and `moss_tts` paths) sounds like a chipmunk/helium voice regardless of which conditioning audio clip is used. The MOSS-Audio-Tokenizer operates at a **native sample rate of 24,000 Hz**. The conditioning/reference WAV files being loaded at startup were recorded at **44,100 Hz** in Audacity. If the tokenizer is receiving 44.1kHz audio but interpreting it as 24kHz (no resample step), the encoded tokens would represent audio at ~1.84× the correct pitch — producing exactly the helium effect we hear.

The MOSS-Audio-Tokenizer's own example code explicitly requires resampling:

```python
wav, sr = torchaudio.load('reference.wav')
if sr != model.sampling_rate:  # model.sampling_rate == 24000
    wav = torchaudio.functional.resample(wav, sr, model.sampling_rate)
```

## What to investigate and fix

### 1. Find the conditioning audio load path

Search the codebase for where the voice conditioning/reference/prompt WAV file gets loaded and passed to the MOSS-Audio-Tokenizer for encoding. This happens at container build time or service startup — it's the "warm up" audio that the tokenizer encodes to establish speaker identity.

Look for:
- `torchaudio.load` calls near tokenizer or codec usage
- Any path referencing `prompt_audio`, `prompt_wav`, `reference_audio`, `conditioning`, `voice_preset`, or `warm` + `audio`
- The `MOSS Default Voice` preset loading logic
- Anywhere `.wav` or `.mp3` files are loaded and fed to `model.encode()` or `processor.audio_tokenizer`

### 2. Verify resampling exists (or add it)

At the point where the conditioning audio waveform is loaded, ensure there is an **explicit resample to 24,000 Hz** before it reaches the tokenizer's `encode()` method. The fix pattern:

```python
import torchaudio

wav, sr = torchaudio.load(conditioning_audio_path)

# CRITICAL: Resample to tokenizer's native rate (24kHz)
TARGET_SR = 24000  # MOSS-Audio-Tokenizer native sample rate
if sr != TARGET_SR:
    wav = torchaudio.functional.resample(wav, sr, TARGET_SR)

# Also ensure mono (single channel)
if wav.shape[0] > 1:
    wav = wav.mean(dim=0, keepdim=True)
```

This must happen **before** the audio is passed to the tokenizer for encoding into discrete tokens. The tokenizer does NOT auto-resample — it trusts that the input is already at 24kHz.

### 3. Check ALL audio load paths

The same resampling guard needs to exist in every place conditioning audio is loaded, including:
- The startup/warmup path that loads the default voice preset
- The Voice Clone workflow (if it accepts user-uploaded WAVs)
- The TTS Studio voice preset loading
- The `moss_realtime` path's `--prompt_wav` equivalent
- The `moss_tts` batch path's reference audio loading
- Any voice library/preset management that stores or retrieves encoded voice tokens

### 4. Check the existing WAV files

The WAV files currently being used as conditioning audio may themselves be at 44,100 Hz or 48,000 Hz. Verify their actual sample rate:

```python
import torchaudio
info = torchaudio.info("path/to/conditioning.wav")
print(f"Sample rate: {info.sample_rate}, Channels: {info.num_channels}, Duration: {info.num_frames / info.sample_rate:.2f}s")
```

If they are not 24kHz mono, either:
- Add the runtime resample (preferred — handles any input format)
- Also pre-convert the asset files to 24kHz mono WAV for belt-and-suspenders safety

### 5. Verify the decode/output path too

On the output side, after the tokenizer decodes generated tokens back to audio, confirm the output is being saved/streamed at the correct sample rate (24,000 Hz). A mismatch here (e.g., writing 24kHz audio with a 44.1kHz header) would also cause pitch distortion.

```python
# After decode
decode_result = codec.decode(tokens, chunk_duration=8)
wav_out = decode_result["audio"][0].cpu().detach()
# Save at the tokenizer's native sample rate
torchaudio.save("output.wav", wav_out, 24000)  # NOT 44100
```

## Expected outcome

After this fix:
- The MOSS-Audio-Tokenizer will correctly encode the speaker's timbre from the conditioning audio
- Generated speech will match the voice identity of the reference clip instead of being pitch-shifted
- Both `moss_realtime` and `moss_tts` paths should produce correct voice since they share the same tokenizer and conditioning layer

## Reference audio best practices (for after the fix)

Once the sample rate issue is resolved, optimal conditioning audio should be:
- **Duration**: 10–15 seconds of clean speech (sweet spot for zero-shot cloning)
- **Format**: WAV, mono, 24kHz (or any format — the resample guard will handle it)
- **Content**: Normal conversational speech, no music/singing/whispering
- **Quality**: Minimal background noise, clear articulation
- **Ending**: Append ~0.5s silence to avoid first-token phoneme bleed

## Hyperparameters that are working well (from live testing)

These are tuned and working on the TTS Live page — don't change them during this fix:
- Temperature: 0.45
- Top P: 0.65
- Top K: 30
- Repetition penalty: 1.1
- Repetition window: 50
- Decode chunk frames: 6
- Prefill text len: 24
