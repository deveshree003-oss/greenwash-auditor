"""Finance agent: extract financial signals and reconcile disclosures."""
from backend.core.llm import ask_with_fallback
from backend.app.tools.parse_utils import parse_first_json
import json


class FinanceAgent:
    def run(self, text: str):
        prompt = f"""
        Carefully extract financial and operational evidence that can be used
        to validate or contradict ESG claims.

        Step-by-step:
        1) Identify numeric and qualitative financial items related to ESG (e.g., capex, investments, divestments).
        2) Normalize amounts and units where possible.
        3) Return structured JSON with the most relevant fields.

        Return JSON:
        {{
          "fossil_investments": "...",
          "renewable_investments": "...",
          "capex": "...",
          "notes": "...",
          "risks": []
        }}

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