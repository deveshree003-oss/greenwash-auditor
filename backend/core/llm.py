import os
from backend.core.config import OPENAI_API_KEY, GROQ_API_KEY
from openai import OpenAI
import requests

try:
    from groq import Groq
except Exception:
    Groq = None

# initialize clients (may be None if package not installed)
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
groq_client = Groq(api_key=GROQ_API_KEY) if (GROQ_API_KEY and Groq is not None) else None
# allow overriding the Groq model via env; default to a smaller Llama3 variant
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")
# Respect explicit provider selection
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "groq").lower()

# Together AI settings (config.py exposes keys too)
from backend.core.config import TOGETHER_API_KEY, TOGETHER_MODEL, TOGETHER_API_URL



# ⚡ FAST TASKS (Groq)
def ask_fast(prompt: str):
    if groq_client is None:
        raise RuntimeError("Groq client not available or GROQ_API_KEY not set")

    try:
        res = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return res.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Groq request failed: {e}. If this mentions a decommissioned model, set GROQ_MODEL to a supported model in your .env")


# 🧠 SMART TASKS (OpenAI)
def ask_smart(prompt: str):
    if openai_client is None:
        raise RuntimeError("OpenAI client not available or OPENAI_API_KEY not set")

    res = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return res.choices[0].message.content


# ==== TOGETHER AI =====
def ask_together(prompt: str):
    if not TOGETHER_API_KEY or not TOGETHER_MODEL:
        raise RuntimeError("Together AI not configured. Set TOGETHER_API_KEY and TOGETHER_MODEL in your .env")

    url = f"{TOGETHER_API_URL.rstrip('/')}/v1/models/{TOGETHER_MODEL}/generate"
    headers = {"Authorization": f"Bearer {TOGETHER_API_KEY}", "Content-Type": "application/json"}
    payload = {"prompt": prompt, "max_tokens": 512}
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=30)
        r.raise_for_status()
        data = r.json()
        # attempt common response fields
        for key in ("output", "text", "completion", "choices", "result"):
            if key in data:
                return str(data[key])
        return str(data)
    except Exception as e:
        raise RuntimeError(f"Together AI request failed: {e}")


# Backwards-compatible alias
def ask_llm(prompt: str):
    return ask_smart(prompt)


def ask_with_fallback(prompt: str):
    """Try `ask_fast` (Groq) first, fall back to `ask_smart` (OpenAI),
    and return a simple error string on failure. Honor `MODEL_PROVIDER`.
    """
    # If the configuration forces OpenAI, skip Groq entirely
    if MODEL_PROVIDER == "openai":
        try:
            return ask_smart(prompt)
        except Exception:
            return "LLM Error"

    # If the configuration forces Groq-only, skip OpenAI fallback
    if MODEL_PROVIDER == "groq":
        try:
            return ask_fast(prompt)
        except Exception:
            return "LLM Error"

    # If the configuration forces Together AI, use it only
    if MODEL_PROVIDER == "together":
        try:
            return ask_together(prompt)
        except Exception:
            return "LLM Error"

    # Default: try Groq first, then Together, then fall back to OpenAI
    try:
        return ask_fast(prompt)
    except Exception:
        try:
            return ask_together(prompt)
        except Exception:
            try:
                return ask_smart(prompt)
            except Exception:
                return "LLM Error"