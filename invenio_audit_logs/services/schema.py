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


class MetadataSchema(Schema):
    """Metadata schema for logging."""

    ip_address = fields.Str(
        required=False,
        description="IP address of the client.",
    )
    session = fields.Str(
        required=False,
        description="Session identifier.",
    )
    request_id = fields.Str(
        required=False,
        description="Unique identifier for the request.",
    )


class AuditLogJsonSchema(Schema):
    """Metadata schema for audit log events (JSON Field)."""

    resource_id = fields.Str(
        required=True, description="Unique identifier of the resource."
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
    metadata = fields.Nested(
        MetadataSchema,
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
        attribute="log_id",
    )
    created = fields.DateTime(
        required=True,
        description="Timestamp when the event occurred.",
        attribute="@timestamp",
    )
    action = fields.Str(
        required=True,
        description="The action that took place (e.g., record.create, community.update).",
    )
    resource_type = fields.Str(
        required=True,
        description="Type of resource (e.g., record, community, user).",
    )
    user_id = fields.Int(
        required=True,
        description="ID of the user who triggered the event.",
    )
    json = fields.Nested(
        AuditLogJsonSchema,
        required=True,
        description="Structured metadata for the audit log event.",
    )

    @pre_load
    def _before_db_insert(self, json, **kwargs):
        """Manipulate fields before DB insert."""
        if "metadata" in self.context:
            metadata = self.context.pop("metadata")
            user = metadata.pop("user_account", None)
            json["user_id"] = user.id
            json["user"] = {
                "name": user.username,
                "email": user.email,
            }
            json["metadata"] = metadata
        data = {
            "created": datetime.now().isoformat(),
            "action": json.pop("action", None),
            "user_id": json.pop("user_id", None),
            "resource_type": json.pop("resource_type", None),
            "json": json.copy(),
        }
        return data

    @pre_dump
    def _after_search_query(self, obj, **kwargs):
        """Convert `timestamp` from ISO string to datetime if needed and set json field."""
        timestamp = getattr(obj, "@timestamp", None)
        if isinstance(timestamp, str):
            obj["@timestamp"] = datetime.fromisoformat(timestamp)
        obj["json"] = {
            "status": getattr(obj, "status", None),
            "message": getattr(obj, "message", None),
            "user": getattr(obj, "user", {}),
            "resource_id": getattr(obj, "resource_id", None),
            "metadata": getattr(obj, "metadata", {}),
        }
        return obj
