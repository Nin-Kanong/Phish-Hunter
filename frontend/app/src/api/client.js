const base = '/api/v1';
function csrf() { const m = document.cookie.match(/(?:^|; )phishhunter_csrf=([^;]+)/); return m ? decodeURIComponent(m[1]) : ''; }
async function request(path, init = {}) { const headers = new Headers(init.headers); if (init.method && init.method !== 'GET') {
    headers.set('X-CSRF-Token', csrf());
    headers.set('Content-Type', headers.get('Content-Type') || 'application/json');
} const r = await fetch(base + path, { ...init, headers, credentials: 'include' }); if (!r.ok) {
    const t = await r.text();
    throw new Error(t || `${r.status} ${r.statusText}`);
} return r.status === 204 ? undefined : await r.json(); }
export const api = {
    me: () => request('/auth/me'), summary: () => request('/dashboard/summary'),
    users: () => request('/users'), createUser: (body) => request('/users', { method: 'POST', body: JSON.stringify(body) }), updateUser: (id, body) => request(`/users/${id}`, { method: 'PATCH', body: JSON.stringify(body) }),
    cases: () => request('/cases'), createCase: (body) => request('/cases', { method: 'POST', body: JSON.stringify(body) }), caseDetail: (id) => request(`/cases/${id}`), updateCase: (id, body) => request(`/cases/${id}`, { method: 'PATCH', body: JSON.stringify(body) }), linkScan: (caseId, scanId) => request(`/cases/${caseId}/link-scan/${scanId}`, { method: 'POST' }),
    iocs: () => request('/iocs'), reports: () => request('/reports'), report: (id) => request(`/reports/${id}`), jobs: () => request('/jobs'), job: (id) => request(`/jobs/${id}`), startJob: (id) => request(`/jobs/${id}/start`, { method: 'POST' }),
    upload: async (files) => { const f = new FormData(); files.forEach(x => f.append('files', x)); const r = await fetch(base + '/artifacts', { method: 'POST', body: f, credentials: 'include', headers: { 'X-CSRF-Token': csrf() } }); if (!r.ok)
        throw new Error(await r.text()); return r.json(); },
    artifacts: () => request('/artifacts')
};
export function jobSocket(id) { const p = location.protocol === 'https:' ? 'wss' : 'ws'; return new WebSocket(`${p}://${location.host}${base}/jobs/ws/${encodeURIComponent(id)}`); }
