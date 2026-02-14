# RVC Setup Guide for Samantha Voice Pipeline

## Overview

RVC (Retrieval-based Voice Conversion) allows us to "skin" the base TTS output with a custom voice model, making Samantha sound human rather than robotic.

Because `rvc-python` requires Python 3.10 and specific dependencies (numpy<=1.25, torch with CUDA), we run it as a **separate API server** that our main AXON system calls.

---

## Quick Setup (Recommended)

### Step 1: Create a Python 3.10 Virtual Environment

You need Python 3.10 installed. Download from: https://www.python.org/downloads/release/python-31011/

```powershell
# Create RVC environment
py -3.10 -m venv C:\samantha-rvc\venv

# Activate it
C:\samantha-rvc\venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip
```

### Step 2: Install RVC Python

```powershell
# Still in the activated venv
pip install rvc-python

# FOR GPU SUPPORT (NVIDIA):
pip install torch==2.1.1+cu118 torchaudio==2.1.1+cu118 --index-url https://download.pytorch.org/whl/cu118
```

### Step 3: Download a Voice Model

You need a `.pth` model file. Options:

1. **Train your own** using RVC WebUI (10-30 min of clean audio)
2. **Download pre-trained models** from:
   - https://huggingface.co/models?search=rvc
   - https://voice-models.com/

Place the model file in `C:\samantha-rvc\models\`

### Step 4: Start the RVC API Server

```powershell
# In the RVC venv
python -m rvc_python api -p 5050 -l

# -p 5050 = port 5050
# -l = listen on all interfaces
```

The server should start and show available models.

### Step 5: Test the Connection

In a new terminal, run:

```powershell
cd C:\Users\HW\.gemini\antigravity\playground\azimuthal-expanse
python rvc_converter.py
```

If connected, you should see:

```
[RVC] API server connected at http://localhost:5050
[RVC] Available models: [...]
```

---

## Usage in AXON

Once the RVC API is running, the VoiceEngine will automatically detect it:

```python
from voice_engine import VoiceEngine

ve = VoiceEngine(use_rvc=True)
ve.speak("[soft] Hello there", apply_rvc=True)  # Uses RVC conversion
```

---

## Training Your Own Voice Model

For the authentic "Samantha" voice, you'll want to train a custom model:

1. **Collect 10-30 minutes of clean audio** from your target voice

   - No background noise
   - Consistent volume
   - Varied sentences (not just repeated phrases)

2. **Use RVC WebUI for training:**

   ```powershell
   # Clone the official RVC repo
   git clone https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI.git
   cd Retrieval-based-Voice-Conversion-WebUI

   # Install dependencies (in Python 3.10 venv)
   pip install -r requirements.txt

   # Run WebUI
   python infer-web.py
   ```

3. **Training steps in WebUI:**

   - Upload your audio files
   - Extract features
   - Train the model (usually 20-50 epochs)
   - Export the `.pth` file

4. **Copy the trained model** to your RVC models folder

---

## Troubleshooting

### "API not available" error

- Make sure the RVC API server is running in a separate terminal
- Check if port 5050 is blocked by firewall
- Try: `curl http://localhost:5050/models`

### CUDA errors

- Ensure NVIDIA drivers are updated
- Try CPU mode: `pip install torch torchaudio` (without CUDA)

### Model not loading

- Verify the .pth file is not corrupted
- Check model is compatible with your RVC version

---

## File Locations

```
C:\samantha-rvc\
├── venv\                    # Python 3.10 virtual environment
├── models\                  # Voice model .pth files
│   └── samantha_v1.pth     # Your trained model
└── logs\                    # Training logs (if using WebUI)

C:\Users\HW\.gemini\antigravity\playground\azimuthal-expanse\
├── rvc_converter.py         # RVC integration layer
├── voice_engine.py          # TTS + RVC pipeline
├── thalamus_engine.py       # Presence engine
├── thalamus_codec.json      # Presence rules
└── axon_server.py           # Main server
```
