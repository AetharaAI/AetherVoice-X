## Platform Execution Lanes  -  Aether Voice X Studio

### Lane 1: Realtime Agent Mode
ASR -> LLM -> realtime TTS

Primary product lane for telephony agents.
Goal: low-latency, interruption-capable, natural live voice interaction.
Current blocker: realtime voice identity and stronger conditioning control.

### Lane 2: Turn-Based Voice Mode
ASR -> LLM -> batch / turn-based TTS

Next implementation lane.
Goal: establish a reliable end-to-end conversational baseline with stronger voice fidelity, cleaner prosody, and easier debugging.
This lane should be completed before additional realtime experimentation.

### Lane 3: Assisted / Staged Streaming Mode
ASR -> LLM -> staged chunk playback

Future enhancement lane.
Goal: create a perceived-realtime conversational experience using staged or chunked playback without requiring full realtime synthesis constraints.
Useful for dispatch, intake, appointment scheduling, and service workflows where slight response latency is acceptable.


