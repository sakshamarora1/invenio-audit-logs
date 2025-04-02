# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Invenio-Audit-Logs is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Resources module."""

from .config import AuditLogsResourceConfig
from .resource import AuditLogsResource

__all__ = (
    "AuditLogsResource",
    "AuditLogsResourceConfig",
)
