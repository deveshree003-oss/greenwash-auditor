"""CSR-specific agent: analyze CSR reports and extract claims."""
from backend.core.llm import ask_with_fallback
from backend.app.tools.parse_utils import parse_first_json
import json


class CSRClaimAgent:
    def run(self, text: str):
        prompt = f"""
        Carefully extract sustainability claims from the text.

        Step-by-step:
        1) Identify each explicit or implicit claim in the document.
        2) Normalize each claim into a short sentence.
        3) Tag the claim type: emissions | net_zero | renewable | ESG | other.

        Return JSON array:
        [
          {{
            "claim": "...",
            "type": "emissions | net_zero | renewable | ESG | other"
          }}
        ]

        TEXT:
        {text[:4000]}
        """

        res = ask_with_fallback(prompt)
        try:
          parsed = parse_first_json(res)
          return parsed
        except Exception:
          try:
            return json.loads(res)
          except Exception:
            return {"raw": res}