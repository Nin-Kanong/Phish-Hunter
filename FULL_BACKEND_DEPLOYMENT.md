# Full Python backend deployment (recommended for accounts and PCAP uploads)

## Why change the hosting path?

The current FastAPI app was designed to behave as one persistent Python process when started with `python run.py`. Vercel runs it as serverless Functions. The app's JWTs are signed with `SECRET_KEY`, users and records are stored through SQLAlchemy, network artifacts are written under `STORAGE_DIR`, and live PCAP jobs are held in an in-process `JobStore`.

If Vercel has no configured `SECRET_KEY`, its fallback is temporary. If Vercel has no `DATABASE_URL`, the visual-preview fallback uses SQLite in `/tmp`. Those choices can make login/session state and user records appear inconsistent between function instances. Also, Vercel Function request bodies have a hard 4.5 MB limit, which is why a 6.93 MB PCAP upload returns `413 FUNCTION_PAYLOAD_TOO_LARGE`.

For the closest feature parity with local `python run.py`, deploy the complete FastAPI app on a persistent Python web service. Vercel can remain online as a preview, but open the persistent host's URL for the fully featured app unless you build a separately tested frontend/API split.

## Render deployment

The included `render.yaml` configures a Python web service on Render plan `1c-2g` (1 CPU / 2 GB RAM) and attaches a 10 GB persistent disk at `/var/data`. These are paid resources; review the current Render price before approving the Blueprint. The service generates a stable `SECRET_KEY`. It intentionally asks you to supply `DATABASE_URL` instead of silently creating an unreliable SQLite production store.

1. Push the updated project root to GitHub (`index.py`, `phishhunter/`, `requirements/`, `requirements.txt`, `render.yaml`, and `gunicorn.conf.py` must be at the repo root).
2. In Render, choose **New + → Blueprint** and select the GitHub repository. Review the Blueprint before confirming.
3. Set `DATABASE_URL` to a managed PostgreSQL connection string. You can use Render Postgres, Neon, or Supabase. The app normalizes `postgres://` and `postgresql://` URLs to the installed Psycopg 3 driver. Keep credentials private.
4. Ensure `SECRET_KEY` is generated and saved as a stable environment variable. The Blueprint uses Render's `generateValue` option. Do not reuse the secret exposed in earlier screenshots/chat.
5. `MAX_UPLOAD_MB` and `MAX_UPLOAD_BATCH_MB` default to `100` in the Blueprint. This lets the observed 6.93 MB PCAP pass the application limit on a host that supports the request body. This is an app-level limit, not an unlimited-size guarantee. For the 100 MB cap, use a service with adequate RAM (preferably 2 GB or more); on a low-memory/free instance reduce both variables to `25` to avoid out-of-memory crashes. Large captures require adequate service RAM because the current parser retains file bytes during processing.
6. To persist uploaded evidence across restarts/deploys, the provided Blueprint attaches a 10 GB persistent disk at `/var/data` and sets `STORAGE_DIR=/var/data/storage`. Persistent disks may require a paid plan. Without a persistent disk or object storage, uploaded local files are ephemeral.
7. Set `COOKIE_SECURE=true`. The service starts one Uvicorn process on Render's `PORT` by default because the PCAP `JobStore` currently lives in process memory. Do not scale to multiple workers/instances until jobs are moved to a shared queue/store.
8. After deployment, open `https://YOUR-SERVICE.onrender.com/health/ready`. It reports stable-secret, database, and upload-platform readiness without revealing any secret values. Fix any warnings before creating real accounts.
9. Test registration, login, click between Home/Services/Workbench, refresh the browser, sign out/in, and upload a PCAP around 7 MB. Check Render logs if any request fails.

## File limits and very large artifacts

There is no meaningful promise of “all file sizes”: every host has resource/timeout/storage constraints. This app's current upload implementation buffers the artifact for parsing, so the included configurable cap is 100 MB per file and 100 MB per PCAP batch. Raise it only when the host has enough memory and the parser is known to handle the artifact size. For hundreds of MB/GB, implement direct multipart object-storage upload plus a durable external job queue/worker; do not proxy the entire file through a serverless Function.

## If you keep Vercel

- Set a fresh stable `SECRET_KEY` in Project Settings → Environment Variables for Production and Preview.
- Set `DATABASE_URL` to managed PostgreSQL (not the `/tmp` SQLite fallback).
- Visit `/health/ready` to confirm these settings are active in the project/domain you actually use.
- The existing `/api/v1/pcap/upload` multipart endpoint still cannot accept files over Vercel's 4.5 MB Function request limit. `MAX_UPLOAD_MB` does not override it. The current project does not include an end-to-end client-direct object-storage workflow, so use the persistent Python host for larger PCAPs.

## Local validation

Kali/WSL:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run.py
```

Do not run system `pip install` on Kali's externally managed Python. Use the project `.venv`.


## Branding update

The public display name is **Phish-Hunter**, and the homepage headline is **Hunting the phish**. The legacy tenant-name reference in `routes.py` is intentional: it migrates existing accounts from the former default tenant name without deleting user data.
