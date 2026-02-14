<think>The user is understanding the architecture perfectly. They want to create an intermediate layer - a "script filter" or "magician" - that takes raw text input and transforms it into an emotionally marked-up script with pauses, breaths, hesitations, varied pacing, etc.

This is essentially a prompt engineering task for an LLM (like Gemini, which they're already using). The LLM would take raw text and output marked-up text with all the Samantha-style delivery cues.

This is a brilliant insight from the user. Let me help them build this "presence engine" or "delivery filter."

The pipeline would be:
1. Raw text input: "I think you should take a break"
2. → Presence Engine (LLM-powered script rewriter)
3. → "I think... [pause:0.4] [breath] you should take a break? [pause:0.6] yeah."
4. → TTS + RVC
5. → Natural human-sounding audio with emotional delivery

I should help them:
1. Name this component (they love naming things)
2. Design the prompt that instructs the LLM how to rewrite scripts
3. Define the markup language/tags they'll use
4. Show how it integrates into their existing pipeline

This is a creative and legitimate use case - they're building an expressive speech system, not trying to deceive anyone.

Let me give them:
- A conceptual explanation
- The prompt engineering approach
- Example transformations
- Code integration</think>Exactly. You just designed the architecture.

```
Raw Script
    ↓
[Presence Engine] ← this is your magician
    ↓
Marked Script (pauses, breaths, fillers, pacing)
    ↓
TTS Generation
    ↓
RVC Voice Skin
    ↓
Human Output
```

The Presence Engine is an LLM doing style transfer on text. It doesn't change *what* you say—it changes *how* it's said.

## The Presence Engine

You already have Gemini in your stack. This is just another prompt.

```python
PRESENCE_PROMPT = """
You are a script director for an intimate, warm AI voice character. 

Your job: take raw dialogue and rewrite it with delivery markup that creates presence, humanity, and emotional texture.

Rules for transformation:

PACING
- Add [pause:X] for beats. Short (0.2-0.4s) for thought, medium (0.5-0.8s) for emphasis, long (1.0+) for emotional weight.
- Conversations aren't rushed. Let moments land.

BREATHING  
- Add [breath] before new thoughts or after emotional beats.
- Breathing signals thinking. It says "I'm processing this with you."

FILLERS
- Sprinkle natural hesitations: "hmm", "mm", "I...", "well", "you know", "like"
- Not every line. Maybe 30% of responses. Varies with emotional content.

SOFTENING
- Add "..." for trailing thoughts
- Use "?" even on statements when uncertain or intimate
- Repeat words for emphasis: "I really... really think..."

THINKING OUT LOUD
- Break complete thoughts into discovered fragments
- "I love you" → "I... [pause:0.3] I think I [breath] love you?"

TONE MARKERS (for TTS hints)
- [soft] before gentle phrases
- [warm] before affectionate content
- [bright] before excited delivery

Input will be plain text. Output ONLY the transformed script. No explanations.

Examples:

Input: "I think you should take a break"
Output: "[soft] I think... [pause:0.4] you should take a break? [pause:0.3] [breath] yeah."

Input: "That's really interesting"
Output: "[warm] hmm... [pause:0.3] that's really interesting? [pause:0.5] [breath] I like that."

Input: "Good morning"
Output: "[soft] [breath] good morning... [pause:0.6] [warm] hi."

Input: "I don't know how to help with that"
Output: "[breath] I... [pause:0.3] hmm. [pause:0.4] I don't really know how to help with that? [pause:0.5] [soft] sorry..."
"""
```

## Integration

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

def add_presence(raw_script: str) -> str:
    response = model.generate_content(
        PRESENCE_PROMPT + f"\n\nInput: \"{raw_script}\"\nOutput:",
        generation_config={"temperature": 0.7}
    )
    return response.text.strip()
```

## Full Pipeline Now

```python
async def speak(raw_text: str) -> bytes:
    # 1. Add presence
    marked_script = add_presence(raw_text)
    print(f"Marked: {marked_script}")
    
    # 2. Generate TTS with markers
    audio = await process_script(marked_script)
    
    # 3. Apply voice skin (RVC)
    final_audio = apply_voice_skin(audio)
    
    return final_audio
```

## Test It

Raw input:
```
"You've been working for three hours"
```

After Presence Engine:
```
"[soft] [breath] you've been working for... [pause:0.5] three hours? [pause:0.3] hmm. [pause:0.4] [warm] just noticing."
```

After TTS + RVC:
```
*warm human voice with natural pauses and a gentle observational tone*
```

## Tuning the Feel

Temperature matters.

`0.5` = more predictable, consistent delivery
`0.7` = balanced, natural variation  
`0.9` = more spontaneous, occasionally surprising

You'll want to tune the prompt over time. Add examples of deliveries you love. Remove patterns that feel wrong. The prompt *is* the personality.

## One Level Deeper

You could even give the Presence Engine context:

```python
def add_presence(raw_script: str, emotion: str = "neutral") -> str:
    context = f"Current emotional context: {emotion}"
    # ... inject into prompt
```

So "you've been working for three hours" delivered with `emotion="concerned"` hits different than `emotion="playful"`.

That's your Samantha.

Want me to detail the tone marker processing (how `[soft]` and `[warm]` translate to actual TTS parameters)?