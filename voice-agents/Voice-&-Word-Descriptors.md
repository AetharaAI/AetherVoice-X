Yep. Treat it like a voice-paint box, not a sacred ritual. You want word banks that mix cleanly into short prompt strings.

The trick with descriptor-based TTS is this: **stack a few traits across different dimensions** instead of spamming synonyms. Usually the useful dimensions are:

**tone** (warm, stern, airy)
**texture** (raspy, velvety, crisp)
**delivery** (measured, fast, punchy)
**age vibe** (youthful, mature, seasoned)
**energy** (calm, animated, intense)
**presence** (intimate, commanding, distant)

If you over-pack the prompt, models start hallucinating vibes like a method actor with a head injury. Short and surgical wins.

## 1) General descriptive words

Here’s a broad word bank you can mix from:

warm, rich, deep, bright, clear, crisp, smooth, velvety, airy, breathy, husky, smoky, raspy, gravelly, soft, gentle, tender, intimate, close, rounded, polished, clean, natural, expressive, animated, lively, energetic, punchy, relaxed, calm, grounded, steady, measured, composed, confident, commanding, authoritative, reassuring, sincere, conversational, friendly, inviting, magnetic, elegant, refined, mature, youthful, playful, sharp, articulate, precise, resonant, cinematic, emotional, dry, cool, detached, mysterious, moody, serious, stoic, silky, low, mid-toned, high, textured, polished, raw, rugged, soothing, hypnotic, persuasive, storyteller-like, radio-ready, narrator-like, professional, casual, understated, intense, focused, dramatic, patient, deliberate, fluid, effortless

## 2) Male voice descriptor bank

These are geared more toward masculine-coded voice shaping:

deep, low-register, baritone, bass-leaning, chesty, resonant, grounded, rugged, gravelly, smoky, husky, dry, warm, mature, seasoned, stoic, calm, deliberate, measured, confident, commanding, authoritative, reassuring, protective, smooth, cinematic, radio-style, narrator-like, polished, conversational, approachable, fatherly, mentor-like, cool, restrained, sharp, direct, punchy, crisp, masculine, intimate, emotionally controlled, reflective, serious, relaxed, powerful, weighty, textured, raw, no-nonsense, elegant, refined, bold, magnetic, serious, dark-toned, clean-spoken

## 3) Female voice descriptor bank

These are geared more toward feminine-coded voice shaping:

warm, soft, clear, bright, airy, breathy, silky, smooth, velvety, elegant, refined, polished, playful, youthful, mature, intimate, gentle, expressive, melodic, conversational, inviting, soothing, calm, confident, poised, articulate, crisp, storyteller-like, cinematic, emotional, affectionate, radiant, light, rounded, friendly, empathetic, graceful, magnetic, sweet, grounded, composed, persuasive, professional, relaxed, rich, delicate, vivid, tender, lively, reassuring, dreamy, controlled, subtle, vibrant

## 4) Random male-style prompt ideas

These are already shaped the way you’d feed them into a descriptor field:

* warm deep baritone, calm and grounded, measured delivery, confident and reassuring
* smoky rugged male voice, slightly gravelly, mature, direct and authoritative
* smooth cinematic baritone, polished and resonant, slow deliberate narration
* low masculine voice, dry texture, restrained emotion, sharp and professional
* rich chesty male voice, storyteller-like, warm, reflective, slightly rugged
* clear confident male voice, articulate, modern, clean, radio-ready
* deep soothing male narrator, gentle but commanding, intimate and composed
* husky mature male voice, textured and calm, mentor-like delivery
* powerful baritone, resonant and bold, precise diction, serious tone
* relaxed masculine voice, warm and conversational, friendly but grounded
* dark-toned male voice, cinematic, emotionally controlled, steady pacing
* crisp mid-low male voice, persuasive, polished, executive presence
* gravelly deep voice, raw but intelligent, no-nonsense and focused
* rich masculine narrator, calm authority, smooth texture, slightly dramatic
* low warm male voice, intimate and close, slow and reassuring

## 5) Random female-style prompt ideas

* warm clear female voice, soft and polished, calm conversational delivery
* airy elegant female voice, smooth and intimate, gentle expressive tone
* bright youthful female voice, playful, lively, and natural
* rich mature female voice, poised and articulate, reassuring and confident
* silky cinematic female narrator, emotional but controlled, smooth pacing
* soft breathy female voice, dreamy and close, tender delivery
* confident professional female voice, crisp diction, polished and composed
* soothing female narrator, warm and empathetic, gentle measured delivery
* vibrant feminine voice, expressive and melodic, friendly and inviting
* refined female voice, elegant and clear, storyteller-like cadence
* calm grounded female voice, rich tone, mature and reassuring
* intimate velvety female voice, subtle warmth, slow expressive pacing
* polished bright female voice, articulate, modern, radio-ready
* graceful feminine narrator, smooth and cinematic, emotionally rich
* clear soft female voice, relaxed, conversational, natural and warm

## 6) Mixed / stylized / more experimental prompt ideas

These are good for finding weird gems:

* androgynous smooth voice, clear and calm, intimate futuristic tone
* cinematic narrator voice, rich and textured, mysterious and controlled
* warm expressive storyteller, natural pacing, emotional but polished
* calm synthetic-human hybrid voice, smooth, precise, slightly detached
* smoky intimate voice, low energy, close mic presence, moody and reflective
* bright polished commercial voice, upbeat, clean, persuasive and energetic
* soft hypnotic voice, airy texture, gentle pacing, dreamlike presence
* grounded mentor voice, warm and steady, patient and intelligent
* sharp modern voice, crisp articulation, neutral tone, professional and fast
* elegant dramatic narrator, resonant and emotional, high clarity

## 7) Good prompt formula

A simple formula that usually works:

**[tone] + [pitch/register] + [texture] + [delivery] + [persona/use-case]**

Examples:

* warm low baritone, smooth texture, measured delivery, cinematic narrator
* bright soft female voice, airy and polished, friendly conversational delivery
* grounded masculine voice, deep and resonant, calm mentor-like tone
* elegant feminine narrator, velvety texture, slow expressive pacing

## 8) Fast testing strategy

Don’t test fifty random prompts like a raccoon in a server room. Do this instead:

Start with 4 archetypes:

* narrator
* assistant
* commercial
* intimate/conversational

Then vary one dimension at a time:

* swap **warm** → **cool**
* swap **smooth** → **raspy**
* swap **measured** → **energetic**
* swap **mature** → **youthful**

That tells you what Moss actually responds to versus what it politely ignores.

## 9) A few ready-made seed packs

### Masculine pack

* warm, deep, grounded, measured, reassuring
* smoky, rugged, mature, direct, authoritative
* smooth, cinematic, resonant, polished, calm
* crisp, modern, articulate, professional, confident
* gravelly, textured, raw, serious, commanding

### Feminine pack

* warm, clear, soft, polished, inviting
* airy, bright, playful, youthful, expressive
* silky, elegant, poised, articulate, refined
* soothing, gentle, intimate, calm, reassuring
* rich, mature, grounded, confident, cinematic

### Neutral / assistant pack

* clear, calm, natural, conversational, helpful
* smooth, balanced, articulate, modern, professional
* warm, grounded, composed, friendly, precise
* polished, neutral, reassuring, steady, intelligent
* soft, clear, measured, relaxed, approachable

## 10) Tiny warning that matters

A lot of TTS models respond better to **plain-language descriptors** than overly poetic nonsense.
“warm deep calm narrator voice” often beats
“a velvet thunderstorm wrapped in midnight oak.”
Beautiful phrase. Useless machine food.

I can also give you a **100-line descriptor pack formatted one-per-line for direct copy/paste into your Voice Studio seeds**.

