import { useEffect, useMemo, useState } from "react";

import { createStudioVoice, fetchProviderModels, fetchStudioOverview, importStudioVoice, saveStudioRouting, warmStudioRoute } from "../api/studio";
import { synthesizeText } from "../api/tts";
import { Badge } from "../components/common/Badge";
import { Panel } from "../components/common/Panel";
import { WaveformPlaceholder } from "../components/tts/WaveformPlaceholder";
import { canPlayAudio, formatMs } from "../lib/format";
import type { ExamplePreset, LLMProviderModel, StudioOverview, StudioRouteDescriptor, StudioVoice, TTSResponse } from "../types/api";

type StudioTab = "Voice Library" | "Voice Clone" | "Voice Design" | "Batch Narration" | "Dialogue Studio" | "LLM Routing" | "Advanced";

const STUDIO_TABS: StudioTab[] = [
  "Voice Library",
  "Voice Clone",
  "Voice Design",
  "Batch Narration",
  "Dialogue Studio",
  "LLM Routing",
  "Advanced"
];

function routeTone(status: StudioRouteDescriptor["status"]) {
  if (status === "ready") {
    return "good" as const;
  }
  if (status === "staged") {
    return "warn" as const;
  }
  if (status === "disabled" || status === "missing") {
    return "danger" as const;
  }
  return "default" as const;
}

function voiceTone(type: StudioVoice["type"]) {
  if (type === "cloned" || type === "generated") {
    return "good" as const;
  }
  if (type === "fallback") {
    return "warn" as const;
  }
  return "default" as const;
}

function flattenDialogueScript(script: string) {
  return script
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .join(" ");
}

function routeLabel(route: StudioRouteDescriptor) {
  if (route.invokable) {
    return route.label;
  }
  return `${route.label} (${route.status})`;
}

function preferredStudioRoute(routes: StudioRouteDescriptor[]) {
  return (
    routes.find((route) => route.name === "moss_voice_generator" && route.invokable)?.name ??
    routes.find((route) => route.name === "moss_voice_generator")?.name ??
    routes.find((route) => route.invokable)?.name ??
    routes[0]?.name ??
    "moss_voice_generator"
  );
}

function preferredVoiceDesignRoute(routes: StudioRouteDescriptor[]) {
  return (
    routes.find((route) => route.name === "moss_voice_generator" && route.invokable)?.name ??
    routes.find((route) => route.name === "moss_voice_generator" && route.status === "staged")?.name ??
    routes.find((route) => route.name === "chatterbox" && route.invokable)?.name ??
    routes.find((route) => route.name === "chatterbox" && route.status === "staged")?.name ??
    routes.find((route) => route.mode === "voice-design")?.name ??
    "moss_voice_generator"
  );
}

function preferredBatchRoute(routes: StudioRouteDescriptor[]) {
  return (
    routes.find((route) => route.name === "moss_tts" && route.invokable)?.name ??
    routes.find((route) => route.name === "chatterbox" && route.invokable)?.name ??
    routes.find((route) => route.mode === "batch" && route.invokable)?.name ??
    "chatterbox"
  );
}

function preferredDialogueRoute(routes: StudioRouteDescriptor[]) {
  return (
    routes.find((route) => route.name === "moss_ttsd" && route.invokable)?.name ??
    routes.find((route) => route.name === "chatterbox" && route.invokable)?.name ??
    routes.find((route) => route.mode === "dialogue" && route.invokable)?.name ??
  "chatterbox"
  );
}

function buildPresetPreviewText(preset: ExamplePreset) {
  return `AetherPro voice design preview for ${preset.title}. Please confirm the line is stable and operator-ready.`;
}

function designPreviewTextForVoice(voice: StudioVoice) {
  const demo = voice.default_params?.demo_sample_text;
  if (typeof demo === "string" && demo.trim()) {
    return demo.trim();
  }
  if (voice.reference_text?.trim()) {
    return voice.reference_text.trim();
  }
  return `Previewing ${voice.display_name} for operator readiness and studio voice quality.`;
}

export function TTSStudio() {
  const [overview, setOverview] = useState<StudioOverview | null>(null);
  const [activeTab, setActiveTab] = useState<StudioTab>("Voice Library");
  const [routeTarget, setRouteTarget] = useState<StudioRouteDescriptor["name"]>("moss_voice_generator");
  const [selectedVoiceId, setSelectedVoiceId] = useState("moss_default");
  const [saveToLibrary, setSaveToLibrary] = useState(true);
  const [voiceFilter, setVoiceFilter] = useState("");
  const [cloneName, setCloneName] = useState("Dispatch Reference");
  const [cloneFile, setCloneFile] = useState<File | null>(null);
  const [cloneTags, setCloneTags] = useState("telephony, support");
  const [cloneNotes, setCloneNotes] = useState("Imported reference voice for future MOSS cloning runs.");
  const [designName, setDesignName] = useState("Warm Dispatcher");
  const [designPrompt, setDesignPrompt] = useState("Warm female dispatcher voice with calm authority, clear articulation, and telephony-friendly pacing.");
  const [designPreviewText, setDesignPreviewText] = useState("AetherPro dispatch confirms the field team is active and en route.");
  const [designPresetSummary, setDesignPresetSummary] = useState("Load a preset to seed the name, prompt, and preview text before rendering or saving.");
  const [designRoute, setDesignRoute] = useState<StudioRouteDescriptor["name"]>("moss_voice_generator");
  const [batchText, setBatchText] = useState("AetherPro dispatch confirms the blue relay opens at noon. Maintain line integrity and proceed with the service window.");
  const [batchFormat, setBatchFormat] = useState("wav");
  const [batchRoute, setBatchRoute] = useState<StudioRouteDescriptor["name"]>("chatterbox");
  const [dialogueScript, setDialogueScript] = useState("[Narrator] The line stabilizes.\n[Dispatcher] A technician is being dispatched to your location now.");
  const [dialogueRoute, setDialogueRoute] = useState<StudioRouteDescriptor["name"]>("chatterbox");
  const [provider, setProvider] = useState<"openai" | "openrouter" | "litellm" | "anthropic">("litellm");
  const [providerModels, setProviderModels] = useState<LLMProviderModel[]>([]);
  const [selectedProviderModel, setSelectedProviderModel] = useState("");
  const [routingMode, setRoutingMode] = useState<"manual" | "asr_llm_tts" | "shadow">("manual");
  const [routingPrompt, setRoutingPrompt] = useState("Respond with short, spoken-ready voice agent deltas.");
  const [response, setResponse] = useState<TTSResponse | null>(null);
  const [busyAction, setBusyAction] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const routes = overview?.routes ?? [];
  const voices = overview?.voices ?? [];
  const voiceDesignRoutes = useMemo(
    () => routes.filter((route) => route.name === "moss_voice_generator" || route.name === "chatterbox"),
    [routes]
  );
  const selectedRoute = routes.find((route) => route.name === routeTarget) ?? null;
  const selectedVoice = voices.find((voice) => voice.voice_id === selectedVoiceId) ?? null;
  const filteredVoices = useMemo(() => {
    const term = voiceFilter.trim().toLowerCase();
    return voices.filter((voice) => {
      if (!term) {
        return true;
      }
      return [voice.display_name, voice.source_model, voice.runtime_target, ...voice.tags].join(" ").toLowerCase().includes(term);
    });
  }, [voiceFilter, voices]);

  const selectedVoiceDemoText = useMemo(() => {
    const demo = selectedVoice?.default_params?.demo_sample_text;
    return typeof demo === "string" ? demo : null;
  }, [selectedVoice]);

  async function refreshOverview() {
    const payload = await fetchStudioOverview();
    setOverview(payload);
    if (!payload.routes.some((route) => route.name === routeTarget)) {
      setRouteTarget(preferredStudioRoute(payload.routes));
    }
    if (!payload.voices.some((voice) => voice.voice_id === selectedVoiceId)) {
      setSelectedVoiceId(payload.voices[0]?.voice_id ?? "moss_default");
    }
    if (!payload.routes.some((route) => route.name === batchRoute && route.invokable)) {
      setBatchRoute(preferredBatchRoute(payload.routes));
    }
    if (!payload.routes.some((route) => route.name === dialogueRoute && route.invokable)) {
      setDialogueRoute(preferredDialogueRoute(payload.routes));
    }
    if (!payload.routes.some((route) => route.name === designRoute && (route.name === "moss_voice_generator" || route.name === "chatterbox"))) {
      setDesignRoute(preferredVoiceDesignRoute(payload.routes));
    }
    setProvider(payload.routing.provider);
    setSelectedProviderModel(payload.routing.model ?? "");
    setRoutingMode(payload.routing.mode);
    setRoutingPrompt(payload.routing.system_prompt ?? "Respond with short, spoken-ready voice agent deltas.");
  }

  useEffect(() => {
    void refreshOverview().catch((err: Error) => setError(err.message));
  }, []);

  useEffect(() => {
    if (!overview) {
      return;
    }
    void fetchProviderModels(provider)
      .then((models) => {
        setProviderModels(models);
        if (!models.some((entry) => entry.id === selectedProviderModel)) {
          setSelectedProviderModel(models[0]?.id ?? "");
        }
      })
      .catch(() => setProviderModels([]));
  }, [overview, provider, selectedProviderModel]);

  useEffect(() => {
    if (!voiceDesignRoutes.length) {
      return;
    }
    if (!voiceDesignRoutes.some((route) => route.name === designRoute)) {
      setDesignRoute(preferredVoiceDesignRoute(routes));
    }
  }, [designRoute, routes, voiceDesignRoutes]);

  const selectedDesignRoute = voiceDesignRoutes.find((route) => route.name === designRoute) ?? null;
  const designRouteWarmable = Boolean(selectedDesignRoute?.status === "staged" && selectedDesignRoute?.name !== "moss_realtime");
  const designPreviewRouteTruth =
    designRoute === "moss_voice_generator"
      ? "Voice Generator preview. Generated timbre should reflect the design prompt when the sidecar is healthy."
      : "Fallback preview. This lets you audition text/audio flow, but it is not true voice-generation conditioning.";

  function applyVoiceDesignState(voice: StudioVoice) {
    setDesignName(voice.display_name);
    setDesignPrompt(voice.generation_prompt?.trim() ? voice.generation_prompt : voice.notes ?? "");
    setDesignPreviewText(designPreviewTextForVoice(voice));
    setDesignPresetSummary(
      voice.generation_prompt
        ? `Loaded ${voice.display_name} from the registry. Review the prompt, render a preview, then save any edits back into the library.`
        : `Loaded ${voice.display_name} from the registry. This record has no stored generation prompt yet, so review the description before previewing.`
    );
    setDesignRoute(voice.source_model === "moss_voice_generator" ? "moss_voice_generator" : preferredVoiceDesignRoute(routes));
  }

  async function warmRoute(routeName: StudioRouteDescriptor["name"], successMessage: string) {
    setBusyAction("warm-route");
    setError(null);
    setMessage(null);
    try {
      const payload = await warmStudioRoute(routeName);
      setOverview(payload);
      setMessage(successMessage);
    } catch (err) {
      setError((err as Error).message);
      throw err;
    } finally {
      setBusyAction(null);
    }
  }

  function handleVoiceLibrarySelect(voice: StudioVoice) {
    setSelectedVoiceId(voice.voice_id);
    setMessage(`Selected ${voice.display_name}.`);
    setError(null);
  }

  function handleVoiceLibraryLoadIntoDesign(voice: StudioVoice) {
    setSelectedVoiceId(voice.voice_id);
    setActiveTab("Voice Design");
    applyVoiceDesignState(voice);
    setMessage(`Loaded ${voice.display_name} into Voice Design.`);
    setError(null);
  }

  function handleSelectedVoiceChange(nextVoiceId: string) {
    setSelectedVoiceId(nextVoiceId);
    const nextVoice = voices.find((voice) => voice.voice_id === nextVoiceId);
    if (activeTab === "Voice Design" && nextVoice) {
      applyVoiceDesignState(nextVoice);
      setMessage(`Loaded ${nextVoice.display_name} into Voice Design.`);
      setError(null);
    }
  }

  async function runBatchGeneration(
    text: string,
    model: string,
    options?: {
      format?: string;
      metadataExtra?: Record<string, unknown>;
      successMessage?: string;
    }
  ) {
    setBusyAction("generate");
    setError(null);
    setMessage(null);
    try {
      const payload = await synthesizeText({
        model,
        voice: selectedVoice?.voice_id ?? "default",
        text,
        format: options?.format ?? batchFormat,
        sample_rate: 24000,
        stream: false,
        style: { speed: 1.0, emotion: "neutral" },
        metadata: {
          source: "tts_studio",
          extra: { tab: activeTab, route_target: model, save_to_library: saveToLibrary, ...(options?.metadataExtra ?? {}) }
        }
      });
      setResponse(payload);
      setMessage(options?.successMessage ?? `Generation completed via ${payload.model_used}.`);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusyAction(null);
    }
  }

  async function handleVoiceImport() {
    if (!cloneFile) {
      setError("Choose a reference file before importing.");
      return;
    }
    setBusyAction("import");
    setError(null);
    setMessage(null);
    try {
      const form = new FormData();
      form.set("file", cloneFile);
      form.set("display_name", cloneName);
      form.set("source_model", "moss_voice_generator");
      form.set("runtime_target", "moss_voice_generator");
      form.set("notes", cloneNotes);
      form.set("tags", cloneTags);
      const voice = await importStudioVoice(form);
      setMessage(`Reference voice imported as ${voice.display_name}.`);
      await refreshOverview();
      setSelectedVoiceId(voice.voice_id);
      setActiveTab("Voice Library");
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusyAction(null);
    }
  }

  async function handleVoiceDesignSave(example?: ExamplePreset) {
    setBusyAction("save-voice");
    setError(null);
    setMessage(null);
    try {
      const voice = await createStudioVoice({
        display_name: example?.title ?? designName,
        type: "generated",
        source_model: "moss_voice_generator",
        runtime_target: designRoute,
        generation_prompt: example?.generation_prompt ?? designPrompt,
        tags: example?.tags ?? ["generated", "voice-design"],
        default_params: { save_to_library: saveToLibrary },
        notes: example?.description ?? "Voice design preset saved from TTS Studio."
      });
      setMessage(`Voice preset saved as ${voice.display_name}.`);
      await refreshOverview();
      setSelectedVoiceId(voice.voice_id);
      if (!example) {
        setActiveTab("Voice Library");
      }
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusyAction(null);
    }
  }

  function handleVoiceDesignPresetLoad(preset: ExamplePreset) {
    setDesignName(preset.title);
    setDesignPrompt(preset.generation_prompt);
    setDesignPreviewText(buildPresetPreviewText(preset));
    setDesignPresetSummary(preset.description);
    setMessage(`Loaded preset: ${preset.title}. Review the prompt, then render a preview or save it into the library.`);
    setError(null);
  }

  async function handleRoutingSave() {
    setBusyAction("save-routing");
    setError(null);
    setMessage(null);
    try {
      await saveStudioRouting({
        provider,
        model: selectedProviderModel || null,
        base_url: overview?.providers.find((entry) => entry.provider === provider)?.base_url ?? null,
        enabled: Boolean(selectedProviderModel),
        mode: routingMode,
        system_prompt: routingPrompt,
        metadata: { source: "tts_studio" }
      });
      setMessage(`Routing updated for ${provider}.`);
      await refreshOverview();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusyAction(null);
    }
  }

  async function handleVoiceDesignPreview() {
    if (!selectedDesignRoute) {
      setError("Choose a valid preview route first.");
      return;
    }
    if (selectedDesignRoute.name === "moss_realtime") {
      setError("MOSS Realtime is a live streaming lane, not a batch preview route. Use Voice Generator or Chatterbox fallback for design previews.");
      return;
    }
    if (designRouteWarmable) {
      try {
        await warmRoute(
          selectedDesignRoute.name,
          `Warmed ${selectedDesignRoute.label}. First load run completed; rendering preview next.`
        );
      } catch {
        return;
      }
    }
    await runBatchGeneration(designPreviewText, designRoute, {
      metadataExtra: {
        generation_prompt: designPrompt,
        source_voice_design: true,
        preview_voice_name: designName
      },
      successMessage: "Voice design preview rendered."
    });
  }

  return (
    <div className="page-grid">
      <Panel title="OpenMOSS capability surface" eyebrow="TTS Studio">
        <section className="studio-hero">
          <div className="studio-hero-copy">
            <p className="eyebrow">Studio control plane</p>
            <h3>Voice design, reusable assets, batch generation, and future LLM routing</h3>
            <p className="field-hint">This surface is additive. `TTS Live` stays the narrow realtime operator lane, while `TTS Studio` holds the broader OpenMOSS workflows.</p>
          </div>
          <div className="studio-hero-actions">
            <div className="field-group">
              <label htmlFor="studio-route-target">Active route</label>
                <select id="studio-route-target" value={routeTarget} onChange={(event) => setRouteTarget(event.target.value as StudioRouteDescriptor["name"])}>
                  {routes.map((route) => (
                    <option key={route.name} value={route.name} disabled={route.status === "disabled"}>
                      {routeLabel(route)}
                    </option>
                  ))}
                </select>
            </div>
            <div className="field-group">
              <label htmlFor="studio-selected-voice">Selected voice</label>
              <select id="studio-selected-voice" value={selectedVoiceId} onChange={(event) => handleSelectedVoiceChange(event.target.value)}>
                {voices.map((voice) => (
                  <option key={voice.voice_id} value={voice.voice_id}>
                    {voice.display_name}
                  </option>
                ))}
              </select>
            </div>
            <label className="switch studio-save-toggle">
              <input type="checkbox" checked={saveToLibrary} onChange={(event) => setSaveToLibrary(event.target.checked)} />
              Save new outputs and presets into the library
            </label>
            <button
              className="secondary square-action"
              onClick={() => selectedRoute && void warmRoute(selectedRoute.name, `Warmed ${selectedRoute.label}. Watch the logs for the first-load GPU pass.`)}
              disabled={busyAction === "warm-route" || !selectedRoute?.runtime_wired || selectedRoute.status === "ready" || selectedRoute.status === "missing" || selectedRoute.status === "disabled"}
              title="Run an explicit warmup request so the first model load happens now instead of on first operator action."
            >
              {busyAction === "warm-route" ? "Warming route..." : "Warm active route"}
            </button>
          </div>
        </section>

        <div className="toolbar">
          {routes.map((route) => (
            <Badge key={route.name} value={`${route.label} · ${route.status}`} tone={routeTone(route.status)} />
          ))}
        </div>

        <div className="studio-tabs">
          {STUDIO_TABS.map((tab) => (
            <button key={tab} className={tab === activeTab ? "secondary studio-tab active" : "secondary studio-tab"} onClick={() => setActiveTab(tab)} title={`Open ${tab}`}>
              {tab}
            </button>
          ))}
        </div>

        {activeTab === "Voice Library" ? (
          <section className="stack">
            <div className="control-grid">
              <div className="field-group">
                <label htmlFor="voice-library-search">Search voices</label>
                <input id="voice-library-search" value={voiceFilter} onChange={(event) => setVoiceFilter(event.target.value)} placeholder="Search preset, cloned, generated, imported..." />
                <p className="field-hint">Seed voices are loaded automatically from the repo-backed studio seed library when present. Use a card action to load a voice into Voice Design or mark it as the current working voice.</p>
              </div>
              <div className="field-group">
                <label>Current selection</label>
                <div className="meta-card compact">
                  <strong>{selectedVoice?.display_name ?? "No voice selected"}</strong>
                  <span className="label">{selectedVoice?.runtime_target ?? "unbound"}</span>
                </div>
                {selectedVoice?.notes ? <p className="field-hint">{selectedVoice.notes}</p> : null}
                {selectedVoiceDemoText ? <p className="field-hint"><strong>Demo text:</strong> {selectedVoiceDemoText}</p> : null}
                {selectedVoice ? (
                  <div className="toolbar">
                    <button className="secondary compact-button square-action" onClick={() => handleVoiceLibrarySelect(selectedVoice)}>
                      Select asset
                    </button>
                    <button className="secondary compact-button square-action" onClick={() => handleVoiceLibraryLoadIntoDesign(selectedVoice)}>
                      Open in Voice Design
                    </button>
                  </div>
                ) : null}
              </div>
            </div>
            <div className="studio-voice-grid">
              {filteredVoices.map((voice) => (
                <article key={voice.voice_id} className="model-card studio-voice-card">
                  <div className="toolbar">
                    <h3>{voice.display_name}</h3>
                    <Badge value={voice.type} tone={voiceTone(voice.type)} />
                  </div>
                  <p className="field-hint">{voice.notes ?? "Reusable voice asset for OpenMOSS and fallback batch routes."}</p>
                  <div className="voice-card-actions">
                    <button className="secondary compact-button square-action" onClick={() => handleVoiceLibrarySelect(voice)}>
                      Select asset
                    </button>
                    <button className="secondary compact-button square-action" onClick={() => handleVoiceLibraryLoadIntoDesign(voice)}>
                      Open in Voice Design
                    </button>
                  </div>
                  <details className="accordion studio-card-details">
                    <summary>Voice record details</summary>
                    <div className="accordion-body">
                      <div className="artifact-list">
                        <div className="artifact-row"><span>voice id</span><code className="inline-code">{voice.voice_id}</code></div>
                        <div className="artifact-row"><span>source model</span><code className="inline-code">{voice.source_model}</code></div>
                        <div className="artifact-row"><span>runtime target</span><code className="inline-code">{voice.runtime_target}</code></div>
                        {voice.reference_audio_path ? <div className="artifact-row"><span>reference</span><code className="inline-code">{voice.reference_audio_path}</code></div> : null}
                        {voice.generation_prompt ? <div className="artifact-row"><span>generation prompt</span><code className="inline-code">{voice.generation_prompt}</code></div> : null}
                      </div>
                      <div className="toolbar">
                        {voice.tags.map((tag) => (
                          <Badge key={`${voice.voice_id}-${tag}`} value={tag} />
                        ))}
                      </div>
                    </div>
                  </details>
                </article>
              ))}
            </div>
          </section>
        ) : null}

        {activeTab === "Voice Clone" ? (
          <section className="stack">
            <div className="control-grid">
              <div className="field-group">
                <label htmlFor="voice-clone-file">Reference audio</label>
                <input id="voice-clone-file" type="file" accept="audio/*" onChange={(event) => setCloneFile(event.target.files?.[0] ?? null)} />
                <p className="field-hint">Imported references become reusable registry assets instead of one-shot uploads.</p>
              </div>
              <div className="field-group">
                <label htmlFor="voice-clone-name">Display name</label>
                <input id="voice-clone-name" value={cloneName} onChange={(event) => setCloneName(event.target.value)} />
              </div>
              <div className="field-group">
                <label htmlFor="voice-clone-tags">Tags</label>
                <input id="voice-clone-tags" value={cloneTags} onChange={(event) => setCloneTags(event.target.value)} placeholder="telephony, support, clone" />
              </div>
            </div>
            <details className="accordion" open>
              <summary>Operator notes</summary>
              <div className="accordion-body">
                <textarea value={cloneNotes} onChange={(event) => setCloneNotes(event.target.value)} rows={4} />
                <p className="field-hint">This pass registers the reusable reference asset. The heavy MOSS cloning execution path can bind to the same stored asset later without changing the UI contract.</p>
              </div>
            </details>
            <button onClick={handleVoiceImport} disabled={busyAction === "import"}>
              {busyAction === "import" ? "Importing reference..." : "Import reference into library"}
            </button>
          </section>
        ) : null}

        {activeTab === "Voice Design" ? (
          <section className="stack">
            <details className="accordion" open>
              <summary>Example presets</summary>
              <div className="accordion-body">
                <p className="field-hint">{designPresetSummary}</p>
                <div className="preset-chip-grid">
                {(overview?.example_presets ?? []).map((preset) => (
                  <button
                    key={preset.title}
                    className="secondary preset-chip"
                    onClick={() => handleVoiceDesignPresetLoad(preset)}
                    title={preset.description}
                    disabled={busyAction === "save-voice" || busyAction === "generate"}
                  >
                    {preset.title}
                  </button>
                ))}
                </div>
              </div>
            </details>
            <div className="control-grid">
              <div className="field-group">
                <label htmlFor="voice-design-name">Preset name</label>
                <input id="voice-design-name" value={designName} onChange={(event) => setDesignName(event.target.value)} />
              </div>
              <div className="field-group">
                <label htmlFor="voice-design-route">Runtime target</label>
                <select id="voice-design-route" value={designRoute} onChange={(event) => setDesignRoute(event.target.value as StudioRouteDescriptor["name"])}>
                  {voiceDesignRoutes.map((route) => (
                      <option key={route.name} value={route.name} disabled={route.name === "moss_realtime"}>
                        {routeLabel(route)}
                      </option>
                    ))}
                </select>
                <p className="field-hint">{designPreviewRouteTruth}</p>
              </div>
            </div>
            <details className="accordion" open>
              <summary>Voice description</summary>
              <div className="accordion-body">
                <textarea value={designPrompt} onChange={(event) => setDesignPrompt(event.target.value)} rows={6} />
                <p className="field-hint">Voice Generator is the preferred OpenMOSS route for studio-side voice creation. Save the preset into the registry, or render a preview when the sidecar is healthy.</p>
              </div>
            </details>
            <details className="accordion" open>
              <summary>Preview utterance</summary>
              <div className="accordion-body">
                <textarea value={designPreviewText} onChange={(event) => setDesignPreviewText(event.target.value)} rows={4} />
                <p className="field-hint">This sample line is spoken with the current generation prompt so you can audition Voice Generator outputs before saving them into the library. If the route is staged, the first click runs a warmup pass and then renders the preview.</p>
              </div>
            </details>
            <div className="toolbar">
              <button
                className="secondary"
                onClick={() => void handleVoiceDesignPreview()}
                disabled={
                  busyAction === "generate" ||
                  busyAction === "warm-route" ||
                  !selectedDesignRoute ||
                  (!selectedDesignRoute.invokable && !designRouteWarmable)
                }
              >
                {busyAction === "generate"
                  ? "Rendering preview..."
                  : busyAction === "warm-route"
                    ? "Warming model..."
                    : designRouteWarmable
                      ? "Warm model + render preview"
                      : "Render design preview"}
              </button>
              <button onClick={() => handleVoiceDesignSave()} disabled={busyAction === "save-voice"}>
                {busyAction === "save-voice" ? "Saving preset..." : "Save design into library"}
              </button>
            </div>
          </section>
        ) : null}

        {activeTab === "Batch Narration" ? (
          <section className="stack">
            <div className="control-grid">
              <div className="field-group">
                <label htmlFor="batch-route">Batch route</label>
                <select id="batch-route" value={batchRoute} onChange={(event) => setBatchRoute(event.target.value as StudioRouteDescriptor["name"])}>
                  {routes.filter((route) => route.mode === "batch").map((route) => (
                    <option key={route.name} value={route.name} disabled={!route.invokable}>
                      {routeLabel(route)}
                    </option>
                  ))}
                </select>
              </div>
              <div className="field-group">
                <label htmlFor="batch-format">Output format</label>
                <select id="batch-format" value={batchFormat} onChange={(event) => setBatchFormat(event.target.value)}>
                  <option value="wav">wav</option>
                  <option value="mp3">mp3</option>
                </select>
              </div>
            </div>
            <details className="accordion" open>
              <summary>Narration body</summary>
              <div className="accordion-body">
                <textarea value={batchText} onChange={(event) => setBatchText(event.target.value)} rows={8} />
                <p className="field-hint">Use this for long-form single-speaker generation. When the OpenMOSS TTS sidecar is healthy it becomes the preferred batch route; Chatterbox remains the fallback for continuity.</p>
              </div>
            </details>
            <button onClick={() => runBatchGeneration(batchText, batchRoute)} disabled={busyAction === "generate"}>
              {busyAction === "generate" ? "Generating narration..." : "Generate narration"}
            </button>
          </section>
        ) : null}

        {activeTab === "Dialogue Studio" ? (
          <section className="stack">
            <div className="control-grid">
              <div className="field-group">
                <label htmlFor="dialogue-route">Dialogue route</label>
                <select id="dialogue-route" value={dialogueRoute} onChange={(event) => setDialogueRoute(event.target.value as StudioRouteDescriptor["name"])}>
                  {routes.filter((route) => route.mode === "dialogue" || route.name === "chatterbox").map((route) => (
                    <option key={route.name} value={route.name} disabled={!route.invokable}>
                      {routeLabel(route)}
                    </option>
                  ))}
                </select>
              </div>
              <div className="field-group">
                <label>Speaker assignment</label>
                <div className="meta-card compact">
                  <strong>{selectedVoice?.display_name ?? "Unassigned"}</strong>
                  <span className="label">Primary speaker voice</span>
                </div>
              </div>
            </div>
            <details className="accordion" open>
              <summary>Scene script</summary>
              <div className="accordion-body">
                <textarea value={dialogueScript} onChange={(event) => setDialogueScript(event.target.value)} rows={8} />
                <p className="field-hint">TTSD becomes the preferred dialogue route when its sidecar is healthy. Chatterbox remains available as the safe compatibility fallback.</p>
              </div>
            </details>
            <button onClick={() => runBatchGeneration(flattenDialogueScript(dialogueScript), dialogueRoute)} disabled={busyAction === "generate"}>
              {busyAction === "generate" ? "Rendering dialogue..." : "Render dialogue preview"}
            </button>
          </section>
        ) : null}

        {activeTab === "LLM Routing" ? (
          <section className="stack">
            <div className="control-grid">
              <div className="field-group">
                <label htmlFor="routing-provider">Provider</label>
                <select id="routing-provider" value={provider} onChange={(event) => setProvider(event.target.value as typeof provider)}>
                  {(overview?.providers ?? []).map((entry) => (
                    <option key={entry.provider} value={entry.provider}>
                      {entry.label}
                    </option>
                  ))}
                </select>
              </div>
              <div className="field-group">
                <label htmlFor="routing-model">Model</label>
                <select id="routing-model" value={selectedProviderModel} onChange={(event) => setSelectedProviderModel(event.target.value)}>
                  <option value="">Select live provider model</option>
                  {providerModels.map((entry) => (
                    <option key={entry.id} value={entry.id}>
                      {entry.label}
                    </option>
                  ))}
                </select>
                <p className="field-hint">This dropdown is fetched live from the provider `/models` endpoint through the backend, not hardcoded in the browser.</p>
              </div>
              <div className="field-group">
                <label htmlFor="routing-mode">Mode</label>
                <select id="routing-mode" value={routingMode} onChange={(event) => setRoutingMode(event.target.value as typeof routingMode)}>
                  <option value="manual">manual</option>
                  <option value="asr_llm_tts">asr_llm_tts</option>
                  <option value="shadow">shadow</option>
                </select>
              </div>
            </div>
            <details className="accordion" open>
              <summary>Backend-held routing prompt</summary>
              <div className="accordion-body">
                <textarea value={routingPrompt} onChange={(event) => setRoutingPrompt(event.target.value)} rows={5} />
                <p className="field-hint">Secrets stay backend-side. This pass only stores provider/base/model choices and the prompt contract for future <code className="inline-code">ASR -&gt; LLM -&gt; TTS</code> loop orchestration.</p>
              </div>
            </details>
            <button onClick={handleRoutingSave} disabled={busyAction === "save-routing"}>
              {busyAction === "save-routing" ? "Saving routing..." : "Save routing config"}
            </button>
          </section>
        ) : null}

        {activeTab === "Advanced" ? (
          <section className="stack">
            <details className="accordion" open>
              <summary>Route catalog</summary>
              <div className="cards-grid">
                {routes.map((route) => (
                  <article key={route.name} className="model-card">
                    <div className="toolbar">
                      <h3>{route.label}</h3>
                      <Badge value={route.status} tone={routeTone(route.status)} />
                    </div>
                    <p className="field-hint">{route.notes}</p>
                    <div className="artifact-list">
                      <div className="artifact-row"><span>mode</span><code className="inline-code">{route.mode}</code></div>
                      {route.model_path ? <div className="artifact-row"><span>model path</span><code className="inline-code">{route.model_path}</code></div> : null}
                      {route.fallback_target ? <div className="artifact-row"><span>fallback</span><code className="inline-code">{route.fallback_target}</code></div> : null}
                    </div>
                  </article>
                ))}
              </div>
            </details>
            <details className="accordion">
              <summary>Canonical OpenMOSS root</summary>
              <div className="accordion-body">
                <code className="inline-code block">{overview?.canonical_model_root ?? "loading..."}</code>
                <p className="field-hint">Studio behavior is anchored to the canonical OpenMOSS model root, not stray cache or snapshot paths.</p>
              </div>
            </details>
          </section>
        ) : null}

        <details className="accordion">
          <summary>Tips &amp; Tricks</summary>
          <div className="accordion-body">
            <ul className="tips-list">
              <li>Use `TTS Live` for low-latency turn-taking. Use `TTS Studio` for design, cloning, and long-form generation.</li>
              <li>Imported reference WAVs become reusable assets in the voice registry, so you do not re-upload them every session.</li>
              <li>Voice Generator is the safest OpenMOSS path for testing new studio voices. Save promising outputs into the library, then bind them to future routes.</li>
              <li>Batch Narration prefers `moss_tts` when healthy. Dialogue Studio prefers `moss_ttsd` when healthy. Chatterbox remains the fallback instead of being silently removed.</li>
              <li>LLM provider model lists are pulled live from backend-discovered `/models` endpoints so operators are not chasing stale dropdowns.</li>
              <li>Keep the canonical OpenMOSS root clean: `/mnt/aetherpro/models/audio/OpenMOSS-Team`.</li>
            </ul>
          </div>
        </details>

        <section className="stream-output-shell">
          <div className="stream-output-header">
            <div>
              <p className="eyebrow">Output surface</p>
              <h3>Waveform, playback, artifacts, and route truth</h3>
              <p className="field-hint">Every studio tab resolves into the same bottom review panel so operators always know what route actually ran, which voice was bound, and what artifact landed.</p>
            </div>
            <div className="stream-output-actions">
              {response && canPlayAudio(response.audio_url) ? <audio controls src={response.audio_url} /> : <div className="playback-placeholder"><span className="label">Playback deck</span><strong>Waiting for browser-reachable audio</strong></div>}
              <a
                className={`button-link ${response ? "" : "disabled"}`}
                href={response?.audio_url ?? "#"}
                download={response ? `${response.session_id}.${batchFormat}` : "tts-studio.wav"}
                aria-disabled={!response}
                onClick={(event) => {
                  if (!response) {
                    event.preventDefault();
                  }
                }}
              >
                Download
              </a>
            </div>
          </div>
          <WaveformPlaceholder chunks={response ? 6 : 0} active={busyAction === "generate"} tone={response ? "good" : error ? "danger" : "default"} />
          <div className="meta-grid">
            <div className="meta-card">
              <span className="label">Route used</span>
              <strong>{response?.model_used ?? selectedRoute?.name ?? routeTarget}</strong>
            </div>
            <div className="meta-card">
              <span className="label">Voice used</span>
              <strong>{String(response?.artifacts?.selected_voice_asset ?? selectedVoice?.display_name ?? "default")}</strong>
            </div>
            <div className="meta-card">
              <span className="label">Generation time</span>
              <strong>{response ? formatMs(response.timings.total_ms) : "pending"}</strong>
            </div>
            <div className="meta-card">
              <span className="label">Duration</span>
              <strong>{response ? formatMs(response.duration_ms) : "pending"}</strong>
            </div>
          </div>
          {response ? (
            <div className="artifact-list">
              <div className="artifact-row"><span>artifact</span><code className="inline-code">{response.audio_url}</code></div>
              {Object.entries(response.artifacts ?? {}).map(([key, value]) => (
                <div key={key} className="artifact-row"><span>{key}</span><code className="inline-code">{String(value)}</code></div>
              ))}
            </div>
          ) : null}
        </section>

        {message ? <p className="success-text">{message}</p> : null}
        {error ? <p className="error-text">{error}</p> : null}
      </Panel>
    </div>
  );
}
