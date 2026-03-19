that 19 seconds you were reading, you got to understand, like, I'm jumping around. So like, what I mean by jumping around is, you probably tell what I really need to do is stop, like, so you can't copy and paste a stream whenever it's like actually reading the logs. So for one, I have to control C so that the terminal stands still, and then I can copy and paste that whole log stream, you can actually read it, decipher it. But if I did that, I would do it in a Markdown so you can read it in chunks, because I don't like giving up, giving you a big-ass fucking, and the screenshots are probably what makes it worse too. If I just put it in a Markdown as text to read, it'd probably be a lot easier. Anyway, so that big long dumb stupid, like, you see that, that, that spoken body that I put on there, that's not, that was just some dumb stuff that I put in there. It's not really, that doesn't really make, you know, that that doesn't, isn't useful. I was just putting some random str, like, sentences together just to see quality, you know what I'm saying? As far as like the voice quality, because you put some random shit in there, you're going to be like, you know what I mean? That, you know, it is kind of funny, but um in a weird, like human kind of way, right? So, but the thing is, all these freaking voices bro, have that, like, they sound like, it sounds like you went to a massage parlor, and the little Chinese ladies are in there, in there be like, how may I help you? I don't know, I can't, you, this is gonna get transcribed, so you're gonna miss the whole of what I'm saying, but you know what I mean? So uh the quality is not the problem, the quality is fucking perfect. The fucking, the chunking, we need to stream. He already said he was gonna go to it, like, he has this whole thing he was talking about. I'll tell you, I'll show you. Codex is already telling me a bunch of shit that you told me, and I'll just show you what he said.Codex:Yes, the current behavior is exactly what I set up.

On voices:
- Qwen currently has 6 seeded built-in voices in your app:
  - `Aiden`
  - `Ryan`
  - `Serena`
  - `Sohee`
  - `Uncle_Fu`
  - `Vivian`
- Those are not an arbitrary subset I invented. They are the Qwen built-ins we wired into the studio registry for `CustomVoice`.
- The rest of the voices you saw before in the bigger pack were mostly Kokoro presets, plus the one Chatterbox fallback.

So right now:
- Qwen voices in app: 6
- Kokoro voices in app: the larger preset list
- Chatterbox: fallback voice

On why it did not stream:
- because it is not streaming yet
- the page is behaving correctly
- `qwen_customvoice` in `TTS Live` is intentionally a `batch-backed live` lane
- it does one finalized generation through `/v1/tts/synthesize`
- that is why you see:
  - `Chunks: 1`
  - `batch-ready`
  - `Delivery contract: batch-backed via /v1/tts/synthesize`

So no, this is not “how you are supposed to stream it.” This is the honest stopgap so you can test:
- voice quality
- total latency
- voice selection
- live operator workflow

The real streaming question is separate:
- Qwen docs say the family supports streaming
- your current in-app provider does not
- your current provider endpoint literally returns `501` on `/v1/audio/speech/stream`
- your adapter has `supports_streaming = False`

So the stack truth today is:
- Qwen works in batch
- Qwen works in the loop
- Qwen works in `TTS Live` as a batch-backed probe
- Qwen does not yet have true live streaming integrated in your provider/app stack

And yes, you are right about rebuild scope. If we touch only frontend/UI:
```bash
docker compose up -d --build --no-deps frontend
```

If we touch only the TTS service:
```bash
docker compose up -d --build --no-deps tts
```

If we touch only gateway:
```bash
docker compose up -d --build --no-deps gateway
```

If we touch Voxtral specifically:
```bash
COMPOSE_PROFILES=voxtral docker compose up -d --build --no-deps voxtral
```

So no, you do not need to keep rebuilding the whole stack if the change is isolated.

Decision point:
- if you want more/better Qwen voices, that is a voice inventory issue
- if you want real streaming, that is a provider/runtime implementation issue

Those are two different tracks.

My recommendation:
1. Keep using the current batch-backed lane to judge quality and latency.
2. If quality is good enough, next build the actual Qwen streaming provider path.
3. Separately, we can expand the Qwen voice surface if the model/provider supports more presets or a better promptable voice path.

If you want, next I can map the exact minimum work to turn `qwen-provider` from `batch-backed` into a real streaming-capable lane, without changing any code yet.

prompt:{screenshots}

Yes. These are clean enough to read now.

For the **Vivian / 109-char** run, your logs line up with the UI almost perfectly.

## What the logs show

Provider call starts here:

* `POST http://qwen-provider:8072/v1/audio/speech`
* timestamp: **08:43:22.232**

Provider finishes here:

* `tts_completed`
* timestamp: **08:43:22.243**

Then your TTS service finishes internal synth here:

* `POST /internal/synthesize`
* timestamp: **08:43:22.244**

Artifact is fetched here:

* `GET /api/v1/tts/artifacts/download?...wav`
* timestamp: **08:43:22.247**

So for that run:

* **provider leg:** about **11 ms**
* **internal finalize:** about **1–4 ms**
* **artifact fetch kickoff:** almost immediate after finalize

That means your **infra path is fast**.

## Why the UI says 7.32s

Because the UI is measuring from when you armed/fired the batch lane to when final audio was ready for playback, not just the tiny logged post step you pasted.

So the real split is:

* **backend logged synth window:** ~**15 ms total**
* **operator-visible total latency:** **7.32s**
* therefore the missing time is almost certainly **before** that logged `POST /v1/audio/speech` line from the TTS service’s perspective, or in the provider’s own generation timing before your app logs completion in that narrow section

In plain English:

Your pasted logs are catching the **tail end** of the transaction, not the whole thing.

## What this proves

It proves three important things:

* the **gateway is not the bottleneck**
* the **artifact handoff is not the bottleneck**
* your **TTS wrapper/service is not the bottleneck**

The slow part is still the actual **Qwen generation path**, or at least the part before your current log markers.

## What you need in the frontend/logs

You need four timestamps, explicitly:

* `batch_request_started`
* `provider_request_started`
* `provider_audio_ready`
* `artifact_ready`

Because right now you only really have the back half.

## Blunt read

For this specific run:

* **7.32s total for 109 chars**
* **actual post-provider plumbing is basically instant**
* the model/provider path is where the time lives

That’s much better than the earlier 19-second junk probe, but it is still **not realtime**.

It is, however, probably good enough for:

* voice QA
* operator review
* preset comparison
* internal tuning

Not good enough yet for live caller turn-taking.

Paste one full raw log block next time and I can map the whole request exactly.
