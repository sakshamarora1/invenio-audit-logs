# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Invenio-Jobs is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Proxies."""

from flask import current_app
from werkzeug.local import LocalProxy

current_audit_logs = LocalProxy(lambda: current_app.extensions["invenio-audit-logs"])
"""Proxy to an instance of ``AuditLogs`` service."""
