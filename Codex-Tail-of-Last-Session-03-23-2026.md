Yes. That came from the test text I gave you, not from the reference script.

I explicitly told you to send this in the curl body:

"input":"Thank you for calling Aethara. I can help you with that now."

So if the generated audio said “Thank you for calling Aethara,” that is expected. The model cloned the voice from your reference WAV, but it spoke the input text from the request payload, not the transcript of the reference audio.

That is actually a strong result:

voice identity matched the reference
spoken content followed the requested text
so the model is doing the right basic job
If you want to prove that cleanly, run the same request again with the exact Syndicate AI text you want:

curl -X POST http://127.0.0.1:8075/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model":"voxtream2_realtime",
    "input":"Thank you for calling Syndicate AI. I can help you with that now.",
    "voice":"reference_audio_required",
    "prompt_audio_path":"/app/audio-refs/bella_voice_ref.wav",
    "speaking_rate":3.0,
    "response_format":"wav"
  }' > voxtream2-syndicate.json
Then decode it the same way and listen. If it still sounds like the same cloned speaker, then you’ve proven zero-shot voice cloning plus new text generation, which is the real thing you wanted.


Cool, that sounds great, I want to do 2 with the male voice


Use this for the male ref with 2.0 speaking rate:

curl -X POST http://127.0.0.1:8075/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model":"voxtream2_realtime",
    "input":"Thank you for calling Syndicate AI. I can help you with that now.",
    "voice":"reference_audio_required",
    "prompt_audio_path":"/app/audio-refs/Adam-voice-ref.wav",
    "speaking_rate":2.0,
    "response_format":"wav"
  }' > voxtream2-adam-rate2.json
Then decode it locally or on the VM:

jq -r '.audio_b64' voxtream2-adam-rate2.json | base64 -d > voxtream2-adam-rate2.wav
If you want to compare timings too:

jq '.model, .sample_rate, .timings, .artifacts' voxtream2-adam-rate2.json

User attachment
User attachment
Dude, I ran six structured passes. So I went ahead and opened up a chat GPT session because normally, like he already knows, we do these kind of things all the time. And he gave me, so, cause I, plus I saved it to a different file. Like I did all the decoding on my computer. He gave me a flow, bro, like two clicks. I copied his curl, then he gave me one block for my computer that I could literally copy the whole file and play it in all with just one block of, yeah. Anyway, I just did six because I wanted to ease my anxiety because of the very first male one. It sounded fine, but there was just one word that was a little like... And I think that was just because it was like a... I know I've done this enough with these audio ones, man, that sometimes the first pass, there's a reason you have to do a warm-up. That warm-up matters. And after a couple passes with different text, it's so... Like I told him, dude, it's so fucking good, it's eerie. It is fucking eerie that it's that good. And the fact that we have knobs that we can control the speaker rate, this is the, I can stop shopping at Huggy Face now, and we can start freaking, yes, I can tell, we can integrate this in here, get this in the studio so I can test it in the studio, man. I want it as a provider in that drop down right there in TTS Live tab, So whats the voices or how is that flow work because I don't think that the TTS Live tab is set up to be able to change the ref-audio dynamically, and I do not want to keep a thousane different .wav voice refs on the VM, I want a drop down for ref audio and a way to add them easily in the TTS Live tab, i am assuming it dones't come with predinfined voices, it clones the ref a runtime?



Reconnecting... 2/5
Reconnecting... 3/5
Reconnecting... 4/5
Reconnecting... 5/5
I’m checking the current TTS Live voice-conditioning flow in the core repo now so I can answer from code truth and see exactly what needs to change for voxtream2 dropdown-based reference audio.

Explored 2 files, 1 search
Context automatically compacted
I’m checking the current TTS Live and Studio voice-asset flow now so I can tell you exactly what already exists and what needs to change for voxtream2 to feel native instead of hacked on.

Explored 3 files, 1 search
The core already has the plumbing for Studio-managed reference voices. I’m reading the API/UI surfaces now so I can wire voxtream2 into TTS Live as a real voice-asset dropdown instead of raw file-path hacks.

Explored 4 files
I’ve confirmed the backend already knows how to persist and resolve reference-audio voice assets. The missing piece is mostly operator UX in TTS Live: surfacing a proper reference-voice dropdown and an inline import path for voxtream2 instead of making you bounce out to raw files.

Explored 2 files, 1 search
I found the seam: TTS Live already sends the selected voice ID through the normal stream contract, and the backend already resolves reference_audio_path from the Studio voice registry. What’s weak is the UX: the live page still feels like a preset picker, not a managed reference-voice picker. I’m going to tighten that up directly.

Explored 2 files, 1 search
The stream contract is already carrying the right voice-asset truth back to the UI: selected voice ID, resolved conditioning asset, and actual runtime conditioning source. I’m checking that section now so I can keep the UI changes tight and avoid touching working runtime plumbing.

Explored 1 file
I’ve got the design now: voxtream2 already clones from reference audio at runtime; it does not ship with meaningful built-in preset voices. I’m adding two things in the core UI: a true reference-voice workflow in TTS Live, and a speaking-rate control that actually maps to the provider.

Explored 1 file, 1 search
I’m editing the live console now. The change is frontend-only: make voxtream/voxtream2 feel like reference-voice routes, add inline reference import on TTS Live, and expose speaking-rate so you can test this without bouncing between tabs.

Edited file
TTSLive.tsx
+196
-9


import { fetchStudioVoices } from "../api/studio";
import { fetchStudioVoices, importStudioVoice } from "../api/studio";
import { fetchModels } from "../api/sessions";

function usesReferenceVoiceAssets(model: string) {
  return model === "voxtream_realtime" || model === "voxtream2_realtime" || model === "chatterbox";
}

function supportsDynamicSpeakingRate(model: string) {
  return model === "voxtream2_realtime" || model === "voxtream_realtime";
}

function voiceSelectorLabel(model: string) {
  return usesReferenceVoiceAssets(model) ? "Reference voice asset" : "Voice preset";
}

function voiceImportDefaultName(model: string) {
  if (model === "voxtream2_realtime") {
    return "Voxtream2 Reference";
  }
  if (model === "voxtream_realtime") {
    return "Voxtream Reference";
  }
  if (model === "chatterbox") {
    return "Chatterbox Reference";
  }
  return "Reference Voice";
}

export function TTSLive() {
  const [repetitionWindow, setRepetitionWindow] = useState(50);
  const [speakingRate, setSpeakingRate] = useState(2.0);
  const [bodyText, setBodyText] = useState("A technician is being dispatched to your location now.");
  const [batchObservedTotalMs, setBatchObservedTotalMs] = useState<number | null>(null);
  const [referenceImportName, setReferenceImportName] = useState("Voxtream2 Reference");
  const [referenceImportFile, setReferenceImportFile] = useState<File | null>(null);
  const [referenceImportTags, setReferenceImportTags] = useState("telephony, reference");
  const [referenceImportNotes, setReferenceImportNotes] = useState("Imported from TTS Live for fast realtime reference-voice evaluation.");
  const [referenceImportText, setReferenceImportText] = useState("");
  const [referenceImportBusy, setReferenceImportBusy] = useState(false);
  const [referenceImportMessage, setReferenceImportMessage] = useState<string | null>(null);
  const [referenceImportError, setReferenceImportError] = useState<string | null>(null);

  const isBatchBackedLive = Boolean(selectedModel && !selectedModel.supports_streaming);
  const referenceVoiceModel = usesReferenceVoiceAssets(model);
  const sortedVoices = useMemo(() => [...voices].sort(sortVoices), [voices]);
    if (model === "voxtream_realtime" || model === "voxtream2_realtime") {
      return sortedVoices.filter((voice) => voice.runtime_target === model || Boolean(voice.reference_audio_path));
      return sortedVoices.filter((voice) => Boolean(voice.reference_audio_path));
    }
    if (model === "chatterbox") {
      return sortedVoices.filter((voice) => voice.runtime_target === "chatterbox" || Boolean(voice.reference_audio_path));
    }
      latency_mode: latencyMode,
      ...(supportsDynamicSpeakingRate(model) ? { speaking_rate: speakingRate } : {}),
      raw_directives: rawDirectives,
    }),
    [cadence, latencyMode, rawDirectives, selectedVoice?.voice_id, sessionProfile, speakingStyle, tone]
    [cadence, latencyMode, model, rawDirectives, selectedVoice?.voice_id, sessionProfile, speakingRate, speakingStyle, tone]
  );
      repetition_window: repetitionWindow,
      ...(supportsDynamicSpeakingRate(model) ? { speaking_rate: speakingRate } : {}),
    }),
    [decodeChunkFrames, decodeOverlapFrames, prefillTextLen, repetitionPenalty, repetitionWindow, temperature, topK, topP]
    [decodeChunkFrames, decodeOverlapFrames, model, prefillTextLen, repetitionPenalty, repetitionWindow, speakingRate, temperature, topK, topP]
  );

  async function refreshVoices() {
    const payload = await fetchStudioVoices();
    setVoices(payload);
    return payload;
  }

  useEffect(() => {
      .catch(() => setModels([]));
    fetchStudioVoices()
      .then((payload) => setVoices(payload))
    refreshVoices()
      .then(() => undefined)
      .catch(() => setVoices([]));
  useEffect(() => {
    if (!referenceVoiceModel) {
      return;
    }
    setReferenceImportName((current) => (current.trim() ? current : voiceImportDefaultName(model)));
    setReferenceImportMessage(null);
    setReferenceImportError(null);
  }, [model, referenceVoiceModel]);

  useEffect(() => {
    if (liveModels.length > 0 && !liveModels.some((entry) => entry.name === model)) {

  async function handleReferenceImport() {
    if (!referenceImportFile) {
      setReferenceImportError("Choose a reference WAV before importing.");
      return;
    }
    setReferenceImportBusy(true);
    setReferenceImportError(null);
    setReferenceImportMessage(null);
    try {
      const form = new FormData();
      form.set("file", referenceImportFile);
      form.set("display_name", referenceImportName.trim() || voiceImportDefaultName(model));
      form.set("source_model", "imported");
      form.set("runtime_target", model);
      form.set("voice_type", "imported");
      form.set("notes", referenceImportNotes.trim());
      form.set("tags", referenceImportTags.trim());
      if (referenceImportText.trim()) {
        form.set("reference_text", referenceImportText.trim());
      }
      const voice = await importStudioVoice(form);
      const nextVoices = await refreshVoices();
      setReferenceImportMessage(`Imported ${voice.display_name} into the shared voice library.`);
      setReferenceImportFile(null);
      setVoiceId(voice.voice_id);
      if (!nextVoices.some((entry) => entry.voice_id === voice.voice_id)) {
        setReferenceImportError(`Imported ${voice.display_name}, but the live voice list did not refresh yet.`);
      }
    } catch (err) {
      setReferenceImportError((err as Error).message);
    } finally {
      setReferenceImportBusy(false);
    }
  }

  async function handleStart() {
          <div className="field-group">
            <label htmlFor="tts-live-voice">Voice preset</label>
            <label htmlFor="tts-live-voice">{voiceSelectorLabel(model)}</label>
            <select id="tts-live-voice" value={selectedVoice?.voice_id ?? voiceId} onChange={(event) => setVoiceId(event.target.value)} disabled={sessionOpen}>
                    ? "This session resolved to a real conditioning asset. Realtime inference is materially using the bound conditioning source."
                    : "This session is falling back to the default global prompt path because the selected voice does not have a usable reference asset."}
                  : "This session is falling back to the default global prompt path because the selected voice does not have a usable reference asset."}
            </p>
        </div>
        {referenceVoiceModel ? (
          <details className="accordion" open>
            <summary>Reference voice library</summary>
            <div className="accordion-body">
              <div className="control-grid">
                <div className="field-group">
                  <label htmlFor="tts-live-reference-file">Reference WAV</label>
                  <input
                    id="tts-live-reference-file"
                    type="file"
                    accept="audio/wav,audio/*"
                    onChange={(event) => setReferenceImportFile(event.target.files?.[0] ?? null)}
                    disabled={sessionOpen || referenceImportBusy}
                  />
                  <p className="field-hint">Imports a reusable voice asset into the Studio registry so Voxtream can clone from a dropdown instead of a raw VM path.</p>
                </div>
                <div className="field-group">
                  <label htmlFor="tts-live-reference-name">Asset name</label>
                  <input
                    id="tts-live-reference-name"
                    value={referenceImportName}
                    onChange={(event) => setReferenceImportName(event.target.value)}
                    placeholder={voiceImportDefaultName(model)}
                    disabled={sessionOpen || referenceImportBusy}
                  />
                </div>
                <div className="field-group">
                  <label htmlFor="tts-live-reference-tags">Tags</label>
                  <input
                    id="tts-live-reference-tags"
                    value={referenceImportTags}
                    onChange={(event) => setReferenceImportTags(event.target.value)}
                    placeholder="telephony, dispatch, male"
                    disabled={sessionOpen || referenceImportBusy}
                  />
                </div>
              </div>
              <div className="control-grid">
                <div className="field-group">
                  <label htmlFor="tts-live-reference-text">Reference transcript</label>
                  <textarea
                    id="tts-live-reference-text"
                    value={referenceImportText}
                    onChange={(event) => setReferenceImportText(event.target.value)}
                    rows={3}
                    placeholder={model === "voxtream_realtime" ? "Optional but recommended for original Voxtream." : "Optional. Voxtream2 can run without it, but save it when you have it."}
                    disabled={sessionOpen || referenceImportBusy}
                  />
                </div>
                <div className="field-group">
                  <label htmlFor="tts-live-reference-notes">Operator notes</label>
                  <textarea
                    id="tts-live-reference-notes"
                    value={referenceImportNotes}
                    onChange={(event) => setReferenceImportNotes(event.target.value)}
                    rows={3}
                    disabled={sessionOpen || referenceImportBusy}
                  />
                </div>
              </div>
              <div className="toolbar">
                <button onClick={() => void handleReferenceImport()} disabled={sessionOpen || referenceImportBusy}>
                  {referenceImportBusy ? "Importing reference..." : "Import reference into library"}
                </button>
                <Badge value={`${modelVoices.length} assets`} tone={modelVoices.length ? "good" : "warn"} />
              </div>
              {selectedVoice?.reference_audio_path ? (
                <p className="field-hint">
                  Active reference asset: <code className="inline-code">{selectedVoice.reference_audio_path}</code>
                </p>
              ) : null}
              {referenceImportMessage ? <p className="muted">{referenceImportMessage}</p> : null}
              {referenceImportError ? <p className="error-text">{referenceImportError}</p> : null}
            </div>
          </details>
        ) : null}
        <div className="control-grid">
              </div>
              {supportsDynamicSpeakingRate(model) ? (
                <div className="field-group">
                  <label htmlFor="tts-live-speaking-rate">Speaking rate</label>
                  <input
                    id="tts-live-speaking-rate"
                    type="number"
                    min={0.5}
                    max={5}
                    step={0.1}
                    value={speakingRate}
                    onChange={(event) => setSpeakingRate(Number(event.target.value))}
                    disabled={sessionOpen}
                  />
                </div>
              ) : null}
            </div>
                ? "These controls are preserved in metadata for the Qwen provider. This lane is for latency and voice evaluation, not true chunked streaming yet."
                : "These controls apply at stream start for the current session only. Use them for immediate live quality tests without changing backend env defaults."}
                : supportsDynamicSpeakingRate(model)
                  ? "These controls apply at stream start for the current session only. Voxtream routes also read the speaking-rate knob here, so you can judge cadence and latency without changing provider env defaults."
                  : "These controls apply at stream start for the current session only. Use them for immediate live quality tests without changing backend env defaults."}
            </p>
          <div className="meta-card">
            <span className="label">Reference path</span>
            <strong className="meta-value-wrap">{selectedVoice?.reference_audio_path ?? "none"}</strong>
          </div>
          <div className="meta-card">
            <span className="label">Runtime conditioning</span>
I’m tightening TTS Studio too so imported references aren’t hardcoded to chatterbox. That way the library stays honest about which runtime lane each asset was meant for.

Edited file
TTSStudio.tsx
+31
-1


function isReferenceVoiceRoute(route: StudioRouteDescriptor) {
  return route.name === "voxtream_realtime" || route.name === "voxtream2_realtime" || route.name === "chatterbox";
}

function buildPresetPreviewText(preset: ExamplePreset) {
  const [cloneNotes, setCloneNotes] = useState("Imported reference voice for future studio voice-family testing.");
  const [cloneRuntimeTarget, setCloneRuntimeTarget] = useState<StudioRouteDescriptor["name"]>("voxtream2_realtime");
  const [cloneReferenceText, setCloneReferenceText] = useState("");
  const [designVoiceId, setDesignVoiceId] = useState<string | null>(null);
  const selectedRoute = routes.find((route) => route.name === routeTarget) ?? null;
  const referenceVoiceRoutes = useMemo(() => routes.filter(isReferenceVoiceRoute), [routes]);
  const selectedVoice = voices.find((voice) => voice.voice_id === selectedVoiceId) ?? null;
    }
    if (!payload.routes.some((route) => route.name === cloneRuntimeTarget && isReferenceVoiceRoute(route))) {
      setCloneRuntimeTarget(payload.routes.find((route) => route.name === "voxtream2_realtime")?.name ?? payload.routes.find(isReferenceVoiceRoute)?.name ?? "chatterbox");
    }
    setProvider(payload.routing.provider);
      form.set("source_model", "imported");
      form.set("runtime_target", "chatterbox");
      form.set("runtime_target", cloneRuntimeTarget);
      form.set("notes", cloneNotes);
      form.set("tags", cloneTags);
      if (cloneReferenceText.trim()) {
        form.set("reference_text", cloneReferenceText.trim());
      }
      const voice = await importStudioVoice(form);
              </div>
              <div className="field-group">
                <label htmlFor="voice-clone-runtime-target">Runtime target</label>
                <select id="voice-clone-runtime-target" value={cloneRuntimeTarget} onChange={(event) => setCloneRuntimeTarget(event.target.value as StudioRouteDescriptor["name"])}>
                  {referenceVoiceRoutes.map((route) => (
                    <option key={route.name} value={route.name}>
                      {routeLabel(route)}
                    </option>
                  ))}
                </select>
              </div>
            </div>
            <details className="accordion" open>
              <summary>Reference transcript</summary>
              <div className="accordion-body">
                <textarea value={cloneReferenceText} onChange={(event) => setCloneReferenceText(event.target.value)} rows={4} />
                <p className="field-hint">Save the transcript when you have it. Original Voxtream benefits from prompt text; Voxtream2 treats it as optional but still useful provenance.</p>
              </div>
            </details>
            <details className="accordion" open>
              <summary>Operator notes</summary>
I’ve got the UI changes in. I’m updating the branch docs now so the new truth is auditable: voxtream2 is not just scaffolded anymore, it now has a live reference-voice workflow in the console.

Explored 2 files
Edited file
CHANGELOG.md
+5
-0

  - corrected the example container model paths to the observed mounted layout: `/models/voice/herimor/voxtream*`
- Tightened the operator-side Voxtream reference voice workflow:
  - `TTS Live` now treats `voxtream_realtime` and `voxtream2_realtime` as reference-audio routes instead of generic preset-only lanes
  - added inline reference-voice import on `TTS Live` so reusable WAV assets can be added to the Studio registry without leaving the live console
  - exposed speaking-rate control on `TTS Live` for Voxtream family routes so runtime cadence tests map to the provider contract
  - `TTS Studio -> Voice Clone` no longer hardcodes imported references to `chatterbox`; operator can bind them directly to `voxtream_realtime`, `voxtream2_realtime`, or `chatterbox`
- Kept the frozen production realtime default unchanged:
Edited file
PROJECT_STATE.md
+4
-2

- `qwen_voice_design` is now integrated as the next studio/provider lane for prompt-driven voice creation and should stay batch-only until it proves out.
- `voxtream_realtime` and `voxtream2_realtime` are now scaffolded in the core repo as external-runner experiment lanes behind the existing stream contract; neither is the production baseline until runtime proof says otherwise.
- `voxtream_realtime` and `voxtream2_realtime` are now wired in the core repo as external-runner experiment lanes behind the existing stream contract; neither is the production baseline until runtime proof says otherwise.
- `voxtream2_realtime` now has external runtime proof in the sibling `voxtream-experiments` repo: warmup and prompt-audio-conditioned synthesis both completed successfully against real reference WAV assets on the L4 node.
- `TTS Live` now surfaces operator latency truth for Qwen lanes, including observed first chunk, observed final audio, and backend/provider timings when available.
- `TTS Live` now exposes a real reference-voice workflow for Voxtream family routes: Studio-managed asset dropdowns, inline reference import, and provider-facing speaking-rate control.
- The frozen realtime production baseline remains `Voxtral ASR + Kokoro TTS`.
  - intended integration shape is an external prompt-audio-conditioned runner on the shared mesh
  - current status is staged only; no runtime proof yet in this repo
  - runtime proof now exists in the sibling `voxtream-experiments` repo; core repo remains additive and non-default until operator latency and telephony harness value are proven
- `chatterbox`
The edits are in. I’m compiling the frontend now so I can catch any TypeScript/UI truth issues before telling you this is ready to pull.

Background terminal finished with git diff -- services/frontend/src/pages/TTSLive.tsx services/frontend/src/pages/TTSStudio.tsx PROJECT_STATE.md CHANGELOG.md


Background terminal finished with npm run build


The frontend compiled cleanly. I’m running the existing studio/streaming Python tests too, just to confirm the live voice-asset contract didn’t get out of sync while I tightened the console UX.

Background terminal finished with PYTHONPATH=/home/cory/Aether-Voice-Platform/Aether-Voice-X/services/worker-common:/home/cory/Aether-Voice-Platform/Aether-Voice-X pytest tests/unit/test_studio_service.py tests/unit/test_tts_streaming_service.py


Worked for 11m 19s
voxtream2 in this stack is a runtime clone lane, not a built-in preset-voice lane. The selected Studio voice asset contributes reference_audio_path at stream start, and the provider clones from that WAV on demand. So your instinct was right: the right UX is not “thousands of WAVs on the VM,” it’s a managed voice-asset dropdown.

I wired that into the core UI locally. TTSLive.tsx now treats voxtream_realtime and voxtream2_realtime as reference-voice routes, adds inline “Import reference into library” on the TTS Live page, shows the active reference path, and exposes a speaking-rate knob that maps into the Voxtream payload. TTSStudio.tsx also no longer hardcodes imported references to chatterbox; you can bind them directly to voxtream_realtime, voxtream2_realtime, or chatterbox. I updated PROJECT_STATE.md and CHANGELOG.md to reflect the new branch truth.

Verification passed:

npm run build in services/frontend
pytest tests/unit/test_studio_service.py tests/unit/test_tts_streaming_service.py
One important operational note: these changes are local in Aether-Voice-X right now. I have not pushed them. If you want, I can give you the exact diff summary or make the next pass on the voice-asset filtering/ranking before you pull it onto the VM.


4 files changed
+236
-12
Undo

Review
CHANGELOG.md
PROJECT_STATE.md
services/frontend/src/pages/TTSLive.tsx
services/frontend/src/pages/TTSStudio.tsx


