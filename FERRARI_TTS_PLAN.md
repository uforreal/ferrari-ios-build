# Project Ferrari: On-Device Human TTS for iPhone

> **Goal:** A real-time, expressive, single-voice TTS engine that runs on iPhone 12 without heat, battery drain, or glitches.

---

## The Architecture (3 Layers)

```
┌─────────────────────────────────────────────────────────────┐
│                     iOS Application                         │
├─────────────────────────────────────────────────────────────┤
│  Layer 1: THE BOUNCER (Always-On, Near-Zero Power)          │
│  ├── Silero VAD (CoreML, <2MB)                              │
│  └── Wakes Layer 2 only when human speech detected          │
├─────────────────────────────────────────────────────────────┤
│  Layer 2: THE BRAIN (On-Demand, LLM + Text Processing)      │
│  ├── Gemini API (Cloud) OR Local Phi-3 (CoreML)             │
│  ├── G2P: Grapheme-to-Phoneme Converter                     │
│  └── Generates Semantic Tokens from text                    │
├─────────────────────────────────────────────────────────────┤
│  Layer 3: THE VOICE (Real-Time, ANE Optimized)              │
│  ├── Matcha-TTS or Piper (Single-Voice Distilled)           │
│  ├── Runs on Apple Neural Engine (FP16)                     │
│  └── Streams to Lock-Free Circular Buffer                   │
├─────────────────────────────────────────────────────────────┤
│  Layer 4: THE SPEAKER (C++ AudioUnit, Real-Time Priority)   │
│  └── Pulls from buffer, plays audio with zero glitches      │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: The Foundation (PC Side - Python)
**Status:** 🔲 Not Started

### 1.1 Select & Test the Base TTS Model
- [ ] Download and test **Matcha-TTS** (Flow Matching, high quality)
- [ ] Download and test **Piper** (VITS, ultra-fast)
- [ ] Compare quality vs. speed on a sample sentence
- [ ] **Decision Point:** Choose the base model

### 1.2 Single-Voice Distillation
- [ ] Select the target voice (e.g., "Jenny" or a custom recording)
- [ ] Create a dataset of ~100 sentences in that voice
- [ ] Fine-tune/Distill the model to only produce that one voice
- [ ] Export the "Student" model (smaller, faster)

### 1.3 Export to ONNX
- [ ] Convert the PyTorch model to ONNX format
- [ ] Verify ONNX model produces identical audio
- [ ] Optimize ONNX graph (remove unused ops)

---

## Phase 2: The Conversion (PC Side - CoreML)
**Status:** 🔲 Not Started

### 2.1 ONNX to CoreML
- [ ] Install `coremltools` (Apple's Python library)
- [ ] Convert ONNX model to CoreML (.mlpackage)
- [ ] Set precision to **FP16** (required for ANE)
- [ ] Set tensor layout to **NCHW** (required for ANE)

### 2.2 Silero VAD to CoreML
- [ ] Download Silero VAD ONNX model
- [ ] Convert to CoreML (.mlpackage)
- [ ] Verify it detects voice correctly

---

## Phase 3: The iOS App (Swift + C++)
**Status:** 🔲 Not Started

### 3.1 Project Setup
- [ ] Create new Xcode project (Swift)
- [ ] Add CoreML models to project bundle
- [ ] Configure `AVAudioSession` for voice processing

### 3.2 Layer 1: The Bouncer (VAD)
- [ ] Load Silero VAD CoreML model
- [ ] Create a low-power audio input stream
- [ ] When VAD detects speech → Wake Layer 2

### 3.3 Layer 2: The Brain (LLM)
- [ ] Integrate Gemini API (or local LLM if chosen)
- [ ] Build G2P (Grapheme-to-Phoneme) pipeline
- [ ] Convert text response to phoneme tokens

### 3.4 Layer 3: The Voice (TTS)
- [ ] Load TTS CoreML model (on ANE)
- [ ] Implement streaming inference (chunk by chunk)
- [ ] Push audio chunks to circular buffer

### 3.5 Layer 4: The Speaker (Audio)
- [ ] Create C++ AudioUnit Render Callback
- [ ] Implement TPCircularBuffer
- [ ] Pull audio from buffer, play to speaker

---

## Phase 4: Polish & Optimization
**Status:** 🔲 Not Started

### 4.1 Latency Tuning
- [ ] Measure end-to-end latency (speech-in to speech-out)
- [ ] Target: < 500ms for first word
- [ ] Optimize buffer sizes

### 4.2 Power Profiling
- [ ] Use Xcode Instruments to measure power consumption
- [ ] Ensure ANE is being used (not CPU/GPU fallback)
- [ ] Target: < 5% battery per hour of active use

### 4.3 Glitch Prevention
- [ ] Stress test with background apps
- [ ] Verify no audio skips under load
- [ ] Add graceful fallback if buffer runs dry

---

## Technology Stack

| Component | Technology | Purpose |
|:---|:---|:---|
| Base TTS | Matcha-TTS or Piper | The "human voice" engine |
| VAD | Silero VAD | Low-power voice detection |
| LLM (Cloud) | Gemini 1.5 Flash | The "thinking" brain |
| Conversion | ONNX + CoreMLTools | PC to iPhone bridge |
| iOS Audio | AVAudioEngine + AudioUnit | Real-time playback |
| Buffer | TPCircularBuffer (C) | Glitch-free streaming |

---

## Files We Will Create

```
d:\Rufen\ferrari_tts\
├── models\
│   ├── base_tts.pt           # Original PyTorch model
│   ├── distilled_tts.pt      # Single-voice student
│   ├── distilled_tts.onnx    # ONNX export
│   └── distilled_tts.mlpackage  # CoreML final
├── scripts\
│   ├── test_models.py        # Compare Matcha vs Piper
│   ├── distill_voice.py      # Fine-tune to one voice
│   ├── export_onnx.py        # PyTorch → ONNX
│   └── convert_coreml.py     # ONNX → CoreML
├── ios_app\
│   └── FerrariTTS.xcodeproj  # The iPhone app
└── README.md
```

---

## Next Step

**Phase 1.1:** Download and test Matcha-TTS and Piper on your PC to compare quality and speed. This will determine which "engine" goes into the Ferrari.

---

*Created: 2026-01-22*
