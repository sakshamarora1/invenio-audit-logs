# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Audit Log data layer definitions."""

from .api import AuditLogEvent
from .models import AuditLogModel

__all__ = (
    "AuditLogEvent",
    "AuditLogModel",
)
