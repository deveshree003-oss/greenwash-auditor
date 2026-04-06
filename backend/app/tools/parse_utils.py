import json
import re
from typing import Any, Optional


def _find_code_block(text: str) -> Optional[str]:
    # look for ```json ... ``` or ``` ... ``` blocks
    m = re.search(r"```json\s*(.*?)```", text, re.S | re.I)
    if m:
        return m.group(1).strip()
    m = re.search(r"```\s*(.*?)```", text, re.S)
    if m:
        return m.group(1).strip()
    return None


def _balanced_brackets_substring(text: str, start_idx: int) -> Optional[str]:
    stack = []
    pairs = {'{': '}', '[': ']'}
    opening = set(pairs.keys())
    closing = set(pairs.values())
    for i in range(start_idx, len(text)):
        ch = text[i]
        if ch in opening:
            stack.append(pairs[ch])
        elif ch in closing:
            if not stack:
                return None
            expected = stack.pop()
            if ch != expected:
                return None
            if not stack:
                return text[start_idx:i+1]
    return None


def parse_first_json(text: str) -> Any:
    """Attempt to extract and parse the first JSON object/array from `text`.

    Returns the parsed JSON structure if found, else raises ValueError.
    """
    if not text or not isinstance(text, str):
        raise ValueError("No text to parse")

    # 1) try direct load
    try:
        return json.loads(text)
    except Exception:
        pass

    # 2) try code block
    code = _find_code_block(text)
    if code:
        try:
            return json.loads(code)
        except Exception:
            # try to strip leading/trailing non-json
            s = code.strip()
            # fallthrough
            pass

    # 3) find first { or [ and attempt to extract balanced substring
    m = re.search(r"[\{\[]", text)
    if m:
        substr = _balanced_brackets_substring(text, m.start())
        if substr:
            try:
                return json.loads(substr)
            except Exception:
                pass

    raise ValueError("No JSON found in text")
