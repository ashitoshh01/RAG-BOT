from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_pipeline import ask_question
from fastapi.responses import FileResponse
import os

app = FastAPI(title="RAG Chatbot API")

# Setup CORS since frontend is running in browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not request.message:
        raise HTTPException(status_code=400, detail="Empty message")

    try:
        answer = ask_question(request.message)
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Optional: serve frontend files if we want to run everything on one port
current_dir = os.path.dirname(os.path.abspath(__file__))


@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(current_dir, "index.html"))


@app.get("/script.js")
async def serve_script():
    return FileResponse(os.path.join(current_dir, "script.js"))


@app.get("/style.css")
async def serve_style():
    return FileResponse(os.path.join(current_dir, "style.css"))


@app.get("/favicon.ico")
async def serve_favicon_ico():
    return FileResponse(os.path.join(current_dir, "favicon.png"))


@app.get("/favicon.png")
async def serve_favicon_png():
    return FileResponse(os.path.join(current_dir, "favicon.png"))
