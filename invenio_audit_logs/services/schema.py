# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2025 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio OpenSearch Datastream Schema."""

from datetime import datetime

from marshmallow import EXCLUDE, Schema, fields, pre_dump, pre_load


class UserSchema(Schema):
    """User schema for logging."""

    id = fields.Str(required=True, description="User ID responsible for the event.")
    email = fields.Email(required=False, description="User email (if available).")
    roles = fields.List(
        fields.Str(), required=False, description="Roles assigned to the user."
    )


class EventSchema(Schema):
    """Event schema for logging."""

    action = fields.Str(
        required=True,
        description="The action that took place (e.g., created, deleted).",
    )
    status = fields.Str(
        required=False,
        description="Status of the event (e.g., success, failure).",
    )
    description = fields.Str(
        required=False, description="Detailed description of the event."
    )


class ResourceSchema(Schema):
    """Resource schema to track affected entities."""

    type = fields.Str(
        required=True,
        description="Type of resource (e.g., record, community, user, file).",
    )
    id = fields.Str(required=True, description="Unique identifier of the resource.")
    metadata = fields.Dict(
        required=False, description="Optional metadata related to the resource."
    )

class AuditLogSchema(Schema):
    """Main schema for audit log events in InvenioRDM."""

    class Meta:
        """Meta class to ignore unknown fields."""

        unknown = EXCLUDE  # Ignore unknown fields

    log_id = fields.Str(
        description="Unique identifier of the audit log event.",
    )
    created = fields.DateTime(
        required=True,
        description="Timestamp when the event occurred.",
        attribute="created",
    )
    action = fields.Str(
        required=True,
        description="The action that took place (e.g., created, deleted).",
        load_only=True,
    )
    event = fields.Nested(EventSchema, required=True, dump_only=True)
    message = fields.Str(
        required=True, description="Human-readable description of the event.",
        dump_only=True,
    )
    user = fields.Nested(
        UserSchema,
        required=True,
        description="Information about the user who triggered the event.",
        dump_only=True,
    )
    resource = fields.Nested(
        ResourceSchema,
        required=True,
        description="Information about the affected resource.",
        dump_only=True,
    )
    extra = fields.Dict(
        required=False, description="Additional structured metadata for logging.",
        dump_only=True,
    )

    @pre_load
    def _propagate_action(self, data, **kwargs):
        """Propagate the `action` field from the `event` field."""
        data["action"] = data["event"]["action"]
        return data

    @pre_dump
    def _convert_timestamp(self, obj, **kwargs):
        """Convert `timestamp` from ISO string to datetime if needed."""
        if isinstance(obj["created"], str):
            obj["created"] = datetime.fromisoformat(obj["created"])
        return obj
