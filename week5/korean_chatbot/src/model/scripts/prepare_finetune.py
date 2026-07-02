import ast
import csv
import random
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw_hf"
OUT_DIR = ROOT / "data" / "processed"

OUT_DIR.mkdir(parents=True, exist_ok=True)

SMALLTALK_PATH = ROOT / "data" / "raw_hf" / "smalltalk" / "smalltalk_all.csv"
PERSONA_PATH = ROOT / "data" / "raw_hf" / "nlpbada" / "korean-persona-chat-dataset-2.csv"

TRAIN_PATH = OUT_DIR / "qa_train.csv"
VAL_PATH = OUT_DIR / "qa_val.csv"


def clean_text(text):
    return str(text).replace("\n", " ").strip()


def load_smalltalk(rows):
    if not SMALLTALK_PATH.exists():
        print(f"skip: {SMALLTALK_PATH} 없음")
        return

    df = pd.read_csv(SMALLTALK_PATH)

    for _, row in df.iterrows():
        question = clean_text(row.get("question", ""))
        answer = clean_text(row.get("answer", ""))

        if question and answer:
            rows.append({
                "question": question,
                "answer": answer,
            })

    print(f"loaded smalltalk: {len(df):,}")


def load_persona(rows):
    if not PERSONA_PATH.exists():
        print(f"skip: {PERSONA_PATH} 없음")
        return

    df = pd.read_csv(PERSONA_PATH)
    count = 0

    for _, row in df.iterrows():
        dialog_text = row.get("session_dialog", "")

        try:
            dialog = ast.literal_eval(dialog_text)
        except Exception:
            continue

        if not isinstance(dialog, list):
            continue

        dialog = [clean_text(x) for x in dialog if clean_text(x)]

        for i in range(len(dialog) - 1):
            question = dialog[i]
            answer = dialog[i + 1]

            if question and answer:
                rows.append({
                    "question": question,
                    "answer": answer,
                })
                count += 1

    print(f"loaded persona pairs: {count:,}")


def save_csv(path, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["question", "answer"])
        writer.writeheader()
        writer.writerows(rows)


def main():
    rows = []

    load_smalltalk(rows)
    load_persona(rows)

    random.seed(42)
    random.shuffle(rows)

    split_idx = int(len(rows) * 0.9)
    train_rows = rows[:split_idx]
    val_rows = rows[split_idx:]

    save_csv(TRAIN_PATH, train_rows)
    save_csv(VAL_PATH, val_rows)

    print(f"saved train: {TRAIN_PATH} ({len(train_rows):,})")
    print(f"saved val: {VAL_PATH} ({len(val_rows):,})")


if __name__ == "__main__":
    main()