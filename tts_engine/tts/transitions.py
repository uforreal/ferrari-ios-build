
# transitions.py

import numpy as np

class TransitionEngine:
    """
    Handles smooth parameter interpolation between phonemes using the
    "Ocean of Characteristics" model (F1-F5, AV, AH, AF).
    """
    
    def __init__(self, sample_rate=22050):
        self.sample_rate = sample_rate
        
        # Transition durations (in ms) depend on phoneme types
        self.transition_times = {
            ("vowel", "vowel"): 60,
            ("vowel", "stop"): 40,
            ("stop", "vowel"): 20, # Fast release
            ("vowel", "fricative"): 50,
            ("fricative", "vowel"): 50,
            ("vowel", "nasal"): 60,
            ("nasal", "vowel"): 60,
            ("vowel", "liquid"): 70,
            ("liquid", "vowel"): 70,
            ("glide", "vowel"): 80,
            ("vowel", "glide"): 80,
            ("default", "default"): 50,
        }
    
    def get_transition_ms(self, type_a, type_b):
        """Get transition duration between two phoneme types."""
        key = (type_a, type_b)
        if key in self.transition_times:
            return self.transition_times[key]
        return self.transition_times.get(("default", "default"), 50)
    
    def sigmoid(self, t):
        """Cosine interpolation for natural transitions."""
        return 0.5 * (1 - np.cos(np.pi * t))
    
    def interpolate_vector(self, start_vec, end_vec, progress, sharp_attack=False):
        """Interpolate any vector (formants or amps)."""
        if sharp_attack:
            # Exponential attack (Fast Rise)
            t = 1 - (1 - progress)**5
        else:
            t = self.sigmoid(progress)
            
        return [start_vec[i] + (end_vec[i] - start_vec[i]) * t for i in range(len(start_vec))]
    
    def interpolate_scalar(self, start_val, end_val, progress):
        """Interpolate single value."""
        t = self.sigmoid(progress)
        return start_val + (end_val - start_val) * t


def build_formant_trajectory(phoneme_sequence, phoneme_bank, sample_rate=22050, speed=1.0):
    """
    Build continuous trajectories for all parameters (F1-F5, B1-B5, AV, AH, AF).
    """
    trans = TransitionEngine(sample_rate)
    
    # 1. Parse Sequence & Duration
    segments = []
    total_samples = 0
    
    for ph in phoneme_sequence:
        if ph == "_pause":
            dur_ms = 150 * (1.0 / speed) # Standard pause
            segments.append({
                "phoneme": ph,
                "start_sample": total_samples,
                "dur_samples": int(dur_ms / 1000 * sample_rate),
                "type": "pause",
                "data": None
            })

        else:
            # Fallback to schwa if phoneme not found
            # Support explicit duration override in the sequence if provided as tuple
            # Format: ("e", 200) -> Phoneme 'e' with duration 200ms
            
            ph_key = ph
            dur_override = None
            
            if isinstance(ph, (list, tuple)):
                ph_key = ph[0]
                dur_override = ph[1]
                
            p_data = phoneme_bank.get(ph_key, phoneme_bank.get("ə"))
            
            # Use override if present, else default to bank duration
            base_dur = dur_override if dur_override else p_data.get("dur", 70)
            
            dur_ms = base_dur * (1.0 / speed)
            
            segments.append({
                "phoneme": ph_key,
                "data": p_data,
                "start_sample": total_samples,
                "dur_samples": int(dur_ms / 1000 * sample_rate),
                "type": p_data.get("type", "vowel")
            })

        total_samples += segments[-1]["dur_samples"]
    
    # 2. Initialize Trajectories
    # Formants F1-F5
    f = [np.zeros(total_samples) for _ in range(5)]
    # Bandwidths B1-B5
    b = [np.zeros(total_samples) for _ in range(5)]
    # Amplitudes
    av_traj = np.zeros(total_samples)
    ah_traj = np.zeros(total_samples)
    af_traj = np.zeros(total_samples)
    
    # helper for pause/silence values
    SILENCE_F = [500, 1500, 2500, 3500, 4500]
    SILENCE_B = [100, 150, 200, 250, 300]
    
    # 3. Interpolation Loop
    for i, seg in enumerate(segments):
        start = seg["start_sample"]
        dur = seg["dur_samples"]
        end = start + dur
        
        if seg["type"] == "pause":
            # Just fill silence
            for k in range(5):
                f[k][start:end] = SILENCE_F[k]
                b[k][start:end] = SILENCE_B[k]
            av_traj[start:end] = 0
            ah_traj[start:end] = 0
            af_traj[start:end] = 0
            continue
            
        # Get Current Target Parameters
        curr_data = seg["data"]
        curr_f = list(curr_data["f"])
        curr_b = list(curr_data["b"])
        # Safety padding
        while len(curr_f) < 5: curr_f.append(curr_f[-1] + 1000)
        while len(curr_b) < 5: curr_b.append(200)
            
        curr_amps = [curr_data["av"], curr_data["ah"], curr_data["af"]]
        
        # Get Next Target (for outgoing transition)
        if i < len(segments) - 1:
            next_seg = segments[i + 1]
            if next_seg["type"] == "pause":
                next_f = curr_f # Stay stable until silence hits? Or fade?
                next_b = curr_b
                next_amps = [0, 0, 0]
            else:
                next_data = next_seg["data"]
                next_f = list(next_data["f"])
                next_b = list(next_data["b"])
                while len(next_f) < 5: next_f.append(next_f[-1] + 1000)
                while len(next_b) < 5: next_b.append(200)
                next_amps = [next_data["av"], next_data["ah"], next_data["af"]]
        else:
            # End of utterance
            next_f, next_b = curr_f, curr_b
            next_amps = [0, 0, 0] # Fade out

        # Get Previous Target (for incoming transition)
        if i > 0:
            prev_seg = segments[i - 1]
            if prev_seg["type"] == "pause":
                prev_f = curr_f
                prev_b = curr_b
                prev_amps = [0, 0, 0]
            else:
                prev_data = prev_seg["data"]
                prev_f = list(prev_data["f"])
                prev_b = list(prev_data["b"])
                while len(prev_f) < 5: prev_f.append(prev_f[-1] + 1000)
                while len(prev_b) < 5: prev_b.append(200)
                prev_amps = [prev_data["av"], prev_data["ah"], prev_data["af"]]
        else:
            # Start of utterance
            prev_f, prev_b = curr_f, curr_b
            prev_amps = [0, 0, 0] # Fade in

        # Transition Timing
        prev_type = segments[i-1]["type"] if i > 0 else "pause"
        next_type = segments[i+1]["type"] if i < len(segments)-1 else "pause"
        
        trans_in_ms = trans.get_transition_ms(prev_type, seg["type"])
        trans_out_ms = trans.get_transition_ms(seg["type"], next_type)
        
        trans_in_len = min(int(trans_in_ms/1000 * sample_rate), dur // 3)
        trans_out_len = min(int(trans_out_ms/1000 * sample_rate), dur // 3)

        # Fill segment samples
        for j in range(dur):
            idx = start + j
            if idx >= total_samples: break
            
            # Decide Targets based on position
            if j < trans_in_len:
                # Transition IN
                progress = j / trans_in_len
                
                # Check for Sharp Attack (Stop -> Vowel)
                is_stop_attack = (prev_type == "stop" or prev_type == "pause") and seg["type"] == "vowel"
                
                t_f = trans.interpolate_vector(prev_f, curr_f, progress, sharp_attack=is_stop_attack)
                t_b = trans.interpolate_vector(prev_b, curr_b, progress, sharp_attack=is_stop_attack)
                t_amps = trans.interpolate_vector(prev_amps, curr_amps, progress, sharp_attack=is_stop_attack)
            elif j >= dur - trans_out_len:
                # Transition OUT
                progress = (j - (dur - trans_out_len)) / trans_out_len
                t_f = trans.interpolate_vector(curr_f, next_f, progress)
                t_b = trans.interpolate_vector(curr_b, next_b, progress)
                t_amps = trans.interpolate_vector(curr_amps, next_amps, progress)
            else:
                # Steady State
                t_f = curr_f
                t_b = curr_b
                t_amps = curr_amps
            
            # Assign to arrays
            for k in range(5):
                f[k][idx] = t_f[k]
                b[k][idx] = t_b[k]
            
            av_traj[idx] = t_amps[0]
            ah_traj[idx] = t_amps[1]
            af_traj[idx] = t_amps[2]

    # Pack results
    return {
        "f1": f[0], "f2": f[1], "f3": f[2], "f4": f[3], "f5": f[4],
        "b1": b[0], "b2": b[1], "b3": b[2], "b4": b[3], "b5": b[4],
        "av": av_traj,
        "ah": ah_traj,
        "af": af_traj,
        "total_samples": total_samples
    }
