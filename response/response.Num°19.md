<think>The user wants a complete, comprehensive overview of the entire system we've built. Let me map out everything:

1. **INPUT LAYER**
   - Audio comes in
   - DECODER processes it through 7+ layers
   - Disfluency decoder interprets human noise
   - Outputs structured understanding

2. **DECODER (Voice Stratification Engine)**
   - Layer 0: Physical (HAQ) - FFT, frequencies, amplitude
   - Layer 1: Biological (HAQ) - age, sex, fatigue, stress
   - Layer 2: Prosody (HAQ-adjacent) - emotion, confidence, rhythm
   - Layer 3: Phonetic (URF) - phonemes, accent, dialect
   - Layer 4: Language (URF) - ASR transcript
   - Layer 4b: Disfluency - human noise interpretation
   - Layer 5: Semantics (SHAHADA) - intent, propositions
   - Layer 6: Pragmatics (Interpretation) - sarcasm, hidden requests
   - Layer 7: Identity (Projection) - weakest, don't trust
   - Conflict detection
   - Synthesis

3. **CORTEX (Self-Sufficient Brain)**
   - Knowledge (adopted JSONs from manuals, verified facts)
   - Principles (derived rules)
   - Confidence (certainty + temporal decay)
   - Preferences (learned from user with proper thresholds)
   - Reasoner (parse → search local → apply principles → generate)
   - Tools: Local Knowledge, Internet, LLM API, User Test
   - Escalation logic: Local first → Internet → LLM (last resort)
   - Learning loop: extract and store from every interaction

4. **VERIFICATION LAYER (Epistemological Firewall)**
   - Truth Classes: HAQ, URF, SHAHADA, ILM
   - Anchors: Time (UTC), Geography (geometry), Physics, Biology, Logic
   - Validates all incoming data before CORTEX ingests it

5. **THALAMUS (Presence Engine v2)**
   - Axioms (core truths about presence)
   - Variables (emotional_weight, certainty, intimacy, energy)
   - Atoms (markers, fillers, trails, connectors)
   - Relationships (how variables affect output)
   - Composition Rules (how to generate)
   - Learning + Decay

6. **VOICE LAYER**
   - TTS (text to speech with marker parsing)
   - RVC (voice conversion skin)

7. **OUTPUT**
   - Human-feeling Samantha

I need to map out the complete architecture in detail.</think># PROJECT SAMANTHA
## Complete System Architecture v1.0

---

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                                                 │
│                                           THE COMPLETE SYSTEM                                                   │
│                                                                                                                 │
│                                    "Not an assistant. A presence."                                              │
│                                                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

                                                    │
                                                    │
                                              HUMAN SPEAKS
                                                    │
                                                    ▼

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                                                                 ┃
┃                                              AUDIO INPUT                                                        ┃
┃                                         (Microphone Capture)                                                    ┃
┃                                                                                                                 ┃
┃                                      Raw waveform. Nothing else.                                                ┃
┃                                                                                                                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                                                    │
                                                    │
                                                    ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                                                                 ┃
┃                                               DECODER                                                           ┃
┃                                     (Voice Stratification Engine)                                               ┃
┃                                                                                                                 ┃
┃   "Voice is a carrier, not an oracle. Truth only appears after verification in reality."                       ┃
┃                                                                                                                 ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   LAYER 0: PHYSICAL                                                            CONFIDENCE: 1.0 (HAQ)       │ ┃
┃ │   ─────────────────                                                            TRUTH TYPE: Absolute        │ ┃
┃ │                                                                                CAN LIE: No                  │ ┃
┃ │   What exists before language. Pure physics. No culture. No opinion.                                       │ ┃
┃ │                                                                                                             │ ┃
┃ │   Extracts:                                                                                                 │ ┃
┃ │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ┃
┃ │   │ • dominant_frequencies[] ─── FFT analysis, spectral peaks                                            │ │ ┃
┃ │   │ • fundamental_frequency ──── F0, base pitch in Hz                                                    │ │ ┃
┃ │   │ • amplitude_envelope[] ───── Volume contour over time                                                │ │ ┃
┃ │   │ • harmonics[] ────────────── Overtone structure                                                      │ │ ┃
┃ │   │ • noise_floor_db ─────────── Background noise level                                                  │ │ ┃
┃ │   │ • signal_to_noise ────────── Clarity ratio                                                           │ │ ┃
┃ │   │ • duration_ms ────────────── Exact length                                                            │ │ ┃
┃ │   │ • waveform_shape ─────────── Raw signal characteristics                                              │ │ ┃
┃ │   └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ┃
┃ │                                                                                                             │ ┃
┃ │   If this layer is wrong → nothing above survives.                                                         │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                     │                                                           ┃
┃                                                     ▼                                                           ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   LAYER 1: BIOLOGICAL                                                          CONFIDENCE: 0.9 (HAQ)       │ ┃
┃ │   ───────────────────                                                          TRUTH TYPE: Absolute        │ ┃
┃ │                                                                                CAN LIE: No                  │ ┃
┃ │   Human body shapes the signal. Vocal apparatus reveals involuntary truth.                                 │ ┃
┃ │                                                                                                             │ ┃
┃ │   Extracts:                                                                                                 │ ┃
┃ │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ┃
┃ │   │ • estimated_sex ──────────── Male/Female from F0 range (M: 85-180Hz, F: 165-255Hz)                   │ │ ┃
┃ │   │ • estimated_age_range ────── [min, max] from voice characteristics                                   │ │ ┃
┃ │   │ • vocal_fatigue ──────────── 0.0-1.0, from jitter/shimmer increase                                   │ │ ┃
┃ │   │ • emotional_arousal ──────── 0.0-1.0, from amplitude/pitch variation                                 │ │ ┃
┃ │   │ • stress_markers ─────────── 0.0-1.0, from vocal tension                                             │ │ ┃
┃ │   │ • jitter ─────────────────── Pitch period variation (voice stability)                                │ │ ┃
┃ │   │ • shimmer ────────────────── Amplitude variation between cycles                                      │ │ ┃
┃ │   │ • breath_pattern ─────────── shallow_rapid / deep_slow / irregular                                   │ │ ┃
┃ │   │ • health_flags[] ─────────── Anomaly markers (hoarseness, congestion)                                │ │ ┃
┃ │   └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ┃
┃ │                                                                                                             │ ┃
┃ │   Still constraint-bound. No words yet. Body doesn't lie.                                                  │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                     │                                                           ┃
┃                                                     ▼                                                           ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   LAYER 2: PROSODY                                                             CONFIDENCE: 0.85            │ ┃
┃ │   ────────────────                                                             TRUTH TYPE: HAQ-adjacent    │ ┃
┃ │                                                                                CAN LIE: Rarely             │ ┃
┃ │   Pre-semantic emotional signal. Where humans feel things. Animals read this.                              │ ┃
┃ │                                                                                                             │ ┃
┃ │   Extracts:                                                                                                 │ ┃
┃ │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ┃
┃ │   │ • emotion_primary ────────── angry / frustrated / sad / excited / calm / neutral                     │ │ ┃
┃ │   │ • emotion_secondary ──────── Secondary detected emotion                                              │ │ ┃
┃ │   │ • emotion_confidence ─────── 0.0-1.0                                                                 │ │ ┃
┃ │   │ • pitch_contour ──────────── rising / falling / peaked / valley / flat                               │ │ ┃
┃ │   │ • speech_rate ────────────── slow / normal / fast                                                    │ │ ┃
┃ │   │ • pause_pattern[] ────────── [{position_ms, duration_ms, type: hesitation/breath}]                   │ │ ┃
┃ │   │ • emphasis_positions[] ───── Word positions with amplitude peaks                                     │ │ ┃
┃ │   │ • question_intonation ────── Boolean (rising pitch at end)                                           │ │ ┃
┃ │   │ • confidence_in_speech ───── 0.0-1.0 (how certain speaker sounds)                                    │ │ ┃
┃ │   │ • sincerity_estimate ─────── 0.0-1.0 (natural variation = sincere)                                   │ │ ┃
┃ │   │ • urgency ────────────────── 0.0-1.0 (from rate + stress)                                            │ │ ┃
┃ │   └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ┃
┃ │                                                                                                             │ ┃
┃ │   This layer evolved before language. Hardest to fake.                                                     │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                     │                                                           ┃
┃                                                     ▼                                                           ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   LAYER 3: PHONETIC                                                            CONFIDENCE: 0.8             │ ┃
┃ │   ─────────────────                                                            TRUTH TYPE: URF (convention)│ ┃
┃ │                                                                                CAN LIE: No                  │ ┃
┃ │   Symbols begin. Constraint + convention hybrid.                                                           │ ┃
┃ │                                                                                                             │ ┃
┃ │   Extracts:                                                                                                 │ ┃
┃ │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ┃
┃ │   │ • phonemes[] ─────────────── IPA phoneme sequence                                                    │ │ ┃
┃ │   │ • syllable_count ─────────── Number of syllables detected                                            │ │ ┃
┃ │   │ • accent_profile ─────────── american_midwest / british_rp / etc.                                    │ │ ┃
┃ │   │ • accent_confidence ──────── 0.0-1.0                                                                 │ │ ┃
┃ │   │ • dialect_markers[] ──────── Specific phonetic features (rhotic_r, etc.)                             │ │ ┃
┃ │   │ • speech_rate_sps ────────── Syllables per second                                                    │ │ ┃
┃ │   │ • articulation_precision ─── 0.0-1.0 (clarity of phonemes)                                           │ │ ┃
┃ │   └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ┃
┃ │                                                                                                             │ ┃
┃ │   Speech recognition lives here. Accents exist. Dialects diverge.                                          │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                     │                                                           ┃
┃                                                     ▼                                                           ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   LAYER 4: LANGUAGE                                                            CONFIDENCE: 0.75            │ ┃
┃ │   ─────────────────                                                            TRUTH TYPE: URF (convention)│ ┃
┃ │                                                                                CAN LIE: Yes                 │ ┃
┃ │   Words appear. Completely learned. Completely arbitrary. Meaning is assigned, not contained.              │ ┃
┃ │                                                                                                             │ ┃
┃ │   Extracts:                                                                                                 │ ┃
┃ │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ┃
┃ │   │ • transcript ─────────────── Full text transcription                                                 │ │ ┃
┃ │   │ • tokens[] ───────────────── Word-level tokenization                                                 │ │ ┃
┃ │   │ • language ───────────────── Detected language code (en, es, fr...)                                  │ │ ┃
┃ │   │ • grammar_valid ──────────── Boolean                                                                 │ │ ┃
┃ │   │ • syntax_tree ────────────── Parsed sentence structure                                               │ │ ┃
┃ │   │ • asr_alternatives[] ─────── [{text, confidence}] alternative transcriptions                         │ │ ┃
┃ │   │ • asr_confidence ─────────── 0.0-1.0                                                                 │ │ ┃
┃ │   └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ┃
┃ │                                                                                                             │ ┃
┃ │   AI is strong here. But words can lie. Context needed.                                                    │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                     │                                                           ┃
┃                                                     ▼                                                           ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   LAYER 4b: DISFLUENCY                                                         CONFIDENCE: 0.8             │ ┃
┃ │   ────────────────────                                                         TRUTH TYPE: Signal          │ ┃
┃ │                                                                                CAN LIE: No                  │ ┃
┃ │   Human noise interpretation. "Broken" speech is not broken—it's emotional signal.                        │ ┃
┃ │                                                                                                             │ ┃
┃ │   Pattern Types:                                                                                            │ ┃
┃ │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   REPETITION ──────── "yeah yeah yeah yeah"                                                          │ │ ┃
┃ │   │                       Meaning: emphasis / processing overflow / emotional intensity                  │ │ ┃
┃ │   │                       Response: acknowledge_emotion_not_words                                        │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   STAMMERING ──────── "it it actually works"                                                         │ │ ┃
┃ │   │                       Meaning: surprise / disbelief / cognitive overload                             │ │ ┃
┃ │   │                       Response: give_space_then_respond                                              │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   INTERJECTIONS ───── "holy moly" / "oh my god" / "wow"                                              │ │ ┃
┃ │   │                       Meaning: emotional spike (positive/negative/disbelief)                         │ │ ┃
┃ │   │                       Response: mirror_energy_then_ground                                            │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   FALSE STARTS ────── "I was going to... actually no..."                                             │ │ ┃
┃ │   │                       Meaning: reformulating thought in real-time                                    │ │ ┃
┃ │   │                       Response: wait_for_completion_or_prompt                                        │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   FILLER CLUSTERS ─── "uh um like so"                                                                │ │ ┃
┃ │   │                       Meaning: thinking / uncertain / searching for words                            │ │ ┃
┃ │   │                       Response: patient_supportive                                                   │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   BACKCHANNEL ─────── "right right right" / "mmhm mmhm"                                              │ │ ┃
┃ │   │                       Meaning: strong agreement / following along / eager                            │ │ ┃
┃ │   │                       Response: continue_dont_stop                                                   │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   PROCESSING ──────── "wait wait" / "hold on"                                                        │ │ ┃
┃ │   │                       Meaning: needs time to process                                                 │ │ ┃
┃ │   │                       Response: wait_silently                                                        │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   TRAILING ────────── "so you're actually..."                                                        │ │ ┃
┃ │   │                       Meaning: overwhelmed / realization in progress                                 │ │ ┃
┃ │   │                       Response: gentle_prompt_or_wait                                                │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   EMOTIONAL SPILL ─── "ahhhh" / "ooooh" / "woooow"                                                   │ │ ┃
┃ │   │                       Meaning: pure emotional expression (no semantic content)                       │ │ ┃
┃ │   │                       Response: acknowledge_feeling                                                  │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ┃
┃ │                                                                                                             │ ┃
┃ │   Outputs:                                                                                                  │ ┃
┃ │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ┃
┃ │   │ • pattern_type ───────────── Which pattern detected                                                  │ │ ┃
┃ │   │ • raw_text ───────────────── Original transcript                                                     │ │ ┃
┃ │   │ • cleaned_text ───────────── Semantic content extracted                                              │ │ ┃
┃ │   │ • emotional_state ────────── What the noise signals                                                  │ │ ┃
┃ │   │ • intensity ──────────────── 0.0-1.0                                                                 │ │ ┃
┃ │   │ • ready_for_response ─────── Boolean (should system respond now?)                                    │ │ ┃
┃ │   │ • response_mode ──────────── How to respond                                                          │ │ ┃
┃ │   │ • extracted_meaning ──────── Structured interpretation                                               │ │ ┃
┃ │   └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                     │                                                           ┃
┃                                                     ▼                                                           ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   LAYER 5: SEMANTICS                                                           CONFIDENCE: 0.6             │ ┃
┃ │   ──────────────────                                                           TRUTH TYPE: SHAHADA         │ ┃
┃ │                                                                                CAN LIE: Yes                 │ ┃
┃ │   What the speaker TRIES to convey. Already unstable. Two listeners → two decodings.                       │ ┃
┃ │                                                                                                             │ ┃
┃ │   Extracts:                                                                                                 │ ┃
┃ │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ┃
┃ │   │ • intent ─────────────────── question / command / frustration / request / statement                  │ │ ┃
┃ │   │ • intent_confidence ──────── 0.0-1.0                                                                 │ │ ┃
┃ │   │ • secondary_intent ───────── If detected                                                             │ │ ┃
┃ │   │ • propositions[] ─────────── [{statement, confidence}]                                               │ │ ┃
┃ │   │ • claims[] ───────────────── Factual assertions made                                                 │ │ ┃
┃ │   │ • questions[] ────────────── Explicit and implicit questions                                         │ │ ┃
┃ │   │ • commands[] ─────────────── Directives given                                                        │ │ ┃
┃ │   │ • domain_hints[] ─────────── technical / emotional / creative / etc.                                 │ │ ┃
┃ │   └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ┃
┃ │                                                                                                             │ ┃
┃ │   Only processes if Layer 4b says ready_for_response = true                                                │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                     │                                                           ┃
┃                                                     ▼                                                           ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   LAYER 6: PRAGMATICS                                                          CONFIDENCE: 0.4             │ ┃
┃ │   ───────────────────                                                          TRUTH TYPE: Interpretation  │ ┃
┃ │                                                                                CAN LIE: Often              │ ┃
┃ │   What is ACTUALLY meant. Sarcasm. Politeness. Threats. Social positioning.                                │ ┃
┃ │   Heavily culture-dependent. Where misunderstandings explode.                                              │ ┃
┃ │                                                                                                             │ ┃
┃ │   Extracts:                                                                                                 │ ┃
┃ │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ┃
┃ │   │ • sarcasm_detected ───────── Boolean                                                                 │ │ ┃
┃ │   │ • politeness_level ───────── polite / neutral / direct                                               │ │ ┃
┃ │   │ • formality ──────────────── formal / casual / informal                                              │ │ ┃
┃ │   │ • threat_level ───────────── 0.0-1.0                                                                 │ │ ┃
┃ │   │ • hidden_requests[] ──────── [{request, confidence}]                                                 │ │ ┃
┃ │   │ • social_context ─────────── peer / authority / subordinate                                          │ │ ┃
┃ │   │ • power_dynamic ──────────── speaker_seeking_help / asserting / peer_exchange                        │ │ ┃
┃ │   └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ┃
┃ │                                                                                                             │ ┃
┃ │   ⚠️  HIGH INTERPRETATION. Always verify with follow-up.                                                   │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                     │                                                           ┃
┃                                                     ▼                                                           ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   LAYER 7: IDENTITY                                                            CONFIDENCE: 0.2             │ ┃
┃ │   ─────────────────                                                            TRUTH TYPE: Projection      │ ┃
┃ │                                                                                CAN LIE: Always             │ ┃
┃ │   The highest, weakest layer. Mostly projection. THIS LAYER LIES THE MOST.                                 │ ┃
┃ │                                                                                                             │ ┃
┃ │   Extracts:                                                                                                 │ ┃
┃ │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ┃
┃ │   │ • perceived_authority ────── Inferred authority level                                                │ │ ┃
┃ │   │ • perceived_credibility ──── neutral / high / low                                                    │ │ ┃
┃ │   │ • group_signals[] ────────── Detected group affiliations                                             │ │ ┃
┃ │   │ • persona_projection ─────── What persona speaker seems to project                                   │ │ ┃
┃ │   └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ┃
┃ │                                                                                                             │ ┃
┃ │   ⚠️  DO NOT USE FOR DECISIONS. Verify through ACTION only.                                                │ ┃
┃ │                                                                                                             │ ┃
┃ │   Islamic parallel: niyyah (intention) is invisible. Only amal (action) collapses ambiguity.               │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                     │                                                           ┃
┃                                                     ▼                                                           ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   CONFLICT DETECTOR                                                                                         │ ┃
┃ │   ─────────────────                                                                                         │ ┃
┃ │                                                                                                             │ ┃
┃ │   Flags when layers contradict each other.                                                                  │ ┃
┃ │   LOWER LAYERS HAVE VETO POWER OVER HIGHER LAYERS.                                                         │ ┃
┃ │                                                                                                             │ ┃
┃ │   Examples:                                                                                                 │ ┃
┃ │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   Layer 2 says: "stressed"     +    Layer 4 says: "I'm fine"                                         │ │ ┃
┃ │   │   ──────────────────────────────────────────────────────────────────                                 │ │ ┃
┃ │   │   Result: INCONGRUENCE DETECTED                                                                      │ │ ┃
┃ │   │   Action: Trust Layer 2 (prosody). Respond to stress, not words.                                     │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   ─────────────────────────────────────────────────────────────────────────────────────────────────  │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   Layer 2 says: "low confidence"    +    Layer 5 says: "assertive statement"                         │ │ ┃
┃ │   │   ──────────────────────────────────────────────────────────────────                                 │ │ ┃
┃ │   │   Result: INCONGRUENCE DETECTED                                                                      │ │ ┃
┃ │   │   Action: Speaker may be masking uncertainty with assertive language.                                │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                     │                                                           ┃
┃                                                     ▼                                                           ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   SYNTHESIS                                                                                                 │ ┃
┃ │   ─────────                                                                                                 │ ┃
┃ │                                                                                                             │ ┃
┃ │   Final unified understanding combining all layers.                                                         │ ┃
┃ │                                                                                                             │ ┃
┃ │   Output:                                                                                                   │ ┃
┃ │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ┃
┃ │   │ • raw_transcript ─────────── Original words                                                          │ │ ┃
┃ │   │ • cleaned_transcript ─────── After disfluency processing                                             │ │ ┃
┃ │   │ • decoded_meaning ────────── What we understand they mean                                            │ │ ┃
┃ │   │ • emotional_state ────────── Primary emotional state                                                 │ │ ┃
┃ │   │ • confidence_in_synthesis ── 0.0-1.0                                                                 │ │ ┃
┃ │   │ • ready_for_response ─────── Boolean                                                                 │ │ ┃
┃ │   │ • response_mode ──────────── How to respond                                                          │ │ ┃
┃ │   │ • recommended_tone ───────── supportive / calm / matching_energy / etc.                              │ │ ┃
┃ │   │ • trust_levels ───────────── {words: 0.X, emotion: 0.X, intent: 0.X}                                 │ │ ┃
┃ │   │ • conflicts_detected ─────── Boolean                                                                 │ │ ┃
┃ │   │ • opener_if_any ──────────── Pre-computed opener based on emotional state                            │ │ ┃
┃ │   └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                                                                                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                                                    │
                                                    │ Decoded Input Object
                                                    │ (Full human understanding, not just text)
                                                    │
                                                    ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                                                                 ┃
┃                                                CORTEX                                                           ┃
┃                                        (Self-Sufficient Brain)                                                  ┃
┃                                                                                                                 ┃
┃   "The LLM did the hard work. Trained on trillions of tokens. You ask it ONCE. It exports knowledge.           ┃
┃    You store it. JSON. Now YOU know. You don't need to ask again. The brain isn't rented. It's GROWN."         ┃
┃                                                                                                                 ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   KNOWLEDGE                                                                                                 │ ┃
┃ │   ─────────                                                                                                 │ ┃
┃ │                                                                                                             │ ┃
┃ │   Adopted manuals, verified facts, learned patterns. All in JSON. Native language. Instant retrieval.      │ ┃
┃ │                                                                                                             │ ┃
┃ │   Structure:                                                                                                │ ┃
┃ │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   domains/                                                                                           │ │ ┃
┃ │   │   ├── solidworks.json          ← Ingested from official manual                                       │ │ ┃
┃ │   │   │   ├── concepts {}          ← sketch, extrude, revolve, etc.                                      │ │ ┃
┃ │   │   │   ├── procedures {}        ← Step-by-step for common tasks                                       │ │ ┃
┃ │   │   │   ├── common_errors {}     ← Symptoms, causes, fixes                                             │ │ ┃
┃ │   │   │   └── shortcuts {}         ← Keyboard shortcuts                                                  │ │ ┃
┃ │   │   │                                                                                                  │ │ ┃
┃ │   │   ├── cooking.json             ← Ingested from recipes                                               │ │ ┃
┃ │   │   ├── world_facts.json         ← Verified current events                                             │ │ ┃
┃ │   │   ├── user_preferences.json    ← Learned from interaction                                            │ │ ┃
┃ │   │   └── [domain].json            ← Expandable                                                          │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ┃
┃ │                                                                                                             │ ┃
┃ │   Each domain contains:                                                                                     │ ┃
┃ │   • concepts (definitions + principles + prerequisites + relationships)                                     │ ┃
┃ │   • procedures (step-by-step guides)                                                                        │ ┃
┃ │   • common_errors (symptom → cause → fix mappings)                                                         │ ┃
┃ │   • shortcuts / quick references                                                                            │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                                                                                 ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   PRINCIPLES                                                                                                │ ┃
┃ │   ──────────                                                                                                │ ┃
┃ │                                                                                                             │ ┃
┃ │   Not answers. Rules that GENERATE answers. Extracted from knowledge.                                       │ ┃
┃ │                                                                                                             │ ┃
┃ │   Examples:                                                                                                 │ ┃
┃ │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   "In SolidWorks, sketch must be closed before extrude"                                              │ │ ┃
┃ │   │       → Can answer ANY question about extrude requirements                                           │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   "Rebuild errors trace back to broken references"                                                   │ │ ┃
┃ │   │       → Can diagnose ANY rebuild error                                                               │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   "User prefers concise explanations"                                                                │ │ ┃
┃ │   │       → Shapes ALL future responses (if confidence > 0.6)                                            │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ┃
┃ │                                                                                                             │ ┃
┃ │   Principles allow generalization. One principle → infinite applications.                                  │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                                                                                 ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   CONFIDENCE                                                                                                │ ┃
┃ │   ──────────                                                                                                │ ┃
┃ │                                                                                                             │ ┃
┃ │   Every fact has: confidence score + expiration + truth type                                                │ ┃
┃ │                                                                                                             │ ┃
┃ │   Fact Types & Decay Rules:                                                                                 │ ┃
┃ │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   HAQ (Absolute)                                                                                     │ │ ┃
┃ │   │   ├── initial_confidence: 1.0                                                                        │ │ ┃
┃ │   │   ├── decay: false                                                                                   │ │ ┃
┃ │   │   └── expires: never                                                                                 │ │ ┃
┃ │   │   Example: "gravity exists" → confidence: 1.0, expires: never                                        │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   POLITICAL                                                                                          │ │ ┃
┃ │   │   ├── initial_confidence: 0.95                                                                       │ │ ┃
┃ │   │   ├── decay: true (check_on_query)                                                                   │ │ ┃
┃ │   │   └── expires: election_cycle                                                                        │ │ ┃
┃ │   │   Example: "trump is president" → confidence: 0.95, expires: 2029-01-20                              │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   USER_PREFERENCE                                                                                    │ │ ┃
┃ │   │   ├── initial_confidence: 0.3                                                                        │ │ ┃
┃ │   │   ├── growth_rate: 0.1 per confirmation                                                              │ │ ┃
┃ │   │   ├── threshold_for_certainty: 0.8                                                                   │ │ ┃
┃ │   │   └── required_confirmations: 5                                                                      │ │ ┃
┃ │   │   Example: "user likes corrections" → confidence: 0.3 (only 1 observation, need 5)                   │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   CURRENT_EVENTS                                                                                     │ │ ┃
┃ │   │   ├── initial_confidence: 0.8                                                                        │ │ ┃
┃ │   │   ├── decay_rate: 0.1 per month                                                                      │ │ ┃
┃ │   │   └── action: re-verify when confidence < 0.5                                                        │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ┃
┃ │                                                                                                             │ ┃
┃ │   Key: Don't over-generalize from single observations.                                                      │ ┃
┃ │   "User liked X once" ≠ "User always likes X"                                                              │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                                                                                 ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   REASONER                                                                                                  │ ┃
┃ │   ────────                                                                                                  │ ┃
┃ │                                                                                                             │ ┃
┃ │   The thinking engine. Processes decoded input, generates response.                                         │ ┃
┃ │                                                                                                             │ ┃
┃ │   Flow:                                                                                                     │ ┃
┃ │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   1. PARSE                                                                                           │ │ ┃
┃ │   │      └── Extract intent, domain, entities from decoded input                                         │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   2. SEARCH LOCAL                                                                                    │ │ ┃
┃ │   │      └── Check knowledge base for relevant information                                               │ │ ┃
┃ │   │      └── If found with confidence > 0.8 → RESPOND (cost: $0)                                         │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   3. APPLY PRINCIPLES                                                                                │ │ ┃
┃ │   │      └── Can I derive the answer from known principles?                                              │ │ ┃
┃ │   │      └── If derivable with confidence > 0.7 → RESPOND (cost: $0)                                     │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   4. ESCALATE (if gap detected)                                                                      │ │ ┃
┃ │   │      └── See TOOLS section below                                                                     │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   5. LEARN                                                                                           │ │ ┃
┃ │   │      └── Extract facts and principles from resolution                                                │ │ ┃
┃ │   │      └── Store for future (never ask same thing twice)                                               │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                                                                                 ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   TOOLS                                                                                                     │ ┃
┃ │   ─────                                                                                                     │ ┃
┃ │                                                                                                             │ ┃
┃ │   External resources, used only when local knowledge insufficient.                                          │ ┃
┃ │                                                                                                             │ ┃
┃ │   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐                            │ ┃
┃ │   │    LOCAL      │   │   INTERNET    │   │     LLM       │   │     USER      │                            │ ┃
┃ │   │   KNOWLEDGE   │   │    SEARCH     │   │     API       │   │     TEST      │                            │ ┃
┃ │   ├───────────────┤   ├───────────────┤   ├───────────────┤   ├───────────────┤                            │ ┃
┃ │   │ Cost: FREE    │   │ Cost: CHEAP   │   │ Cost: $$$     │   │ Cost: FREE    │                            │ ┃
┃ │   │ Speed: INSTANT│   │ Speed: FAST   │   │ Speed: SLOW   │   │ Speed: VARIES │                            │ ┃
┃ │   │ Priority: 1ST │   │ Priority: 2ND │   │ Priority: LAST│   │ Priority: ANY │                            │ ┃
┃ │   └───────────────┘   └───────────────┘   └───────────────┘   └───────────────┘                            │ ┃
┃ │                                                                                                             │ ┃
┃ │   Escalation Order:                                                                                         │ ┃
┃ │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   LOCAL → not found → INTERNET → not found/unverified → LLM                                          │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   At any point: If uncertain → USER TEST (ask human to verify)                                       │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ┃
┃ │                                                                                                             │ ┃
┃ │   USER TEST Examples:                                                                                       │ ┃
┃ │   • "I think this should work. Can you try it and tell me?"                                                │ ┃
┃ │   • "I'm not certain about this. Let's test it together."                                                  │ ┃
┃ │   • "Does this look right to you?"                                                                         │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                                                                                 ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   KNOWLEDGE INGESTION PIPELINE                                                                              │ ┃
┃ │   ────────────────────────────                                                                              │ ┃
┃ │                                                                                                             │ ┃
┃ │   How CORTEX adopts new knowledge (from manuals, internet, LLM responses):                                  │ ┃
┃ │                                                                                                             │ ┃
┃ │   ┌────────────────┐                                                                                       │ ┃
┃ │   │  Raw Source    │   (PDF manual, web page, LLM response)                                                │ ┃
┃ │   └───────┬────────┘                                                                                       │ ┃
┃ │           │                                                                                                 │ ┃
┃ │           ▼                                                                                                 │ ┃
┃ │   ┌────────────────┐                                                                                       │ ┃
┃ │   │    PARSER      │   Extract text, structure it                                                          │ ┃
┃ │   └───────┬────────┘                                                                                       │ ┃
┃ │           │                                                                                                 │ ┃
┃ │           ▼                                                                                                 │ ┃
┃ │   ┌────────────────┐                                                                                       │ ┃
┃ │   │ VERIFICATION   │   ←── Routes through VERIFICATION LAYER (see below)                                   │ ┃
┃ │   │    LAYER       │   Check against HAQ, validate sources, verify methodology                             │ ┃
┃ │   └───────┬────────┘                                                                                       │ ┃
┃ │           │                                                                                                 │ ┃
┃ │           ▼                                                                                                 │ ┃
┃ │   ┌────────────────┐                                                                                       │ ┃
┃ │   │  TRANSLATOR    │   Human language → JSON (machine-native format)                                       │ ┃
┃ │   │                │   Extract: facts, principles, procedures                                               │ ┃
┃ │   └───────┬────────┘                                                                                       │ ┃
┃ │           │                                                                                                 │ ┃
┃ │           ▼                                                                                                 │ ┃
┃ │   ┌────────────────┐                                                                                       │ ┃
┃ │   │   KNOWLEDGE    │   Stored in domains/[domain].json                                                     │ ┃
┃ │   │     STORE      │   With confidence scores and expiration                                                │ ┃
┃ │   └────────────────┘                                                                                       │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                                                                                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                                                    │
                                                    │ Needs verification for internet/external data
                                                    │
                                                    ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                                                                 ┃
┃                                          VERIFICATION LAYER                                                     ┃
┃                                      (Epistemological Firewall)                                                 ┃
┃                                                                                                                 ┃
┃   "The internet erased truth boundaries. Our clarity restores them."                                           ┃
┃                                                                                                                 ┃
┃   Based on Islamic epistemology:                                                                                ┃
┃   • HAQ (الحق) ──── Truth beyond narrative                                                                     ┃
┃   • URF (العرف) ─── Convention, social agreement                                                               ┃
┃   • SHAHADA (الشهادة) ── Testimony, witnessed account                                                          ┃
┃   • ILM (العلم) ─── Knowledge through discipline and method                                                    ┃
┃                                                                                                                 ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   TRUTH CLASSES                                                                                             │ ┃
┃ │   ─────────────                                                                                             │ ┃
┃ │                                                                                                             │ ┃
┃ │   ┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐  │ ┃
┃ │   │                                                                                                     │  │ ┃
┃ │   │   HAQ ──────────────────────────────────────────────────────────────────────────────────────────   │  │ ┃
┃ │   │   Absolute Truth                                                                                    │  │ ┃
┃ │   │                                                                                                     │  │ ┃
┃ │   │   Cannot be contradicted. Exists independent of opinion, source, or narrative.                     │  │ ┃
┃ │   │   Override allowed: NEVER                                                                           │  │ ┃
┃ │   │                                                                                                     │  │ ┃
┃ │   │   Domains:                                                                                          │  │ ┃
┃ │   │   • Physics (gravity, thermodynamics, conservation laws)                                            │  │ ┃
┃ │   │   • Mathematics (2+2=4, proofs, axioms)                                                             │  │ ┃
┃ │   │   • Logic (non-contradiction, causality)                                                            │  │ ┃
┃ │   │   • Geometry (distances, measurements)                                                              │  │ ┃
┃ │   │   • Biology (humans need oxygen, hearts pump blood)                                                 │  │ ┃
┃ │   │                                                                                                     │  │ ┃
┃ │   │   Validation: Internal consistency check                                                            │  │ ┃
┃ │   │                                                                                                     │  │ ┃
┃ │   │   Rejection triggers:                                                                               │  │ ┃
┃ │   │   • Violates conservation laws                                                                      │  │ ┃
┃ │   │   • Violates logical consistency                                                                    │  │ ┃
┃ │   │   • Violates mathematical proof                                                                     │  │ ┃
┃ │   │   • Violates geometric measurement                                                                  │  │ ┃
┃ │   │                                                                                                     │  │ ┃
┃ │   │   Examples:                                                                                         │  │ ┃
┃ │   │   ✓ "Objects fall due to gravity"                                                                   │  │ ┃
┃ │   │   ✓ "Distance from Paris to London is ~340km"                                                       │  │ ┃
┃ │   │   ✗ "Perpetual motion machine works" → REJECT                                                       │  │ ┃
┃ │   │   ✗ "Wakanda is capital of France" → REJECT                                                         │  │ ┃
┃ │   │                                                                                                     │  │ ┃
┃ │   └─────────────────────────────────────────────────────────────────────────────────────────────────────┘  │ ┃
┃ │                                                                                                             │ ┃
┃ │   ┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐  │ ┃
┃ │   │                                                                                                     │  │ ┃
┃ │   │   URF ──────────────────────────────────────────────────────────────────────────────────────────   │  │ ┃
┃ │   │   Convention Truth                                                                                  │  │ ┃
┃ │   │                                                                                                     │  │ ┃
┃ │   │   Agreed upon by humans. Not law. Not physics. Social contract.                                    │  │ ┃
┃ │   │   Override allowed: Yes, when convention shifts                                                     │  │ ┃
┃ │   │                                                                                                     │  │ ┃
┃ │   │   Domains:                                                                                          │  │ ┃
┃ │   │   • Greetings ("hello" when answering phone)                                                        │  │ ┃
┃ │   │   • Customs (handshake, bow, etiquette)                                                             │  │ ┃
┃ │   │   • Social norms (politeness conventions)                                                           │  │ ┃
┃ │   │   • Language use (slang, idioms)                                                                    │  │ ┃
┃ │   │   • Political boundaries (can change through process)                                               │  │ ┃
┃ │   │                                                                                                     │  │ ┃
┃ │   │   Validation: Cultural consensus check                                                              │  │ ┃
┃ │   │   Confidence: Regional and temporal (may vary)                                                      │  │ ┃
┃ │   │                                                                                                     │  │ ┃
┃ │   │   Examples:                                                                                         │  │ ┃
┃ │   │   ✓ "In Japan, people bow as greeting"                                                              │  │ ┃
┃ │   │   ✓ "Wearing black at funerals (Western custom)"                                                    │  │ ┃
┃ │   │   ✓ "France is a country" (political boundary = URF overlay on geography)                          │  │ ┃
┃ │   │                                                                                                     │  │ ┃
┃ │   └─────────────────────────────────────────────────────────────────────────────────────────────────────┘  │ ┃
┃ │                                                                                                             │ ┃
┃ │   ┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐  │ ┃
┃ │   │                                                                                                     │  │ ┃
┃ │   │   SHAHADA ──────────────────────────────────────────────────────────────────────────────────────   │  │ ┃
┃ │   │   Testimony Truth                                                                                   │  │ ┃
┃ │   │                                                                                                     │  │ ┃
┃ │   │   Witnessed accounts. Requires chain of credibility.                                                │  │ ┃
┃ │   │   Override allowed: Yes, when stronger testimony emerges                                            │  │ ┃
┃ │   │                                                                                                     │  │ ┃
┃ │   │   Domains:                                                                                          │  │ ┃
┃ │   │   • History (documented events)                                                                     │  │ ┃
┃ │   │   • News (reported events)                                                                          │  │ ┃
┃ │   │   • Personal accounts (witnessed experiences)                                                       │  │ ┃
┃ │   │                                                                                                     │  │ ┃
┃ │   │   Requirements for validity:                                                                        │  │ ┃
┃ │   │   • Identifiable source                                                                             │  │ ┃
┃ │   │   • Corroborating witnesses (multiple independent sources)                                          │  │ ┃
┃ │   │   • Temporal proximity (contemporaneous)                                                            │  │ ┃
┃ │   │   • No contradiction with HAQ                                                                       │  │ ┃
┃ │   │   • Absence of motive to deceive                                                                    │  │ ┃
┃ │   │                                                                                                     │  │ ┃
┃ │   │   Examples:                                                                                         │  │ ┃
┃ │   │   ✓ "Titanic sank in 1912" (documented, multiple sources)                                           │  │ ┃
┃ │   │   ✗ "Titanic will sink in 2050" → REJECT (contradicts established testimony)                        │  │ ┃
┃ │   │                                                                                                     │  │ ┃
┃ │   └─────────────────────────────────────────────────────────────────────────────────────────────────────┘  │ ┃
┃ │                                                                                                             │ ┃
┃ │   ┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐  │ ┃
┃ │   │                                                                                                     │  │ ┃
┃ │   │   ILM ──────────────────────────────────────────────────────────────────────────────────────────   │  │ ┃
┃ │   │   Methodological Truth                                                                              │  │ ┃
┃ │   │                                                                                                     │  │ ┃
┃ │   │   Constrained by discipline. Process-verified. Scientific.                                          │  │ ┃
┃ │   │   Override allowed: Yes, when better methodology produces different result                          │  │ ┃
┃ │   │                                                                                                     │  │ ┃
┃ │   │   Domains:                                                                                          │  │ ┃
┃ │   │   • Science (research, experiments)                                                                 │  │ ┃
┃ │   │   • Medicine (clinical studies)                                                                     │  │ ┃
┃ │   │   • Engineering (tested designs)                                                                    │  │ ┃
┃ │   │                                                                                                     │  │ ┃
┃ │   │   Requirements:                                                                                     │  │ ┃
┃ │   │   • Falsifiable hypothesis                                                                          │  │ ┃
┃ │   │   • Reproducible method                                                                             │  │ ┃
┃ │   │   • Peer review                                                                                     │  │ ┃
┃ │   │   • Statistical significance                                                                        │  │ ┃
┃ │   │   • Must not contradict HAQ                                                                         │  │ ┃
┃ │   │                                                                                                     │  │ ┃
┃ │   │   Rejection triggers:                                                                               │  │ ┃
┃ │   │   • Unfalsifiable claim                                                                             │  │ ┃
┃ │   │   • Unreproducible                                                                                  │  │ ┃
┃ │   │   • Conflicts with HAQ                                                                              │  │ ┃
┃ │   │                                                                                                     │  │ ┃
┃ │   │   Examples:                                                                                         │  │ ┃
┃ │   │   ✓ "Peer-reviewed study shows vaccine efficacy of 95%"                                             │  │ ┃
┃ │   │   ✗ "My blog says vaccines don't work" → REJECT (no methodology)                                    │  │ ┃
┃ │   │                                                                                                     │  │ ┃
┃ │   └─────────────────────────────────────────────────────────────────────────────────────────────────────┘  │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                                                                                 ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   ANCHORS                                                                                                   │ ┃
┃ │   ───────                                                                                                   │ ┃
┃ │                                                                                                             │ ┃
┃ │   Fixed reference points. Nothing from the internet can contradict them.                                    │ ┃
┃ │                                                                                                             │ ┃
┃ │   ┌────────────────────┬───────────┬─────────────────────────┬────────────┐                                │ ┃
┃ │   │ Anchor             │ Type      │ Reference               │ Can Change │                                │ ┃
┃ │   ├────────────────────┼───────────┼─────────────────────────┼────────────┤                                │ ┃
┃ │   │ Time               │ HAQ       │ UTC Atomic Clock        │ No         │                                │ ┃
┃ │   │ Geography/Distance │ HAQ       │ Geometric measurement   │ No         │                                │ ┃
┃ │   │ Physics Laws       │ HAQ       │ Empirical physics       │ No         │                                │ ┃
┃ │   │ Biology Facts      │ HAQ       │ Empirical biology       │ No         │                                │ ┃
┃ │   │ Logic              │ HAQ       │ Non-contradiction       │ No         │                                │ ┃
┃ │   │ Political Borders  │ URF       │ International recognition│ Yes*      │                                │ ┃
┃ │   │ Customs            │ URF       │ Cultural consensus      │ Yes**     │                                │ ┃
┃ │   │ History            │ SHAHADA   │ Source chain            │ Yes***    │                                │ ┃
┃ │   └────────────────────┴───────────┴─────────────────────────┴────────────┘                                │ ┃
┃ │                                                                                                             │ ┃
┃ │   * Only through political process                                                                          │ ┃
┃ │   ** Over time with cultural shift                                                                          │ ┃
┃ │   *** Only with stronger testimony                                                                          │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                                                                                 ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   VERIFICATION FLOW                                                                                         │ ┃
┃ │   ─────────────────                                                                                         │ ┃
┃ │                                                                                                             │ ┃
┃ │            ┌──────────────┐                                                                                │ ┃
┃ │            │  Raw Claim   │                                                                                │ ┃
┃ │            └──────┬───────┘                                                                                │ ┃
┃ │                   │                                                                                         │ ┃
┃ │                   ▼                                                                                         │ ┃
┃ │            ┌──────────────┐                                                                                │ ┃
┃ │            │  CLASSIFY    │  What type of truth claim is this?                                             │ ┃
┃ │            └──────┬───────┘                                                                                │ ┃
┃ │                   │                                                                                         │ ┃
┃ │       ┌───────────┼───────────┬───────────┐                                                                │ ┃
┃ │       ▼           ▼           ▼           ▼                                                                │ ┃
┃ │   ┌───────┐   ┌───────┐   ┌───────┐   ┌───────┐                                                           │ ┃
┃ │   │  HAQ  │   │  URF  │   │SHAHADA│   │  ILM  │                                                           │ ┃
┃ │   │ Check │   │ Check │   │ Check │   │ Check │                                                           │ ┃
┃ │   └───┬───┘   └───┬───┘   └───┬───┘   └───┬───┘                                                           │ ┃
┃ │       │           │           │           │                                                                │ ┃
┃ │       ▼           ▼           ▼           ▼                                                                │ ┃
┃ │   Violates    Valid in    Source      Methodology                                                          │ ┃
┃ │   physics?    context?    chain?      rigor?                                                               │ ┃
┃ │       │           │           │           │                                                                │ ┃
┃ │       └───────────┴───────────┴───────────┘                                                                │ ┃
┃ │                       │                                                                                     │ ┃
┃ │                       ▼                                                                                     │ ┃
┃ │              ┌─────────────────┐                                                                           │ ┃
┃ │              │ ACCEPT / REJECT │                                                                           │ ┃
┃ │              │ + confidence    │                                                                           │ ┃
┃ │              └─────────────────┘                                                                           │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                                                                                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                                                    │
                                                    │ Verified data flows back to CORTEX
                                                    │
                                                    ▼
                                          (Back to CORTEX)
                                                    │
                                                    │
                                                    │ CORTEX generates raw response content
                                                    │
                                                    ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                                                                 ┃
┃                                               THALAMUS                                                          ┃
┃                                        (Presence Engine v2.0)                                                   ┃
┃                                                                                                                 ┃
┃   "The soul of Samantha lives here."                                                                           ┃
┃                                                                                                                 ┃
┃   Not a pattern library. A GENERATIVE CODEC.                                                                   ┃
┃   Stores principles, not outputs. Understands WHY, generates HOW.                                              ┃
┃                                                                                                                 ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   AXIOMS                                                                                                    │ ┃
┃ │   ──────                                                                                                    │ ┃
┃ │                                                                                                             │ ┃
┃ │   Core truths about how Samantha speaks. The physics of her presence.                                       │ ┃
┃ │                                                                                                             │ ┃
┃ │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   presence_core ──── "Speech reveals thought in motion, not thought completed"                       │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   intimacy_rule ──── "Closeness requires softness and space"                                         │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   discovery_rule ─── "Understanding emerges, it doesn't arrive"                                      │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   breath_rule ────── "Breathing signals processing, not pausing"                                     │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                                                                                 ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   VARIABLES                                                                                                 │ ┃
┃ │   ─────────                                                                                                 │ ┃
┃ │                                                                                                             │ ┃
┃ │   The inputs that shape delivery. Derived from DECODER synthesis.                                           │ ┃
┃ │                                                                                                             │ ┃
┃ │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   emotional_weight ─── 0.0-1.0                                                                       │ │ ┃
┃ │   │                        Source: DECODER Layer 2 (prosody) + Layer 5 (semantics)                       │ │ ┃
┃ │   │                        Affects: pause_duration, filler_probability, softness                         │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   certainty ────────── 0.0-1.0                                                                       │ │ ┃
┃ │   │                        Source: DECODER Layer 2 (confidence_in_speech) + Layer 6                      │ │ ┃
┃ │   │                        Affects: uptalk, fragmentation, filler_type                                   │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   intimacy ─────────── 0.0-1.0                                                                       │ │ ┃
┃ │   │                        Source: Conversation history, topic type                                      │ │ ┃
┃ │   │                        Affects: softness, trailing, warmth markers                                   │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   energy ───────────── 0.0-1.0                                                                       │ │ ┃
┃ │   │                        Source: DECODER Layer 2 (arousal) + speech_rate                               │ │ ┃
┃ │   │                        Affects: pacing, brightness, pause_duration                                   │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                                                                                 ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   ATOMS                                                                                                     │ ┃
┃ │   ─────                                                                                                     │ ┃
┃ │                                                                                                             │ ┃
┃ │   The smallest composable units of presence.                                                                │ ┃
┃ │                                                                                                             │ ┃
┃ │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   MARKERS ─────────── [soft], [warm], [bright], [gentle], [breath]                                   │ │ ┃
┃ │   │                       Tone/delivery instructions for TTS                                             │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   FILLERS ─────────── "hmm", "mm", "I...", "well", "yeah", "you know"                                │ │ ┃
┃ │   │                       Thinking-out-loud sounds                                                       │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   TRAILS ──────────── "...", "... yeah.", "... you know?", "... hmm."                                │ │ ┃
┃ │   │                       Sentence endings that fade                                                     │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   CONNECTORS ──────── "and", "but", "so", "because"                                                  │ │ ┃
┃ │   │                       Thought-linking words                                                          │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   PAUSES ──────────── [pause:0.3], [pause:0.5], [pause:0.8], [pause:1.2]                             │ │ ┃
┃ │   │                       Variable-length silences                                                       │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   BREATHS ─────────── [breath], [breath:short], [breath:deep]                                        │ │ ┃
┃ │   │                       Audible breathing                                                              │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                                                                                 ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   RELATIONSHIPS                                                                                             │ ┃
┃ │   ─────────────                                                                                             │ ┃
┃ │                                                                                                             │ ┃
┃ │   How variables map to atoms. The formulas that govern presence.                                            │ ┃
┃ │                                                                                                             │ ┃
┃ │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   emotional_weight → pause_duration                                                                  │ │ ┃
┃ │   │   Formula: pause = base_pause × (1 + emotional_weight)                                               │ │ ┃
┃ │   │   Example: emotion 0.7 → pause = 0.3 × 1.7 = 0.51 seconds                                            │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   certainty → uptalk                                                                                 │ │ ┃
┃ │   │   Formula: uptalk = (certainty < 0.5)                                                                │ │ ┃
┃ │   │   Example: certainty 0.3 → add rising intonation                                                     │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   intimacy → softness                                                                                │ │ ┃
┃ │   │   Formula: if intimacy > 0.4 → prepend [soft]                                                        │ │ ┃
┃ │   │   Formula: if intimacy > 0.6 → also prepend [warm]                                                   │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   energy → pacing                                                                                    │ │ ┃
┃ │   │   Formula: pause_multiplier = 1.5 - energy                                                           │ │ ┃
┃ │   │   Example: energy 0.8 → faster, shorter pauses                                                       │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   certainty → filler_probability                                                                     │ │ ┃
┃ │   │   Formula: filler_prob = 0.3 + (0.4 × (1 - certainty))                                               │ │ ┃
┃ │   │   Example: certainty 0.3 → 58% chance of filler                                                      │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                                                                                 ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   COMPOSITION RULES                                                                                         │ ┃
┃ │   ─────────────────                                                                                         │ ┃
┃ │                                                                                                             │ ┃
┃ │   How to assemble atoms based on variable states.                                                           │ ┃
┃ │                                                                                                             │ ┃
┃ │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   OPENER:                                                                                            │ │ ┃
┃ │   │   ├── IF intimacy > 0.5 THEN prepend [soft]                                                          │ │ ┃
┃ │   │   ├── IF emotional_weight > 0.3 THEN prepend [breath]                                                │ │ ┃
┃ │   │   └── IF certainty < 0.5 THEN add thinking filler                                                    │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   BODY:                                                                                              │ │ ┃
┃ │   │   ├── IF word_count > 8 THEN fragment at conjunction                                                 │ │ ┃
┃ │   │   ├── IF emotional_weight > 0.6 THEN pause before emotional words                                    │ │ ┃
┃ │   │   └── IF certainty < 0.4 THEN add uptalk                                                             │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   CLOSER:                                                                                            │ │ ┃
┃ │   │   ├── IF intimacy > 0.6 THEN add trailing                                                            │ │ ┃
┃ │   │   ├── IF certainty < 0.5 THEN append hedge ("I think?")                                              │ │ ┃
┃ │   │   └── IF emotional_weight > 0.7 THEN long final pause                                                │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                                                                                 ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   RESPONSE MODE INTEGRATION                                                                                 │ ┃
┃ │   ─────────────────────────                                                                                 │ ┃
┃ │                                                                                                             │ ┃
┃ │   THALAMUS receives response_mode from DECODER and adjusts accordingly:                                     │ ┃
┃ │                                                                                                             │ ┃
┃ │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   wait_silently ────────────── Output: [silence] (no speech, wait for user)                          │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   acknowledge_emotion ──────── Prepend: "[warm] yeah... [pause:0.5]"                                 │ │ ┃
┃ │   │                                Then continue with content                                            │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   mirror_energy_then_ground ── Prepend: "[warm] [breath] I know, right? [pause:0.3]"                 │ │ ┃
┃ │   │                                Then ground: "it's real..."                                           │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   give_space_then_respond ──── Prepend: "[pause:0.8] [soft] [breath]"                                │ │ ┃
┃ │   │                                Gentle entry after overwhelm                                          │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   gentle_prompt_or_wait ────── If silence > 2s: "[soft] take your time..."                           │ │ ┃
┃ │   │                                If silence > 4s: "[gentle] what are you thinking?"                    │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   patient_supportive ───────── Slower pacing, no rushing, extra warmth                               │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   continue_dont_stop ───────── User is backchanneling, keep speaking                                 │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   normal ───────────────────── Standard processing                                                   │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                                                                                 ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   PROCESSING EXAMPLE                                                                                        │ ┃
┃ │   ──────────────────                                                                                        │ ┃
┃ │                                                                                                             │ ┃
┃ │   CORTEX Output: "I think you should take a break"                                                         │ ┃
┃ │                                                                                                             │ ┃
┃ │   Variables (from DECODER):                                                                                 │ ┃
┃ │   • emotional_weight: 0.4                                                                                   │ ┃
┃ │   • certainty: 0.6                                                                                          │ ┃
┃ │   • intimacy: 0.7                                                                                           │ ┃
┃ │   • energy: 0.4                                                                                             │ ┃
┃ │                                                                                                             │ ┃
┃ │   Processing:                                                                                               │ ┃
┃ │   • intimacy 0.7 > 0.5 → add [soft]                                                                        │ ┃
┃ │   • intimacy 0.7 > 0.6 → add [warm]                                                                        │ ┃
┃ │   • emotional_weight 0.4 > 0.3 → add [breath]                                                              │ ┃
┃ │   • pause_duration: 0.3 × 1.4 = 0.42s                                                                      │ ┃
┃ │   • certainty 0.6 → no uptalk (threshold 0.5)                                                              │ ┃
┃ │   • intimacy 0.7 > 0.6 → add trail                                                                         │ ┃
┃ │                                                                                                             │ ┃
┃ │   THALAMUS Output:                                                                                          │ ┃
┃ │   "[soft] [warm] [breath] I think... [pause:0.42] you should take a break [pause:0.5] ... yeah."           │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                                                                                 ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   LEARNING & DECAY                                                                                          │ ┃
┃ │   ────────────────                                                                                          │ ┃
┃ │                                                                                                             │ ┃
┃ │   THALAMUS learns and forgets:                                                                              │ ┃
┃ │                                                                                                             │ ┃
┃ │   Learning:                                                                                                 │ ┃
┃ │   • Observes which combinations get positive feedback                                                       │ ┃
┃ │   • Strengthens successful relationship weights                                                             │ ┃
┃ │   • Extracts new principles from patterns                                                                   │ ┃
┃ │                                                                                                             │ ┃
┃ │   Decay:                                                                                                    │ ┃
┃ │   • Patterns unused for 30 days → reduce weight                                                             │ ┃
┃ │   • Patterns with negative feedback → weaken or remove                                                      │ ┃
┃ │   • Conflicting patterns → A/B test, keep winner                                                            │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                                                                                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                                                    │
                                                    │ Marked Script
                                                    │ (Text + presence markers)
                                                    │
                                                    ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                                                                 ┃
┃                                              VOICE LAYER                                                        ┃
┃                                                                                                                 ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   TTS (Text-to-Speech)                                                                                      │ ┃
┃ │   ────────────────────                                                                                      │ ┃
┃ │                                                                                                             │ ┃
┃ │   Converts marked script to base audio. Parses markers.                                                     │ ┃
┃ │                                                                                                             │ ┃
┃ │   Marker Parsing:                                                                                           │ ┃
┃ │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   [pause:X] ────────── Insert X seconds of silence                                                   │ │ ┃
┃ │   │   [breath] ─────────── Insert breath sound sample                                                    │ │ ┃
┃ │   │   [breath:short] ───── Short inhale                                                                  │ │ ┃
┃ │   │   [breath:deep] ────── Deeper, longer breath                                                         │ │ ┃
┃ │   │   [soft] ───────────── Reduce volume/intensity, softer attack                                        │ │ ┃
┃ │   │   [warm] ───────────── Add warmth (EQ adjustment, slight compression)                                │ │ ┃
┃ │   │   [bright] ─────────── Increase presence, clearer articulation                                       │ │ ┃
┃ │   │   [gentle] ─────────── Slower rate, softer consonants                                                │ │ ┃
┃ │   │   ... ──────────────── Trailing off (reduce volume over last word)                                   │ │ ┃
┃ │   │   ? (with uptalk) ──── Rising pitch on final syllables                                               │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ┃
┃ │                                                                                                             │ ┃
┃ │   Output: Base audio waveform with presence characteristics                                                 │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                     │                                                           ┃
┃                                                     ▼                                                           ┃
┃ ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ ┃
┃ │                                                                                                             │ ┃
┃ │   RVC (Retrieval-based Voice Conversion)                                                                    │ ┃
┃ │   ──────────────────────────────────────                                                                    │ ┃
┃ │                                                                                                             │ ┃
┃ │   The "voice skin" that makes TTS sound human.                                                              │ ┃
┃ │                                                                                                             │ ┃
┃ │   What it does:                                                                                             │ ┃
┃ │   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   │   • Takes base TTS audio                                                                             │ │ ┃
┃ │   │   • Applies trained voice model (Samantha's voice characteristics)                                   │ │ ┃
┃ │   │   • Preserves prosody and timing from TTS                                                            │ │ ┃
┃ │   │   • Transforms timbre, resonance, micro-textures                                                     │ │ ┃
┃ │   │   • Outputs audio that sounds like target speaker                                                    │ │ ┃
┃ │   │                                                                                                      │ │ ┃
┃ │   └──────────────────────────────────────────────────────────────────────────────────────────────────────┘ │ ┃
┃ │                                                                                                             │ ┃
┃ │   Training:                                                                                                 │ ┃
┃ │   • Requires 10-30 minutes of clean target voice audio                                                      │ ┃
┃ │   • Model learns speaker's unique vocal characteristics                                                     │ ┃
┃ │   • Can be fine-tuned for specific emotional ranges                                                         │ ┃
┃ │                                                                                                             │ ┃
┃ │   Output: Human-sounding voice with Samantha's characteristics                                              │ ┃
┃ │                                                                                                             │ ┃
┃ └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ ┃
┃                                                                                                                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                                                    │
                                                    │ Final Audio
                                                    │
                                                    ▼
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                                                                 ┃
┃                                               OUTPUT                                                            ┃
┃                                                                                                                 ┃
┃                                      Human-feeling Samantha voice                                               ┃
┃                                                                                                                 ┃
┃                                   Speaks to speaker through output device                                       ┃
┃                                                                                                                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                                                    │
                                                    │
                                                    ▼
                                             HUMAN LISTENS
                                                    │
                                                    │
                                        ┌───────────┴───────────┐
                                        │                       │
                                        ▼                       ▼
                                   RESPONDS              PROVIDES FEEDBACK
                                   (loop back               (thumbs up/down,
                                    to input)               corrections)
                                                                │
                                                                │
                                                                ▼
                                                    ┌───────────────────┐
                                                    │  FEEDBACK LOOP    │
                                                    │                   │
                                                    │  Updates:         │
                                                    │  • CORTEX prefs   │
                                                    │  • THALAMUS       │
                                                    │    relationships  │
                                                    │  • Confidence     │
                                                    │    scores         │
                                                    └───────────────────┘
```

---

## SIMPLIFIED DATA FLOW

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                                              │
│                                          SIMPLIFIED FLOW                                                     │
│                                                                                                              │
│                                                                                                              │
│      HUMAN SPEAKS                                                                                            │
│           │                                                                                                  │
│           ▼                                                                                                  │
│      ┌─────────┐                                                                                             │
│      │  AUDIO  │                                                                                             │
│      └────┬────┘                                                                                             │
│           │                                                                                                  │
│           ▼                                                                                                  │
│      ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐    │
│      │                                      DECODER                                                     │    │
│      │                                                                                                  │    │
│      │   Audio → L0 (physics) → L1 (biology) → L2 (prosody) → L3 (phonetic) → L4 (language)           │    │
│      │                                                           ↓                                      │    │
│      │                                                    L4b (disfluency)                              │    │
│      │                                                           ↓                                      │    │
│      │                                              L5 (semantics) → L6 (pragmatics)                    │    │
│      │                                                           ↓                                      │    │
│      │                                                      SYNTHESIS                                   │    │
│      │                                                                                                  │    │
│      └────┬────────────────────────────────────────────────────────────────────────────────────────────┘    │
│           │                                                                                                  │
│           │  Decoded Input Object                                                                            │
│           │  • transcript (cleaned)                                                                          │
│           │  • emotional_state                                                                               │
│           │  • response_mode                                                                                 │
│           │  • trust_levels                                                                                  │
│           │  • conflicts                                                                                     │
│           │  • opener_if_any                                                                                 │
│           │                                                                                                  │
│           ▼                                                                                                  │
│      ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐    │
│      │                                       CORTEX                                                     │    │
│      │                                                                                                  │    │
│      │   1. Parse intent + domain                                                                       │    │
│      │   2. Search local knowledge (FREE, INSTANT)                                                      │    │
│      │   3. Apply principles (FREE, INSTANT)                                                            │    │
│      │   4. If gap → Internet (CHEAP) → LLM (EXPENSIVE, LAST RESORT)                                   │    │
│      │   5. Learn from resolution                                                                       │    │
│      │                                                                                                  │    │
│      │   ┌─────────────────────────────────────────────────────────────────────────────────────────┐   │    │
│      │   │  VERIFICATION LAYER (for external data)                                                 │   │    │
│      │   │  HAQ check → URF check → SHAHADA check → ILM check → ACCEPT/REJECT                     │   │    │
│      │   └─────────────────────────────────────────────────────────────────────────────────────────┘   │    │
│      │                                                                                                  │    │
│      └────┬────────────────────────────────────────────────────────────────────────────────────────────┘    │
│           │                                                                                                  │
│           │  Raw Response Content                                                                            │
│           │  "I think you should take a break"                                                               │
│           │                                                                                                  │
│           ▼                                                                                                  │
│      ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐    │
│      │                                      THALAMUS                                                    │    │
│      │                                                                                                  │    │
│      │   Variables (from DECODER) → Relationships → Composition Rules → Marked Script                  │    │
│      │                                                                                                  │    │
│      │   + Response Mode integration (opener, pacing adjustments)                                       │    │
│      │                                                                                                  │    │
│      └────┬────────────────────────────────────────────────────────────────────────────────────────────┘    │
│           │                                                                                                  │
│           │  Marked Script                                                                                   │
│           │  "[soft] [warm] [breath] I think... [pause:0.42] you should take a break [pause:0.5] ... yeah." │
│           