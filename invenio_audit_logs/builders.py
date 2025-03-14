# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2025 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Datastream Logging Builder module."""

from invenio_logging.engine.builders import LogBuilder

from .backends import AuditLogSearchBackend
from .services.schema import AuditLogSchema


class AuditLogBuilder(LogBuilder):
    """Builder for structured audit logs."""

    type = "audit"

    backend_cls = AuditLogSearchBackend

    schema = AuditLogSchema()

    @classmethod
    def build(cls, log_event):
        """Build an audit log event context."""
        return cls.validate(log_event)

    @classmethod
    def send(cls, log_event):
        """Send log event using the backend."""
        cls.backend_cls().send(log_event)

    @classmethod
    def search(cls, query):
        """Search logs."""
        results = cls.backend_cls().search(query)
        return cls.schema.dump(results, many=True)

    @classmethod
    def list(cls):
        """List audit logs."""
        results = cls.backend_cls().list()
        return cls.schema.dump(results, many=True)
