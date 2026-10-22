"""Gunicorn configuration for the FastAPI/ASGI application.

Use one worker by default because live PCAP jobs currently use an in-process
JobStore. Increase WEB_CONCURRENCY only after moving jobs to a shared queue/store.
Render supplies PORT at runtime; local scripts may override PORT as needed.
"""
import os

bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
worker_class = "uvicorn.workers.UvicornWorker"
workers = max(1, int(os.getenv("WEB_CONCURRENCY", "1")))
timeout = max(30, int(os.getenv("WEB_TIMEOUT_SECONDS", "300")))
keepalive = 5
accesslog = "-"
errorlog = "-"
forwarded_allow_ips = "*"
