# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2025 CERN.
#
# Invenio-Audit-Logs is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio OpenSearch Datastream Schema."""

from datetime import datetime

from marshmallow import EXCLUDE, Schema, fields, pre_dump, pre_load


class UserSchema(Schema):
    """User schema for logging."""

    name = fields.Str(required=False, description="User name (if available).")
    email = fields.Email(required=False, description="User email (if available).")


class ResourceSchema(Schema):
    """Resource schema to track affected entities."""

    id = fields.Str(required=True, description="Unique identifier of the resource.")


class AuditLogMetadata(Schema):
    """Metadata schema for audit log events (JSON Field)."""

    status = fields.Str(
        required=False,
        description="Status of the event (e.g., success, failure).",
    )
    message = fields.Str(
        required=False,
        description="Human-readable description of the event.",
    )
    user = fields.Nested(
        UserSchema,
        required=False,
        description="Information about the user who triggered the event.",
    )
    resource = fields.Nested(
        ResourceSchema,
        required=True,
        description="Information about the affected resource.",
    )
    metadata = fields.Dict(
        required=False,
        description="Additional structured metadata for logging.",
    )


class AuditLogSchema(Schema):
    """Main schema for audit log events in InvenioRDM."""

    class Meta:
        """Meta class to ignore unknown fields."""

        unknown = EXCLUDE  # Ignore unknown fields

    id = fields.Str(
        description="Unique identifier of the audit log event.",
    )
    created = fields.DateTime(
        required=True,
        description="Timestamp when the event occurred.",
    )
    action = fields.Str(
        required=True,
        description="The action that took place (e.g., record.create, community.update).",
        load_only=True,
    )
    resource_type = fields.Str(
        required=True,
        description="Type of resource (e.g., record, community, user).",
    )
    user_id = fields.Str(
        required=True,
        description="ID of the user who triggered the event.",
    )
    json = fields.Nested(
        AuditLogMetadata,
        required=True,
        description="Structured metadata for the audit log event.",
    )

    @pre_load
    def _before_db_insert(self, json, **kwargs):
        """Manipulate fields before DB insert."""
        data = {
            "created": datetime.now().isoformat(),
            "action": json.pop("action", None),
            "user_id": json["user"].pop("id", None),
            "resource_type": json["resource"].pop("type", None),
            "json": json.copy(),
        }
        return data

    @pre_dump
    def _convert_timestamp(self, data, **kwargs):
        """Convert `created` from ISO string to datetime if needed."""
        created = getattr(data, "created", None)
        if isinstance(created, str):
            data["created"] = datetime.fromisoformat(created)
        return data
