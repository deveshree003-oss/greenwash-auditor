from fastapi import APIRouter, UploadFile, Form
from typing import Optional
from datetime import datetime
from backend.app.services.orchestrator import AuditOrchestrator
from backend.core import supabase_client

router = APIRouter()

# in-memory report store (process-lifetime, fallback)
REPORT_STORE = {}

# whether Supabase is configured
USE_SUPABASE = False
try:
    USE_SUPABASE = supabase_client.is_configured()
except Exception:
    USE_SUPABASE = False


def _slugify(value: str) -> str:
    if not value:
        return f"uploaded-{int(datetime.utcnow().timestamp())}"
    return "".join(c.lower() if c.isalnum() else "-" for c in value).strip("-")


@router.post("/audit")
async def audit(
    company: Optional[str] = Form(None),
    # support multiple possible frontend field names
    csr: UploadFile = None,
    finance: UploadFile = None,
    csr_file: UploadFile = None,
    tenk_file: UploadFile = None,
    csr_url: Optional[str] = Form(None),
    tenk_url: Optional[str] = Form(None),
):
    orchestrator = AuditOrchestrator()

    # prefer direct UploadFile fields if provided
    csr_file_obj = csr.file if csr else (csr_file.file if csr_file else None)
    finance_file_obj = finance.file if finance else (tenk_file.file if tenk_file else None)

    result = orchestrator.run(
        csr_file_obj,
        finance_file_obj,
        company or "",
    )

    report_id = _slugify(company or "")

    # build a frontend-friendly report object and store it in memory
    # normalize contradictions into an array the frontend expects
    raw_contradictions = result.get("contradictions")
    if isinstance(raw_contradictions, dict):
        contradictions_list = (
            raw_contradictions.get("consensus")
            or raw_contradictions.get("groq")
            or raw_contradictions.get("together")
            or []
        )
    else:
        contradictions_list = raw_contradictions or []

    # ensure each contradiction is a dict and has a `whyItMatters` explanation
    normalized = []
    for idx, c in enumerate(contradictions_list):
        if not isinstance(c, dict):
            # coerce simple string entries into a minimal structure
            c = {"claim": str(c), "contradiction": "", "evidence": "", "severity": "Unknown"}

        # synthesize a short 'whyItMatters' if missing
        if not c.get("whyItMatters"):
            claim = c.get("claim", "(no claim provided)")
            contradiction = c.get("contradiction", "(no contradiction provided)")
            severity = c.get("severity", "Unknown")
            c["whyItMatters"] = (
                f"Severity: {severity}. The claim '{claim}' may be misleading because {contradiction}."
            )

        # ensure there's an id for frontend keys
        if not c.get("id"):
            c["id"] = f"c-{report_id}-{idx}"

        normalized.append(c)

    contradictions_list = normalized

    # upload any provided files to Supabase Storage (optional)
    files_meta = []
    if USE_SUPABASE:
        try:
            # default bucket name
            bucket = os.environ.get("SUPABASE_STORAGE_BUCKET", "pdfs")
            if csr_file_obj:
                try:
                    csr_file_obj.seek(0)
                except Exception:
                    pass
                data = csr_file_obj.read()
                path = f"reports/{report_id}/csr.pdf"
                public_url = supabase_client.upload_file(bucket, path, data)
                files_meta.append({"field": "csr", "path": path, "url": public_url})

            if finance_file_obj:
                try:
                    finance_file_obj.seek(0)
                except Exception:
                    pass
                data = finance_file_obj.read()
                path = f"reports/{report_id}/finance.pdf"
                public_url = supabase_client.upload_file(bucket, path, data)
                files_meta.append({"field": "finance", "path": path, "url": public_url})
        except Exception:
            # ignore upload errors; still return report
            pass

    if files_meta:
        full_report["files"] = files_meta

    full_report = {
        "id": report_id,
        "company": company or report_id,
        "sector": result.get("sector", ""),
        "scanDate": datetime.utcnow().strftime("%Y-%m-%d"),
        "riskScore": result.get("score", 50),
        "severityBreakdown": result.get("severityBreakdown", {
            "disclosure": 0,
            "capexAlignment": 0,
            "supplyChain": 0,
            "governance": 0,
            "mediaExposure": 0,
        }),
        "stats": {
            "contradictions": len(contradictions_list),
            "documentsScanned": 1 if csr_file_obj or finance_file_obj else 0,
            "regulatoryExposure": 0,
            "flaggedCapex": result.get("financials", {}).get("capex", "Not available"),
        },
        "executiveSummary": result.get("executiveSummary", "Automated audit completed."),
        "legalBrief": {
            "summary": result.get("legal", ""),
            "regulations": [],
            "actions": [],
        },
        "contradictions": contradictions_list,
        "timeline": result.get("timeline", []),
        "news": [
            item if isinstance(item, str) else item.get("title", "") for item in (result.get("news") or [])
        ],
    }

    # simple in-memory storage for generated reports (lifetime: process)
    # persist to Supabase when configured, otherwise keep in-memory
    if USE_SUPABASE:
        saved = supabase_client.save_report(report_id, full_report)
        if not saved:
            # fallback to in-memory if save fails
            REPORT_STORE[report_id] = full_report
    else:
        REPORT_STORE[report_id] = full_report

    return {
        "reportId": report_id,
        "report": full_report,
        "mock": False,
    }





@router.get("/report/{report_id}")
async def get_report(report_id: str):
    """Return a previously generated report by id."""
    # try Supabase first when available
    if USE_SUPABASE:
        try:
            report = supabase_client.fetch_report(report_id)
            if report:
                return {"report": report, "mock": False}
        except Exception:
            # ignore and fallback to in-memory
            pass

    # fallback to in-memory store
    report = REPORT_STORE.get(report_id)
    if report:
        return {"report": report, "mock": False}

    # fallback: return the most recently stored report if any (developer convenience)
    if REPORT_STORE:
        last_key = list(REPORT_STORE.keys())[-1]
        return {"report": REPORT_STORE.get(last_key), "mock": False, "fallback": last_key}

    return {"report": None, "mock": False}