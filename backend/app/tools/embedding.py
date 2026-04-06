"""Lightweight embedding utilities.

Prefer `sentence-transformers` when available; otherwise fall back to a
deterministic, dependency-free pseudo-embedding implementation using
SHA-256. This keeps editor/type-checker happy if `sentence-transformers`
is not installed.
"""
from typing import List
import hashlib

_ST_AVAILABLE = False
_MODEL = None
try:
    from sentence_transformers import SentenceTransformer

    _MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    _ST_AVAILABLE = True
except Exception:
    # sentence-transformers not available in this environment; fall back
    _ST_AVAILABLE = False


def get_embeddings(texts: List[str]) -> List[List[float]]:
    """Return embeddings for `texts`.

    Uses `sentence-transformers` when available, otherwise returns a
    deterministic 32-d pseudo-embedding for each string.
    """
    if _ST_AVAILABLE and _MODEL is not None:
        vecs = _MODEL.encode(texts)
        # ensure list-of-lists of floats
        return [list(map(float, v)) for v in vecs]

    vectors: List[List[float]] = []
    for t in texts:
        h = hashlib.sha256(t.encode("utf-8")).digest()
        vec = [b / 255.0 for b in h[:32]]
        vectors.append(vec)
    return vectors