# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Invenio-Audit-Logs is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Module providing audit logging features for Invenio.."""

from invenio_logging.datastream import InvenioLoggingDatastreams

from . import config
from .resources import AuditLogsResource, AuditLogsResourceConfig


class InvenioAuditLogs(object):
    """Invenio-Audit-Logs extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initializ§ation."""
        self.init_config(app)
        self.init_resources(app)

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("AUDIT_LOGS_"):
                app.config.setdefault(k, getattr(config, k))

    def init_resources(self, app):
        """Init resources."""
        self.resource = AuditLogsResource(
            config=AuditLogsResourceConfig.build(app),
            manager=self.manager,
        )
