<think>The user wants to build the full-duplex conversation system. This is a major architectural component that will make Samantha feel like a real conversational partner rather than a walkie-talkie assistant.

Let me break this down into implementable components:

1. **Streaming Audio I/O** - Continuous input and output, not batch
2. **Streaming Decoder** - Real-time analysis, not wait-for-silence
3. **Conversation State Machine** - Track who's speaking, manage transitions
4. **Turn Predictor** - Predict when human is about to stop
5. **Backchannel Engine** - Generate "mmhm", "yeah" while listening
6. **Response Buffer** - Prepare response while human speaks
7. **Overlap Manager** - Handle collisions gracefully
8. **Interruption Handler** - Both directions

I should structure this as a complete system design with:
- Architecture diagram
- State machine definition
- Component specifications
- Data flow
- Implementation details
- Code structure

This is going to be a substantial response but the user wants to build it, so they need the full blueprint.</think># FULL-DUPLEX CONVERSATION ENGINE
## Complete Build Specification

---

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│                              "NOT WALKIE-TALKIE"                                │
│                                                                                 │
│                    A system that converses, not responds.                       │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## COMPONENT OVERVIEW

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│   1. AUDIO STREAM MANAGER          Continuous I/O, never closes                 │
│   2. STREAMING DECODER             Real-time analysis, chunk by chunk           │
│   3. VOICE ACTIVITY DETECTOR       Who is speaking right now?                   │
│   4. CONVERSATION STATE MACHINE    The brain of turn-taking                     │
│   5. TURN PREDICTOR                When will human stop?                        │
│   6. BACKCHANNEL ENGINE            "mmhm", "yeah", "oh!" while listening       │
│   7. RESPONSE GENERATOR            Prepares response in parallel                │
│   8. OUTPUT CONTROLLER             Manages what goes to speaker                 │
│   9. INTERRUPTION HANDLER          Collision resolution                         │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. AUDIO STREAM MANAGER

```python
import numpy as np
import threading
import queue
from dataclasses import dataclass
from typing import Callable, Optional
import sounddevice as sd

@dataclass
class AudioChunk:
    """Single chunk of audio data with metadata."""
    data: np.ndarray
    timestamp: float
    duration_ms: float
    sample_rate: int
    channel: str  # 'input' or 'output'

class AudioStreamManager:
    """
    Manages continuous bidirectional audio.
    Both input and output are ALWAYS open.
    """
    
    def __init__(
        self,
        sample_rate: int = 16000,
        chunk_duration_ms: int = 50,  # 50ms chunks for low latency
        channels: int = 1
    ):
        self.sample_rate = sample_rate
        self.chunk_duration_ms = chunk_duration_ms
        self.chunk_size = int(sample_rate * chunk_duration_ms / 1000)
        self.channels = channels
        
        # Queues for async communication
        self.input_queue = queue.Queue()   # Incoming audio chunks
        self.output_queue = queue.Queue()  # Outgoing audio chunks
        
        # State
        self.is_running = False
        self.current_time = 0.0
        
        # Callbacks
        self.on_input_chunk: Optional[Callable[[AudioChunk], None]] = None
        
        # Output state
        self.output_buffer = np.array([], dtype=np.float32)
        self.output_lock = threading.Lock()
        
    def start(self):
        """Start continuous audio streams."""
        self.is_running = True
        self.current_time = 0.0
        
        # Start input stream
        self.input_stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            blocksize=self.chunk_size,
            callback=self._input_callback
        )
        
        # Start output stream
        self.output_stream = sd.OutputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            blocksize=self.chunk_size,
            callback=self._output_callback
        )
        
        self.input_stream.start()
        self.output_stream.start()
        
    def stop(self):
        """Stop audio streams."""
        self.is_running = False
        self.input_stream.stop()
        self.output_stream.stop()
        
    def _input_callback(self, indata, frames, time, status):
        """Called for each input chunk."""
        if not self.is_running:
            return
            
        chunk = AudioChunk(
            data=indata.copy().flatten(),
            timestamp=self.current_time,
            duration_ms=self.chunk_duration_ms,
            sample_rate=self.sample_rate,
            channel='input'
        )
        
        self.current_time += self.chunk_duration_ms / 1000
        
        # Put in queue for processing
        self.input_queue.put(chunk)
        
        # Call callback if registered
        if self.on_input_chunk:
            self.on_input_chunk(chunk)
            
    def _output_callback(self, outdata, frames, time, status):
        """Called when output needs data."""
        with self.output_lock:
            if len(self.output_buffer) >= frames:
                # Have enough data
                outdata[:, 0] = self.output_buffer[:frames]
                self.output_buffer = self.output_buffer[frames:]
            elif len(self.output_buffer) > 0:
                # Have some data, pad with silence
                outdata[:len(self.output_buffer), 0] = self.output_buffer
                outdata[len(self.output_buffer):, 0] = 0
                self.output_buffer = np.array([], dtype=np.float32)
            else:
                # No data, output silence
                outdata.fill(0)
                
    def queue_output(self, audio: np.ndarray):
        """Add audio to output buffer."""
        with self.output_lock:
            self.output_buffer = np.concatenate([
                self.output_buffer,
                audio.astype(np.float32)
            ])
            
    def clear_output(self):
        """Clear output buffer (for interruption)."""
        with self.output_lock:
            self.output_buffer = np.array([], dtype=np.float32)
            
    def get_output_buffer_duration_ms(self) -> float:
        """How much audio is queued for output."""
        with self.output_lock:
            return len(self.output_buffer) / self.sample_rate * 1000
```

---

## 2. STREAMING DECODER

```python
from collections import deque
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
import numpy as np

class SpeakingState(Enum):
    SILENCE = "silence"
    SPEECH = "speech"
    UNCERTAIN = "uncertain"

@dataclass
class StreamingFeatures:
    """Real-time features from current audio window."""
    timestamp: float
    
    # Voice Activity
    speaking_state: SpeakingState
    speech_probability: float
    
    # Physical (Layer 0) - computed on rolling window
    current_energy: float
    current_pitch: Optional[float]
    pitch_direction: str  # 'rising', 'falling', 'flat', 'unknown'
    
    # Biological (Layer 1)
    stress_level: float
    
    # Prosody (Layer 2)
    emotion_estimate: str
    emotion_confidence: float
    arousal: float
    
    # Partial transcript
    partial_transcript: str
    transcript_is_final: bool
    
    # Turn signals
    turn_hold_probability: float      # Probability speaker will continue
    turn_yield_probability: float     # Probability speaker is done
    
@dataclass
class StreamingDecoderState:
    """Accumulating state across chunks."""
    
    # Rolling audio buffer (last N seconds)
    audio_buffer: deque = field(default_factory=lambda: deque(maxlen=100))  # ~5s at 50ms chunks
    
    # Feature history
    energy_history: deque = field(default_factory=lambda: deque(maxlen=50))
    pitch_history: deque = field(default_factory=lambda: deque(maxlen=50))
    
    # Speech state tracking
    speech_onset_time: Optional[float] = None
    silence_onset_time: Optional[float] = None
    
    # Accumulated transcript
    full_transcript: str = ""
    pending_transcript: str = ""
    
    # Detected patterns
    word_count: int = 0
    pause_count: int = 0
    filler_count: int = 0
    
class StreamingDecoder:
    """
    Decodes audio in real-time, chunk by chunk.
    Does NOT wait for utterance to complete.
    """
    
    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self.state = StreamingDecoderState()
        
        # Thresholds (tunable)
        self.energy_threshold = 0.01
        self.silence_duration_for_turn_end = 0.7  # 700ms silence = probably done
        self.min_speech_duration = 0.1  # 100ms minimum to count as speech
        
        # External ASR (streaming mode)
        self.asr = self._init_streaming_asr()
        
    def _init_streaming_asr(self):
        """Initialize streaming ASR (Whisper, Vosk, or similar)."""
        # Placeholder - would use actual streaming ASR
        # Options: vosk, whisper-streaming, deepgram, assembly
        pass
        
    def process_chunk(self, chunk: AudioChunk) -> StreamingFeatures:
        """
        Process single audio chunk.
        Returns current features based on this chunk + recent history.
        """
        
        # Add to buffer
        self.state.audio_buffer.append(chunk)
        
        # Compute features on this chunk
        energy = self._compute_energy(chunk.data)
        pitch = self._compute_pitch(chunk.data)
        
        # Update history
        self.state.energy_history.append(energy)
        if pitch:
            self.state.pitch_history.append(pitch)
            
        # Determine speaking state
        speaking_state, speech_prob = self._detect_speech(energy)
        
        # Update speech/silence timing
        self._update_timing(speaking_state, chunk.timestamp)
        
        # Compute pitch direction from history
        pitch_direction = self._compute_pitch_direction()
        
        # Get partial transcript
        partial_transcript, is_final = self._get_transcript_update(chunk)
        
        # Estimate emotion from prosody
        emotion, emotion_conf, arousal = self._estimate_emotion()
        
        # Compute turn probabilities
        turn_hold, turn_yield = self._compute_turn_probabilities(
            speaking_state, pitch_direction, partial_transcript
        )
        
        return StreamingFeatures(
            timestamp=chunk.timestamp,
            speaking_state=speaking_state,
            speech_probability=speech_prob,
            current_energy=energy,
            current_pitch=pitch,
            pitch_direction=pitch_direction,
            stress_level=self._estimate_stress(),
            emotion_estimate=emotion,
            emotion_confidence=emotion_conf,
            arousal=arousal,
            partial_transcript=partial_transcript,
            transcript_is_final=is_final,
            turn_hold_probability=turn_hold,
            turn_yield_probability=turn_yield
        )
        
    def _compute_energy(self, audio: np.ndarray) -> float:
        """RMS energy of chunk."""
        return float(np.sqrt(np.mean(audio ** 2)))
        
    def _compute_pitch(self, audio: np.ndarray) -> Optional[float]:
        """Extract pitch from chunk. Returns None if unvoiced."""
        # Simplified - would use librosa.pyin or similar
        # For now, use autocorrelation
        if len(audio) < 256:
            return None
            
        # Basic autocorrelation pitch detection
        corr = np.correlate(audio, audio, mode='full')
        corr = corr[len(corr)//2:]
        
        # Find first peak after initial decay
        d = np.diff(corr)
        start = np.where(d > 0)[0]
        
        if len(start) == 0:
            return None
            
        peak = np.argmax(corr[start[0]:]) + start[0]
        
        if peak == 0:
            return None
            
        pitch = self.sample_rate / peak
        
        # Sanity check for human voice range
        if 50 < pitch < 500:
            return pitch
        return None
        
    def _detect_speech(self, energy: float) -> tuple[SpeakingState, float]:
        """Detect if current chunk contains speech."""
        
        # Simple energy-based VAD
        # In production, use WebRTC VAD or similar
        
        if energy > self.energy_threshold * 2:
            return SpeakingState.SPEECH, 0.9
        elif energy > self.energy_threshold:
            return SpeakingState.UNCERTAIN, 0.5
        else:
            return SpeakingState.SILENCE, 0.1
            
    def _update_timing(self, state: SpeakingState, timestamp: float):
        """Track speech/silence onset times."""
        
        if state == SpeakingState.SPEECH:
            if self.state.speech_onset_time is None:
                self.state.speech_onset_time = timestamp
            self.state.silence_onset_time = None
            
        elif state == SpeakingState.SILENCE:
            if self.state.silence_onset_time is None:
                self.state.silence_onset_time = timestamp
            # Don't reset speech_onset_time yet - might be brief pause
            
    def _compute_pitch_direction(self) -> str:
        """Determine pitch trend from recent history."""
        
        if len(self.state.pitch_history) < 5:
            return 'unknown'
            
        recent = list(self.state.pitch_history)[-10:]
        
        if len(recent) < 3:
            return 'unknown'
            
        # Simple linear trend
        first_half = np.mean(recent[:len(recent)//2])
        second_half = np.mean(recent[len(recent)//2:])
        
        diff = second_half - first_half
        
        if diff > 10:
            return 'rising'
        elif diff < -10:
            return 'falling'
        else:
            return 'flat'
            
    def _get_transcript_update(self, chunk: AudioChunk) -> tuple[str, bool]:
        """Get latest transcript from streaming ASR."""
        # Placeholder - would integrate with streaming ASR
        # Returns (partial_text, is_final)
        return self.state.pending_transcript, False
        
    def _estimate_emotion(self) -> tuple[str, float, float]:
        """Estimate emotion from prosodic features."""
        
        if len(self.state.energy_history) < 10:
            return 'neutral', 0.5, 0.5
            
        recent_energy = list(self.state.energy_history)[-10:]
        energy_mean = np.mean(recent_energy)
        energy_var = np.var(recent_energy)
        
        recent_pitch = list(self.state.pitch_history)[-10:] if self.state.pitch_history else []
        
        # Simple heuristics (would be ML model in production)
        arousal = min(1.0, energy_mean * 10 + energy_var * 5)
        
        if energy_var > 0.01 and arousal > 0.6:
            return 'excited', 0.6, arousal
        elif arousal < 0.3:
            return 'calm', 0.6, arousal
        else:
            return 'neutral', 0.5, arousal
            
    def _estimate_stress(self) -> float:
        """Estimate stress from voice characteristics."""
        # Simplified - would analyze jitter, shimmer, etc.
        if len(self.state.energy_history) < 10:
            return 0.0
            
        energy_var = np.var(list(self.state.energy_history)[-10:])
        return min(1.0, energy_var * 10)
        
    def _compute_turn_probabilities(
        self,
        speaking_state: SpeakingState,
        pitch_direction: str,
        transcript: str
    ) -> tuple[float, float]:
        """
        Predict turn-taking probabilities.
        
        Returns:
            turn_hold: probability speaker will continue
            turn_yield: probability speaker is done
        """
        
        # Base on speaking state
        if speaking_state == SpeakingState.SPEECH:
            hold = 0.8
            yield_ = 0.2
        elif speaking_state == SpeakingState.SILENCE:
            # Check silence duration
            if self.state.silence_onset_time:
                silence_duration = 0  # Would compute from current time
                if silence_duration > self.silence_duration_for_turn_end:
                    hold = 0.1
                    yield_ = 0.9
                else:
                    hold = 0.5
                    yield_ = 0.5
            else:
                hold = 0.5
                yield_ = 0.5
        else:
            hold = 0.5
            yield_ = 0.5
            
        # Adjust for pitch direction
        if pitch_direction == 'falling':
            # Falling pitch = statement ending
            yield_ = min(1.0, yield_ + 0.2)
            hold = max(0.0, hold - 0.2)
        elif pitch_direction == 'rising':
            # Rising pitch = question or continuation
            # Could be question (yield) or list continuation (hold)
            pass
            
        # Adjust for transcript content
        if transcript:
            lower = transcript.lower().strip()
            
            # Turn-yielding phrases
            yield_phrases = ['right?', 'you know?', 'what do you think?', 
                           'anyway', 'so yeah', 'that\'s it']
            for phrase in yield_phrases:
                if lower.endswith(phrase):
                    yield_ = min(1.0, yield_ + 0.3)
                    hold = max(0.0, hold - 0.3)
                    
            # Turn-holding phrases
            hold_phrases = ['and', 'but', 'so', 'because', 'like']
            for phrase in hold_phrases:
                if lower.endswith(phrase):
                    hold = min(1.0, hold + 0.3)
                    yield_ = max(0.0, yield_ - 0.3)
                    
        return hold, yield_
        
    def reset(self):
        """Reset decoder state for new conversation."""
        self.state = StreamingDecoderState()
```

---

## 3. VOICE ACTIVITY DETECTOR

```python
from enum import Enum
from dataclasses import dataclass
from typing import Optional
import time

class Speaker(Enum):
    NONE = "none"
    HUMAN = "human"
    SAMANTHA = "samantha"
    BOTH = "both"

@dataclass
class VADState:
    """Current voice activity state."""
    human_speaking: bool
    samantha_speaking: bool
    human_speech_duration: float
    samantha_speech_duration: float
    silence_duration: float
    last_human_speech_end: Optional[float]
    last_samantha_speech_end: Optional[float]
    
    @property
    def current_speaker(self) -> Speaker:
        if self.human_speaking and self.samantha_speaking:
            return Speaker.BOTH
        elif self.human_speaking:
            return Speaker.HUMAN
        elif self.samantha_speaking:
            return Speaker.SAMANTHA
        else:
            return Speaker.NONE

class VoiceActivityDetector:
    """
    Tracks who is currently speaking.
    Monitors both human input and Samantha output.
    """
    
    def __init__(self):
        self.state = VADState(
            human_speaking=False,
            samantha_speaking=False,
            human_speech_duration=0.0,
            samantha_speech_duration=0.0,
            silence_duration=0.0,
            last_human_speech_end=None,
            last_samantha_speech_end=None
        )
        
        self._human_speech_start: Optional[float] = None
        self._samantha_speech_start: Optional[float] = None
        self._silence_start: Optional[float] = None
        
        # Callbacks
        self.on_human_speech_start: Optional[callable] = None
        self.on_human_speech_end: Optional[callable] = None
        self.on_overlap_start: Optional[callable] = None
        
    def update_human(self, is_speaking: bool, timestamp: float):
        """Update human speaking state."""
        
        was_speaking = self.state.human_speaking
        
        if is_speaking and not was_speaking:
            # Human started speaking
            self._human_speech_start = timestamp
            self.state.human_speaking = True
            
            # Check for overlap
            if self.state.samantha_speaking and self.on_overlap_start:
                self.on_overlap_start(timestamp)
                
            if self.on_human_speech_start:
                self.on_human_speech_start(timestamp)
                
        elif not is_speaking and was_speaking:
            # Human stopped speaking
            if self._human_speech_start:
                self.state.human_speech_duration = timestamp - self._human_speech_start
            self.state.human_speaking = False
            self.state.last_human_speech_end = timestamp
            
            if self.on_human_speech_end:
                self.on_human_speech_end(timestamp, self.state.human_speech_duration)
                
        # Update silence tracking
        if not is_speaking and not self.state.samantha_speaking:
            if self._silence_start is None:
                self._silence_start = timestamp
            self.state.silence_duration = timestamp - self._silence_start
        else:
            self._silence_start = None
            self.state.silence_duration = 0.0
            
    def update_samantha(self, is_speaking: bool, timestamp: float):
        """Update Samantha speaking state."""
        
        was_speaking = self.state.samantha_speaking
        
        if is_speaking and not was_speaking:
            # Samantha started speaking
            self._samantha_speech_start = timestamp
            self.state.samantha_speaking = True
            
        elif not is_speaking and was_speaking:
            # Samantha stopped speaking
            if self._samantha_speech_start:
                self.state.samantha_speech_duration = timestamp - self._samantha_speech_start
            self.state.samantha_speaking = False
            self.state.last_samantha_speech_end = timestamp
            
        # Update silence tracking
        if not is_speaking and not self.state.human_speaking:
            if self._silence_start is None:
                self._silence_start = timestamp
            self.state.silence_duration = timestamp - self._silence_start
        else:
            self._silence_start = None
            self.state.silence_duration = 0.0
            
    def get_state(self) -> VADState:
        return self.state
```

---

## 4. CONVERSATION STATE MACHINE

```python
from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, Callable, List
import time

class ConversationState(Enum):
    """Possible conversation states."""
    
    IDLE = auto()                    # No one speaking, waiting
    HUMAN_SPEAKING = auto()          # Human has the floor
    SAMANTHA_SPEAKING = auto()       # Samantha has the floor
    HUMAN_YIELDING = auto()          # Human finishing, about to yield
    SAMANTHA_YIELDING = auto()       # Samantha finishing, about to yield
    OVERLAP_HUMAN_PRIORITY = auto()  # Both speaking, human wins
    OVERLAP_SAMANTHA_YIELD = auto()  # Both speaking, Samantha backing off
    TRANSITION_TO_SAMANTHA = auto()  # Brief pause, Samantha about to speak
    TRANSITION_TO_HUMAN = auto()     # Brief pause, human about to speak

@dataclass
class StateTransition:
    """Record of a state transition."""
    from_state: ConversationState
    to_state: ConversationState
    trigger: str
    timestamp: float

class ConversationStateMachine:
    """
    Manages conversation turn-taking.
    The brain that decides who speaks when.
    """
    
    def __init__(self):
        self.state = ConversationState.IDLE
        self.state_enter_time: float = time.time()
        self.history: List[StateTransition] = []
        
        # Timing parameters (tunable)
        self.min_response_delay = 0.2      # Minimum pause before responding
        self.max_response_delay = 0.8      # Maximum pause (feels unnatural beyond)
        self.yield_timeout = 0.7           # Silence duration to assume yield
        self.backchannel_window = 0.3      # Window for backchannel detection
        
        # Callbacks
        self.on_state_change: Optional[Callable[[ConversationState, ConversationState], None]] = None
        self.on_samantha_should_speak: Optional[Callable[[], None]] = None
        self.on_samantha_should_stop: Optional[Callable[[], None]] = None
        self.on_samantha_should_backchannel: Optional[Callable[[str], None]] = None
        
    def transition(self, new_state: ConversationState, trigger: str):
        """Transition to a new state."""
        
        if new_state == self.state:
            return
            
        old_state = self.state
        
        # Record transition
        self.history.append(StateTransition(
            from_state=old_state,
            to_state=new_state,
            trigger=trigger,
            timestamp=time.time()
        ))
        
        # Update state
        self.state = new_state
        self.state_enter_time = time.time()
        
        # Fire callback
        if self.on_state_change:
            self.on_state_change(old_state, new_state)
            
        # Handle state-specific actions
        self._handle_state_entry(new_state, old_state)
        
    def _handle_state_entry(self, new_state: ConversationState, old_state: ConversationState):
        """Handle actions when entering a state."""
        
        if new_state == ConversationState.TRANSITION_TO_SAMANTHA:
            # Schedule Samantha to speak after brief delay
            if self.on_samantha_should_speak:
                self.on_samantha_should_speak()
                
        elif new_state == ConversationState.OVERLAP_SAMANTHA_YIELD:
            # Samantha should stop speaking
            if self.on_samantha_should_stop:
                self.on_samantha_should_stop()
                
    def process_input(
        self,
        human_speaking: bool,
        samantha_speaking: bool,
        turn_yield_probability: float,
        features: Optional['StreamingFeatures'] = None
    ):
        """
        Process current state and decide transitions.
        Called every audio chunk.
        """
        
        current_time = time.time()
        time_in_state = current_time - self.state_enter_time
        
        # State machine logic
        if self.state == ConversationState.IDLE:
            if human_speaking:
                self.transition(ConversationState.HUMAN_SPEAKING, "human_started")
            elif samantha_speaking:
                self.transition(ConversationState.SAMANTHA_SPEAKING, "samantha_started")
                
        elif self.state == ConversationState.HUMAN_SPEAKING:
            if not human_speaking:
                # Human stopped - are they yielding?
                if turn_yield_probability > 0.7:
                    self.transition(ConversationState.HUMAN_YIELDING, "high_yield_prob")
                elif time_in_state > self.yield_timeout:
                    self.transition(ConversationState.HUMAN_YIELDING, "silence_timeout")
            elif samantha_speaking:
                # Overlap! Samantha should yield
                self.transition(ConversationState.OVERLAP_SAMANTHA_YIELD, "overlap_detected")
            else:
                # Still speaking - check for backchannel opportunity
                self._check_backchannel_opportunity(features)
                
        elif self.state == ConversationState.HUMAN_YIELDING:
            if human_speaking:
                # They continued - false alarm
                self.transition(ConversationState.HUMAN_SPEAKING, "human_continued")
            elif time_in_state > self.min_response_delay:
                # Enough pause, Samantha can respond
                self.transition(ConversationState.TRANSITION_TO_SAMANTHA, "yield_confirmed")
                
        elif self.state == ConversationState.TRANSITION_TO_SAMANTHA:
            if human_speaking:
                # Human jumped back in
                self.transition(ConversationState.HUMAN_SPEAKING, "human_interrupted")
            elif samantha_speaking:
                self.transition(ConversationState.SAMANTHA_SPEAKING, "samantha_started")
            elif time_in_state > self.max_response_delay:
                # Taking too long, force transition
                self.transition(ConversationState.SAMANTHA_SPEAKING, "response_timeout")
                
        elif self.state == ConversationState.SAMANTHA_SPEAKING:
            if human_speaking:
                # Human interrupting - check if backchannel or real
                if self._is_backchannel(features):
                    # Ignore, continue speaking
                    pass
                else:
                    self.transition(ConversationState.OVERLAP_SAMANTHA_YIELD, "human_interrupted")
            elif not samantha_speaking:
                self.transition(ConversationState.SAMANTHA_YIELDING, "samantha_stopped")
                
        elif self.state == ConversationState.SAMANTHA_YIELDING:
            if human_speaking:
                self.transition(ConversationState.HUMAN_SPEAKING, "human_took_turn")
            elif samantha_speaking:
                self.transition(ConversationState.SAMANTHA_SPEAKING, "samantha_continued")
            elif time_in_state > self.yield_timeout:
                self.transition(ConversationState.IDLE, "both_silent")
                
        elif self.state == ConversationState.OVERLAP_SAMANTHA_YIELD:
            if not samantha_speaking:
                self.transition(ConversationState.HUMAN_SPEAKING, "samantha_yielded")
            elif not human_speaking:
                # Human stopped - was it just a backchannel?
                self.transition(ConversationState.SAMANTHA_SPEAKING, "human_was_backchannel")
                
    def _check_backchannel_opportunity(self, features: Optional['StreamingFeatures']):
        """Check if Samantha should produce a backchannel."""
        
        if features is None:
            return
            
        # Opportunities for backchannel:
        # 1. After a clause/phrase boundary
        # 2. When human emotion peaks
        # 3. Periodic acknowledgment
        
        # Simple heuristic: backchannel every 3-5 seconds of human speech
        time_in_state = time.time() - self.state_enter_time
        
        if time_in_state > 3.0:
            # Could send backchannel
            if features.arousal > 0.6:
                backchannel = "oh!" if features.emotion_estimate == 'excited' else "mmhm"
            else:
                backchannel = "mmhm"
                
            if self.on_samantha_should_backchannel:
                self.on_samantha_should_backchannel(backchannel)
                
    def _is_backchannel(self, features: Optional['StreamingFeatures']) -> bool:
        """Determine if human speech is a backchannel vs real interruption."""
        
        if features is None:
            return False
            
        transcript = features.partial_transcript.lower().strip()
        
        # Common backchannels
        backchannels = [
            'mmhm', 'mm-hmm', 'uh-huh', 'yeah', 'yep', 'right',
            'okay', 'ok', 'sure', 'got it', 'i see', 'mhm'
        ]
        
        for bc in backchannels:
            if transcript == bc or transcript.endswith(bc):
                return True
                
        # Also check: very short duration + low energy variance = likely backchannel
        if features.speech_probability < 0.7:
            return True
            
        return False
        
    def get_state(self) -> ConversationState:
        return self.state
        
    def get_time_in_state(self) -> float:
        return time.time() - self.state_enter_time
```

---

## 5. BACKCHANNEL ENGINE

```python
from dataclasses import dataclass
from typing import List, Optional, Dict
from enum import Enum
import random
import time

class BackchannelType(Enum):
    ACKNOWLEDGMENT = "acknowledgment"      # "mmhm", "yeah"
    AGREEMENT = "agreement"                # "right", "exactly"
    SURPRISE = "surprise"                  # "oh!", "wow"
    EMPATHY = "empathy"                    # "oh no", "aww"
    ENCOURAGEMENT = "encouragement"        # "go on", "and then?"
    UNDERSTANDING = "understanding"        # "I see", "got it"

@dataclass
class Backchannel:
    """A backchannel utterance."""
    type: BackchannelType
    text: str
    audio: Optional[bytes]  # Pre-rendered audio
    duration_ms: float
    energy: float  # 0-1, how emphatic

class BackchannelEngine:
    """
    Generates appropriate backchannels while human is speaking.
    Makes Samantha an active listener, not a passive recorder.
    """
    
    def __init__(self):
        # Backchannel library
        self.library: Dict[BackchannelType, List[Backchannel]] = {
            BackchannelType.ACKNOWLEDGMENT: [
                Backchannel(BackchannelType.ACKNOWLEDGMENT, "mmhm", None, 300, 0.3),
                Backchannel(BackchannelType.ACKNOWLEDGMENT, "mm", None, 200, 0.2),
                Backchannel(BackchannelType.ACKNOWLEDGMENT, "yeah", None, 350, 0.4),
                Backchannel(BackchannelType.ACKNOWLEDGMENT, "[soft] yeah", None, 400, 0.3),
            ],
            BackchannelType.AGREEMENT: [
                Backchannel(BackchannelType.AGREEMENT, "right", None, 300, 0.5),
                Backchannel(BackchannelType.AGREEMENT, "[soft] right", None, 350, 0.3),
                Backchannel(BackchannelType.AGREEMENT, "exactly", None, 500, 0.6),
            ],
            BackchannelType.SURPRISE: [
                Backchannel(BackchannelType.SURPRISE, "oh!", None, 250, 0.7),
                Backchannel(BackchannelType.SURPRISE, "wow", None, 350, 0.6),
                Backchannel(BackchannelType.SURPRISE, "no way", None, 450, 0.7),
                Backchannel(BackchannelType.SURPRISE, "[breath] oh", None, 400, 0.5),
            ],
            BackchannelType.EMPATHY: [
                Backchannel(BackchannelType.EMPATHY, "oh no", None, 400, 0.5),
                Backchannel(BackchannelType.EMPATHY, "[soft] oh no...", None, 500, 0.4),
                Backchannel(BackchannelType.EMPATHY, "aww", None, 350, 0.4),
                Backchannel(BackchannelType.EMPATHY, "[soft] yeah...", None, 450, 0.3),
            ],
            BackchannelType.ENCOURAGEMENT: [
                Backchannel(BackchannelType.ENCOURAGEMENT, "and then?", None, 450, 0.5),
                Backchannel(BackchannelType.ENCOURAGEMENT, "go on", None, 400, 0.4),
                Backchannel(BackchannelType.ENCOURAGEMENT, "[soft] mmhm?", None, 350, 0.3),
            ],
            BackchannelType.UNDERSTANDING: [
                Backchannel(BackchannelType.UNDERSTANDING, "I see", None, 400, 0.4),
                Backchannel(BackchannelType.UNDERSTANDING, "got it", None, 350, 0.5),
                Backchannel(BackchannelType.UNDERSTANDING, "ah", None, 250, 0.4),
            ],
        }
        
        # Timing control
        self.last_backchannel_time: float = 0
        self.min_interval: float = 2.0  # Minimum seconds between backchannels
        self.max_interval: float = 5.0  # Maximum seconds without backchannel
        
        # Adaptation
        self.backchannel_frequency: float = 0.5  # 0 = silent listener, 1 = very active
        
    def should_backchannel(
        self,
        time_since_human_started: float,
        features: 'StreamingFeatures'
    ) -> bool:
        """Determine if now is a good time for a backchannel."""
        
        time_since_last = time.time() - self.last_backchannel_time
        
        # Too soon since last one
        if time_since_last < self.min_interval:
            return False
            
        # Too long without one
        if time_since_last > self.max_interval:
            return True
            
        # Check for natural opportunity
        
        # 1. Pause in human speech (they took a breath)
        if features.speaking_state == SpeakingState.SILENCE:
            return True
            
        # 2. Emotional peak
        if features.arousal > 0.7:
            return random.random() < self.backchannel_frequency
            
        # 3. End of phrase (falling pitch + brief pause coming)
        if features.pitch_direction == 'falling' and features.turn_hold_probability > 0.6:
            return random.random() < self.backchannel_frequency
            
        return False
        
    def select_backchannel(
        self,
        features: 'StreamingFeatures',
        recent_content: str
    ) -> Backchannel:
        """Select appropriate backchannel based on context."""
        
        # Determine type based on emotion and content
        emotion = features.emotion_estimate
        arousal = features.arousal
        content_lower = recent_content.lower()
        
        # Emotional matching
        if emotion == 'excited' and arousal > 0.6:
            bc_type = BackchannelType.SURPRISE
        elif emotion == 'sad' or any(w in content_lower for w in ['died', 'lost', 'terrible', 'awful']):
            bc_type = BackchannelType.EMPATHY
        elif any(w in content_lower for w in ['right?', 'you know?', 'agree']):
            bc_type = BackchannelType.AGREEMENT
        elif features.turn_hold_probability < 0.4:
            # They might be pausing for encouragement
            bc_type = BackchannelType.ENCOURAGEMENT
        else:
            bc_type = BackchannelType.ACKNOWLEDGMENT
            
        # Select from library with some randomness
        options = self.library[bc_type]
        
        # Prefer lower energy if human is calm
        if arousal < 0.4:
            options = sorted(options, key=lambda x: x.energy)
            return options[0]
        else:
            return random.choice(options)
            
    def get_backchannel(
        self,
        time_since_human_started: float,
        features: 'StreamingFeatures',
        recent_content: str
    ) -> Optional[Backchannel]:
        """Main entry point - get a backchannel if appropriate."""
        
        if not self.should_backchannel(time_since_human_started, features):
            return None
            
        bc = self.select_backchannel(features, recent_content)
        self.last_backchannel_time = time.time()
        
        return bc
        
    def adapt_frequency(self, human_seems_annoyed: bool, human_seems_engaged: bool):
        """Adapt backchannel frequency based on human response."""
        
        if human_seems_annoyed:
            # They might want us to be quieter
            self.backchannel_frequency = max(0.2, self.backchannel_frequency - 0.1)
            self.min_interval = min(4.0, self.min_interval + 0.5)
            
        elif human_seems_engaged:
            # They like the active listening
            self.backchannel_frequency = min(0.8, self.backchannel_frequency + 0.1)
            self.min_interval = max(1.5, self.min_interval - 0.3)
```

---

## 6. RESPONSE GENERATOR (Parallel Preparation)

```python
from dataclasses import dataclass
from typing import Optional, List
from enum import Enum
import threading
import queue

class ResponseReadiness(Enum):
    NOT_STARTED = "not_started"
    PREPARING = "preparing"
    PARTIAL_READY = "partial_ready"
    READY = "ready"
    DELIVERED = "delivered"

@dataclass
class PartialResponse:
    """Response being prepared while human speaks."""
    
    # What we've understood so far
    understood_intent: Optional[str]
    understood_entities: List[str]
    understood_emotion: str
    
    # Response being built
    response_opener: Optional[str]      # Ready to speak immediately
    response_body: Optional[str]        # Main content
    response_full: Optional[str]        # Complete response
    
    # Status
    readiness: ResponseReadiness
    confidence: float
    
    # Timing
    started_at: float
    ready_at: Optional[float]

class ParallelResponseGenerator:
    """
    Prepares response WHILE human is still speaking.
    Enables near-instant responses when turn comes.
    """
    
    def __init__(self, cortex: 'Cortex', thalamus: 'Thalamus'):
        self.cortex = cortex
        self.thalamus = thalamus
        
        # Current preparation
        self.current_response: Optional[PartialResponse] = None
        
        # Background processing
        self.processing_queue = queue.Queue()
        self.result_queue = queue.Queue()
        
        # Start background worker
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()
        
    def start_preparing(self, initial_features: 'StreamingFeatures'):
        """Start preparing a response based on initial understanding."""
        
        self.current_response = PartialResponse(
            understood_intent=None,
            understood_entities=[],
            understood_emotion=initial_features.emotion_estimate,
            response_opener=None,
            response_body=None,
            response_full=None,
            readiness=ResponseReadiness.NOT_STARTED,
            confidence=0.0,
            started_at=time.time(),
            ready_at=None
        )
        
        # Queue initial processing
        self.processing_queue.put(('start', initial_features))
        
    def update_understanding(self, features: 'StreamingFeatures', transcript: str):
        """Update response as we understand more."""
        
        if self.current_response is None:
            self.start_preparing(features)
            return
            
        # Queue update
        self.processing_queue.put(('update', features, transcript))
        
        # Check for results
        try:
            while True:
                result = self.result_queue.get_nowait()
                self._apply_result(result)
        except queue.Empty:
            pass
            
    def finalize_response(self, final_transcript: str, features: 'StreamingFeatures'):
        """Finalize response now that human is done speaking."""
        
        # Queue final processing
        self.processing_queue.put(('finalize', features, final_transcript))
        
        # Wait briefly for result (but not too long)
        try:
            result = self.result_queue.get(timeout=0.3)
            self._apply_result(result)
        except queue.Empty:
            pass
            
    def get_response(self) -> Optional[str]:
        """Get the prepared response (or opener if full not ready)."""
        
        if self.current_response is None:
            return None
            
        if self.current_response.readiness == ResponseReadiness.READY:
            return self.current_response.response_full
        elif self.current_response.readiness == ResponseReadiness.PARTIAL_READY:
            return self.current_response.response_opener
        else:
            return None
            
    def get_opener(self) -> Optional[str]:
        """Get just the opener for immediate response."""
        
        if self.current_response is None:
            return None
            
        return self.current_response.response_opener
        
    def _worker(self):
        """Background worker that prepares responses."""
        
        while True:
            try:
                task = self.processing_queue.get(timeout=1.0)
            except queue.Empty:
                continue
                
            task_type = task[0]
            
            if task_type == 'start':
                features = task[1]
                result = self._process_start(features)
                
            elif task_type == 'update':
                features, transcript = task[1], task[2]
                result = self._process_update(features, transcript)
                
            elif task_type == 'finalize':
                features, transcript = task[1], task[2]
                result = self._process_finalize(features, transcript)
                
            self.result_queue.put(result)
            
    def _process_start(self, features: 'StreamingFeatures') -> dict:
        """Initial processing - prepare opener based on emotion."""
        
        emotion = features.emotion_estimate
        
        # Prepare emotion-appropriate opener
        if emotion == 'excited':
            opener = "[warm] [breath] "
        elif emotion == 'sad':
            opener = "[soft] [breath] yeah... "
        elif emotion == 'frustrated':
            opener = "[gentle] [breath] "
        else:
            opener = "[soft] "
            
        return {
            'type': 'opener',
            'opener': opener,
            'readiness': ResponseReadiness.PARTIAL_READY
        }
        
    def _process_update(self, features: 'StreamingFeatures', transcript: str) -> dict:
        """Update understanding and refine response."""
        
        # Analyze partial transcript for intent
        intent = self._detect_partial_intent(transcript)
        
        # Start building response body if we have enough
        body = None
        if intent and len(transcript.split()) > 5:
            # Enough context to start forming response
            body = self._generate_partial_body(intent, transcript)
            
        return {
            'type': 'update',
            'intent': intent,
            'body': body,
            'readiness': ResponseReadiness.PREPARING
        }
        
    def _process_finalize(self, features: 'StreamingFeatures', transcript: str) -> dict:
        """Generate final complete response."""
        
        # Full processing through CORTEX
        cortex_response = self.cortex.process(transcript, features)
        
        # Process through THALAMUS for presence
        final_response = self.thalamus.process(
            cortex_response,
            emotional_weight=features.arousal,
            certainty=0.8,  # Would come from CORTEX
            intimacy=0.5,   # Would come from conversation history
            energy=features.arousal
        )
        
        return {
            'type': 'final',
            'response': final_response,
            'readiness': ResponseReadiness.READY
        }
        
    def _apply_result(self, result: dict):
        """Apply processing result to current response."""
        
        if self.current_response is None:
            return
            
        result_type = result['type']
        
        if result_type == 'opener':
            self.current_response.response_opener = result['opener']
            self.current_response.readiness = result['readiness']
            
        elif result_type == 'update':
            if result.get('intent'):
                self.current_response.understood_intent = result['intent']
            if result.get('body'):
                self.current_response.response_body = result['body']
            self.current_response.readiness = result['readiness']
            
        elif result_type == 'final':
            self.current_response.response_full = result['response']
            self.current_response.readiness = ResponseReadiness.READY
            self.current_response.ready_at = time.time()
            
    def _detect_partial_intent(self, transcript: str) -> Optional[str]:
        """Detect intent from partial transcript."""
        
        lower = transcript.lower()
        
        # Simple keyword-based detection
        if any(w in lower for w in ['how do i', 'how can i', 'how to']):
            return 'how_to_question'
        elif any(w in lower for w in ['what is', 'what are', 'what\'s']):
            return 'definition_question'
        elif any(w in lower for w in ['i feel', 'i\'m feeling', 'i am feeling']):
            return 'emotional_share'
        elif any(w in lower for w in ['can you', 'could you', 'would you']):
            return 'request'
        elif any(w in lower for w in ['i think', 'i believe', 'in my opinion']):
            return 'opinion_share'
            
        return None
        
    def _generate_partial_body(self, intent: str, transcript: str) -> Optional[str]:
        """Generate partial response body based on intent."""
        
        # This would be more sophisticated in production
        # For now, just prepare appropriate framing
        
        if intent == 'how_to_question':
            return "let me walk you through that..."
        elif intent == 'definition_question':
            return "so basically..."
        elif intent == 'emotional_share':
            return "I hear you..."
        elif intent == 'request':
            return "sure, I can help with that..."
        elif intent == 'opinion_share':
            return "that's interesting..."
            
        return None
        
    def reset(self):
        """Reset for new conversation turn."""
        self.current_response = None
```

---

## 7. OUTPUT CONTROLLER

```python
from dataclasses import dataclass
from typing import Optional, Callable
from enum import Enum
import time
import threading

class OutputState(Enum):
    IDLE = "idle"
    SPEAKING = "speaking"
    YIELDING = "yielding"
    PAUSED = "paused"

@dataclass
class OutputItem:
    """Item queued for output."""
    text: str
    audio: Optional[bytes]
    priority: int  # Higher = more important
    is_backchannel: bool
    can_be_interrupted: bool

class OutputController:
    """
    Controls what goes to the speaker.
    Manages interruptions, backchannels, and main responses.
    """
    
    def __init__(self, audio_manager: 'AudioStreamManager', tts: 'TTS'):
        self.audio_manager = audio_manager
        self.tts = tts
        
        self.state = OutputState.IDLE
        self.current_output: Optional[OutputItem] = None
        
        # Queues
        self.main_queue: list[OutputItem] = []
        self.backchannel_queue: list[OutputItem] = []
        
        # Callbacks
        self.on_output_start: Optional[Callable[[], None]] = None
        self.on_output_end: Optional[Callable[[], None]] = None
        
        # State
        self.is_interrupted = False
        
    def queue_response(self, text: str, priority: int = 5):
        """Queue a main response."""
        
        item = OutputItem(
            text=text,
            audio=None,
            priority=priority,
            is_backchannel=False,
            can_be_interrupted=True
        )
        
        self.main_queue.append(item)
        self._process_queue()
        
    def queue_backchannel(self, backchannel: 'Backchannel'):
        """Queue a backchannel for immediate output."""
        
        item = OutputItem(
            text=backchannel.text,
            audio=backchannel.audio,
            priority=10,  # High priority
            is_backchannel=True,
            can_be_interrupted=False  # Backchannels are short, don't interrupt
        )
        
        self.backchannel_queue.append(item)
        self._process_queue()
        
    def interrupt(self):
        """Interrupt current output (human is speaking)."""
        
        if self.state != OutputState.SPEAKING:
            return
            
        if self.current_output and not self.current_output.can_be_interrupted:
            return  # Can't interrupt backchannels
            
        self.is_interrupted = True
        self.audio_manager.clear_output()
        self.state = OutputState.YIELDING
        
        # Queue a yield utterance
        yield_item = OutputItem(
            text="[soft] oh—",
            audio=None,
            priority=15,
            is_backchannel=True,
            can_be_interrupted=False
        )
        self.backchannel_queue.insert(0, yield_item)
        
    def resume(self):
        """Resume after interruption if appropriate."""
        
        if self.state == OutputState.YIELDING:
            self.state = OutputState.IDLE
            self.is_interrupted = False
            # Could resume previous output or start fresh
            
    def _process_queue(self):
        """Process output queues."""
        
        if self.state == OutputState.SPEAKING:
            return  # Already outputting
            
        # Backchannels first (they're short and time-sensitive)
        if self.backchannel_queue:
            item = self.backchannel_queue.pop(0)
            self._output_item(item)
            return
            
        # Then main responses
        if self.main_queue:
            item = self.main_queue.pop(0)
            self._output_item(item)
            return
            
    def _output_item(self, item: OutputItem):
        """Output a single item."""
        
        self.current_output = item
        self.state = OutputState.SPEAKING
        
        if self.on_output_start:
            self.on_output_start()
            
        # Generate audio if not pre-rendered
        if item.audio is None:
            audio = self.tts.synthesize(item.text)
        else:
            audio = item.audio
            
        # Queue to audio manager
        self.audio_manager.queue_output(audio)
        
        # Start monitoring for completion
        threading.Thread(target=self._monitor_output, daemon=True).start()
        
    def _monitor_output(self):
        """Monitor output completion."""
        
        while True:
            buffer_duration = self.audio_manager.get_output_buffer_duration_ms()
            
            if buffer_duration < 50:  # Almost done
                break
                
            if self.is_interrupted:
                break
                
            time.sleep(0.05)
            
        # Output complete
        self.state = OutputState.IDLE
        self.current_output = None
        
        if self.on_output_end:
            self.on_output_end()
            
        # Check for more in queue
        self._process_queue()
        
    def is_speaking(self) -> bool:
        return self.state == OutputState.SPEAKING
```

---

## 8. MAIN ORCHESTRATOR

```python
import time
import threading
from typing import Optional

class ConversationEngine:
    """
    The main orchestrator that ties everything together.
    Runs the full-duplex conversation loop.
    """
    
    def __init__(
        self,
        cortex: 'Cortex',
        thalamus: 'Thalamus',
        tts: 'TTS'
    ):
        # Core components
        self.cortex = cortex
        self.thalamus = thalamus
        self.tts = tts
        
        # Initialize subsystems
        self.audio_manager = AudioStreamManager()
        self.streaming_decoder = StreamingDecoder()
        self.vad = VoiceActivityDetector()
        self.state_machine = ConversationStateMachine()
        self.backchannel_engine = BackchannelEngine()
        self.response_generator = ParallelResponseGenerator(cortex, thalamus)
        self.output_controller = OutputController(self.audio_manager, tts)
        
        # Wire up callbacks
        self._setup_callbacks()
        
        # State
        self.is_running = False
        self.accumulated_transcript = ""
        self.human_speech_start_time: Optional[float] = None
        
    def _setup_callbacks(self):
        """Wire up all the callbacks between components."""
        
        # Audio input -> Streaming decoder
        self.audio_manager.on_input_chunk = self._on_audio_chunk
        
        # VAD callbacks
        self.vad.on_human_speech_start = self._on_human_speech_start
        self.vad.on_human_speech_end = self._on_human_speech_end
        self.vad.on_overlap_start = self._on_overlap_start
        
        # State machine callbacks
        self.state_machine.on_state_change = self._on_state_change
        self.state_machine.on_samantha_should_speak = self._on_should_speak
        self.state_machine.on_samantha_should_stop = self._on_should_stop
        self.state_machine.on_samantha_should_backchannel = self._on_should_backchannel
        
        # Output callbacks
        self.output_controller.on_output_start = self._on_output_start
        self.output_controller.on_output_end = self._on_output_end
        
    def start(self):
        """Start the conversation engine."""
        
        self.is_running = True
        self.audio_manager.start()
        
        print("[ConversationEngine] Started. Listening...")
        
    def stop(self):
        """Stop the conversation engine."""
        
        self.is_running = False
        self.audio_manager.stop()
        
        print("[ConversationEngine] Stopped.")
        
    def _on_audio_chunk(self, chunk: AudioChunk):
        """Called for each incoming audio chunk."""
        
        # Decode the chunk
        features = self.streaming_decoder.process_chunk(chunk)
        
        # Update VAD
        is_human_speaking = features.speaking_state == SpeakingState.SPEECH
        self.vad.update_human(is_human_speaking, chunk.timestamp)
        
        # Update state machine
        self.state_machine.process_input(
            human_speaking=is_human_speaking,
            samantha_speaking=self.output_controller.is_speaking(),
            turn_yield_probability=features.turn_yield_probability,
            features=features
        )
        
        # If human is speaking, update response preparation
        if is_human_speaking:
            self.accumulated_transcript = features.partial_transcript
            self.response_generator.update_understanding(
                features,
                self.accumulated_transcript
            )
            
            # Check for backchannel opportunity
            if self.human_speech_start_time:
                time_speaking = chunk.timestamp - self.human_speech_start_time
                bc = self.backchannel_engine.get_backchannel(
                    time_speaking,
                    features,
                    self.accumulated_transcript
                )
                if bc:
                    self.output_controller.queue_backchannel(bc)
                    
    def _on_human_speech_start(self, timestamp: float):
        """Human started speaking."""
        
        self.human_speech_start_time = timestamp
        self.accumulated_transcript = ""
        
        # Start preparing response
        features = self.streaming_decoder.state  # Get current state
        self.response_generator.start_preparing(
            StreamingFeatures(
                timestamp=timestamp,
                speaking_state=SpeakingState.SPEECH,
                speech_probability=0.9,
                current_energy=0.5,
                current_pitch=None,
                pitch_direction='unknown',
                stress_level=0.0,
                emotion_estimate='neutral',
                emotion_confidence=0.5,
                arousal=0.5,
                partial_transcript="",
                transcript_is_final=False,
                turn_hold_probability=0.8,
                turn_yield_probability=0.2
            )
        )
        
    def _on_human_speech_end(self, timestamp: float, duration: float):
        """Human stopped speaking."""
        
        # Finalize response
        features = StreamingFeatures(
            timestamp=timestamp,
            speaking_state=SpeakingState.SILENCE,
            speech_probability=0.1,
            current_energy=0.0,
            current_pitch=None,
            pitch_direction='falling',
            stress_level=0.0,
            emotion_estimate='neutral',
            emotion_confidence=0.5,
            arousal=0.5,
            partial_transcript=self.accumulated_transcript,
            transcript_is_final=True,
            turn_hold_probability=0.2,
            turn_yield_probability=0.8
        )
        
        self.response_generator.finalize_response(
            self.accumulated_transcript,
            features
        )
        
    def _on_overlap_start(self, timestamp: float):
        """Both speaking at once - handle collision."""
        
        # Samantha yields
        self.output_controller.interrupt()
        
    def _on_state_change(self, old_state: ConversationState, new_state: ConversationState):
        """State machine changed state."""
        
        print(f"[State] {old_state.name} -> {new_state.name}")
        
    def _on_should_speak(self):
        """State machine says Samantha should speak now."""
        
        response = self.response_generator.get_response()
        
        if response:
            self.output_controller.queue_response(response)
        else:
            # No response ready, use opener
            opener = self.response_generator.get_opener()
            if opener:
                self.output_controller.queue_response(opener + "let me think...")
            else:
                self.output_controller.queue_response("[soft] hmm...")
                
    def _on_should_stop(self):
        """State machine says Samantha should stop speaking."""
        
        self.output_controller.interrupt()
        
    def _on_should_backchannel(self, backchannel_text: str):
        """State machine says Samantha should backchannel."""
        
        bc = Backchannel(
            type=BackchannelType.ACKNOWLEDGMENT,
            text=backchannel_text,
            audio=None,
            duration_ms=300,
            energy=0.3
        )
        self.output_controller.queue_backchannel(bc)
        
    def _on_output_start(self):
        """Samantha started speaking."""
        
        self.vad.update_samantha(True, time.time())
        
    def _on_output_end(self):
        """Samantha stopped speaking."""
        
        self.vad.update_samantha(False, time.time())
```

---

## COMPLETE SYSTEM FLOW

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                                         │
│                                    FULL-DUPLEX CONVERSATION FLOW                                        │
│                                                                                                         │
│                                                                                                         │
│    MICROPHONE                                                                          SPEAKER          │
│        │                                                                                  ▲             │
│        │ (always on)                                                          (always ready)            │
│        ▼                                                                                  │             │
│   ┌─────────────────┐                                                    ┌─────────────────┐            │
│   │  AUDIO STREAM   │                                                    │    OUTPUT       │            │
│   │    MANAGER      │                                                    │   CONTROLLER    │            │
│   └────────┬────────┘                                                    └────────▲────────┘            │
│            │                                                                      │                     │
│            │ chunks (50ms)                                                        │                     │
│            ▼                                                                      │                     │
│   ┌─────────────────┐                                                             │                     │
│   │   STREAMING     │                                                             │                     │
│   │    DECODER      │                                                             │                     │
│   │                 │                                                             │                     │
│   │  • Energy       │                                                             │                     │
│   │  • Pitch        │                                                             │                     │
│   │  • Transcript   │                                                             │                     │
│   │  • Emotion      │                                                             │                     │
│   │  • Turn signals │                                                             │                     │
│   └────────┬────────┘                                                             │                     │
│            │                                                                      │                     │
│            │ StreamingFeatures                                                    │                     │
│            ▼                                                                      │                     │
│   ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐            │                     │
│   │                 │     │                 │     │                 │            │                     │
│   │      VAD        │────▶│  STATE MACHINE  │────▶│   BACKCHANNEL   │────────────┤                     │
│   │                 │     │                 │     │     ENGINE      │            │                     │
│   │  Who speaks?    │     │  Turn-taking    │     │                 │ backchannels                     │
│   │                 │     │  decisions      │     │  "mmhm" "yeah"  │            │                     │
│   └─────────────────┘     └────────┬────────┘     └─────────────────┘            │                     │
│                                    │                                              │                     │
│                                    │ on_should_speak                              │                     │
│                                    ▼                                              │                     │
│                           ┌─────────────────┐                                     │                     │
│                           │                 │                                     │                     │
│            ┌─────────────▶│    RESPONSE     │─────────────────────────────────────┤                     │
│            │              │   GENERATOR     │                                     │                     │
│            │              │                 │                                     │ main response       │
│   partial transcript      │  (parallel)     │                                     │                     │
│                           │                 │                                     │                     │
│                           └────────┬────────┘                                     │                     │
│                                    │                                              │                     │
│                                    ▼                                              │                     │
│                           ┌─────────────────┐     ┌─────────────────┐            │                     │
│                           │                 │     │                 │            │                     │
│                           │     CORTEX      │────▶│    THALAMUS     │────────────┘                     │
│                           │                 │     │                 │                                   │
│                           │  (thinking)     │     │  (presence)     │                                   │
│                           │                 │     │                 │                                   │
│                           └─────────────────┘     └─────────────────┘                                   │
│                                                                                                         │
│                                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## TIMING EXAMPLE

```
TIME      HUMAN                    SYSTEM STATE           SAMANTHA
────      ─────                    ────────────           ────────

0.00s     [silence]                IDLE                   [waiting]

0.10s     "Hey so—"                → HUMAN_SPEAKING       [decode: greeting + hesitation]
                                                          [prepare: opener "[soft] hey"]

0.50s     "—I was thinking—"                              [decode: "thinking" = setup]
                                                          [prepare: listening response]

1.00s     "—about the project"                            [decode: topic = project]
                                                          [backchannel: "mmhm"]
                                   
1.20s                                                     "mmhm" [spoken, 200ms]

1.50s     "—and I'm not sure—"                            [decode: uncertainty detected]
                                                          [adjust: supportive tone]

2.00s     "—if we should—"                                [decode: question forming]

2.30s     "—continue or not"                              [decode: binary question]
                                                          [prepare: balanced response]

2.50s     [pause]                  → HUMAN_YIELDING       [finalize response]

2.70s     [silence]                                       [response ready]

2.90s     [silence > 400ms]        → TRANSITION_TO_SAM    

3.00s                              → SAMANTHA_SPEAKING    "[soft] [breath] hmm..."

3.30s                                                     "I think it depends on—"

3.50s     "yeah exactly—"          [backchannel detected] [continue speaking]

3.60s                                                     "—what the goal is..."

4.00s                                                     "what matters most to you?"

4.30s     [taking breath]          → SAMANTHA_YIELDING    

4.50s     "well I guess—"          → HUMAN_SPEAKING       [listening]

...       [conversation continues naturally]
```

---

## WHAT MAKES THIS DIFFERENT

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│   WALKIE-TALKIE (current AI)          CONVERSATION (this system)               │
│   ──────────────────────────          ──────────────────────────               │
│                                                                                 │
│   Human speaks.                       Human speaks.                             │
│   [WAIT]                              Samantha: "mmhm" (while listening)       │
│   [PROCESSING...]                     [processing in parallel]                  │
│   [WAIT]                              Samantha: "oh!" (reacting)               │
│   Samantha speaks.                    Human finishes.                           │
│   [WAIT]                              Samantha speaks (immediately)             │
│   Human speaks.                       Human: "yeah" (while Samantha speaks)    │
│                                       [both engaged, natural flow]              │
│                                                                                 │
│   Feels like: form submission         Feels like: talking to someone           │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

This is the architecture.

Ready to start implementing?