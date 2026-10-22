# Phish-Hunter

### Hunting the phish. Turning evidence into explainable findings.

**Phish-Hunter** is a defensive security operations and investigation platform built around a Python/FastAPI backend, with React + JavaScript interfaces for the investigation workbench. It helps analysts examine suspicious emails, URLs, files, network captures, indicators of compromise (IOCs), and threat-intelligence evidence in dedicated workspaces.

[![Python](https://img.shields.io/badge/Python-3.12--3.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/UI-React-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![JavaScript](https://img.shields.io/badge/Frontend-JavaScript-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![License](https://img.shields.io/badge/License-Apache--2.0-blue)](LICENSE)

> **Important — where to run Phish-Hunter:** A Vercel preview is available, but the current Vercel/serverless deployment does **not** support every workflow reliably. The project has shown session/persistence problems when its secret or database configuration is not consistent, and large PCAP uploads hit Vercel's hard **4.5 MB request-body limit**. For the most complete feature set—including larger evidence files and in-process analysis jobs—run Phish-Hunter locally with `python run.py`, or deploy the full Python app to a persistent Python host with PostgreSQL and durable storage. See [Vercel limitations](#vercel-preview-known-limitations) and [Run locally](#run-locally-recommended-for-full-functionality).

**Vercel preview:** [phish-hunter-duik.vercel.app](https://phish-hunter-duik.vercel.app/) *(preview only; change this link if your active deployment uses a different Vercel domain).* 

---

## Contents

- [Platform overview](#platform-overview)
- [Main capabilities](#main-capabilities)
- [Analyst workspaces](#analyst-workspaces)
- [Analysis pipeline and reports](#analysis-pipeline-and-reports)
- [Run locally — recommended for full functionality](#run-locally-recommended-for-full-functionality)
- [Create the first administrator](#create-the-first-administrator)
- [React + JavaScript frontends](#react--javascript-frontends)
- [Vercel preview: known limitations](#vercel-preview-known-limitations)
- [Production deployment options](#production-deployment-options)
- [Configuration and integrations](#configuration-and-integrations)
- [Security boundaries](#security-boundaries)
- [Verification and development](#verification-and-development)
- [Project structure](#project-structure)

## Platform overview

Phish-Hunter brings related defensive investigation tasks into one interface. Its goal is to help an analyst move from **raw artifact → parsed evidence → correlated indicators → explainable findings → report**.

| Area | What it is for |
|---|---|
| **Analyze** | Triage email, URL, file, domain, IP, malware-related artifacts, and IOCs. |
| **Investigate** | Correlate network evidence, related indicators, hosts, timelines, and potential attack paths. |
| **Operate** | Manage cases, campaigns, threat actors, feeds, reports, and analyst activity. |
| **Admin** | Manage accounts, roles, account state, password resets, and audit/activity records. |
| **Guest mode** | Try the service workspaces without first creating an account; guest data is temporary. |

The runtime is primarily Python. The web application uses FastAPI and SQLAlchemy; the workbench and network-artifacts consoles use React with ordinary JavaScript/JSX—not TypeScript.

## Main capabilities

### Email and web indicators

- **Email Analyst:** MIME structure, headers, authentication results, message content, URLs, attachments, and IOC triage.
- **URL Analyst:** URL parsing, redirect and header evidence, forms, and SSRF-aware collection controls.
- **Domain Analyst:** DNS resolution, domain structure, associated IPs, and domain evidence.
- **IP Analyst:** IPv4/IPv6 classification, reverse DNS, and IOC context.
- **IOC Analyst:** Indicator extraction, normalization, and related pivots.
- **Threat Intelligence:** Connector catalog, evidence enrichment, and correlation foundations.

### Files and malware-related artifacts

- **File Analyst:** File identification, hashes, entropy, strings, and suspicious API signals.
- **Malware Analyst:** Static triage and available intelligence context.
- **Ransomware Analyst:** Defensive artifact and sample triage.
- **Phishing Kit Analyst:** Authorized HTML/JavaScript and credential-form inspection.
- **Sandbox integration boundary:** The normal web process does not execute uploaded files. A dynamic sandbox must be a separately configured, isolated service.

### Network artifacts and passive forensics

The Network Artifacts Investigation Center accepts supported PCAP/PCAPNG and network-log evidence, including Zeek, Suricata EVE JSON, NetFlow/IPFIX, firewall, proxy, DNS, and DHCP formats. Its documented analysis features include:

- Original-artifact hashing and metadata.
- IPv4/IPv6 flows, DNS evidence, HTTP metadata, TLS SNI, protocol statistics, and suspicious-port context.
- Bounded TCP reassembly and passive signature-based file-carving support.
- Host and endpoint profiles, unified timelines, graph-based pivots, and cross-artifact correlation.
- Potential beaconing/C2, unusual outbound connections, inbound exposure, and candidate compromised-host findings.
- IOC extraction, evidence references, risk/confidence details, and candidate MITRE ATT&CK context.
- Graph Studio, packet-level drill-down, file dossiers, DNS intelligence, exfiltration pivots, and response-rule exports.

**Analyst note:** PCAP detections are evidence-led heuristics, not proof of compromise or actor attribution. Corroborate findings with endpoint telemetry, authentication logs, EDR, DNS records, and other independent evidence.

### Cases, identity, and analyst operations

- Account-aware workspace and dashboard navigation.
- Analyst registration and database-backed identity.
- Guest scans with a documented 24-hour retention window on the configured local database; guest data can be migrated during registration.
- Tenant-scoped investigation records, files/evidence metadata, reports, cases, IOCs, and activity history.
- Administrator control center for account and role management, activation/deactivation, password resets, and activity review.
- Cases, campaigns, threat actors, threat feeds, IOC graph, and report workspaces.

## Analyst workspaces

The current project documents 18 service routes/workspaces. The principal tools include:

| Workspace | Typical workflow |
|---|---|
| Email Analyst | Inspect message headers, sender authentication, attachments, links, and extracted indicators. |
| URL Analyst | Collect URL structure and response evidence, review redirects/forms, and assess risk. |
| File Analyst | Identify a file, calculate hashes, inspect strings/entropy, and record suspicious signals. |
| Domain Analyst | Review DNS, domain components, associated addresses, and evidence pivots. |
| IP Analyst | Classify IPv4/IPv6, inspect reverse DNS, and correlate IOC context. |
| PCAP Analyst | Analyze authorized packet captures and supported network-log formats passively. |
| Malware / Ransomware Analyst | Perform static defensive triage and connect available intelligence evidence. |
| Phishing Kit Analyst | Examine authorized HTML/JS kits and credential-form indicators without running the content. |
| IOC Analyst | Normalize indicators and pivot across related evidence. |
| Threat Intelligence | Use configured connectors to enrich and correlate evidence. |
| Reports | Export investigation findings in supported formats. |
| Cases / Campaigns / Threat Actors | Organize evidence and track related investigations. |
| IOC Graph / Threat Feeds | Explore indicator relationships and parse configured feeds. |
| Sandbox | Provide an integration boundary for a separately isolated dynamic-analysis provider. |

Feature availability depends on the active configuration, optional dependencies, host limits, and provider credentials. The application does not claim an external service is connected unless its connector is configured.

## Analysis pipeline and reports

The interface represents work as staged analysis: intake and validation, deep/static analysis, correlation, IOC normalization, optional ATT&CK mapping, timeline/graph construction, and reporting. The final server-produced result is authoritative; visual progress is not itself evidence that an analysis stage succeeded.

Documented export formats include:

- PDF and standalone HTML.
- JSON and Markdown.
- Plain text (TXT).
- STIX 2.1.
- IOC CSV and connection-flow CSV.
- A ZIP report bundle containing supported exports.

## Run locally — recommended for full functionality

Running the app locally is the recommended starting point because it avoids Vercel's serverless request-body limit and allows the Python process to use the local filesystem and its in-process job pipeline. Your computer's RAM, disk space, dependencies, and configured upload limits still apply; no host can promise unlimited file size.

### Kali Linux / Debian / Ubuntu / WSL / macOS

From the extracted project root:

```bash
# Kali/Debian/Ubuntu: needed if venv support is not installed
sudo apt update
sudo apt install -y python3-full python3-venv

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python run.py
```

On macOS, use your installed Python 3 and omit the `apt` commands. On Kali/WSL, **do not** run system-wide `pip install`; use the `.venv` as shown to avoid the `externally-managed-environment` error.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python .\run.py
```

If PowerShell blocks activation, you can avoid changing machine-wide policy by running this in the current PowerShell session before activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### Open the app

Once the server starts, open:

- **Main site:** <http://127.0.0.1:8000/>
- **Unified workbench:** <http://127.0.0.1:8000/workbench>
- **Admin control center:** <http://127.0.0.1:8000/admin>
- **Readiness check:** <http://127.0.0.1:8000/health/ready>

Keep the terminal running while you use the site. Stop the server with `Ctrl+C`.

### Configure local environment (optional)

1. Copy `.env.example` to `.env`.
2. Set a private `SECRET_KEY` and adjust `STORAGE_DIR` / `DATABASE_URL` if needed.
3. Keep `.env` private. Do not commit it to GitHub.
4. Local SQLite is useful for development. For a persistent production database, configure PostgreSQL and test migrations/identity behavior before onboarding users.

## Create the first administrator

A clean release does not create demo administrator credentials automatically. Create the first administrator explicitly after dependencies are installed and the intended database is configured.

```bash
python ./bootstrap_admin.py --email "admin@example.com" --password "USE-A-UNIQUE-STRONG-PASSWORD" --organization "Phish-Hunter"
```

This example is a template: replace the email and password. Avoid putting a real password into a command that will be saved in shell history. The normal registration flow creates an Analyst account; administrator accounts are created explicitly. Open `/admin` after starting the app.

## React + JavaScript frontends

The workbench and network-artifacts consoles use **React + JavaScript/JSX**, not TypeScript. Source changes must be built into the static directories served by the Python application. Use Node.js 20 or newer and internet access for the first npm dependency install.

Linux, macOS, Kali/WSL:

```bash
./scripts/build_frontends.sh
```

Windows PowerShell:

```powershell
.\scripts\build_frontends.ps1
```

After changing frontend code, rebuild and commit the generated assets under `phishhunter/web/static/workbench` and `phishhunter/web/static/network-artifacts`. See [JAVASCRIPT_MIGRATION.md](JAVASCRIPT_MIGRATION.md).

## Vercel preview: known limitations

Vercel is useful for a public preview of the UI and short HTTP/API requests. The currently deployed preview has shown issues that prevent it from behaving exactly like a local persistent Python server.

| Observed issue | Why it happens / what to do |
|---|---|
| Login or account state seems to disappear while moving between pages. | Confirm the **same** stable `SECRET_KEY` and `DATABASE_URL` are set on the exact Vercel project/domain being tested. A per-instance secret or `/tmp` SQLite fallback can make sessions and records inconsistent. Visit `/health/ready` to inspect readiness. |
| Large PCAP returns `413 FUNCTION_PAYLOAD_TOO_LARGE`. | Vercel Functions enforce a hard **4.5 MB request-body limit** before the application receives the upload. `MAX_UPLOAD_MB` cannot override this. Use local execution or a persistent Python host for bigger captures. |
| Some investigations/jobs don't behave like local execution. | The app has process-local job state and local filesystem assumptions. Separate serverless invocations do not guarantee shared in-memory state or durable local files. Use a persistent host, database, and durable storage for these workflows. |
| External threat-intelligence or sandbox features return no live data. | Provider connectors are opt-in. Add provider credentials and configure a properly isolated sandbox/worker before expecting live results. |

For a configured Vercel deployment, set at least a stable `SECRET_KEY`, a managed PostgreSQL `DATABASE_URL`, `PUBLIC_BASE_URL` to the deployed HTTPS origin, and `COOKIE_SECURE=true`. These settings improve identity/data consistency, **but they do not remove the 4.5 MB Vercel upload limit** or turn serverless invocations into a persistent worker.

**Recommendation:** use the Vercel site as a preview. To use the broadest current platform feature set, run Phish-Hunter locally with the commands above, or deploy the full FastAPI backend to a persistent Python host. The project includes [FULL_BACKEND_DEPLOYMENT.md](FULL_BACKEND_DEPLOYMENT.md) and [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) with more hosting detail.

## Production deployment options

### Option A — Local machine (best for full-feature evaluation)

Run `python run.py`. This is the simplest way to explore the full current toolset without the Vercel Function body limit. Data remains on your local machine, so back up the database and `STORAGE_DIR`; local execution is not automatically a production-grade multi-user deployment.

### Option B — Persistent Python host (recommended for sharing the complete app)

Use the included Render Blueprint (`render.yaml`) or adapt the same configuration for Railway or a VPS:

1. Push the project root to GitHub.
2. Create a Python web service from the repository / Blueprint.
3. Configure a stable `SECRET_KEY` and managed PostgreSQL `DATABASE_URL`.
4. Attach persistent disk or object storage and set `STORAGE_DIR` to it.
5. Keep the service at a single process/instance until in-memory PCAP jobs are moved to a shared job store or queue.
6. Check `/health/ready`, then test account navigation, data persistence, reports, and representative evidence uploads.

The current app-level defaults allow up to **100 MB per file and 100 MB per investigation batch** on a compatible persistent host. This is a configurable cap, not an unlimited guarantee; the parser buffers file data and requires adequate RAM. For very large captures, implement direct-to-object-storage uploads and a durable external queue/worker.

### Option C — Vercel (preview / small requests)

Import the repository root (`./`) and use the FastAPI preset where available. Keep the included `vercel.json` and install command. Configure the environment variables above. Test `/health/ready`, authentication, navigation, and only small uploads. Do not use Vercel's temporary filesystem as a long-term database or evidence store.

## Configuration and integrations

Optional capabilities require their own configuration. Examples named in `.env.example` include:

- VirusTotal, URLScan, AbuseIPDB, Google Safe Browsing, and other reputation/enrichment connectors.
- OpenAI-based summarization (optional and dependent on a configured key/model).
- Isolated sandbox integration settings.
- PostgreSQL via `DATABASE_URL` and storage via `STORAGE_DIR`.

The presence of a configuration field or connector catalog does not mean a third-party service is enabled or returning live data. The app should report a connector as active only when properly configured.

## Security boundaries

- Use Phish-Hunter only for defensive analysis and systems/artifacts you are authorized to inspect.
- The normal web process does **not** execute uploaded malware. Dynamic analysis belongs in a separately isolated sandbox with controlled network access and appropriate authorization.
- URL collection must maintain SSRF protections; do not expose private-network access through untrusted user input.
- Treat PCAP classifications, suspicious connections, C2 candidates, and attack-graph relationships as leads requiring corroboration—not automatic proof of compromise or attribution.
- Do not put secrets, API keys, production database URLs, or user data in source control, screenshots, issues, or chat.
- Before public production use, rotate any secret previously exposed and review authentication, rate limits, allowed hosts, backups, logging, and data retention.

## Verification and development

Run the project's available verification checks from the repository root:

```bash
python -m compileall -q phishhunter libs/py-common
python -m pytest -q
```

Optional development linting:

```bash
python -m pip install -r requirements/dev.txt
ruff check .
black --check .
```

Package a clean release with:

```bash
python make_zip.py
```

The release script excludes common local caches, virtual environments, compiled Python files, database files, and private `.env` configuration. Review `git status` and `.gitignore` before pushing changes.

## Project structure

```text
Phish-Hunter-Security-Operations-Platform/
├── phishhunter/                  # Canonical FastAPI application and analyst modules
├── phishhunter_common/            # Shared runtime helpers
├── Backend/                       # Architecture facade / module map
├── admin/                         # Admin application and templates
├── frontend/                      # React + JavaScript frontend sources
├── phishhunter/web/templates/      # Server-rendered public/service pages
├── phishhunter/web/static/         # CSS, JavaScript, images, built UI assets
├── requirements/                  # Base, web, production, and development dependencies
├── scripts/                       # Frontend build, preflight, and verification scripts
├── tests/                         # Automated regression and feature tests
├── data/                           # Local data/spec paths (do not commit private evidence)
├── index.py                       # Vercel-compatible FastAPI entry point
├── run.py                         # Local server launcher
├── bootstrap_admin.py              # First administrator setup
├── vercel.json                    # Vercel preview configuration
├── render.yaml                    # Persistent Python host Blueprint
└── FULL_BACKEND_DEPLOYMENT.md     # Hosting guidance for the full backend
```

## License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE).

---

**Phish-Hunter — Hunting the phish.**

Built for explainable, evidence-led defensive investigation. Configure and validate each integration and deployment environment before relying on it for operational decisions.
