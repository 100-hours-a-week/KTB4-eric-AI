import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "model")
sys.path.append(MODEL_DIR)

from model import device, KoreanGPT
from sp_tokenizer import load_sp
from chat import generate_reply_qa

SP_PREFIX = os.path.join(MODEL_DIR, "data", "sp_korean")
QA_CKPT = os.path.join(MODEL_DIR, "checkpoints", "KoreanGPT_qa.pt")

model_store = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.exists(f"{SP_PREFIX}.model"):
        raise FileNotFoundError(
            f"{SP_PREFIX}.model 이 없습니다. src/model 폴더에서 "
            "`python3 main.py train` 을 먼저 실행해주세요."
        )
    if not os.path.exists(QA_CKPT):
        raise FileNotFoundError(
            f"{QA_CKPT} 가 없습니다. src/model 폴더에서 "
            "`python3 main.py train_qa` 를 먼저 실행해주세요."
        )

    print("모델 로딩 중...")
    sp = load_sp(SP_PREFIX)
    vocab_size = sp.get_piece_size()

    model = KoreanGPT(vocab_size).to(device)
    import torch
    model.load_state_dict(torch.load(QA_CKPT, map_location=device))
    model.eval()

    model_store["model"] = model
    model_store["sp"] = sp
    print(f"모델 로딩 완료. (vocab_size={vocab_size}, device={device})")
    yield
    model_store.clear()


app = FastAPI(title="한국어 챗봇 API (KoreanGPT)", lifespan=lifespan)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.get("/generate")
def health_check():
    return {"status": "ok", "device": str(device)}


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="message가 비어있습니다.")

    reply = generate_reply_qa(model_store["model"], model_store["sp"], request.message)
    return ChatResponse(reply=reply)