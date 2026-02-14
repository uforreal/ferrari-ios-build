
import asyncio
import os
import json
import logging
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from dotenv import load_dotenv

# New Gemini SDK
from google import genai
from google.genai import types

# TTS
import edge_tts

# CONFIG
load_dotenv()
logger = logging.getLogger("AXON_PIPECAT")
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# 1. SETUP GEMINI (New SDK)
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# 2. SETUP TTS (Voice - Jenny)
VOICE = "en-US-JennyNeural"

class AudioPipeline:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.history = []
        
        # System instruction for Samantha
        self.system_instruction = "You are Samantha, a warm and witty AI assistant. Keep responses short and conversational (1-2 sentences max). Never be boring."

    async def process_text_input(self, text: str, vibe: dict = None):
        """Process user text and respond with audio"""
        logger.info(f"[USER] Text: {text} | Vibe: {vibe}")
        response_text = await self.ask_gemini(text, vibe)
        await self.speak_response(response_text)

    async def ask_gemini(self, input_text: str, vibe: dict = None) -> str:
        """Get text response from Gemini using new SDK"""
        try:
            # Construct context based on vibe (The "Soul" Decoder)
            vibe_context = ""
            if vibe:
                energy = vibe.get("energy", 0.5)
                if energy > 0.8: vibe_context = "[User sounds very excited/loud]"
                elif energy < 0.2: vibe_context = "[User sounds very quiet/sad]"
                
                # Add more sophisticated signal interpretation here
                if vibe.get("stuttering"): vibe_context += "[User is hesitating]"

            full_prompt = f"{vibe_context} {input_text}" if vibe_context else input_text

            # Add user message to history
            self.history.append(types.Content(role="user", parts=[types.Part(text=full_prompt)]))
            
            # Generate response
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=self.history,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    max_output_tokens=150,
                    temperature=0.9
                )
            )
            
            response_text = response.text
            
            # Add assistant response to history
            self.history.append(types.Content(role="model", parts=[types.Part(text=response_text)]))
            
            # Keep history manageable
            if len(self.history) > 10:
                self.history = self.history[-10:]
            
            return response_text
            
        except Exception as e:
            logger.error(f"[GEMINI ERROR] {e}")
            return "Sorry, I couldn't process that."

    async def speak_response(self, text: str):
        """Generate Audio (Jenny) and Stream to Client"""
        logger.info(f"[SAMANTHA] Speaking: {text}")
        
        # Tell client we're speaking
        await self.websocket.send_json({"type": "status", "mode": "speaking", "text": text})

        # Stream audio from EdgeTTS
        communicate = edge_tts.Communicate(text, VOICE)
        
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                await self.websocket.send_bytes(chunk["data"])
        
        # Tell client we're done
        await self.websocket.send_json({"type": "status", "mode": "listening"})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("Client connected")
    pipeline = AudioPipeline(websocket)
    
    try:
        while True:
            message = await websocket.receive()
            
            if "text" in message:
                data = json.loads(message["text"])
                if data.get("type") == "voice_input":
                    user_text = data.get("content")
                    vibe = data.get("vibe", {})
                    await pipeline.process_text_input(user_text, vibe)
                elif data.get("type") == "ping":
                    pass  # Keepalive, do nothing
                    
            elif "bytes" in message:
                # Phase 2: Raw audio streaming
                pass

    except WebSocketDisconnect:
        logger.info("Client disconnected")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
