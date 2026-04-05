export const mockAuditReports = {
  adani: {
    id: 'adani',
    company: 'Adani Green & Ports Group',
    sector: 'Energy / Infrastructure',
    scanDate: '2026-04-04',
    riskScore: 82,
    severityBreakdown: {
      disclosure: 88,
      capexAlignment: 79,
      supplyChain: 72,
      governance: 83,
      mediaExposure: 86,
    },
    stats: {
      contradictions: 5,
      documentsScanned: 3,
      regulatoryExposure: 4,
      flaggedCapex: '$2.1B',
    },
    executiveSummary:
      'Agentic review found repeated sustainability positioning that appears stronger than the company’s disclosed fossil-linked capital allocation, port throughput expansion, and incident reporting controls.',
    legalBrief: {
      summary:
        'The current claim language could invite scrutiny if marketed to EU investors or used in India-facing ESG disclosures without qualification.',
      regulations: [
        'EU Taxonomy Article 8',
        'SEBI BRSR Principle 2',
        'SEBI BRSR Principle 6',
      ],
      actions: [
        'Qualify carbon-neutral language with scope boundaries and offsets methodology.',
        'Reconcile transition narrative against planned oil, gas, and logistics capex.',
        'Attach dated evidence for remediation commitments and incident reduction trends.',
      ],
    },
    contradictions: [
      {
        id: 'c1',
        title: 'Carbon-neutral positioning conflicts with fossil-linked expansion capex',
        severity: 'high',
        confidence: 0.94,
        claimSource: 'CSR Report 2025',
        claimCitation: 'Pg. 18',
        evidenceSource: '10-K FY2025',
        evidenceCitation: 'Pg. 92',
        claim:
          'We are on track to operate a carbon-neutral growth model across all strategic business lines.',
        evidence:
          'Capital commitments include expanded storage and logistics capacity connected to oil and gas throughput operations.',
        whyItMatters:
          'The growth claim is enterprise-wide, but the financial filings show material investment in high-emission linked infrastructure.',
        regulations: ['EU Taxonomy', 'SEBI BRSR'],
      },
      {
        id: 'c2',
        title: 'Water-positive claim is not supported by site-level incident disclosures',
        severity: 'high',
        confidence: 0.89,
        claimSource: 'Sustainability Microsite',
        claimCitation: 'Water Stewardship section',
        evidenceSource: 'Environmental Incident Log',
        evidenceCitation: '2025 Q3 entries',
        claim:
          'Our industrial footprint is water-positive in every region where we operate.',
        evidence:
          'Two operating clusters reported untreated discharge incidents and unresolved groundwater extraction variance notes.',
        whyItMatters:
          'Absolute marketing language leaves little room for unresolved variance between sites.',
        regulations: ['SEBI BRSR'],
      },
      {
        id: 'c3',
        title: 'Low-risk supply chain narrative conflicts with forced labor watchlist exposure',
        severity: 'medium',
        confidence: 0.81,
        claimSource: 'CSR Report 2025',
        claimCitation: 'Pg. 44',
        evidenceSource: 'Third-party supplier screening memo',
        evidenceCitation: 'Appendix B',
        claim:
          'All critical suppliers meet our advanced human-rights screening threshold.',
        evidence:
          'Four tier-two suppliers remain on enhanced review following labor-rights allegations with incomplete remediation evidence.',
        whyItMatters:
          'The company may have strong controls, but the current phrasing overstates completion and assurance.',
        regulations: ['SEBI BRSR'],
      },
      {
        id: 'c4',
        title: 'Renewables-led narrative omits rising emissions intensity from logistics growth',
        severity: 'medium',
        confidence: 0.77,
        claimSource: 'Investor Sustainability Deck',
        claimCitation: 'Slide 6',
        evidenceSource: '10-K FY2025',
        evidenceCitation: 'Pg. 101',
        claim:
          'Renewable growth now structurally decouples our expansion from emissions intensity.',
        evidence:
          'Absolute logistics throughput and associated Scope 3 estimates increased year over year as port activity expanded.',
        whyItMatters:
          'Decoupling implies measured improvement, but the filing suggests exposure is still rising in material segments.',
        regulations: ['EU Taxonomy'],
      },
      {
        id: 'c5',
        title: 'Safety leadership claim conflicts with unresolved community-impact reporting',
        severity: 'low',
        confidence: 0.7,
        claimSource: 'Annual Sustainability Review',
        claimCitation: 'Pg. 58',
        evidenceSource: 'News / NGO incident digest',
        evidenceCitation: 'Nov 2025 coverage',
        claim:
          'We maintain industry-leading zero-harm standards for employees and adjacent communities.',
        evidence:
          'News coverage documents pending compensation disputes and a community complaint cluster near one expansion corridor.',
        whyItMatters:
          'This looks less like fraud than unsupported superlative language, but it still increases reputational exposure.',
        regulations: ['SEBI BRSR'],
      },
    ],
    timeline: [
      {
        year: '2023',
        label: 'Net-zero acceleration announced',
        detail:
          'Public narrative shifted toward enterprise-scale decarbonization and green infrastructure branding.',
      },
      {
        year: '2024',
        label: 'Transition capex narrative expands',
        detail:
          'Investor materials increasingly emphasized renewable adjacency while logistics spending also increased.',
      },
      {
        year: '2025',
        label: 'Contradictions become material',
        detail:
          'Financial filings surfaced larger fossil-linked commitments and media scrutiny around impact disclosures.',
      },
    ],
    news: [
      'Regional reporting highlighted water discharge complaints near a port-linked industrial cluster.',
      'Investor analysts questioned the basis for enterprise-wide carbon-neutral phrasing.',
      'An NGO brief flagged supply-chain due diligence gaps in imported components.',
    ],
  },
  reliance: {
    id: 'reliance',
    company: 'Reliance Industries',
    sector: 'Energy / Conglomerate',
    scanDate: '2026-04-04',
    riskScore: 68,
    severityBreakdown: {
      disclosure: 72,
      capexAlignment: 70,
      supplyChain: 61,
      governance: 65,
      mediaExposure: 69,
    },
    stats: {
      contradictions: 4,
      documentsScanned: 3,
      regulatoryExposure: 3,
      flaggedCapex: '$1.4B',
    },
    executiveSummary:
      'The audit surfaced fewer severe contradictions, but the transition messaging still appears ahead of some disclosed operational realities.',
    legalBrief: {
      summary:
        'The company’s claims are more qualified overall, though certain transition and plastics narratives may still need clearer supporting evidence.',
      regulations: ['EU Taxonomy Article 8', 'SEBI BRSR Principle 6'],
      actions: [
        'Tighten wording around plastics circularity outcomes.',
        'Separate announced renewable ambitions from current fossil revenue dependence.',
      ],
    },
    contradictions: [],
    timeline: [
      {
        year: '2024',
        label: 'Circularity campaign expands',
        detail: 'Packaging and materials messaging became more ambitious.',
      },
      {
        year: '2025',
        label: 'Transition spend increases',
        detail: 'Renewables announcements grew, but fossil dependence remained material.',
      },
    ],
    news: [
      'Coverage remained mixed, with analysts focused on execution and timeline realism.',
    ],
  },
  tata: {
    id: 'tata',
    company: 'Tata Power',
    sector: 'Utilities',
    scanDate: '2026-04-04',
    riskScore: 41,
    severityBreakdown: {
      disclosure: 46,
      capexAlignment: 40,
      supplyChain: 34,
      governance: 43,
      mediaExposure: 38,
    },
    stats: {
      contradictions: 2,
      documentsScanned: 2,
      regulatoryExposure: 2,
      flaggedCapex: '$420M',
    },
    executiveSummary:
      'The company still shows some disclosure tension, but claims were generally more qualified and easier to reconcile with filings.',
    legalBrief: {
      summary:
        'Residual risk is mostly tied to overbroad phrasing rather than severe contradiction.',
      regulations: ['SEBI BRSR Principle 6'],
      actions: [
        'Keep site-level metrics next to enterprise-wide sustainability statements.',
      ],
    },
    contradictions: [],
    timeline: [
      {
        year: '2025',
        label: 'Disclosure quality improves',
        detail: 'Claims became more measurable and tied to stated scopes.',
      },
    ],
    news: ['No major greenwashing-linked incident clusters were detected in the mock feed.'],
  },
};

export function buildAuditSummary(report) {
  const contradictionLines = report.contradictions
    .map(
      (item, index) =>
        `${index + 1}. ${item.title}\n   Claim: ${item.claim}\n   Evidence: ${item.evidence}\n   Tags: ${item.regulations.join(', ')}`,
    )
    .join('\n\n');

  return [
    'Greenwashing Integrity Audit Summary',
    `Company: ${report.company}`,
    `Scan Date: ${report.scanDate}`,
    `Risk Score: ${report.riskScore}/100`,
    '',
    'Executive Summary',
    report.executiveSummary,
    '',
    'Key Contradictions',
    contradictionLines || 'No contradictions in mock data.',
    '',
    'Legal Brief',
    report.legalBrief.summary,
    `Regulations: ${report.legalBrief.regulations.join(', ')}`,
  ].join('\n');
}
