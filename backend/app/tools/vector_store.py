"""Vector store with FAISS backend when available, otherwise in-memory fallback.

This module exposes `VectorStore` with `add` and `search` methods. When
`faiss` and `numpy` are available in the environment, a FAISS IndexFlatL2 is
used for efficient nearest-neighbor search. If not, a simple in-memory
cosine-similarity store is used (suitable for small datasets and testing).
"""
from typing import List, Sequence, Tuple
import math

try:
    import faiss
    import numpy as np
    _FAISS_AVAILABLE = True
except Exception:
    _FAISS_AVAILABLE = False


def _cosine(a: Sequence[float], b: Sequence[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


if _FAISS_AVAILABLE:
    class VectorStore:
        def __init__(self, dim: int = 384):
            self.dim = dim
            self.index = faiss.IndexFlatL2(dim)
            self.data: List[str] = []

        def add(self, texts: List[str], embeddings: List[List[float]]) -> None:
            arr = np.array(embeddings).astype('float32')
            if arr.ndim == 1:
                arr = arr.reshape(1, -1)
            self.index.add(arr)
            self.data.extend(texts)

        def search(self, query_embedding: Sequence[float], k: int = 5) -> List[dict]:
            q = np.array([query_embedding]).astype('float32')
            D, I = self.index.search(q, k)
            results = []
            for dist, idx in zip(D[0], I[0]):
                if idx < 0 or idx >= len(self.data):
                    continue
                results.append({"item": self.data[idx], "score": float(-dist)})
            return results
else:
    class VectorStore:
        def __init__(self) -> None:
            self.items: List[str] = []
            self.vectors: List[List[float]] = []

        def add(self, items: List[str], embeddings: List[List[float]]) -> None:
            for it, emb in zip(items, embeddings):
                self.items.append(it)
                self.vectors.append(list(emb))

        def search(self, query_emb: Sequence[float], top_k: int = 5) -> List[dict]:
            scores: List[Tuple[int, float]] = []
            for i, v in enumerate(self.vectors):
                s = _cosine(query_emb, v)
                scores.append((i, s))

            scores.sort(key=lambda x: x[1], reverse=True)
            results = []
            for idx, score in scores[:top_k]:
                results.append({"item": self.items[idx], "score": float(score)})
            return results