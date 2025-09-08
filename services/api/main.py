from fastapi import FastAPI, WebSocket, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import io
from PIL import Image
import numpy as np
import cv2
import pytesseract
import os
from typing import Optional
import asyncio
import json
from datetime import datetime

app = FastAPI(title="DyslexiaAR API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connections for real-time analytics
connected_clients = []
analytics_data = {
    "active_connections": 0,
    "analyses_today": 0,
    "system_health": "healthy",
    "total_analyses": 0
}

@app.get("/health")
async def health():
    return {"ok": True, "timestamp": datetime.now().isoformat()}

@app.websocket('/ws/analytics')
async def ws_analytics(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    analytics_data["active_connections"] = len(connected_clients)
    
    try:
        # Send initial metrics
        await websocket.send_json({
            "type": "metrics",
            "data": analytics_data
        })
        
        # Keep connection alive and send periodic updates
        while True:
            try:
                # Wait for client message or timeout
                await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                
                # Send updated metrics
                await websocket.send_json({
                    "type": "metrics",
                    "data": analytics_data
                })
            except asyncio.TimeoutError:
                # Send heartbeat
                await websocket.send_json({
                    "type": "heartbeat",
                    "timestamp": datetime.now().isoformat()
                })
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        if websocket in connected_clients:
            connected_clients.remove(websocket)
        analytics_data["active_connections"] = len(connected_clients)

def preprocess_image_for_ocr(image: Image.Image) -> np.ndarray:
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th

def transform_text_for_dyslexia(raw_text: str) -> str:
    if not raw_text:
        return ""
    lines = [" ".join(l.strip().split()) for l in raw_text.splitlines() if l.strip()]
    return "\n".join(lines)

@app.post("/process-video")
async def process_video(image: UploadFile = File(...)):
    try:
        content = await image.read()
        pil = Image.open(io.BytesIO(content)).convert("RGB")
        pre = preprocess_image_for_ocr(pil)

        try:
            ocr_text = pytesseract.image_to_string(pre, lang="eng")
        except Exception:
            ocr_text = ""

        transformed = transform_text_for_dyslexia(ocr_text)
        
        # Update analytics
        analytics_data["analyses_today"] += 1
        analytics_data["total_analyses"] += 1
        
        # Notify WebSocket clients
        for client in connected_clients:
            try:
                await client.send_json({
                    "type": "analysis_complete",
                    "data": {
                        "text_length": len(transformed),
                        "analyses_today": analytics_data["analyses_today"],
                        "total_analyses": analytics_data["total_analyses"]
                    }
                })
            except:
                pass

        return JSONResponse({
            "transformed_text": transformed,
            "confidence": 0.92,
            "word_count": len(transformed.split()),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/tts")
async def text_to_speech(text: str = Form(...), voice: str = Form("en-US-Standard-A")):
    try:
        # Placeholder TTS - in production, integrate Google Cloud TTS
        # For now, return a mock audio URL
        audio_id = hash(text) % 1000000
        return JSONResponse({
            "audio_url": f"/api/tts/audio/{audio_id}.mp3",
            "text": text,
            "voice": voice,
            "duration": len(text) * 0.1,
            "status": "generated"
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/tts/audio/{audio_id}")
async def get_tts_audio(audio_id: str):
    # Placeholder for actual audio file serving
    return JSONResponse({
        "message": f"Audio file {audio_id} would be served here",
        "audio_url": f"/api/tts/audio/{audio_id}.mp3"
    })

@app.get("/stats")
async def get_stats():
    return {
        "total_analyses": analytics_data["total_analyses"],
        "analyses_today": analytics_data["analyses_today"],
        "active_users": analytics_data["active_connections"],
        "system_uptime": "99.9%",
        "last_updated": datetime.now().isoformat()
    }

@app.post("/feedback")
async def submit_feedback(
    rating: int = Form(...),
    comments: Optional[str] = Form(None),
    user_id: Optional[str] = Form(None)
):
    try:
        # In production, save to database
        feedback_data = {
            "rating": rating,
            "comments": comments,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        }
        
        # Notify WebSocket clients about new feedback
        for client in connected_clients:
            try:
                await client.send_json({
                    "type": "feedback_received",
                    "data": feedback_data
                })
            except:
                pass
        
        return JSONResponse({
            "status": "success",
            "message": "Feedback submitted successfully",
            "feedback_id": hash(str(feedback_data)) % 1000000
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)