# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Base model classes for Audit Logs in Invenio."""

from datetime import datetime, timezone

from invenio_db import db
from invenio_records.models import RecordMetadataBase
from sqlalchemy.dialects import mysql
from sqlalchemy.types import String


class AuditLogModel(db.Model, RecordMetadataBase):
    """Model class for Audit Log."""

    __tablename__ = "audit_logs_metadata"

    encoder = None

    id = None
    updated = None

    log_id = db.Column(db.Integer, primary_key=True)

    created = db.Column(
        db.DateTime().with_variant(mysql.DATETIME(fsp=6), "mysql"),
        default=datetime.now(timezone.utc),
        nullable=False,
    )

    action = db.Column(String(255), nullable=False)
