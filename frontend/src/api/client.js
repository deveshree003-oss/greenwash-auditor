import axios from 'axios';
import { buildAuditSummary, mockAuditReports } from '../data/mock';

const http = axios.create({
  baseURL: '/api',
  timeout: 12000,
});

function wait(ms) {
  return new Promise((resolve) => {
    window.setTimeout(resolve, ms);
  });
}

function slugify(value) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
}

export async function runAudit(payload) {
  try {
    const formData = new FormData();
    if (payload.company) {
      formData.append('company', payload.company);
    }

    if (payload.csrUrl) {
      formData.append('csr_url', payload.csrUrl);
    }

    if (payload.tenKUrl) {
      formData.append('tenk_url', payload.tenKUrl);
    }

    if (payload.csrFile) {
      formData.append('csr_file', payload.csrFile);
    }

    if (payload.tenKFile) {
      formData.append('tenk_file', payload.tenKFile);
    }

    const response = await http.post('/audit', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    return response.data;
  } catch (error) {
    // If the proxied request failed (vite proxy not running or 404),
    // try the backend directly before returning demo mock data.
    try {
      const formData = new FormData();
      if (payload.company) formData.append('company', payload.company);
      if (payload.csrUrl) formData.append('csr_url', payload.csrUrl);
      if (payload.tenKUrl) formData.append('tenk_url', payload.tenKUrl);
      if (payload.csrFile) formData.append('csr_file', payload.csrFile);
      if (payload.tenKFile) formData.append('tenk_file', payload.tenKFile);

      const direct = await fetch('http://127.0.0.1:8000/audit', {
        method: 'POST',
        body: formData,
      });

      if (direct.ok) {
        const data = await direct.json();
        return data;
      }
    } catch (directErr) {
      // swallow and fall back to mock below
      // console.debug('Direct backend attempt failed', directErr);
    }

    await wait(800);
    const fallbackKey =
      Object.keys(mockAuditReports).find((key) =>
        payload.company?.toLowerCase().includes(key),
      ) || 'adani';

    return {
      reportId: mockAuditReports[fallbackKey].id,
      report: mockAuditReports[fallbackKey],
      mock: true,
      error: error.message,
    };
  }
}

export async function fetchReport(companyId) {
  try {
    const response = await http.get(`/report/${companyId}`);
    return response.data;
  } catch (error) {
    await wait(500);
    return {
      report: mockAuditReports[companyId] || mockAuditReports.adani,
      mock: true,
      error: error.message,
    };
  }
}

export async function fetchComparison(ids) {
  await wait(300);
  return ids.map((id) => mockAuditReports[id]).filter(Boolean);
}

export function getAvailableCompanies() {
  return Object.values(mockAuditReports).map((report) => ({
    id: report.id,
    company: report.company,
    sector: report.sector,
    riskScore: report.riskScore,
  }));
}

export function downloadAuditSummary(report) {
  const blob = new Blob([buildAuditSummary(report)], {
    type: 'text/plain;charset=utf-8',
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `${slugify(report.company)}-audit-summary.txt`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

// Direct helper to POST two file objects (`csrFile`, `financeFile`) to
// the backend `/audit` endpoint running on localhost:8000. Use when you
// want to call the Python FastAPI server directly instead of the proxy.
export async function runAuditFiles(csrFile, financeFile) {
  const formData = new FormData();
  formData.append('csr', csrFile);
  formData.append('finance', financeFile);

  const res = await fetch('http://localhost:8000/audit', {
    method: 'POST',
    body: formData,
  });

  return res.json();
}
