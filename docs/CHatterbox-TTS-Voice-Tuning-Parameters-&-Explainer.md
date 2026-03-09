Yes. There are some usable tuning patterns, and the biggest gotcha is that these knobs interact rather than behaving independently.

What the controls mean, based on the Chatterbox docs and related server docs:

* **Exaggeration** controls expressiveness/emphasis. `0.5` is treated as neutral; higher values add more emotion and emphasis, but extreme values can get unstable. ([Replicate][1])
* **Temperature** controls randomness. Lower values give more consistent pronunciation and prosody; higher values give more variation and can sound less predictable. ([Replicate][1])
* **CFG weight** is basically a **guidance / pace control** knob in the Chatterbox ecosystem. `0.5` is the normal default, and lower values can slow/calmer the pacing, especially when a reference speaker tends to come out too fast. ([Replicate][2])

The most important interaction is this:

* **higher exaggeration tends to speed up delivery**
* **lower CFG weight can compensate by making pacing slower/more deliberate** ([Replicate][2])

So if your complaint is “it talks too damn fast,” the first thing I would try is **not** temperature. I’d do this instead:

### Good starting presets

**1. Safe / natural baseline**

* exaggeration: `0.5`
* temperature: `0.7` to `0.8`
* cfg_weight: `0.5`

This is the general default-style setup the docs and related Chatterbox materials point to. ([Replicate][2])

**2. Slower / calmer / more deliberate**

* exaggeration: `0.4` to `0.5`
* temperature: `0.6` to `0.75`
* cfg_weight: `0.25` to `0.35`

Reason: lower exaggeration avoids “pushing” the performance, and lower CFG is specifically called out as helpful when the speaker/reference feels too fast. ([Replicate][2])

**3. More expressive / dramatic**

* exaggeration: `0.7` to `0.9`
* temperature: `0.75` to `0.95`
* cfg_weight: `0.25` to `0.35`

This one is straight from the pattern the Chatterbox docs suggest: lower CFG, higher exaggeration. The reason is that exaggeration gives you drama, but also tends to speed speech up, so reducing CFG helps keep it from turning into a caffeinated auctioneer. ([Replicate][2])

**4. Very stable / less wobbly**

* exaggeration: `0.45` to `0.55`
* temperature: `0.4` to `0.6`
* cfg_weight: `0.45` to `0.6`

Use this when delivery is getting weird, too animated, or inconsistent. Lower temperature reduces randomness. ([Replicate][1])

### How I’d tune it in practice

Don’t move all three knobs wildly at once. That’s how you summon nonsense.

Use this order:

**Step 1: fix pacing first**

* If it’s too fast, lower `cfg_weight` first.
* Then, if it’s still too hyped, lower `exaggeration`.

**Step 2: fix expressiveness**

* If it sounds flat, raise `exaggeration` a little.
* If it gets too theatrical or rushed, back it down and/or reduce CFG.

**Step 3: fix consistency**

* If the prosody or pronunciation is too unpredictable, lower `temperature`.
* If it sounds too stiff or repetitive, raise `temperature` slightly.

### Concrete test grid

If you want a fast sweep, try these four combinations on the same sentence:

**A. Baseline**

* `exaggeration=0.5`
* `temperature=0.8`
* `cfg_weight=0.5`

**B. Slower**

* `exaggeration=0.5`
* `temperature=0.8`
* `cfg_weight=0.3`

**C. Calmer + slower**

* `exaggeration=0.4`
* `temperature=0.7`
* `cfg_weight=0.3`

**D. Dramatic but controlled**

* `exaggeration=0.8`
* `temperature=0.85`
* `cfg_weight=0.3`

That’ll tell you very quickly which direction the voice wants to go.

### My blunt recommendation for your case

Since you said it keeps sounding too fast, I’d start here:

```text
exaggeration = 0.45
temperature  = 0.75
cfg_weight   = 0.30
```

Then compare against:

```text
exaggeration = 0.50
temperature  = 0.80
cfg_weight   = 0.50
```

That A/B should expose the pacing difference pretty clearly. The docs specifically support the “lower CFG when the voice/reference comes out too fast” move. ([Replicate][2])

One more subtle thing: if you’re splitting long text into chunks, chunk boundaries can also make pacing feel weird even when parameters are fine. Your screenshot shows chunking enabled, so some “fast” feeling may be chunk-level rhythm, not just model settings. The Chatterbox server docs note chunking controls are part of long-form generation. ([GitHub][3])

Best short answer for daily use:

* start at `0.5 / 0.8 / 0.5`
* if too fast, go to `0.45 / 0.75 / 0.3`
* if too flat, go to `0.7 / 0.85 / 0.3`

That gets you 80% of the way without knob-fiddling yourself into the abyss.

[1]: https://replicate.com/resemble-ai/chatterbox-multilingual/readme?utm_source=chatgpt.com "resemble-ai/chatterbox-multilingual | Readme and Docs"
[2]: https://replicate.com/resemble-ai/chatterbox?utm_source=chatgpt.com "Resemble Chatterbox | Text to Speech"
[3]: https://github.com/devnen/Chatterbox-TTS-Server?utm_source=chatgpt.com "devnen/Chatterbox-TTS-Server: Self-host the powerful ..."

