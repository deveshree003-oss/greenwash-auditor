"""Scoring agent: compute risk scores and tiering.

This agent is defensive about the shape of the input from upstream
reasoning components. `reasoning.run()` may return a dict with keys
like `consensus`, `groq`, or `together`. We normalize that here so the
scoring logic always receives a list of contradiction objects.
"""

class ScoringAgent:
    def _extract_list(self, contradictions):
        # If the upstream returns None, treat as unexpected and
        # allow the caller to trigger the numeric fallback.
        if contradictions is None:
            return None

        if isinstance(contradictions, dict):
            return (
                contradictions.get("consensus")
                or contradictions.get("groq")
                or contradictions.get("together")
                or []
            )

        return contradictions or []

    def _normalize_severity(self, item):
        # Accept dicts with different severity keys, or simple strings.
        sev = None
        if isinstance(item, dict):
            for key in ("severity", "Severity", "level", "severity_level"):
                if key in item and item[key] is not None:
                    sev = item[key]
                    break

        if sev is None and isinstance(item, str):
            s = item.lower()
            if "high" in s:
                return "high"
            if "medium" in s:
                return "medium"
            if "low" in s:
                return "low"

        if sev is None:
            return "low"

        return str(sev).strip().lower()

    def run(self, contradictions):
        score = 0

        items = self._extract_list(contradictions)

        # If we still don't have a list, keep the safe fallback.
        if not isinstance(items, (list, tuple)):
            return 50

        for c in items:
            severity = self._normalize_severity(c)

            if severity.startswith("h"):
                score += 30
            elif severity.startswith("m"):
                score += 15
            else:
                score += 5

        return min(score, 100)