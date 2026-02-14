<think>The user has brilliantly broken down the human voice into 7 layers, from pure physics to narrative/identity. Now they want to:

1. Build a decoder that extracts each layer from audio input
2. Integrate this with the existing system (CORTEX, THALAMUS, VERIFICATION LAYER)

This is essentially building a "voice understanding" pipeline that goes far beyond simple speech-to-text (which only captures Layer 4).

Let me design this DECODER system:

Layer 0 - Physical: Use signal processing (FFT, spectrograms)
Layer 1 - Biological: Voice analysis (fundamental frequency, formants, jitter/shimmer)
Layer 2 - Prosody: Pitch contours, energy patterns, pause detection
Layer 3 - Phonetic: Phoneme recognition, accent detection
Layer 4 - Language: ASR (Automatic Speech Recognition)
Layer 5 - Semantics: Intent parsing, proposition extraction
Layer 6 - Pragmatics: Context analysis, sarcasm detection, social cues
Layer 7 - Identity: Speaker profiling, credibility assessment (most uncertain)

The key insight is that each layer has different confidence levels:
- Layer 0-2: High confidence (physics/biology)
- Layer 3-4: Medium confidence (convention)
- Layer 5-7: Low confidence (interpretation)

And importantly, higher layers should NOT override lower layers. If Layer 2 says "stressed/angry" but Layer 4 words say "I'm fine", the system should note the discrepancy.

This creates a rich understanding of the input that goes into CORTEX, not just text.

Let me design this architecture.</think>You've mapped the voice like a geologist maps earth. Layers. Each with different truth density.

Now we build the **DECODER** — a system that peels the voice layer by layer and outputs structured understanding, not just text.

---

## THE DECODER

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                                DECODER                                      │
│                        (Voice Stratification Engine)                        │
│                                                                             │
│   Audio In ──────────────────────────────────────────────────────────────▶ │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │ LAYER 0: PHYSICAL          Confidence: 1.0 (HAQ)                    │  │
│   │ FFT, spectrogram, waveform                                          │  │
│   │ Output: frequencies[], amplitude[], harmonics[], noise_floor        │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                              ↓                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │ LAYER 1: BIOLOGICAL        Confidence: 0.9 (HAQ-adjacent)           │  │
│   │ Formants, jitter, shimmer, F0                                       │  │
│   │ Output: age_range, sex_estimate, fatigue, arousal, health_flags     │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                              ↓                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │ LAYER 2: PROSODY           Confidence: 0.85                         │  │
│   │ Pitch contour, rhythm, pauses, emphasis                             │  │
│   │ Output: emotion_state, question_vs_statement, confidence_level,     │  │
│   │         sincerity_estimate, urgency                                 │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                              ↓                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │ LAYER 3: PHONETIC          Confidence: 0.8                          │  │
│   │ Phoneme sequence, syllable timing, accent markers                   │  │
│   │ Output: phonemes[], accent_profile, dialect_estimate, speech_rate   │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                              ↓                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │ LAYER 4: LANGUAGE          Confidence: 0.75 (URF)                   │  │
│   │ ASR, tokenization, grammar parse                                    │  │
│   │ Output: transcript, tokens[], syntax_tree, language_detected        │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                              ↓                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │ LAYER 5: SEMANTICS         Confidence: 0.6 (SHAHADA-like)           │  │
│   │ Intent parsing, proposition extraction                              │  │
│   │ Output: intent, propositions[], claims[], questions[], commands[]   │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                              ↓                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │ LAYER 6: PRAGMATICS        Confidence: 0.4 (interpretation)         │  │
│   │ Context analysis, implicature, social signals                       │  │
│   │ Output: sarcasm_flag, politeness_level, threat_level,              │  │
│   │         hidden_request, power_dynamic                               │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                              ↓                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │ LAYER 7: IDENTITY          Confidence: 0.2 (projection)             │  │
│   │ Speaker profiling, credibility heuristics                           │  │
│   │ Output: authority_estimate, credibility_flags, group_signals        │  │
│   │ ⚠️ WARNING: This layer lies. Use minimally. Verify with action.    │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│   ══════════════════════════════════════════════════════════════════════   │
│                                                                             │
│   CONFLICT DETECTOR                                                        │
│   Flags when layers contradict:                                            │
│   - Layer 2 says "stressed" + Layer 4 says "I'm fine" → INCONGRUENCE      │
│   - Layer 1 says "fatigue" + Layer 5 says "I'm energized" → FLAG          │
│                                                                             │
│   Lower layers have VETO POWER over higher layer interpretations           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## The Output Schema

```json
{
  "meta": {
    "timestamp": "2025-01-07T08:39:00Z",
    "audio_duration_ms": 3400,
    "sample_rate": 44100,
    "decoder_version": "1.0"
  },

  "layer_0_physical": {
    "confidence": 1.0,
    "truth_type": "HAQ",
    "data": {
      "dominant_frequencies": [120, 240, 360, 480],
      "fundamental_frequency": 120.4,
      "amplitude_envelope": [0.2, 0.4, 0.6, 0.5, 0.3],
      "noise_floor_db": -45,
      "signal_to_noise": 32,
      "clipping_detected": false,
      "duration_ms": 3400
    }
  },

  "layer_1_biological": {
    "confidence": 0.9,
    "truth_type": "HAQ",
    "data": {
      "estimated_sex": "male",
      "sex_confidence": 0.92,
      "estimated_age_range": [25, 35],
      "age_confidence": 0.7,
      "vocal_fatigue": 0.3,
      "emotional_arousal": 0.6,
      "stress_markers": 0.45,
      "breath_pattern": "shallow_rapid",
      "health_flags": []
    }
  },

  "layer_2_prosody": {
    "confidence": 0.85,
    "truth_type": "HAQ_ADJACENT",
    "data": {
      "emotion_primary": "frustrated",
      "emotion_confidence": 0.75,
      "emotion_secondary": "tired",
      "pitch_contour": "falling_then_rising",
      "speech_rate": "fast",
      "pause_pattern": [
        {"position_ms": 1200, "duration_ms": 400, "type": "hesitation"},
        {"position_ms": 2800, "duration_ms": 200, "type": "breath"}
      ],
      "emphasis_words_positions": [2, 7],
      "question_intonation": false,
      "confidence_in_speech": 0.4,
      "sincerity_estimate": 0.7,
      "urgency": 0.65
    }
  },

  "layer_3_phonetic": {
    "confidence": 0.8,
    "truth_type": "URF",
    "data": {
      "phonemes": ["aɪ", "k", "æ", "n", "t", "f", "ɪ", "ɡ", "j", "ər"],
      "syllable_count": 8,
      "accent_profile": "american_midwest",
      "accent_confidence": 0.6,
      "dialect_markers": ["rhotic_r", "caught_cot_merged"],
      "speech_rate_syllables_per_sec": 4.2,
      "articulation_precision": 0.85
    }
  },

  "layer_4_language": {
    "confidence": 0.75,
    "truth_type": "URF",
    "data": {
      "transcript": "I can't figure out why this keeps failing",
      "tokens": ["I", "can't", "figure", "out", "why", "this", "keeps", "failing"],
      "language": "en",
      "grammar_valid": true,
      "syntax_tree": {
        "type": "statement",
        "subject": "I",
        "verb_phrase": "can't figure out",
        "object_clause": "why this keeps failing"
      },
      "asr_alternatives": [
        {"text": "I can't figure out why this keeps failing", "confidence": 0.92},
        {"text": "I can't figure out why this keeps fading", "confidence": 0.06}
      ]
    }
  },

  "layer_5_semantics": {
    "confidence": 0.6,
    "truth_type": "SHAHADA",
    "data": {
      "intent": "express_frustration",
      "secondary_intent": "implicit_request_for_help",
      "propositions": [
        {"statement": "speaker is attempting something", "confidence": 0.9},
        {"statement": "the attempt is failing repeatedly", "confidence": 0.95},
        {"statement": "speaker does not understand cause", "confidence": 0.85}
      ],
      "claims": [],
      "questions": [
        {"implicit": true, "content": "why is this failing?"}
      ],
      "commands": [],
      "domain_hints": ["technical", "debugging", "software_or_mechanical"]
    }
  },

  "layer_6_pragmatics": {
    "confidence": 0.4,
    "truth_type": "INTERPRETATION",
    "data": {
      "sarcasm_detected": false,
      "politeness_level": "neutral",
      "formality": "informal",
      "threat_level": 0.0,
      "hidden_requests": [
        {"request": "help me solve this", "confidence": 0.7},
        {"request": "validate my frustration", "confidence": 0.5}
      ],
      "social_context": "peer_or_assistant",
      "power_dynamic": "speaker_seeking_help",
      "face_threatening_act": false
    },
    "warning": "High interpretation. Verify with follow-up."
  },

  "layer_7_identity": {
    "confidence": 0.2,
    "truth_type": "PROJECTION",
    "data": {
      "perceived_authority": "low_in_current_domain",
      "perceived_credibility": "neutral",
      "group_signals": [],
      "persona_projection": "frustrated_learner"
    },
    "warning": "This layer lies. Do not use for decisions. Verify through action."
  },

  "conflicts": [
    {
      "type": "incongruence",
      "layers": [2, 5],
      "description": "Prosody shows low confidence (0.4), but semantic structure is declarative statement",
      "implication": "Speaker may be masking uncertainty with assertive language"
    }
  ],

  "synthesis": {
    "raw_transcript": "I can't figure out why this keeps failing",
    "decoded_meaning": "Speaker is frustrated and implicitly requesting help with a recurring failure they don't understand",
    "emotional_state": "frustrated + tired",
    "confidence_in_synthesis": 0.65,
    "recommended_response_tone": "supportive + solution_oriented",
    "trust_level": {
      "words": 0.75,
      "emotion": 0.85,
      "intent": 0.6
    }
  }
}
```

---

## The Technical Implementation

### Layer 0-1: Signal Processing

```python
import numpy as np
import librosa
from scipy.signal import find_peaks

class PhysicalDecoder:
    """Layer 0: Pure physics. No interpretation."""
    
    def __init__(self, sample_rate: int = 44100):
        self.sr = sample_rate
    
    def decode(self, audio: np.ndarray) -> dict:
        # FFT for frequency content
        fft = np.fft.fft(audio)
        frequencies = np.fft.fftfreq(len(audio), 1/self.sr)
        magnitudes = np.abs(fft)
        
        # Find dominant frequencies
        peaks, _ = find_peaks(magnitudes[:len(magnitudes)//2], height=np.max(magnitudes)*0.1)
        dominant_freqs = frequencies[peaks][:10].tolist()
        
        # Fundamental frequency (F0)
        f0 = self.estimate_f0(audio)
        
        # Amplitude envelope
        envelope = self.get_envelope(audio)
        
        # Noise floor
        noise_floor = self.estimate_noise_floor(audio)
        
        return {
            "confidence": 1.0,
            "truth_type": "HAQ",
            "data": {
                "dominant_frequencies": dominant_freqs,
                "fundamental_frequency": f0,
                "amplitude_envelope": envelope,
                "noise_floor_db": noise_floor,
                "duration_ms": len(audio) / self.sr * 1000
            }
        }
    
    def estimate_f0(self, audio: np.ndarray) -> float:
        f0, _, _ = librosa.pyin(audio, fmin=50, fmax=500, sr=self.sr)
        return float(np.nanmedian(f0))
    
    def get_envelope(self, audio: np.ndarray, window: int = 1024) -> list:
        envelope = np.array([
            np.max(np.abs(audio[i:i+window])) 
            for i in range(0, len(audio), window)
        ])
        # Normalize and downsample for storage
        envelope = envelope / np.max(envelope)
        return envelope[::10].tolist()
    
    def estimate_noise_floor(self, audio: np.ndarray) -> float:
        # Find quietest 10% of signal
        sorted_amp = np.sort(np.abs(audio))
        noise_sample = sorted_amp[:len(sorted_amp)//10]
        rms = np.sqrt(np.mean(noise_sample**2))
        return float(20 * np.log10(rms + 1e-10))


class BiologicalDecoder:
    """Layer 1: What the body reveals."""
    
    def __init__(self, sample_rate: int = 44100):
        self.sr = sample_rate
    
    def decode(self, audio: np.ndarray, layer_0: dict) -> dict:
        f0 = layer_0['data']['fundamental_frequency']
        
        # Sex estimation from F0
        sex, sex_conf = self.estimate_sex(f0)
        
        # Age estimation from voice characteristics
        age_range, age_conf = self.estimate_age(audio, f0)
        
        # Jitter and shimmer (voice stability)
        jitter = self.calculate_jitter(audio)
        shimmer = self.calculate_shimmer(audio)
        
        # Emotional arousal from voice variation
        arousal = self.estimate_arousal(audio)
        
        # Fatigue markers
        fatigue = self.estimate_fatigue(jitter, shimmer, f0)
        
        # Stress from voice tension
        stress = self.estimate_stress(audio, f0)
        
        return {
            "confidence": 0.9,
            "truth_type": "HAQ",
            "data": {
                "estimated_sex": sex,
                "sex_confidence": sex_conf,
                "estimated_age_range": age_range,
                "age_confidence": age_conf,
                "vocal_fatigue": fatigue,
                "emotional_arousal": arousal,
                "stress_markers": stress,
                "jitter": jitter,
                "shimmer": shimmer
            }
        }
    
    def estimate_sex(self, f0: float) -> tuple:
        # Male F0: 85-180 Hz, Female F0: 165-255 Hz
        if f0 < 150:
            return "male", min(0.95, (150 - f0) / 65 + 0.5)
        elif f0 > 180:
            return "female", min(0.95, (f0 - 180) / 75 + 0.5)
        else:
            # Ambiguous zone
            return "uncertain", 0.5
    
    def estimate_age(self, audio: np.ndarray, f0: float) -> tuple:
        # Simplified: voice characteristics change with age
        # Young: higher F0, more stable
        # Old: lower F0, more jitter/shimmer
        jitter = self.calculate_jitter(audio)
        
        if jitter < 0.01 and f0 > 150:
            return [18, 30], 0.6
        elif jitter < 0.02:
            return [25, 45], 0.5
        else:
            return [40, 70], 0.5
    
    def calculate_jitter(self, audio: np.ndarray) -> float:
        # Pitch period variation
        f0, voiced_flag, _ = librosa.pyin(audio, fmin=50, fmax=500, sr=self.sr)
        f0_clean = f0[~np.isnan(f0)]
        if len(f0_clean) < 2:
            return 0.0
        periods = 1 / f0_clean
        jitter = np.mean(np.abs(np.diff(periods))) / np.mean(periods)
        return float(jitter)
    
    def calculate_shimmer(self, audio: np.ndarray) -> float:
        # Amplitude variation between cycles
        envelope = np.abs(librosa.effects.preemphasis(audio))
        peaks, _ = find_peaks(envelope, distance=50)
        if len(peaks) < 2:
            return 0.0
        peak_amps = envelope[peaks]
        shimmer = np.mean(np.abs(np.diff(peak_amps))) / np.mean(peak_amps)
        return float(shimmer)
    
    def estimate_arousal(self, audio: np.ndarray) -> float:
        # High arousal: more variation, higher energy, faster changes
        rms = librosa.feature.rms(y=audio)[0]
        rms_var = np.std(rms) / (np.mean(rms) + 1e-10)
        return float(min(1.0, rms_var * 2))
    
    def estimate_fatigue(self, jitter: float, shimmer: float, f0: float) -> float:
        # Fatigue: higher jitter/shimmer, lower F0
        fatigue_score = (jitter * 10 + shimmer * 5) / 2
        return float(min(1.0, fatigue_score))
    
    def estimate_stress(self, audio: np.ndarray, f0: float) -> float:
        # Stress: higher F0, more tension, faster speech
        f0_series, _, _ = librosa.pyin(audio, fmin=50, fmax=500, sr=self.sr)
        f0_clean = f0_series[~np.isnan(f0_series)]
        if len(f0_clean) < 2:
            return 0.0
        f0_range = np.max(f0_clean) - np.min(f0_clean)
        return float(min(1.0, f0_range / 100))
```

### Layer 2: Prosody

```python
class ProsodyDecoder:
    """Layer 2: Pre-semantic emotional signals."""
    
    def __init__(self, sample_rate: int = 44100):
        self.sr = sample_rate
    
    def decode(self, audio: np.ndarray, layer_0: dict, layer_1: dict) -> dict:
        # Pitch contour analysis
        pitch_contour = self.analyze_pitch_contour(audio)
        
        # Pause detection
        pauses = self.detect_pauses(audio)
        
        # Speech rate
        speech_rate = self.estimate_speech_rate(audio)
        
        # Emphasis detection
        emphasis = self.detect_emphasis(audio)
        
        # Emotion from prosody
        emotion = self.classify_emotion(
            pitch_contour, 
            speech_rate, 
            layer_1['data']['emotional_arousal'],
            layer_1['data']['stress_markers']
        )
        
        # Question vs statement
        is_question = self.detect_question_intonation(audio)
        
        # Confidence in speech
        confidence = self.estimate_speaker_confidence(pitch_contour, pauses)
        
        # Sincerity estimate
        sincerity = self.estimate_sincerity(audio, layer_1)
        
        return {
            "confidence": 0.85,
            "truth_type": "HAQ_ADJACENT",
            "data": {
                "emotion_primary": emotion['primary'],
                "emotion_confidence": emotion['confidence'],
                "emotion_secondary": emotion.get('secondary'),
                "pitch_contour": pitch_contour['shape'],
                "speech_rate": speech_rate,
                "pause_pattern": pauses,
                "emphasis_positions": emphasis,
                "question_intonation": is_question,
                "confidence_in_speech": confidence,
                "sincerity_estimate": sincerity,
                "urgency": self.estimate_urgency(speech_rate, layer_1['data']['stress_markers'])
            }
        }
    
    def analyze_pitch_contour(self, audio: np.ndarray) -> dict:
        f0, _, _ = librosa.pyin(audio, fmin=50, fmax=500, sr=self.sr)
        f0_clean = f0[~np.isnan(f0)]
        
        if len(f0_clean) < 10:
            return {"shape": "flat", "values": []}
        
        # Divide into thirds
        third = len(f0_clean) // 3
        start_mean = np.mean(f0_clean[:third])
        mid_mean = np.mean(f0_clean[third:2*third])
        end_mean = np.mean(f0_clean[2*third:])
        
        # Classify shape
        if end_mean > start_mean * 1.1:
            shape = "rising"
        elif end_mean < start_mean * 0.9:
            shape = "falling"
        elif mid_mean > start_mean * 1.1 and mid_mean > end_mean * 1.1:
            shape = "peaked"
        elif mid_mean < start_mean * 0.9 and mid_mean < end_mean * 0.9:
            shape = "valley"
        else:
            shape = "flat"
        
        return {"shape": shape, "start": start_mean, "mid": mid_mean, "end": end_mean}
    
    def detect_pauses(self, audio: np.ndarray) -> list:
        # Find silent regions
        rms = librosa.feature.rms(y=audio, frame_length=512, hop_length=128)[0]
        threshold = np.mean(rms) * 0.3
        
        pauses = []
        in_pause = False
        pause_start = 0
        
        for i, val in enumerate(rms):
            time_ms = i * 128 / self.sr * 1000
            
            if val < threshold and not in_pause:
                in_pause = True
                pause_start = time_ms
            elif val >= threshold and in_pause:
                in_pause = False
                duration = time_ms - pause_start
                if duration > 100:  # Minimum 100ms pause
                    pause_type = "hesitation" if duration > 300 else "breath"
                    pauses.append({
                        "position_ms": pause_start,
                        "duration_ms": duration,
                        "type": pause_type
                    })
        
        return pauses
    
    def detect_question_intonation(self, audio: np.ndarray) -> bool:
        # Rising pitch at end = question
        f0, _, _ = librosa.pyin(audio, fmin=50, fmax=500, sr=self.sr)
        f0_clean = f0[~np.isnan(f0)]
        
        if len(f0_clean) < 10:
            return False
        
        # Compare last 20% to previous
        cutoff = int(len(f0_clean) * 0.8)
        end_mean = np.mean(f0_clean[cutoff:])
        before_mean = np.mean(f0_clean[cutoff-10:cutoff])
        
        return end_mean > before_mean * 1.15
    
    def classify_emotion(self, pitch: dict, rate: str, arousal: float, stress: float) -> dict:
        # Simplified emotion classification from prosodic features
        
        if stress > 0.7 and arousal > 0.6:
            return {"primary": "angry", "confidence": 0.7}
        elif stress > 0.5 and pitch['shape'] == "falling":
            return {"primary": "frustrated", "confidence": 0.65, "secondary": "tired"}
        elif arousal < 0.3 and rate == "slow":
            return {"primary": "sad", "confidence": 0.6}
        elif arousal > 0.7 and pitch['shape'] == "rising":
            return {"primary": "excited", "confidence": 0.65}
        elif arousal < 0.4 and stress < 0.3:
            return {"primary": "calm", "confidence": 0.7}
        else:
            return {"primary": "neutral", "confidence": 0.5}
    
    def estimate_speaker_confidence(self, pitch: dict, pauses: list) -> float:
        # Many hesitation pauses = low confidence
        hesitations = len([p for p in pauses if p['type'] == 'hesitation'])
        pause_penalty = min(0.5, hesitations * 0.15)
        
        # Falling pitch = more confident
        pitch_bonus = 0.1 if pitch['shape'] == 'falling' else 0
        
        base = 0.5
        return max(0.1, min(1.0, base - pause_penalty + pitch_bonus))
    
    def estimate_sincerity(self, audio: np.ndarray, layer_1: dict) -> float:
        # Mismatches between content and prosody suggest performance
        # This is imperfect - noted in confidence
        jitter = layer_1['data'].get('jitter', 0)
        
        # Very smooth = possibly rehearsed
        # Some natural variation = more sincere
        if jitter < 0.005:
            return 0.5  # Too smooth, possibly performed
        elif jitter > 0.03:
            return 0.6  # High variation, possibly stressed but genuine
        else:
            return 0.75  # Natural variation
    
    def estimate_speech_rate(self, audio: np.ndarray) -> str:
        # Estimate syllables per second
        onset_env = librosa.onset.onset_strength(y=audio, sr=self.sr)
        tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=self.sr)[0]
        
        # Rough mapping: tempo correlates with speech rate
        if tempo < 80:
            return "slow"
        elif tempo > 140:
            return "fast"
        else:
            return "normal"
    
    def detect_emphasis(self, audio: np.ndarray) -> list:
        # Find amplitude peaks that indicate emphasis
        rms = librosa.feature.rms(y=audio, frame_length=1024, hop_length=256)[0]
        mean_rms = np.mean(rms)
        
        emphasis = []
        for i, val in enumerate(rms):
            if val > mean_rms * 1.5:
                time_ms = i * 256 / self.sr * 1000
                emphasis.append(time_ms)
        
        return emphasis
    
    def estimate_urgency(self, speech_rate: str, stress: float) -> float:
        rate_score = {"slow": 0.2, "normal": 0.5, "fast": 0.8}[speech_rate]
        return (rate_score + stress) / 2
```

### Layer 3-4: Phonetic + Language

```python
import whisper  # Or any ASR

class PhoneticDecoder:
    """Layer 3: Symbol emergence."""
    
    def __init__(self):
        self.phoneme_model = None  # Would load a phoneme recognizer
    
    def decode(self, audio: np.ndarray, layer_0: dict, sr: int = 44100) -> dict:
        # Using librosa for basic phonetic features
        # In production, use a proper phoneme recognizer
        
        # Estimate speech rate in syllables
        onset_env = librosa.onset.onset_strength(y=audio, sr=sr)
        onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
        syllable_rate = len(onsets) / (len(audio) / sr)
        
        # Accent would require a trained classifier
        # Placeholder for structure
        
        return {
            "confidence": 0.8,
            "truth_type": "URF",
            "data": {
                "estimated_syllable_count": len(onsets),
                "speech_rate_syllables_per_sec": syllable_rate,
                "accent_profile": "unknown",  # Requires trained model
                "accent_confidence": 0.0,
                "articulation_precision": self.estimate_articulation(audio, sr)
            }
        }
    
    def estimate_articulation(self, audio: np.ndarray, sr: int) -> float:
        # High frequency content indicates clear articulation
        spec = np.abs(librosa.stft(audio))
        high_freq_energy = np.mean(spec[spec.shape[0]//2:, :])
        total_energy = np.mean(spec)
        return float(min(1.0, high_freq_energy / total_energy * 3))


class LanguageDecoder:
    """Layer 4: Words emerge. Convention truth."""
    
    def __init__(self, model_size: str = "base"):
        self.asr = whisper.load_model(model_size)
    
    def decode(self, audio: np.ndarray, sr: int = 44100) -> dict:
        # Resample to 16kHz for Whisper
        if sr != 16000:
            audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)
        
        # Transcribe
        result = self.asr.transcribe(audio)
        
        transcript = result['text'].strip()
        language = result['language']
        
        # Get word-level timestamps if available
        segments = result.get('segments', [])
        
        # Tokenize
        tokens = transcript.split()
        
        return {
            "confidence": 0.75,
            "truth_type": "URF",
            "data": {
                "transcript": transcript,
                "tokens": tokens,
                "language": language,
                "segments": segments,
                "asr_confidence": self.estimate_asr_confidence(result)
            }
        }
    
    def estimate_asr_confidence(self, result: dict) -> float:
        # Whisper provides segment-level confidence
        if 'segments' in result and result['segments']:
            probs = [s.get('no_speech_prob', 0) for s in result['segments']]
            return 1.0 - np.mean(probs)
        return 0.7
```

### Layer 5-7: Interpretation (Higher uncertainty)

```python
class SemanticDecoder:
    """Layer 5: What speaker tries to convey. Unstable territory."""
    
    def __init__(self):
        self.intent_patterns = {
            "question": ["what", "why", "how", "when", "where", "who", "?"],
            "command": ["do", "make", "create", "stop", "start", "help"],
            "frustration": ["can't", "won't", "failing", "broken", "stuck", "ugh"],
            "request": ["could you", "would you", "can you", "please", "need"],
            "statement": []  # Default
        }
    
    def decode(self, layer_4: dict, layer_2: dict) -> dict:
        transcript = layer_4['data']['transcript'].lower()
        tokens = layer_4['data']['tokens']
        
        # Intent classification
        intent = self.classify_intent(transcript)
        
        # Extract propositions
        propositions = self.extract_propositions(transcript, tokens)
        
        # Detect implicit questions
        implicit_questions = self.detect_implicit_questions(transcript, layer_2)
        
        # Domain hints
        domain_hints = self.detect_domain(transcript)
        
        return {
            "confidence": 0.6,
            "truth_type": "SHAHADA",
            "data": {
                "intent": intent['primary'],
                "intent_confidence": intent['confidence'],
                "secondary_intent": intent.get('secondary'),
                "propositions": propositions,
                "questions": implicit_questions,
                "domain_hints": domain_hints
            }
        }
    
    def classify_intent(self, transcript: str) -> dict:
        scores = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = sum(1 for p in patterns if p in transcript)
            scores[intent] = score
        
        if max(scores.values()) == 0:
            return {"primary": "statement", "confidence": 0.5}
        
        primary = max(scores, key=scores.get)
        confidence = min(0.8, 0.4 + scores[primary] * 0.15)
        
        # Check for secondary intent
        scores[primary] = 0
        secondary = max(scores, key=scores.get) if max(scores.values()) > 0 else None
        
        return {"primary": primary, "confidence": confidence, "secondary": secondary}
    
    def extract_propositions(self, transcript: str, tokens: list) -> list:
        # Simplified proposition extraction
        propositions = []
        
        if "i " in transcript.lower() or "i'" in transcript.lower():
            propositions.append({
                "statement": "speaker references self",
                "confidence": 0.9
            })
        
        if any(word in transcript.lower() for word in ["can't", "won't", "failing", "unable"]):
            propositions.append({
                "statement": "speaker indicates inability or failure",
                "confidence": 0.85
            })
        
        if "?" in transcript:
            propositions.append({
                "statement": "speaker is asking a question",
                "confidence": 0.9
            })
        
        return propositions
    
    def detect_implicit_questions(self, transcript: str, layer_2: dict) -> list:
        questions = []
        
        # Rising intonation but no question mark = implicit question
        if layer_2['data']['question_intonation'] and "?" not in transcript:
            questions.append({
                "implicit": True,
                "content": f"Implicit question in: {transcript}",
                "confidence": 0.6
            })
        
        # "I don't know why X" = implicit "why X?"
        if "don't know why" in transcript.lower() or "can't figure out" in transcript.lower():
            questions.append({
                "implicit": True,
                "content": "Why is this happening?",
                "confidence": 0.7
            })
        
        return questions
    
    def detect_domain(self, transcript: str) -> list:
        domains = []
        
        domain_keywords = {
            "technical": ["error", "code", "bug", "crash", "software", "system"],
            "mechanical": ["broken", "fix", "tool", "machine", "part"],
            "emotional": ["feel", "sad", "happy", "angry", "upset"],
            "creative": ["design", "draw", "create", "build", "make"]
        }
        
        for domain, keywords in domain_keywords.items():
            if any(kw in transcript.lower() for kw in keywords):
                domains.append(domain)
        
        return domains if domains else ["general"]


class PragmaticDecoder:
    """Layer 6: What is actually meant. High interpretation."""
    
    def decode(self, layer_4: dict, layer_5: dict, layer_2: dict, context: dict = {}) -> dict:
        transcript = layer_4['data']['transcript']
        intent = layer_5['data']['intent']
        emotion = layer_2['data']['emotion_primary']
        
        # Sarcasm detection (very imperfect)
        sarcasm = self.detect_sarcasm(transcript, emotion, layer_2)
        
        # Hidden requests
        hidden_requests = self.detect_hidden_requests(transcript, intent, emotion)
        
        # Power dynamic
        power = self.analyze_power_dynamic(transcript, layer_2)
        
        return {
            "confidence": 0.4,
            "truth_type": "INTERPRETATION",
            "data": {
                "sarcasm_detected": sarcasm,
                "hidden_requests": hidden_requests,
                "power_dynamic": power,
                "politeness_level": self.assess_politeness(transcript),
                "formality": self.assess_formality(transcript)
            },
            "warning": "High interpretation. Verify with follow-up."
        }
    
    def detect_sarcasm(self, transcript: str, emotion: str, layer_2: dict) -> bool:
        # Mismatch between words and prosody might indicate sarcasm
        positive_words = ["great", "wonderful", "perfect", "love", "amazing"]
        negative_emotion = emotion in ["frustrated", "angry", "sad"]
        
        has_positive_words = any(w in transcript.lower() for w in positive_words)
        
        return has_positive_words and negative_emotion
    
    def detect_hidden_requests(self, transcript: str, intent: str, emotion: str) -> list:
        requests = []
        
        # Frustration often implies request for help
        if emotion in ["frustrated", "confused"] and "help" not in transcript.lower():
            requests.append({
                "request": "help me solve this",
                "confidence": 0.6
            })
        
        # Statements about inability often seek validation
        if "can't" in transcript.lower() or "unable" in transcript.lower():
            requests.append({
                "request": "validate my struggle",
                "confidence": 0.5
            })
        
        return requests
    
    def analyze_power_dynamic(self, transcript: str, layer_2: dict) -> str:
        confidence = layer_2['data']['confidence_in_speech']
        
        if confidence < 0.4:
            return "speaker_seeking_help"
        elif confidence > 0.7:
            return "speaker_asserting"
        else:
            return "peer_exchange"
    
    def assess_politeness(self, transcript: str) -> str:
        polite_markers = ["please", "thank", "would you", "could you", "sorry"]
        count = sum(1 for m in polite_markers if m in transcript.lower())
        
        if count >= 2:
            return "polite"
        elif count == 1:
            return "neutral"
        else:
            return "direct"
    
    def assess_formality(self, transcript: str) -> str:
        informal_markers = ["gonna", "wanna", "yeah", "yep", "nope", "kinda", "gotta"]
        count = sum(1 for m in informal_markers if m in transcript.lower())
        
        if count >= 2:
            return "informal"
        elif count == 1:
            return "casual"
        else:
            return "neutral"


class IdentityDecoder:
    """Layer 7: Projection layer. THE WEAKEST. Use minimally."""
    
    def decode(self, all_layers: dict) -> dict:
        return {
            "confidence": 0.2,
            "truth_type": "PROJECTION",
            "data": {
                "perceived_authority": "unknown",
                "perceived_credibility": "neutral",
                "group_signals": [],
                "persona_projection": "unknown"
            },
            "warning": "This layer lies. Do not use for decisions. Verify through action only."
        }
```

---

## The Complete Decoder

```python
class Decoder:
    """
    Full voice stratification engine.
    Peels audio layer by layer, outputs structured understanding.
    """
    
    def __init__(self, sample_rate: int = 44100):
        self.sr = sample_rate
        
        # Initialize all decoders
        self.physical = PhysicalDecoder(sample_rate)
        self.biological = BiologicalDecoder(sample_rate)
        self.prosody = ProsodyDecoder(sample_rate)
        self.phonetic = PhoneticDecoder()
        self.language = LanguageDecoder()
        self.semantic = SemanticDecoder()
        self.pragmatic = PragmaticDecoder()
        self.identity = IdentityDecoder()
    
    def decode(self, audio: np.ndarray, context: dict = {}) -> dict:
        """
        Full decode pipeline.
        Each layer builds on previous.
        Lower layers have veto power.
        """
        
        # Layer 0: Physics (HAQ)
        layer_0 = self.physical.decode(audio)
        
        # Layer 1: Biology (HAQ)
        layer_1 = self.biological.decode(audio, layer_0)
        
        # Layer 2: Prosody (HAQ-adjacent)
        layer_2 = self.prosody.decode(audio, layer_0, layer_1)
        
        # Layer 3: Phonetic (URF)
        layer_3 = self.phonetic.decode(audio, layer_0, self.sr)
        
        # Layer 4: Language (URF)
        layer_4 = self.language.decode(audio, self.sr)
        
        # Layer 5: Semantics (SHAHADA)
        layer_5 = self.semantic.decode(layer_4, layer_2)
        
        # Layer 6: Pragmatics (Interpretation)
        layer_6 = self.pragmatic.decode(layer_4, layer_5, layer_2, context)
        
        # Layer 7: Identity (Projection - use minimally)
        layer_7 = self.identity.decode({
            "layer_0": layer_0,
            "layer_1": layer_1,
            "layer_2": layer_2
        })
        
        # Detect conflicts between layers
        conflicts = self.detect_conflicts(layer_2, layer_4, layer_5)
        
        # Synthesize final understanding
        synthesis = self.synthesize(layer_2, layer_4, layer_5, layer_6, conflicts)
        
        return {
            "meta": {
                "timestamp": datetime.utcnow().isoformat(),
                "audio_duration_ms": len(audio) / self.sr * 1000,
                "sample_rate": self.sr,
                "decoder_version": "1.0"
            },
            "layer_0_physical": layer_0,
            "layer_1_biological": layer_1,
            "layer_2_prosody": layer_2,
            "layer_3_phonetic": layer_3,
            "layer_4_language": layer_4,
            "layer_5_semantics": layer_5,
            "layer_6_pragmatics": layer_6,
            "layer_7_identity": layer_7,
            "conflicts": conflicts,
            "synthesis": synthesis
        }
    
    def detect_conflicts(self, layer_2: dict, layer_4: dict, layer_5: dict) -> list:
        """Find contradictions between layers."""
        
        conflicts = []
        
        # Prosody vs Words
        emotion = layer_2['data']['emotion_primary']
        transcript = layer_4['data']['transcript'].lower()
        
        # "I'm fine" + frustrated prosody
        positive_claims = ["fine", "good", "okay", "great", "happy"]
        negative_emotions = ["frustrated", "angry", "sad", "stressed"]
        
        if any(p in transcript for p in positive_claims) and emotion in negative_emotions:
            conflicts.append({
                "type": "incongruence",
                "layers": [2, 4],
                "description": f"Words claim positive state, prosody shows {emotion}",
                "implication": "Possible masking of true emotional state"
            })
        
        # Low confidence prosody + assertive language
        confidence = layer_2['data']['confidence_in_speech']
        assertive_words = ["definitely", "absolutely", "certainly", "always", "never"]
        
        if confidence < 0.4 and any(a in transcript for a in assertive_words):
            conflicts.append({
                "type": "incongruence",
                "layers": [2, 5],
                "description": "Assertive language with low prosodic confidence",
                "implication": "Speaker may be overcompensating for uncertainty"
            })
        
        return conflicts
    
    def synthesize(self, layer_2, layer_4, layer_5, layer_6, conflicts) -> dict:
        """Create final understanding with trust levels."""
        
        transcript = layer_4['data']['transcript']
        emotion = layer_2['data']['emotion_primary']
        intent = layer_5['data']['intent']
        
        # Adjust trust based on conflicts
        word_trust = 0.75
        emotion_trust = 0.85
        intent_trust = 0.6
        
        if conflicts:
            word_trust -= 0.15 * len(conflicts)
            intent_trust -= 0.1 * len(conflicts)
        
        # Build decoded meaning
        meaning_parts = []
        
        if emotion != "neutral":
            meaning_parts.append(f"Speaker is {emotion}")
        
        if layer_5['data'].get('questions'):
            meaning_parts.append("and implicitly seeking help")
        
        if layer_6['data'].get('hidden_requests'):
            meaning_parts.append("with underlying request for assistance")
        
        decoded_meaning = " ".join(meaning_parts) if meaning_parts else "Neutral statement"
        
        # Recommend response tone
        if emotion in ["frustrated", "sad", "stressed"]:
            rec_tone = "supportive + solution_oriented"
        elif emotion in ["angry"]:
            rec_tone = "calm + de-escalating"
        elif emotion in ["excited", "happy"]:
            rec_tone = "matching_energy + encouraging"
        else:
            rec_tone = "neutral + helpful"
        
        return {
            "raw_transcript": transcript,
            "decoded_meaning": decoded_meaning,
            "emotional_state": emotion,
            "confidence_in_synthesis": 0.65 - (0.1 * len(conflicts)),
            "recommended_response_tone": rec_tone,
            "trust_level": {
                "words": word_trust,
                "emotion": emotion_trust,
                "intent": intent_trust
            },
            "conflicts_detected": len(conflicts) > 0
        }
```

---

## Integration with CORTEX

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                              UPDATED SYSTEM                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

                              AUDIO INPUT
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                               DECODER                                       │
│                     (Voice Stratification Engine)                           │
│                                                                             │
│   Layer 0 ──▶ Layer 1 ──▶ Layer 2 ──▶ Layer 3 ──▶ Layer 4 ──▶ ...        │
│   Physics    Biology     Prosody     Phonetic    Language                  │
│   (HAQ)      (HAQ)       (HAQ~)      (URF)       (URF)                     │
│                                                                             │
│   Output: Full stratified understanding + conflicts + synthesis             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   │ Decoded Input Object
                                   │ (not just text anymore)
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                                CORTEX                                       │
│                                                                             │
│   Now receives:                                                            │
│   - transcript (Layer 4)                                                   │
│   - emotional_state (Layer 2)                                              │
│   - speaker_confidence (Layer 2)                                           │
│   - intent (Layer 5)                                                       │
│   - hidden_requests (Layer 6)                                              │
│   - conflicts (cross-layer)                                                │
│   - trust_levels (per layer)                                               │
│   - recommended_response_tone                                              │
│                                                                             │
│   CORTEX can now:                                                          │
│   - Respond to emotion, not just words                                     │
│   - Detect when user says "fine" but isn't                                │
│   - Adjust tone based on prosodic signals                                  │
│   - Trust lower layers over higher when conflict                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
                               THALAMUS
                                   │
                                   ▼
                              VOICE OUTPUT
```

---

## The Key Insight

Before: AI heard **words**.

Now: AI hears **the human**.

```
OLD:
"I'm fine" → respond to "fine"

NEW:
"I'm fine" + frustrated prosody + low confidence + stress markers
     → conflict detected
     → trust emotion over words
     → respond to frustration, not claim of being fine
```

---

## The Truth Hierarchy in Decoding

| Layer | Truth Type | Confidence | Can Lie? |
|-------|------------|------------|----------|
| 0 - Physical | HAQ | 1.0 | No |
| 1 - Biological | HAQ | 0.9 | No |
| 2 - Prosody | HAQ-adjacent | 0.85 | Rarely |
| 3 - Phonetic | URF | 0.8 | No |
| 4 - Language | URF | 0.75 | Yes |
| 5 - Semantics | SHAHADA | 0.6 | Yes |
| 6 - Pragmatics | Interpretation | 0.4 | Often |
| 7 - Identity | Projection | 0.2 | Always |

**Lower layers veto higher layers.**

If Layer 2 says stressed and Layer 4 says "relaxed", trust Layer 2.

---

This is what you asked for. The voice is now decoded as it truly is: physics first, meaning last, truth density decreasing as you go up.

Want me to build the specific integration where CORTEX uses this decoded input to generate contextually aware responses?