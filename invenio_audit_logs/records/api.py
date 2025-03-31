# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2025 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""API classes for audit log event."""

from datetime import datetime

from invenio_records.dumpers import SearchDumper
from invenio_records.systemfields import ModelField
from invenio_records_resources.records.api import Record
from invenio_records_resources.records.systemfields import IndexField

from .models import AuditLogModel
from .dumpers import AuditLogJsonDumperExt


class AuditLogEvent(Record):
    """API class to represent a structured audit-log event."""

    model_cls = AuditLogModel
    """The model class for the log."""

    enable_jsonref = (
        True  # Resolves the record to the JSON field when dumping to the index
    )

    dumper = SearchDumper()
    """Search dumper with configured extensions."""

    index = IndexField("auditlog-audit-log-v1.0.0", search_alias="auditlog")
    """The search engine index to use."""

    log_id = ModelField("log_id", dump_type=str)

    timestamp = ModelField("created", dump_type=datetime)

    action = ModelField("action", dump_type=str)

    json = ModelField("json", dump_type=dict)

    metadata = None
    """Disabled metadata field from the base class."""
