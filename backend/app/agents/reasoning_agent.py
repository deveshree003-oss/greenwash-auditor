"""Reasoning agent: orchestrates evidence and derives contradictions.

Implements multi-step, agentic reasoning and dual-validation using Groq
and Together AI. Uses the project's embedding utilities and a vector store
for optional semantic matching.
"""
from backend.core.llm import ask_with_fallback, ask_together
from backend.core.utils import clean_json
from typing import List, Dict, Any

from backend.app.tools.embedding import get_embeddings
from backend.app.tools.vector_store import VectorStore


class SemanticMatcher:
    def __init__(self) -> None:
        self.store = VectorStore()

    def build_index(self, claims: List[str]) -> None:
        embeddings = get_embeddings(claims)
        self.store.add(claims, embeddings)

    def find_similar(self, financial_text: str):
        query_emb = get_embeddings([financial_text])[0]
        return self.store.search(query_emb)


class ReasoningAgent:
    def _build_prompt(self, claims, financials, news) -> str:
                # Enforce strict JSON-only output from the LLM to avoid parsing fallbacks
                return f"""
You are an ESG forensic auditor. STRICT RULES:
- Output ONLY valid JSON (no markdown, no backticks, no extra text).
- Output must be a JSON array (even if empty): []
- Each item must be an object with keys: claim, contradiction, evidence, severity

FORMAT:
[
    {{
        "claim": "...",
        "contradiction": "...",
        "evidence": "...",
        "severity": "High | Medium | Low"
    }}
]

DATA:
CLAIMS: {claims}
FINANCIALS: {financials}
NEWS: {news}
"""

    def _try_parse(self, s: str) -> Any:
        # Use a robust cleaner that extracts/parses JSON blocks and
        # always returns a safe structure (list or dict). Also print
        # the raw output once for debugging.
        try:
            if isinstance(s, str):
                print("RAW LLM OUTPUT:", s)
        except Exception:
            pass

        try:
            return clean_json(s)
        except Exception:
            return []

    def _consensus(self, a: Any, b: Any) -> Any:
        # If both are lists of dicts, return intersection by claim text
        if isinstance(a, list) and isinstance(b, list):
            a_claims = {json.dumps(item.get('claim','')): item for item in a if isinstance(item, dict)}
            b_claims = {json.dumps(item.get('claim','')): item for item in b if isinstance(item, dict)}
            common = []
            for k, item in a_claims.items():
                if k in b_claims:
                    # simple merge: prefer a's fields, supplement with b's
                    merged = {**b_claims[k], **item}
                    common.append(merged)
            return common
        # otherwise, no consensus
        return None
        def _consensus(self, a: Any, b: Any) -> Any:
            """Produce consensus between two agent outputs using fuzzy matching
            and optional embedding similarity.

            Algorithm:
            - Normalize claim text.
            - For each claim in `a`, find best match in `b` using fuzzy ratio.
            - If embeddings available, compute cosine similarity and combine
              into a weighted score.
            - Accept matches with combined score >= threshold and merge fields.
            """
            def normalize(s: str) -> str:
                if not isinstance(s, str):
                    return ""
                s = s.lower()
                s = re.sub(r"\s+", " ", s)
                s = s.translate(str.maketrans('', '', string.punctuation))
                return s.strip()

            def fuzzy_score(x: str, y: str) -> float:
                if not x or not y:
                    return 0.0
                return difflib.SequenceMatcher(None, x, y).ratio()

            def emb_score(x: str, y: str) -> Optional[float]:
                try:
                    emb = get_embeddings([x, y])
                    a_emb, b_emb = emb[0], emb[1]
                    # cosine
                    dot = sum(u * v for u, v in zip(a_emb, b_emb))
                    na = sum(u * u for u in a_emb) ** 0.5
                    nb = sum(v * v for v in b_emb) ** 0.5
                    if na == 0 or nb == 0:
                        return 0.0
                    return dot / (na * nb)
                except Exception:
                    return None

            # thresholds and weights
            FUZZY_THRESH = 0.72
            EMB_THRESH = 0.78
            EMB_WEIGHT = 0.6
            FUZZY_WEIGHT = 0.4
            CONSENSUS_SCORE = 0.75

            if not (isinstance(a, list) and isinstance(b, list)):
                return None

            out = []
            used_b = set()

            for item_a in a:
                if not isinstance(item_a, dict):
                    continue
                claim_a = normalize(item_a.get('claim', ''))
                best = None
                best_score = 0.0
                best_b = None

                for idx_b, item_b in enumerate(b):
                    if not isinstance(item_b, dict):
                        continue
                    claim_b = normalize(item_b.get('claim', ''))
                    f = fuzzy_score(claim_a, claim_b)
                    e = emb_score(claim_a, claim_b)
                    if e is None:
                        combined = f
                    else:
                        combined = FUZZY_WEIGHT * f + EMB_WEIGHT * e

                    if combined > best_score:
                        best_score = combined
                        best = item_b
                        best_b = idx_b

                if best_score >= CONSENSUS_SCORE and best_b not in used_b:
                    # merge: prefer fields from item_a, add score and sources
                    merged = {**best, **item_a}
                    merged['_consensus_score'] = best_score
                    merged['_sources'] = ['groq', 'together']
                    out.append(merged)
                    used_b.add(best_b)

            return out if out else None

    def run(self, claims, financials, news) -> Dict[str, Any]:
        prompt = self._build_prompt(claims, financials, news)

        groq_raw = None
        together_raw = None
        groq_parsed = None
        together_parsed = None

        # Dual validation: Groq primary, Together secondary for reasoning
        try:
            groq_raw = ask_with_fallback(prompt)
            groq_parsed = self._try_parse(groq_raw)
        except Exception as e:
            groq_raw = f"ERROR: {e}"

        try:
            together_raw = ask_together(prompt)
            together_parsed = self._try_parse(together_raw)
        except Exception as e:
            together_raw = f"ERROR: {e}"

        consensus = self._consensus(groq_parsed, together_parsed)

        return {
            "groq": groq_parsed if groq_parsed is not None else groq_raw,
            "together": together_parsed if together_parsed is not None else together_raw,
            "consensus": consensus,
            "raw": {"groq": groq_raw, "together": together_raw},
        }