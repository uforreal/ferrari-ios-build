# Project Antigravity — Ferrari Voice Engine

**Current Version:** Phase 4 (Real Device Integration)

The **Ferrari Voice Engine** is the iOS frontend for Project Antigravity, a sovereign, local-first AI architecture. It implements a "Split-Brain" design where the iPhone handles sensory input/output (Voice/Hearing) and a local PC handles heavy cognitive processing (The Brain).

## 🏗 Architecture

```mermaid
graph LR
    User((User)) <-->|Voice| iPhone[Ferrari iOS Client]
    iPhone <-->|WebSocket (WiFi)| PC[Orchestrator]
    PC <-->|IPC| Brain[Sovereign Core]
    PC <-->|Subprocess| RAE[Rational Analysis Engine]
```

### 📱 iPhone Client (The Talker)
- **Role:** Sensory Interface & formatting.
- **Tech Stack:** Swift, SwiftUI, ONNX Runtime (C++), `Speech.framework`.
- **Components:**
  - **BouncerVAD:** Voice Activity Detection (silero-vad).
  - **SpeechTranscriber:** On-device Speech-to-Text (`SFSpeechRecognizer`).
  - **TalkerClient:** WebSocket manager with auto-reconnect & heartbeat.
  - **ServiceDiscovery:** Bonjour/mDNS (`_antigravity._tcp`) locator.
  - **FerrariEngine:** Neural TTS (Kokoro-82M via ONNX).
  - **ConversationManager:** Manages the loop: Listen → Transcribe → Send → Receive VKP → Format → Speak.

### 🖥️ PC Server (The Orchestrator)
- **Role:** Cognitive Router & State Manager.
- **Tech Stack:** Node.js, `ws`, `bonjour-service`.
- **Features:**
  - **Traffic Light System:** Enforces serial execution (Read OR Think OR Hunt) to respect hardware constraints.
  - **Semantic Bridge:** Loads 400k GloVe vectors for concept matching (Warm-up on boot).
  - **VKP Dispatch:** Returns raw "Verified Knowledge Packets" to the client.

---

## 🚀 Setup & Usage

### 1. Start the Orchestrator (PC)
The Brain must be running before the client connects.

```bash
cd D:\Brain\Harvester
node orchestrator.js
```
*Wait for the "warm up semantic bridge" to complete (~10s). The server listens on port 9000 and advertises via Bonjour.*

### 2. Build & Sideload the Client (iPhone)
**NOTE:** The iOS app is built as an **UNSIGNED IPA** via GitHub Actions. No Apple Developer account is required.

1.  **Build:** Push to `main`. GitHub Actions runs `XcodeGen` -> `pod install` -> `xcodebuild` -> Packages IPA.
2.  **Download:** Get `Ferrari-unsigned-ipa.zip` from the Actions run artifacts.
3.  **Sideload:** Use **TrollStore** (recommended), AltStore, or Sideloadly to install `Ferrari-unsigned.ipa` on your device.
4.  **Trust:** Settings → General → VPN & Device Management (if required).

### 3. Run
1.  Ensure iPhone and PC are on the **same WiFi network**.
2.  Open **Ferrari** on iPhone.
3.  Grant Microphone and Speech Recognition permissions.
4.  The app will auto-discover the Orchestrator (`found at <IP>:9000`).
5.  **Speak.**

---

## 🧠 Key Features

- **Verified Knowledge:** Responses are based on "Verified Knowledge Packets" (VKP) containing a trust score and proof chain.
- **Rich Personalities:** The client formats VKP data into natural language based on trust (e.g., "I'm confident that..." vs "This is speculative...").
- **User State Model:** Tracks engagement, emotion, and expertise to tailor responses (Uhud/Ibrahim principles).
- **Zero-Cloud Dependency (Runtime):**
  - STT: On-device.
  - TTS: On-device.
  - Brain: Local Node.js.
  - *Note: Build process uses GitHub Actions (Cloud), but runtime is local.*

## 📂 Project Structure
- `D:\Rufen\ferrari_tts\ios_code`: iOS Source (Code, Resources, Project.yml).
- `D:\Brain\Harvester`: Orchestrator & Sovereign Core.
- `D:\Brain\Harvester\assemblies`: Knowledge Graph storage.

## ⚠️ Known Constraints
- **Serial Execution:** The Brain cannot Think and Read at the same time. The Orchestrator queues requests.
- **Warm-up:** First boot takes ~10-15s to load embedding vectors.
- **Network:** Strictly local WiFi. No remote access implemented.

## License
Proprietary. Project Antigravity.
