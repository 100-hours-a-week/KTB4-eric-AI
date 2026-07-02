"""
진입점. 실행 모드 4가지:
  python main.py train      -> Stage 1 사전학습 (챗봇 데이터로 "이어쓰기" 학습)
  python main.py train_qa   -> Stage 2 파인튜닝 (챗봇 Q&A 포맷으로 추가 학습)
  python main.py chat       -> Stage 1 모델과 "이어쓰기" 대화
  python main.py chat_qa    -> Stage 2 모델과 "질문-답변" 대화
"""
import os
import sys
import torch

from chat import chat, chat_qa
from model import device, steps, lr, KoreanGPT
from tokenizer import load_korean_chatbot_data, load_chatbot_qa_data, load_qa_pairs
from sp_tokenizer import train_sp, load_sp, encode, decode
from train_utils import make_batcher, train_loop, make_qa_batcher

SP_VOCAB_SIZE = 16000
SP_PREFIX = "data/sp_korean"   # data/sp_korean.model / .vocab 으로 생성됨

CKPT_DIR = "checkpoints"
GEN_CKPT = os.path.join(CKPT_DIR, "KoreanGPT.pt")      # Stage 1 가중치
QA_CKPT = os.path.join(CKPT_DIR, "KoreanGPT_qa.pt")    # Stage 2 가중치

EARLY_STOP_PATIENCE = 50     # 연속 10번 평가(=200 step) 동안 개선이 없으면 중단
EARLY_STOP_MIN_DELTA = 1e-4

FT_STEPS = 8000
FT_LR = 1e-4                 # Stage 1보다 낮은 lr로 미세조정 (급격한 망각 방지)

def pretrain_path() -> str:
    return "data/processed/pretrain.txt"

def build_pretrain_text() -> str:
    return load_korean_chatbot_data()


os.makedirs("data", exist_ok=True)
os.makedirs(CKPT_DIR, exist_ok=True)

if os.path.exists(f"{SP_PREFIX}.model"):
    sp = load_sp(SP_PREFIX)
else:
    sp = train_sp(pretrain_path(), SP_PREFIX, SP_VOCAB_SIZE)

vocab_size = sp.get_piece_size()


def train_stage1(model):
    token_cache = "data/processed/pretrain_tokens.pt"

    if os.path.exists(token_cache):
        print(f"loading token cache: {token_cache}", flush=True)
        data = torch.load(token_cache, map_location="cpu")
    else:
        print("loading pretrain text...", flush=True)
        text = build_pretrain_text()
        print(f"loaded text: {len(text):,} chars", flush=True)

        print("encoding pretrain text...", flush=True)
        ids = encode(text, sp)
        print(f"encoded tokens: {len(ids):,}", flush=True)

        data = torch.tensor(ids, dtype=torch.long)

        print(f"saving token cache: {token_cache}", flush=True)
        torch.save(data, token_cache)

    print(f"tokens: {len(data):,}, vocab_size: {vocab_size}, device: {device}", flush=True)

    n_train = int(0.9 * len(data))
    get_batch = make_batcher(data[:n_train], data[n_train:])

    print(f"{sum(p.numel() for p in model.parameters()):,} parameters, device={device}", flush=True)

    train_loop(
        model,
        get_batch,
        steps,
        lr,
        GEN_CKPT,
        EARLY_STOP_PATIENCE,
        EARLY_STOP_MIN_DELTA,
        eval_interval=100,
        eval_iters=10,
    )

def train_stage2(model):
    train_pairs = load_qa_pairs(split="train")
    val_pairs = load_qa_pairs(split="val")

    print(f"qa train pairs: {len(train_pairs):,}")
    print(f"qa val pairs: {len(val_pairs):,}, vocab_size: {vocab_size}, device: {device}")

    get_batch = make_qa_batcher(train_pairs, val_pairs, sp)

    if not os.path.exists(GEN_CKPT):
        raise FileNotFoundError(f"{GEN_CKPT} 가 없습니다. 먼저 `python main.py train`을 실행하세요.")

    model.load_state_dict(torch.load(GEN_CKPT, map_location=device))
    print(f"loaded {GEN_CKPT}, fine-tuning device={device}")

    train_loop(
        model,
        get_batch,
        FT_STEPS,
        FT_LR,
        QA_CKPT,
        EARLY_STOP_PATIENCE,
        EARLY_STOP_MIN_DELTA,
        eval_interval=50,
        eval_iters=10,
    )

MODES = {
    "train": train_stage1,
    "train_qa": train_stage2,
    "chat": lambda model: chat(model, sp, GEN_CKPT),
    "chat_qa": lambda model: chat_qa(model, sp, QA_CKPT),
}

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "chat"
    if mode not in MODES:
        sys.exit(f"알 수 없는 모드: {mode} (다음 중 하나를 쓰세요: {', '.join(MODES)})")

    model = KoreanGPT(vocab_size).to(device)
    MODES[mode](model)
