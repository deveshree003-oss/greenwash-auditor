from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="GreenTrace API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "GreenTrace API is running!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/audit/mock/{company_name}")
def mock_audit(company_name: str):
    return {
        "company_name": company_name,
        "risk_score": 74,
        "risk_tier": "HIGH",
        "contradictions_found": 5,
        "pages_analyzed": 312,
        "documents_processed": 2,
        "score_breakdown": {
            "csr_vs_financial": 82,
            "csr_vs_news": 68,
            "financial_vs_news": 71
        },
        "contradictions": [
            {
                "id": "c1",
                "severity": "CRITICAL",
                "category": "Carbon Emissions",
                "claim": "Committed to net-zero by 2030.",
                "source_doc": "CSR Report 2024",
                "source_page": 14,
                "evidence": "Rs 12,400 Cr allocated to coal infrastructure in FY24.",
                "evidence_doc": "10-K Filing 2024",
                "evidence_page": 87,
                "news_corroboration": None,
                "contradiction_score": 91,
                "regulations": ["SEBI BRSR Principle 1", "GRI 305-1"]
            },
            {
                "id": "c2",
                "severity": "HIGH",
                "category": "Deforestation",
                "claim": "Zero deforestation policy in place.",
                "source_doc": "CSR Report 2024",
                "source_page": 28,
                "evidence": "4,200 hectares of forest land cleared for port expansion.",
                "evidence_doc": "10-K Filing 2024",
                "evidence_page": 142,
                "news_corroboration": "Locals protest mangrove clearing near Mundra",
                "contradiction_score": 85,
                "regulations": ["SEBI BRSR Principle 6"]
            },
            {
                "id": "c3",
                "severity": "HIGH",
                "category": "Water Stewardship",
                "claim": "Achieved 45% water recycling rate, targeting 100% ZLD by 2026.",
                "source_doc": "CSR Report 2024",
                "source_page": 41,
                "evidence": "Rs 340 Cr penalty paid for unauthorized water discharge.",
                "evidence_doc": "10-K Filing 2024",
                "evidence_page": 201,
                "news_corroboration": "Queensland authority fines for groundwater breach",
                "contradiction_score": 78,
                "regulations": ["SEBI BRSR Principle 6", "GRI 303-4"]
            }
        ],
        "legal_briefing": {
            "jurisdiction": "India (SEBI BRSR)",
            "summary": "Material violations found under SEBI BRSR Principles 1 and 6. GHG discrepancies constitute potential misrepresentation under SEBI Circular 2021/562.",
            "violations": [
                {
                    "regulation": "SEBI BRSR Principle 1",
                    "clause": "Essential Indicator 4",
                    "description": "GHG emission disclosures must reconcile with financial capex filings.",
                    "severity": "CRITICAL"
                }
            ]
        },
        "timeline": [
            {"date": "Jan 2024", "event": "CSR Report published claiming net-zero roadmap", "type": "claim"},
            {"date": "Mar 2024", "event": "10-K filed: Rs 12,400 Cr coal capex disclosed", "type": "contradiction"},
            {"date": "Jun 2024", "event": "Mangrove forest clearing reported by local NGO", "type": "news"}
        ]
    }