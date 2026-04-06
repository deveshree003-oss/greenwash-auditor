"""Legal agent: map findings to potential regulatory violations and briefs."""
from backend.core.llm import ask_with_fallback

class LegalAgent:
    def run(self, contradictions):
        prompt = f"""
        Map contradictions to regulations:

        - EU Taxonomy
        - SEBI BRSR

        Provide legal explanation.

        DATA:
        {contradictions}
        """

        return ask_with_fallback(prompt)