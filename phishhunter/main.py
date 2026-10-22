import os
import secrets

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles

from phishhunter.api.v1 import router as api_router
from phishhunter.config import settings
from phishhunter.db.database import database_url, engine
from phishhunter.lifespan import lifespan
from phishhunter.logging import configure_logging, trace_id_ctx
from phishhunter.security.csrf import issue_csrf
from phishhunter.security.rate_limit import enforce_rate_limit
from phishhunter.web.routes import router as web_router
from phishhunter.web.services import router as services_router
from phishhunter.version import APP_VERSION
from admin_app import app as admin_app

configure_logging()

app = FastAPI(title=settings.app_name, version=APP_VERSION, lifespan=lifespan, docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory="phishhunter/web/static"), name="static")
# Unified single-port deployment: the administrator control plane is mounted
# under /admin and shares the same authentication cookies and database.
app.mount("/admin", admin_app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.public_base_url.rstrip("/")],
    allow_origin_regex=r"https?://(127\.0\.0\.1|localhost)(:\d+)?",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-CSRF-Token"],
)


@app.middleware("http")
async def request_middleware(request: Request, call_next):
    trace_id = secrets.token_hex(16)
    trace_id_ctx.set(trace_id)
    enforce_rate_limit(request)
    issue_csrf(request)
    response = await call_next(request)
    response.headers["X-Trace-ID"] = trace_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=(), payment=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' https://cdn.tailwindcss.com https://unpkg.com 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' data:; "
        "connect-src 'self'; "
        "object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'self'"
    )
    if settings.cookie_secure or request.url.scheme == "https":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    if getattr(request.state, "set_csrf_cookie", False):
        response.set_cookie(
            settings.csrf_cookie_name,
            request.state.csrf_token,
            httponly=False,
            secure=settings.cookie_secure or request.url.scheme == "https",
            samesite="strict",
            max_age=60 * 60 * 24,
        )
    return response


@app.get("/health")
def health():
    return {"status": "ok", "service": "phishhunter", "version": APP_VERSION}


@app.get("/health/ready")
def readiness():
    """Deployment diagnostics safe for public monitoring; never returns secret values."""
    serverless = bool(os.getenv("VERCEL") or os.getenv("VERCEL_ENV"))
    render_hosted = bool(os.getenv("RENDER") or os.getenv("RENDER_EXTERNAL_URL"))
    hosted = serverless or render_hosted
    stable_secret = bool(os.getenv("SECRET_KEY"))
    persistent_database = not database_url.startswith("sqlite")
    configured_storage = os.getenv("STORAGE_DIR", "").strip()
    durable_storage_configured = bool(configured_storage) and not configured_storage.startswith("/tmp") and configured_storage not in {"./data/storage", "data/storage"}
    database_connected = False
    try:
        with engine.connect() as connection:
            connection.exec_driver_sql("SELECT 1")
        database_connected = True
    except Exception:
        database_connected = False

    warnings = []
    if hosted and not stable_secret:
        warnings.append("SECRET_KEY is not configured as a stable environment variable; login tokens may fail across instances/restarts.")
    if hosted and not persistent_database:
        warnings.append("The hosted runtime is using SQLite. Configure managed PostgreSQL so accounts and investigation records persist across instances/restarts.")
    if serverless:
        warnings.append("Vercel Function requests have a hard 4.5 MB body limit. Use the persistent Python deployment for larger artifact uploads.")
    if render_hosted and not durable_storage_configured:
        warnings.append("Configure a persistent disk or object storage and set STORAGE_DIR to its durable mount path before storing evidence.")
    if not database_connected:
        warnings.append("The configured database is not reachable from this runtime.")

    ready = database_connected and (not hosted or (stable_secret and persistent_database))
    if render_hosted and not durable_storage_configured:
        ready = False
    return {
        "status": "ready" if ready else "degraded",
        "ready": ready,
        "runtime": "vercel-serverless" if serverless else ("render-python-web-service" if render_hosted else "local-or-other-python-host"),
        "checks": {
            "database_connected": database_connected,
            "persistent_database_configured": persistent_database,
            "stable_secret_configured": stable_secret if hosted else True,
            "durable_storage_configured": durable_storage_configured if hosted else True,
            "max_upload_mb_per_file": settings.max_upload_mb,
            "max_upload_mb_per_batch": settings.max_upload_batch_mb,
            "vercel_function_upload_limit_applies": serverless,
        },
        "warnings": warnings,
    }


@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return "# HELP phishhunter_up application health\n# TYPE phishhunter_up gauge\nphishhunter_up 1\n"


app.include_router(web_router)
app.include_router(services_router)
app.include_router(api_router)
