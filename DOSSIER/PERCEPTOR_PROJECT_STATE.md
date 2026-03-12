# Perceptor Project State

## Product Definition
Perceptor is AetherPro’s multimodal perception and sensor-fusion platform.
It converts raw visual, textual, audio, biometric, and environmental inputs into structured machine-interpretable detections, events, and contextual signals.

## Current Product Frame
- Desktop operator console: present / in progress
- Existing local-capable perception stack: yes
- Core modalities already explored:
  - object detection
  - pose detection
  - OCR
  - face / identity analysis
- Core libraries / engines already used:
  - YOLO
  - YOLO pose
  - PaddleOCR
  - InsightFace

## Current State
- Existing internal system works without full polished UI
- UI layer exists / is being refined
- Local-only execution is constrained by current hardware
- Remote GPU backend architecture is becoming necessary
- Product framing needs to evolve from “vision app” to “multimodal perception platform”

## Target Architecture
### Local
- desktop operator console
- device controls
- local event handling
- preview / session UX
- lightweight fallback logic

### Remote
- GPU-backed inference services
- model-specific workers
- stream/event processing
- secure API surface
- structured output and event normalization

### Future
- sensor bus
- plug-in modality adapters
- hardware ingestion layer
- multimodal reasoning loops
- Perceptor-backed products across security, industrial, and operator workflows

## Immediate Next Steps
1. Write Perceptor architecture dossier.
2. Define local vs remote responsibilities.
3. Define capability matrix by modality.
4. Define model placement strategy.
5. Define public positioning for perceptor.us.
6. Separate internal platform truth from external marketing language.

## Current Open Questions
- Which modalities are phase 1 vs phase 2?
- Which model lanes must be remote-only?
- What minimum viable operator workflow should the UI optimize for?
- How much inference should remain local for low-latency tasks?
- What is the first public-facing Perceptor use case?

## Notable Constraints
- laptop VRAM limits local execution
- GPU VM backend likely required for full-capability runtime
- architecture must support future multimodal expansion cleanly