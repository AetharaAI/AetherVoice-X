Yeah — I dug through the actual OpenMOSS docs instead of doing cargo-cult TTS astrology.

Your main issue is probably this:

**MOSS-TTS-Realtime is not documented as a “prepend arbitrary XML-ish control tags to spoken text” model.** The official description is that it works by conditioning on **dialogue history**, including prior **text** and prior **user acoustics**, and the reference implementation emphasizes **multi-turn context**, **KV-cache reuse**, and an optional **prompt_wav** rather than a tag lane stuffed into the same body text. I could not find official docs showing an XML/control-tag format like `<agent tone="warm" cadence="telephony" />` for Realtime. That means Codex’s suspicion is likely right: if those tags are being shoved into the utterance stream, you’re probably feeding the model something it was not explicitly trained to interpret as a separate control channel. ([Hugging Face][1])

So the clean mental model is:

**Realtime wants**

1. the current text to speak,
2. prior turn history,
3. optional prior acoustic/reference audio,
4. a persistent session so it can reuse context across turns. ([Hugging Face][1])

Not:

1. “spoken body”
2. plus random sidecar pseudo-XML glued to the front and prayed over.

That gremlin behavior fits your symptom too: you finally get audio back, but the first warm pass is slow, and the beginning is off. The official Realtime examples explicitly call out **multi-turn streaming** with **turn 0 resetting KV cache** and later turns **reusing KV cache**, plus a `prompt_wav` in the demo path. That strongly suggests your backend contract should be built around **session state + reference audio + turn history**, not “UI tag text prepended to body text.” ([GitHub][2])

Here’s the blunt recommendation for your backend contract:

**For MOSS-TTS-Realtime**

* Keep `spoken_body` as plain natural-language text only.
* Move your “tone / cadence / telephony” controls into a **server-side control object**, not directly into the utterance string.
* Convert that control object into one of three things:

  * a **system prompt template** on the LLM side before text reaches TTS,
  * a **voice preset selection**,
  * or a **session profile** that determines reference voice / prosody defaults.
* Persist **session history** and reuse it across turns.
* Preserve **reference audio** or voice state for continuity.
* Warm the model once at startup with a tiny dummy pass so first-token latency stops looking drunk. ([Hugging Face][1])

So, in practice, your UI should become:

* **Voice preset** dropdown
* **Session** / conversation memory
* **Reference voice** or cloned voice ID
* **Plain text body**
* maybe advanced **style controls** that are translated server-side

Not a raw “tag lane” unless you personally verify in the model code that those tags are parsed semantically. Right now, the public docs do not show that. ([GitHub][2])

## What each model in your stack is actually for

### 1) MOSS-TTS-Realtime

This is your **live agent lane**. It is a **1.7B** realtime model designed for **interactive voice agents**, **multi-turn context**, **incremental synthesis**, and **voice consistency across turns**. It supports a max context length of **32K**, which they describe as about **40 minutes**. This is the right engine for telephony-style back-and-forth once your session contract is correct. ([Hugging Face][1])

### 2) MOSS-VoiceGenerator

This is your **voice design engine**, not your telephony runtime. It generates speaker timbres directly from **free-form text descriptions** without reference audio. The docs explicitly say the **voice description instructions and the text to be synthesized are concatenated and jointly tokenized**. That is a big clue: **VoiceGenerator** is where text-instruction-style conditioning is documented, not Realtime. It also has recommended decoding settings: `audio_temperature 1.5`, `audio_top_p 0.6`, `audio_top_k 50`, `audio_repetition_penalty 1.1`. ([Hugging Face][3])

Translation: use VoiceGenerator to create named voices like:

* “Warm, confident American male service dispatcher”
* “Friendly calm female customer-support agent”
* “Gruff field-tech voice with slight blue-collar rasp”

Then save those as presets.

### 3) MOSS-TTSD

This is your **dialogue / podcast / multi-speaker longform engine**. It is built for **1 to 5 speakers**, long-form continuity, and **zero-shot voice cloning from short references**. In the legacy/public docs, the input format uses explicit **speaker tags like `[S1]` and `[S2]`** plus prompt audio/text for each speaker. That means if you want structured dialogue control, TTSD already has an actual documented format for it. ([GitHub][4])

This is important:

* **TTSD is not a replacement for Realtime**
* **TTSD is your batch/longform conversation renderer**
* Realtime is your live lane

So your instinct was mostly right: grabbing TTSD gave you the “conversation-grade” synthesis layer. But for a live phone agent, **Realtime stays primary**.

### 4) MOSS-TTS

This is the **flagship base TTS engine**. It is the one for **high-fidelity zero-shot cloning**, **ultra-long generation**, **duration control**, **pronunciation control**, and multilingual/code-switched speech. If you want the strongest general-purpose single-speaker production engine, this is the one you’re missing. TTSD does **not** make MOSS-TTS redundant; they solve different problems. ([Hugging Face][5])

My ranking for you:

* **Realtime** = phone agents / live assistants
* **TTS** = premium single-speaker production and cloning
* **TTSD** = podcast/dialogue/multi-speaker scripted generation
* **VoiceGenerator** = create voices from text descriptions
* **SoundEffect** = non-speech audio layer

So yes: **you should probably download MOSS-TTS too.** Not because you’re missing oxygen, but because it gives you the proper single-speaker backbone for premium narration, ads, content, and cloning workflows. ([Hugging Face][5])

## How to store voices properly

Do **not** store “voices” as blobs of prompt text only. That turns into a junk drawer fast.

Store them as a structured preset object, something like:

```json
{
  "voice_id": "dispatch_warm_01",
  "display_name": "Dispatcher Warm",
  "source_model": "moss_voice_generator",
  "generation_prompt": "Warm, clear, confident American dispatcher voice with telephony-friendly pacing and calm authority.",
  "reference_audio_path": null,
  "reference_text": null,
  "sample_rate": 24000,
  "language": "en",
  "tags": ["telephony", "service", "warm", "dispatcher"],
  "decoding": {
    "audio_temperature": 1.5,
    "audio_top_p": 0.6,
    "audio_top_k": 50,
    "audio_repetition_penalty": 1.1
  },
  "fallback_runtime_model": "moss_tts_realtime",
  "notes": "Generated with VoiceGenerator; intended for call flows."
}
```

Then later, for cloning voices:

```json
{
  "voice_id": "cj_clone_01",
  "display_name": "CJ Clone",
  "source_model": "moss_tts",
  "generation_prompt": null,
  "reference_audio_path": "/voices/cj/ref_01.wav",
  "reference_text": "Exact transcript of reference audio",
  "sample_rate": 24000,
  "language": "en",
  "tags": ["clone", "founder", "english"],
  "decoding": {},
  "fallback_runtime_model": "moss_tts_realtime"
}
```

That lets your dropdown work cleanly:

* some presets come from **VoiceGenerator**
* some come from **cloned references**
* all can be routed into **Realtime** for live playback

That’s the scalable way. Otherwise six weeks from now you’ll have “voice_final_v2_REAL_last.json” and a small cemetery of regret.

## Best architecture for your studio

Given what you’re building, your strongest stack is:

**Voice design**

* `MOSS-VoiceGenerator` for creating base personas from text descriptions. ([Hugging Face][3])

**Premium single-speaker generation / cloning**

* `MOSS-TTS` for polished voice output, cloning, duration/pronunciation control. ([Hugging Face][5])

**Long-form scripted conversations**

* `MOSS-TTSD` for multi-speaker scripts, podcasting, roleplay, dubbing, and dialogue. ([GitHub][4])

**Live telephony / live agents**

* `MOSS-TTS-Realtime` with persistent session context and voice preset binding. ([Hugging Face][1])

**Non-speech effects**

* `MOSS-SoundEffect` if you want IVR ambiance, branded earcons, UI sounds, content production, game/media audio, or richer call experiences. It is not necessary for the core phone agent path, but it is useful for product polish and media workflows. ([Hugging Face][1])

## Direct answers to your specific questions

**Do you need MOSS-TTS if you already have TTSD?**
Yes, probably. TTSD is the dialogue specialist. MOSS-TTS is the flagship single-speaker synthesis backbone with stronger explicit support for cloning, long-form narration, and fine-grained speech control. ([Hugging Face][5])

**Is TTSD basically the beefier TTS model?**
Not exactly. It is beefier for **dialogue**, not a blanket replacement for the base TTS engine. Different job, different beast. ([GitHub][4])

**What is VoiceGenerator for?**
Creating voices from text descriptions with no reference audio. Best used to generate preset personas that you save and reuse. ([Hugging Face][3])

**How should you store voices?**
As structured presets in config/database, with model source, prompt or reference audio, decoding defaults, and runtime routing target.

**What about SoundEffect?**
Not required for end-to-end speech agents. Worth adding later for IVR polish, content production, app sounds, branded audio UX, and synthetic environments. ([Hugging Face][1])

## My verdict on the bug

Most likely root cause:

* your UI has a “directive/tag” field,
* backend is concatenating it into text,
* Realtime is treating it as normal input text instead of structured control,
* so output starts weird / slow / not quite right.

That is the most plausible explanation from the official docs plus your observed behavior. The docs support **history + acoustics + streaming context**; they do **not** show a documented XML-style control grammar for Realtime. That part is my inference, but it’s a grounded one, not hand-wavy goblin smoke. ([Hugging Face][1])

The next move is simple:
**tell Codex to rework the Realtime request contract so tags are not prepended to spoken text, and make the session carry history/reference voice instead.**

If you want, I’ll turn this into a **drop-in engineering spec for Codex** with:

* exact request/response schema,
* voice preset schema,
* session memory schema,
* routing rules for Realtime vs TTSD vs TTS vs VoiceGenerator,
* and the UI behavior changes for that TTS Live screen.

[1]: https://huggingface.co/OpenMOSS-Team/MOSS-TTS-Realtime "OpenMOSS-Team/MOSS-TTS-Realtime · Hugging Face"
[2]: https://github.com/OpenMOSS/MOSS-TTS/blob/main/docs/moss_tts_realtime_model_card.md?utm_source=chatgpt.com "MOSS-TTS/docs/moss_tts_realtime_model_card.md at main"
[3]: https://huggingface.co/OpenMOSS-Team/MOSS-VoiceGenerator "OpenMOSS-Team/MOSS-VoiceGenerator · Hugging Face"
[4]: https://github.com/OpenMOSS/MOSS-TTS/blob/main/docs/moss_ttsd_model_card.md?utm_source=chatgpt.com "MOSS-TTS/docs/moss_ttsd_model_card.md at main"
[5]: https://huggingface.co/OpenMOSS-Team/MOSS-TTS "OpenMOSS-Team/MOSS-TTS · Hugging Face"

