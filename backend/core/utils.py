import json
import re
from typing import Any


def clean_json(text: str) -> Any:
    """Attempt to return parsed JSON from `text`.

    - First try a direct json.loads
    - Then try to extract the first JSON array or object block using regex
    - If parsing fails, return an empty list as a safe fallback
    """
    if not isinstance(text, str):
        return []

    try:
        return json.loads(text)
    except Exception:
        pass

    # try to find a JSON array first
    arr_match = re.search(r"\[\s*\{.*?\}\s*\]", text, re.DOTALL)
    if arr_match:
        try:
            return json.loads(arr_match.group(0))
        except Exception:
            pass

    # try to find a JSON object
    obj_match = re.search(r"\{.*\}", text, re.DOTALL)
    if obj_match:
        try:
            return json.loads(obj_match.group(0))
        except Exception:
            pass

    return []
