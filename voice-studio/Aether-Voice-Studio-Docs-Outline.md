# Aether Voice Studio — Docs Outline

## 1. Overview
- What Aether Voice Studio is
- Who it is for
- Core capabilities
- Product surfaces
- Internal vs external use cases

## 2. Quick Start
- First launch
- Required services
- Minimum working path
- Generate first audio
- Run first live session
- Save first voice asset

## 3. Architecture
- System overview
- Model families
- Route targets
- Canonical storage paths
- Cache paths
- Runtime separation
- Internal dependency graph

## 4. Core Concepts
- Route target
- Voice asset
- Voice registry
- Session profile
- Realtime session
- Batch generation
- Dialogue scene
- LLM roundtrip
- Provider config

## 5. Navigation Guide
- Dashboard
- ASR Live
- ASR File
- TTS Live
- TTS File
- TTS Studio
- Sessions
- Models
- Metrics

## 6. ASR Live
- Purpose
- Input flow
- Realtime transcription
- Session behavior
- Use cases
- Troubleshooting

## 7. ASR File
- Batch transcription workflow
- Uploads
- Output artifacts
- Transcripts
- Troubleshooting

## 8. TTS Live
- Purpose
- Realtime route behavior
- Start / send / end flow
- Session voice binding
- Style controls
- Live output behavior
- Known constraints
- Troubleshooting

## 9. TTS File
- Batch generation workflow
- Route selection
- Output formats
- Chunking
- Troubleshooting

## 10. TTS Studio
### 10.1 Overview
- What Studio is for
- Why it is separate from TTS Live
- Supported workflows

### 10.2 Voice Library
- Browsing voices
- Filtering
- Tagging
- Previewing
- Reusing
- Archiving

### 10.3 Voice Clone
- Uploading reference audio
- Reference transcript guidance
- Preview flow
- Saving cloned voices
- Best practices

### 10.4 Voice Design
- Prompt-based voice creation
- Prompt examples
- Tag usage
- Preview and save flow
- Example presets

### 10.5 Batch Narration
- Single-speaker long-form generation
- Chunking strategy
- Export formats
- Creator workflows

### 10.6 Dialogue Studio
- Multi-speaker setup
- Speaker assignment
- Script formatting
- Scene generation
- Export flow

### 10.7 LLM Routing
- Provider selection
- Base URL selection
- Model selection
- Dynamic model discovery
- Auth handling
- Roundtrip configuration

### 10.8 Advanced
- Runtime paths
- Cache settings
- Diagnostics
- Operator controls

## 11. Voice Registry
- Registry schema
- Voice types
- Metadata fields
- Saved references
- Generated assets
- Seed voices
- Archive behavior

## 12. Routes and Models
- `moss_realtime`
- `moss_tts`
- `moss_ttsd`
- `moss_voice_generator`
- `moss_soundeffect`
- `chatterbox` fallback
- Route/model matrix

## 13. Sound Design
- Planned capability
- Sound effect prompt patterns
- Future tab behavior
- Creator workflows

## 14. LLM Roundtrip
- `ASR -> LLM -> TTS` architecture
- Provider model config
- Internal LiteLLM usage
- OpenAI/OpenRouter support
- Future public-user secrets vault

## 15. API Reference
- Realtime endpoints
- Batch generation endpoints
- Voice endpoints
- LLM provider endpoints
- Response schemas
- Error shapes

## 16. Configuration
- `.env` variables
- cache paths
- model paths
- output paths
- provider credentials
- internal routing config

## 17. Storage and Paths
- canonical model root
- HF cache root
- output paths
- voice reference paths
- what not to use
- path normalization rules

## 18. Operators Guide
- bringing the stack up
- restarting services
- validating models
- checking health
- monitoring output
- common operational issues

## 19. Troubleshooting
- realtime audio sounds wrong
- cloned voice sounds weak
- model missing or incomplete
- session issues
- provider auth issues
- model list not loading
- cache/path issues

## 20. FAQ
- Why separate TTS Live from TTS Studio?
- Why use a voice registry?
- When to use MOSS vs Chatterbox?
- Why does live lane avoid raw tag injection?
- Why does provider selection matter?
- Can users bring their own provider/model?

## 21. Roadmap
- Sound Design tab
- asset layering
- public secrets vault
- multi-tenant credentialing
- creator export packs
- integrated docs improvements
