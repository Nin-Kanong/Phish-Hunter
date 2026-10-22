# Vercel deployment — preview mode and known production limits

The repository root is the FastAPI entry point (`index.py`). Vercel can host the pages and short API requests, but the current app architecture also uses local filesystem storage and an in-process PCAP job store. For a complete production workflow, deploy the Python application on a persistent Python host; see [FULL_BACKEND_DEPLOYMENT.md](FULL_BACKEND_DEPLOYMENT.md).

## Vercel setup

1. Push the repository root to GitHub.
2. Import `NinKanong/Phish-Hunter` in Vercel.
3. Set Root Directory to `./` and select FastAPI (or Other).
4. Use the checked-in install command: `python -m pip install -r requirements.txt`.
5. Configure a stable `SECRET_KEY` and a persistent PostgreSQL `DATABASE_URL` for the exact Vercel project and Production environment. Variables do not automatically carry between separate Vercel projects; confirm the project that owns the domain you are actually opening (the screenshots/logs showed both `hunter0.vercel.app` and `phish-hunter-duik.vercel.app`). Do not rely on `/tmp` SQLite for accounts or saved investigations.
6. Visit `/health/ready` and inspect its checks before accepting real users or evidence.

## Hard upload limit

Vercel Function request bodies are limited to 4.5 MB. This limit is enforced by Vercel before the FastAPI route receives the upload and cannot be raised with `MAX_UPLOAD_MB`, `vercel.json`, or an Install/Build setting. This is why a 6.93 MB PCAP receives `413 FUNCTION_PAYLOAD_TOO_LARGE`. Use the persistent Python deployment for uploads that exceed the Vercel limit, or implement direct-to-object-storage uploads with a server-authorized upload-token flow and an external durable job queue.

## Session and data persistence

- `SECRET_KEY` must be the same stable random value for every invocation and every deployment instance. A process-generated fallback can make tokens fail validation on another instance.
- `DATABASE_URL` must point to a managed PostgreSQL database. The `/tmp` SQLite fallback is only for visual preview; different serverless instances may have different temporary databases.
- `STORAGE_DIR` on Vercel is temporary. Use durable object storage or process evidence on the persistent Python host with a persistent disk.

The `/health/ready` endpoint reports readiness checks without exposing secret values. Rotate any secret previously pasted into chats, screenshots, or public repository content.


## Authentication/session readiness

The hosted pages display a configuration warning and pause registration/sign-in if a stable `SECRET_KEY` or persistent PostgreSQL `DATABASE_URL` is missing. Configure both values in the environment used by the actual deployment and redeploy. Visit `/health/ready`; do not use real user accounts while readiness is degraded. Vercel's 4.5 MB request-body cap is platform-enforced, so a large PCAP must use a persistent Python host or a separately implemented direct-to-object-storage upload flow.
