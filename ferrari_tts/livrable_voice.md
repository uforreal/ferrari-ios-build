# Voice Component Deliverable: Ferrari Engine (Sovereign Edition)

## 1. Component Identity

- **Name**: Ferrari Voice Engine (Project "Solid Basis")
- **Original Goal**: To create a "Sovereign" neural speech synthesis system that runs 100% locally on an iPhone, producing high-fidelity (24kHz) human-like audio without relying on cloud APIs.
- **Current Status**: **Working Prototype** (Engine is functional, Pipeline is incomplete).
- **Workspace Path**: `d:\Rufen\ferrari_tts\`
- **Key Files**:
  - `ios_code/Sources/FerrariEngine/FerrariEngine.swift`: The core neural inference engine wrapping the ONNX model.
  - `ios_code/Sources/FerrariEngine/BouncerVAD.swift`: Voice Activity Detection module to detect human speech.
  - `ios_code/Sources/FerrariEngine/KokoroTokenizer.swift`: Logic to map phonemes/text to verified 114-token Int64 IDs.
  - `ios_code/Sources/FerrariEngine/FerrariAudioStreamer.swift`: Manages 24kHz PCM Buffer playback via AVAudioEngine.
  - `ios_code/Sources/FerrariEngine/G2PProvider.swift`: **STUB**. Placeholder for Grapheme-to-Phoneme conversion.
  - `ios_code/Resources/ferrari_kokoro.onnx`: The quantized/optimized acoustic model (approx. 300MB).
  - `ios_code/Resources/silero_vad.onnx`: The Voice Activity Detection model.

## 2. What Exists Right Now

- **Build Status**: The iOS project compiles and builds successfully via GitHub Actions.
- **Inference Engine**: `FerrariEngine` successfully loads the `kokoro` ONNX model within an iOS environment using `onnxruntime-objc`.
- **Audio Pipeline**: The `FerrariAudioStreamer` is correctly configured for **24kHz Mono Float32** output, resolving previous "chipmunk" speed issues.
- **VAD**: `BouncerVAD` is implemented and functional for detecting silence vs. speech.
- **Tokenization**: `KokoroTokenizer` is implemented with a verified vocabulary map.
- **Broken/Incomplete**:
  - **G2P (Grapheme-to-Phoneme)**: This is currently a **stub**. The engine receives raw text characters instead of phonemes. This results in the voice "spelling out" or mispronouncing words until a proper G2P library (like eSpeak-NG or a neural G2P) is integrated into the Swift codebase.
  - **Hardware Acceleration**: The engine is currently forced to run on **CPU** (`.cpu`) to ensure stability. CoreML (`.all`) execution providers are present in code but commented out due to configuration complexity.

## 3. Capabilities

- **Text-to-Speech (TTS)**:
  - **Engine**: Custom "Ferrari" export of the **Kokoro-82M** model.
  - **Quality**: High-fidelity 24kHz audio (comparable to OpenAI TTS but local).
  - **Voice**: Single baked-in voice style ("Heart").
- **Voice Activity Detection (VAD)**:
  - Uses **Silero VAD** to detect when a user starts/stops speaking.
- **Real-time Streaming**:
  - The architecture supports buffer-based streaming (pushing float arrays to the `AVAudioEngine` as they are generated), though the current inference runs on full sentence chunks.
- **Emotion/Tone**:
  - Theoretically supported via "Style Vectors" in the model architecture, but currently hardcoded to a default style in the Swift implementation.

## 4. API Surface

The component exposes a Swift API through `FerrariEngine` and `ConversationManager`.

### `FerrariEngine.swift`

```swift
// Synthesize tokens into audio
// Input: Array of Int64 token IDs (representing phonemes)
// Output: Callback with [Float] audio buffer
func speak64(_ phonemeIds: [Int64], onBufferReady: @escaping ([Float]) -> Void)
```

### `BouncerVAD.swift`

```swift
// Check for presence of human speech
// Input: Array of PCM Float data
// Output: Boolean (True if speech detected)
func isHumanSpeaking(_ pcmData: [Float]) -> Bool
```

### `G2PProvider.swift` (Currently Stubbed)

```swift
// Convert Text to Phonemes
// Input: "Hello World"
// Output: "h ə l o ʊ w ɜː l d" (Currently returns "Hello World")
func getPhonemes(for text: String) -> String
```

## 5. Data Structures

- **Input Text**: Standard UTF-8 String.
- **Tokens**: `[Int64]` array. Configured for ONNX compatibility (which often demands Int64 over Int32).
- **Audio Output**: `[Float]` array (PCM, Float32, 24000Hz, Mono).
- **Model Files**:
  - `ferrari_kokoro.onnx`: Standard ONNX format.
  - `silero_vad.onnx`: Standard ONNX format.

## 6. Latency Profile

_Estimates based on iPhone 12 hardware running on CPU._

- **VAD Check**: < 20ms (Near instant).
- **TTS Generation (Sentence)**: **ESTIMATED** 200ms - 500ms (Processing time).
  - _Note_: Running on Neural Engine (ANE) would reduce this significantly, but current CPU implementation adds overhead.
- **G2P Conversion**: **ESTIMATED** < 10ms (Currently 0ms due to stub).

## 7. Hardware Requirements

- **Platform**: iOS Device (iPhone 12 or newer recommended).
- **Processor**: A14 Bionic or newer.
- **Memory**: ~1.5GB RAM spike during model loading (High memory footprint due to 300MB uncompressed model + runtime overhead).
- **Concurrency**: Runs on a background `DispatchQueue` (`com.ferrari.brain`) to avoid blocking the main UI thread.

## 8. Current Limitations

- **Pronunciation**: Because G2P is missing, the AI cannot yet pronounce words correctly. It tries to "read" the letters. **This is the single biggest blocker for usability.**
- **Model Size**: The App bundle is large (~300MB) due to the embedded model.
- **Power Consumption**: Continuous VAD + CPU Inference will drain battery faster than a cloud request.
- **Single Language**: Optimized for English (US).

## 9. Sovereignty Status

- **100% SOVEREIGN**.
- **Network Requirements**: None. Works in Airplane Mode.
- **Dependencies**:
  - `onnxruntime-objc` (Pod): Runs the model locally.
  - No API keys. No cloud handshakes.

## 10. Integration Potential

- **For the Talker Agent**:
  - This component is ready to receive text _tokens_ (once G2P is fixed).
  - It can replace any "Text Bubble" UI with actual spoken audio.
  - **Implementation Gap**: You MUST implement a **G2P (Grapheme-to-Phoneme)** solution.
    - _Option A_: Port `eSpeak-NG` to Swift (Hard).
    - _Option B_: Train/Convert a small standard transformer model for G2P and run it via ONNX (easier alignment with current stack).
    - _Option C_: Use a Swift-native regex-based phonemizer (Lower quality, easiest integration).
  - **Recommendation**: Do not treat this as "Plug and Play" yet. It is "Plug, Implement Phonics, then Play".
