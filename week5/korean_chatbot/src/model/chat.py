"""
CLI 대화 인터페이스 (SentencePiece 버전).
chat(): Stage 1 가중치로 "이어쓰기" 데모
chat_qa(): Stage 2 가중치로 "질문: ...\n답변: " Q&A REPL

generate_reply_qa()는 chat_qa()와 같은 로직을 함수로 분리해둔 것으로,
app.py(FastAPI)에서 그대로 재사용합니다.
"""
import torch

from model import device


def _qa_stop_tokens(sp):
    """줄바꿈으로 끝나는 piece가 나오면 '답변: ...' 한 줄이 끝난 것으로 본다."""
    return {
        i for i in range(sp.get_piece_size())
        if sp.id_to_piece(i).endswith("\n")
    }


def _sentence_end_stop_tokens(sp):
    """'.', '?', '!'로 끝나는 piece가 나오면 한 문장이 끝난 것으로 본다."""
    return {
        i for i in range(sp.get_piece_size())
        if sp.id_to_piece(i) and sp.id_to_piece(i)[-1] in ".?!"
    }


@torch.no_grad()
def generate_reply_qa(model, sp, question: str, max_new_tokens: int = 60) -> str:
    """질문 문자열 하나를 받아 "질문: ...\n답변: " 포맷으로 모델에 넣고, 답변 부분만 반환."""
    stop_tokens = _qa_stop_tokens(sp)
    prompt = f"질문: {question}\n답변: "
    ids = sp.encode(prompt, out_type=int)
    idx = torch.tensor([ids], dtype=torch.long, device=device)
    out = model.generate(
        idx, max_new_tokens, stop_tokens=stop_tokens,
        temperature=0.2, top_k=1, repetition_penalty=1.2,
    )[0].tolist()
    return sp.decode(out[len(ids):]).strip()


def chat(model, sp, ckpt_path: str = "checkpoints/KoreanGPT.pt"):
    model.load_state_dict(torch.load(ckpt_path, map_location=device))
    model.eval()
    stop_tokens = _sentence_end_stop_tokens(sp)
    print("프롬프트를 입력하면 이어서 문장을 생성합니다 (빈 줄 또는 Ctrl-D로 종료).")
    while True:
        try:
            prompt = input("> ")
        except EOFError:
            break
        if not prompt:
            break
        ids = sp.encode(prompt, out_type=int)
        idx = torch.tensor([ids], dtype=torch.long, device=device)
        out = model.generate(
            idx, 200, stop_tokens=stop_tokens,
            temperature=0.8, top_k=1, repetition_penalty=1.3,
        )[0].tolist()
        print(sp.decode(out[len(ids):]))  # 이어진 부분만 출력


def chat_qa(model, sp, ckpt_path: str = "checkpoints/KoreanGPT_qa.pt"):
    """Stage 2: "질문: ...\n답변: " 포맷으로 파인튜닝된 모델과의 Q&A REPL."""
    model.load_state_dict(torch.load(ckpt_path, map_location=device))
    model.eval()
    print("질문을 입력하세요 (빈 줄 또는 Ctrl-D로 종료).")
    while True:
        try:
            question = input("질문: ")
        except EOFError:
            break
        if not question:
            break
        reply = generate_reply_qa(model, sp, question)
        print("답변:", reply)
