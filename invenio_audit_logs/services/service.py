# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2025 CERN.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Audit Logs Service API."""

from invenio_records_resources.services.records import RecordService


class AuditLogService(RecordService):
    """Audit log service layer."""

    def search(self, identity, params=None, search_preference=None, **kwargs):
        """Search for app logs."""
        self.require_permission(identity, "search")

        return super().search(
            identity,
            params=params,
            search_preference=search_preference,
            **kwargs,
        )
