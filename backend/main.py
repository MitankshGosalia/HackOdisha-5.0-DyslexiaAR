from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
import uvicorn
import io
from PIL import Image
import numpy as np
import cv2
import pytesseract

from .database import Database


app = FastAPI(title="DyslexiaAR API", version="1.0.0")

# CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"]
    ,
    allow_headers=["*"]
)

db = Database()


def preprocess_image_for_ocr(image: Image.Image) -> np.ndarray:
    # Convert PIL Image to OpenCV BGR
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Light denoise and threshold
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th


def transform_text_for_dyslexia(raw_text: str, letter_spacing_px: int = 1, line_height: float = 1.6) -> str:
    # Basic text normalization: collapse whitespace, ensure line breaks make sense
    if not raw_text:
        return ""
    lines = [" ".join(l.strip().split()) for l in raw_text.splitlines() if l.strip()]
    text = "\n".join(lines)
    # For now, return text. Typographic styling is applied on the client via CSS.
    return text


@app.post("/process-video")
async def process_video(image: UploadFile = File(...)):
    try:
        content = await image.read()
        pil = Image.open(io.BytesIO(content)).convert("RGB")
        pre = preprocess_image_for_ocr(pil)

        # OCR with pytesseract; fallback to blank string on error
        try:
            ocr_text = pytesseract.image_to_string(pre, lang="eng")
        except Exception:
            ocr_text = ""

        transformed = transform_text_for_dyslexia(ocr_text)

        # record usage
        db.increment_usage()

        return JSONResponse({
            "transformed_text": transformed
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/feedback")
async def feedback(rating: int = Form(...), comments: Optional[str] = Form(None)):
    try:
        db.add_feedback(rating=rating, comments=comments)
        return {"status": "ok"}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/stats")
async def stats():
    try:
        return db.get_stats()
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)


