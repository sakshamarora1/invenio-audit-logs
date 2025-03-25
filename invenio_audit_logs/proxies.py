from flask import current_app
from werkzeug.local import LocalProxy

current_audit_logs = LocalProxy(lambda: current_app.extensions["invenio-audit-logs"])
"""Proxy to an instance of ``AuditLogs`` service."""
