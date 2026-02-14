# PROJECT AXON: Voice Bridge - Handover Log
**Date:** January 4, 2026
**Status:** ✅ Operational (PC Server + iOS Client Connected)

## 📂 Project Structure

1.  **`voice_bridge/` (PC Server)**
    *   `run_system.py`: **Main Server**. Runs the WebSocket (port 8765) and Windows perception loop.
    *   `axon_simple.py`: The "stable core" logic used by `run_system.py`.
    *   `manual_speak.py`: Debug script to manually force the iPhone to speak unique phrases.
    *   `diagnostic.py`: Tests individual PC components (mic, speakers, window detection).
    *   `optic_nerve.py`: Critical perception module (Windows API hooks).

2.  **`axon-voice-expo/` (iOS App)**
    *   `App.js`: **Main iOS Logic**. Handles WebSocket connection (`ws://192.168.1.81:8765`), UI with "Tap to Connect", and Text-to-Speech.
    *   `app.json`: Expo configuration (Bundle ID: `com.axon.voice`).
    *   `eas.json`: Build configuration (set to `simulator: true` to bypass Apple login for builds).

3.  **`.github/workflows/` (CI/CD)**
    *   `build-expo-ipa.yml`: **The Secret Sauce**. This GitHub Action builds the **Unsigned ARM64 IPA** specifically for ESign/Sideloading. It uses `macos-15` (Xcode 16) and Node 20.

---

## 🧠 Logic & Architecture

**The Loop:**
1.  **Perception:** `run_system.py` polls the active window every 100ms.
2.  **Decision:** If the window changes (e.g., Chrome -> VS Code), it selects a template phrase ("Back to coding").
3.  **Transport:** It sends a JSON message `{"type": "speak", "text": "..."}` via WebSocket.
4.  **Reaction:** The iPhone (`App.js`) receives the message and uses native TTS (`expo-speech`) to say it.

**Why Unsigned IPA?**
*   We wanted to avoid paying $99/year for an Apple Developer Account.
*   We used **GitHub Actions** to build the app in the cloud.
*   The resulting `.ipa` is "unsigned", which allows **ESign** (on the iPhone with a cert) to sign it locally and install it.

---

## 🛠 Troubleshooting History & Solutions

### 1. The "Simulator Build" Crash
*   **Error:** App installed but crashed instantly on launch.
*   **Cause:** We initially built for the iOS Simulator (x86 architecture) to avoid Apple login prompts. iPhones use ARM64.
*   **Solution:** Switched to GitHub Actions to run `npx expo prebuild` and `xcodebuild` with `sdk iphoneos` (ARM64), creating a proper device build.

### 2. The "Missing Artifact"
*   **Error:** GitHub Action succeeded but no IPA data was found.
*   **Cause:** The IPA was created in `axon-voice-expo/` but the uploader looked in `axon-voice-expo/build/`.
*   **Solution:** Updated the workflow to point to the correct path.

### 3. Node.js Version Error
*   **Error:** `TypeError: configs.toReversed is not a function`.
*   **Cause:** GitHub Actions `macos-15` runner used Node 18. New React Native requires Node 20+.
*   **Solution:** Forced `node-version: 20` in the workflow.

---

## 🚀 How to Run on New Machine

### 1. Setup PC Server
```bash
cd voice_bridge
pip install -r requirements.txt  # If needed (websockets, psutil, pywin32)
python run_system.py
```

### 2. Modify IP Address
If your new PC has a different IP than `192.168.1.81`:
1.  Edit `axon-voice-expo/App.js`: Change `SERVER_URL`.
2.  Commit & Push to GitHub.
3.  Wait for **GitHub Actions** to build a new IPA.
4.  Download & Sideload update.

### 3. Debugging
*   **No Audio?** Check PC logs. If you see `[AXON] Client connected`, connection is good.
*   **Run Manual Test:** `python manual_speak.py` to force a message.
*   **Firewall:** Ensure port **8765** is open (`netsh advfirewall...`).

---
**Enjoy your bespoke AI companion.**
