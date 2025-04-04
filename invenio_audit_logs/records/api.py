# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2025 CERN.
#
# Invenio-Audit-Logs is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""API classes for audit log event."""

from datetime import datetime
from uuid import UUID

from invenio_records.dumpers import SearchDumper
from invenio_records.systemfields import ModelField
from invenio_records_resources.records.api import Record
from invenio_records_resources.records.systemfields import IndexField

from .dumpers import AuditLogJsonDumperExt
from .models import AuditLogModel


class AuditLogEvent(Record):
    """API class to represent a structured audit-log event."""

    model_cls = AuditLogModel
    """The model class for the log."""

    dumper = SearchDumper(
        model_fields={
            "id": ("log_id", UUID),
            "created": ("@timestamp", datetime),
        },
        extensions=[
            AuditLogJsonDumperExt(),
        ],
    )
    """Search dumper with configured extensions."""

    index = IndexField("auditlog-audit-log-v1.0.0", search_alias="auditlog")
    """The search engine index to use."""

    id = ModelField("id", dump_type=UUID)

    created = ModelField("created", dump_type=datetime)

    action = ModelField("action", dump_type=str)

    resource_type = ModelField("resource_type", dump_type=str)

    user_id = ModelField("user_id", dump_type=str)
