import os, faiss, pickle, numpy as np
from utils.embedding import get_embedding

def retrieve(query: str, k=4, index_dir="index"):
    index = faiss.read_index(f"{index_dir}/chunks.index")
    with open(f"{index_dir}/chunks.pkl", "rb") as f:
        data = pickle.load(f)
    q = np.array([get_embedding(query)], dtype="float32")
    faiss.normalize_L2(q)
    scores, ids = index.search(q, k)
    res = []
    for s, i in zip(scores[0], ids[0]):
        res.append({"score": float(s), "text": data["texts"][i], "meta": data["metas"][i]})
    return res
