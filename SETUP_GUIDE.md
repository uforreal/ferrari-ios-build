# 🚀 Project AXON: Setup Guide

Complete setup guide for testing the Voice Bridge system.

---

## Step 1: PC Setup (Python Server)

### Prerequisites
```bash
pip install websockets python-dotenv google-generativeai
```

### Configuration

1. **Get your PC's local IP address:**
   ```bash
   # Windows PowerShell
   ipconfig
   # Look for "IPv4 Address" under your WiFi/Ethernet adapter
   # Example: 192.168.1.100
   ```

2. **Create `.env` file:**
   ```bash
   cd voice_bridge
   cp .env.example .env
   ```

3. **Edit `.env`** and add your **NEW** Gemini API key:
   ```
   GEMINI_API_KEY=your_new_api_key_here
   ```

   > ⚠️ Get a new key from: https://aistudio.google.com/app/apikey

---

## Step 2: iPhone Setup (Flutter App)

### Prerequisites
- iPhone connected via USB OR on same WiFi as PC
- Flutter installed

### Configuration

1. **Update server IP in `main.dart`:**
   ```bash
   cd voice_app
   ```

   Open `lib/main.dart` and find line ~48:
   ```dart
   serverUrl: 'ws://192.168.1.100:8765',  // Replace with YOUR PC IP
   ```

   Replace `192.168.1.100` with your actual PC IP from Step 1.

2. **Install dependencies:**
   ```bash
   flutter pub get
   ```

3. **Run on iPhone:**
   ```bash
   flutter run
   ```

   If you have multiple devices, select your iPhone when prompted.

---

## Step 3: Start the System

### On PC:

```bash
cd voice_bridge
python run_system.py
```

You should see:
```
╔═══════════════════════════════════════════════════════════╗
║   PROJECT AXON: Voice Bridge v1.0                        ║
╚═══════════════════════════════════════════════════════════╝

[AXON] Starting Perception Layer...
AXON Server (RAMEN Transport)
Listening on ws://0.0.0.0:8765
```

### On iPhone:

The app should auto-connect. You'll see:
- Green "CONNECTED TO PC" indicator
- Current context updates as you switch apps

---

## Step 4: Test the System

### Test 1: Basic Push
1. On PC, switch to **Chrome** or **Arc**
2. iPhone should speak: *"Switched to research mode."*

### Test 2: Dead Reckoning (Ctrl+S)
1. On PC, open **Antigravity** (this IDE)
2. Press **Ctrl+S**
3. iPhone should speak: *"Code saved. Ready to build?"*
4. Check PC console - should say: `[AXON] → Pushed: Code saved...`

### Test 3: Hex Change (Dev → Research)
1. Switch from **cmd.exe** to **Chrome**
2. iPhone should detect the context shift (different hexagons)

### Test 4: Flow Mode (Silence)
1. Stay in one app for 5+ minutes
2. System should stop pushing (Flow Mode activated)

---

## Troubleshooting

### iPhone Can't Connect

**Problem:** "DISCONNECTED" status

**Solutions:**
1. Check PC IP address is correct in `main.dart`
2. Ensure PC and iPhone on same WiFi network
3. Check firewall isn't blocking port 8765:
   ```bash
   # Windows: Allow port 8765
   netsh advfirewall firewall add rule name="AXON" dir=in action=allow protocol=TCP localport=8765
   ```

### No Voice Output

**Problem:** iPhone connects but doesn't speak

**Solutions:**
1. Check iPhone volume is turned up
2. Check "Silent Mode" switch on iPhone (should be OFF)
3. In Flutter app, check console logs for TTS errors

### PC Console Errors

**Problem:** `ModuleNotFoundError: No module named 'websockets'`

**Solution:**
```bash
pip install websockets python-dotenv google-generativeai
```

**Problem:** `ImportError: cannot import name 'WindowMap'`

**Solution:** Ensure `optic_nerve.py` was copied correctly:
```bash
# Re-copy if needed
copy "c:\Users\HW\.gemini\antigravity\playground\azimuthal-expanse\v3_extracted\optic_nerve.py" "voice_bridge\optic_nerve.py"
```

---

## Architecture Flow (For Reference)

```
PC (You switch to Chrome)
  ↓
Optic Nerve detects: "chrome.exe in focus"
  ↓
Fireball decides: "Hex changed (DEV → RESEARCH), priority=75, PUSH"
  ↓
IPA Gateway enriches: "Switched to research mode."
  ↓
AXON Server broadcasts via WebSocket
  ↓
iPhone receives message
  ↓
Dead Reckoner checks patterns (85% confidence match)
  ↓
TTS speaks: "Research mode active."
```

---

## Next Steps (Phase 5)

After confirming basic functionality:
1. Test all hexagon transitions
2. Verify Dead Reckoner confidence scoring
3. Test LLM fallback for unknown apps
4. Test reconnection (turn off/on WiFi)
5. Measure token savings (compare LLM calls vs local predictions)

---

**Questions?** Check console logs on both PC and iPhone for detailed debug info.
