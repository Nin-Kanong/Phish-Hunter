# Phish-Hunter Workbench (React + JavaScript)

This is the JavaScript/JSX source for the investigation workbench. It uses React, Vite, React Query, React Router, and Zustand, and communicates with the existing FastAPI API.

- `src/api/client.js` calls the `/api/v1/*` API.
- `src/pages/` contains dashboard, cases, artifacts, jobs, IOCs, reports, timeline, graph, upload, users, and settings screens.
- `src/hooks/useLiveJob.js` manages live job updates.
- `src/store/uiStore.js` stores navigation state.
- `src/components/` contains shared UI components.

## Build

```bash
npm install
npm run build
```

The Vite output is configured to land in `phishhunter/web/static/workbench`.

The Python application also ships its server-side workbench, so this React bundle is an enhancement rather than a replacement for the main site.
