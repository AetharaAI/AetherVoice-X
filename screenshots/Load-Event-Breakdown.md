The short read: no, this does not look like an OOM event. It looks like normal model-load behavior.

What your screenshots show:
- GPU `0`: `moss` realtime on `8021` plus `moss-ttsd` on `8023`
- GPU `2`: `voxtral` / `vLLM EngineCore`
- GPU `3`: external `chatterbox`
- GPU `1`: your embedding routers

The startup spike to `100%` on GPU `0` is not the dangerous part. That is normal during weight materialization and first init. The real signal is VRAM, and that is where the important story is:

- GPU `0` climbed from roughly `14.4 GiB` to `16.0 GiB` to about `22.35 GiB / 22.49 GiB`
- GPU `2` climbed up to about `19.33 GiB / 22.49 GiB`
- GPU `3` sat around `5.9 GiB`
- GPU `1` sat around `3.1 GiB`

So:
- `moss_realtime + moss_ttsd` on GPU `0` did boot without OOM
- `voxtral` on GPU `2` also booted without OOM
- the stack shown is stable enough to start
- but GPU `0` is effectively full

That last point matters. This is the part I would not hand-wave away:
- GPU `0` is not “comfortable”
- GPU `0` is “barely fits”
- adding another resident OpenMOSS family model there, especially `moss-tts` or `moss-soundeffect`, is likely to tip it over

So I would describe the current GPU contract as:
- good: `moss_realtime` on `0`
- acceptable but tight: `moss_realtime + moss_ttsd` on `0`
- good: `voxtral` on `2`
- acceptable shared lane: `moss_voice_generator` and external `chatterbox` on `3`, as long as you do not rely on both hot at once
- low confidence: “all OpenMOSS sidecars resident at once” on this exact layout

One important caveat: your nvtop shots do not show `moss-tts`, `moss-voice-generator`, and `moss-soundeffect` all resident at the same time. So I would not call this “the entire stack fully loaded” yet. I would call it:
- base stack up
- `moss`
- `moss-ttsd`
- `voxtral`
- external `chatterbox`
- no OOM seen

The unrelated warning in logs:
- Redis `vm.overcommit_memory=1`
- that is not a GPU issue, but you should still fix it on the VM

If you want exact proof of “full stack without OOM”, run these on the VM:

```bash
# Show which compose services are actually up.
docker compose \
  --profile voxtral \
  --profile moss \
  --profile moss-tts \
  --profile moss-ttsd \
  --profile moss-voicegen \
  --profile moss-sfx \
  ps

# Scan recent logs for successful model boot vs OOM.
docker compose \
  --profile voxtral \
  --profile moss \
  --profile moss-tts \
  --profile moss-ttsd \
  --profile moss-voicegen \
  --profile moss-sfx \
  logs --since=15m \
  | rg "Application startup complete|Uvicorn running|EngineCore|OutOfMemory|CUDA out of memory|exited with code"

# Snapshot GPU allocations in plain text.
nvidia-smi
```

My current verdict:
- you did not OOM
- the startup spike is normal
- the GPU pinning is mostly correct
- GPU `0` is too tight to be treated as a safe home for more resident OpenMOSS family services than the ones already shown

If you want, I can give you the next step as a hard recommendation: a “safe resident layout” vs an “all models loaded layout” for these 4 L4s.
