# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Audit Logs Service Config."""

from invenio_i18n import lazy_gettext as _
from invenio_indexer.api import RecordIndexer
from invenio_records_resources.services.base import ServiceConfig
from invenio_records_resources.services.base.config import ConfiguratorMixin, FromConfig
from invenio_records_resources.services.records.config import (
    SearchOptions as SearchOptionsBase,
)
from sqlalchemy import asc, desc

from . import results
from .permissions import AuditLogPermissionPolicy
from .schema import AuditLogSchema


class AuditLogSearchOptions(SearchOptionsBase):
    """Audit log search options."""

    sort_default = "timestamp"
    sort_direction_default = "desc"
    sort_direction_options = {
        "asc": dict(title=_("Ascending"), fn=asc),
        "desc": dict(title=_("Descending"), fn=desc),
    }
    sort_options = {
        "timestamp": dict(title=_("Timestamp"), fields=["@timestamp"]),
    }

    pagination_options = {"default_results_per_page": 25}


class AuditLogServiceConfig(ServiceConfig, ConfiguratorMixin):
    """App log service configuration."""

    service_id = "app-logs"
    permission_policy_cls = FromConfig(
        "APP_LOGS_PERMISSION_POLICY",
        default=AuditLogPermissionPolicy,
    )
    search = AuditLogSearchOptions
    schema = AuditLogSchema
    components = []
    links_item = None
    result_item_cls = results.AuditLogItem
    result_list_cls = results.AuditLogList
