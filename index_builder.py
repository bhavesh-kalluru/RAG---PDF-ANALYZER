import os, faiss, pickle
from pathlib import Path
import numpy as np
from utils.embedding import get_embedding

CHUNK_SIZE, CHUNK_OVERLAP = 500, 100

def chunk_text(text: str) -> list[str]:
    words = text.split()
    step = CHUNK_SIZE - CHUNK_OVERLAP
    return [" ".join(words[i:i+CHUNK_SIZE]) for i in range(0, len(words), step)]

def run(data_dir="data", index_dir="index"):
    os.makedirs(index_dir, exist_ok=True)
    texts, metas = [], []
    for path in Path(data_dir).glob("*.txt"):
        content = path.read_text(encoding="utf-8", errors="ignore").strip()
        for i, ch in enumerate(chunk_text(content)):
            texts.append(ch)
            metas.append({"source": str(path), "chunk_id": i})
    if not texts:
        raise RuntimeError("No .txt files found in data/")
    vecs = np.array([get_embedding(t) for t in texts]).astype("float32")
    faiss.normalize_L2(vecs)
    index = faiss.IndexFlatIP(vecs.shape[1])
    index.add(vecs)
    faiss.write_index(index, f"{index_dir}/chunks.index")
    with open(f"{index_dir}/chunks.pkl", "wb") as f:
        pickle.dump({"texts": texts, "metas": metas}, f)
    print(f"Indexed {len(texts)} chunks from {len(metas)} docs.")
