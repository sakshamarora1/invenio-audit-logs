# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Invenio-Audit-Logs is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Audit logs resource config."""

from flask_resources import HTTPJSONException, create_error_handler
from invenio_records_resources.resources import (
    RecordResourceConfig,
    SearchRequestArgsSchema,
)
from invenio_records_resources.services.base.config import ConfiguratorMixin
from marshmallow import fields

from ..errors import InvalidLogQueryError


#
# Request args
#
class AuditLogSearchRequestArgsSchema(SearchRequestArgsSchema):
    """Search parameters for audit-logs."""

    resource_id = fields.String()
    resource_type = fields.String()
    user_id = fields.String()
    action = fields.String()


error_handlers = {
    InvalidLogQueryError: create_error_handler(
        lambda e: HTTPJSONException(code=400, description=str(e))
    ),
}


#
# Resource config
#
class AuditLogsResourceConfig(RecordResourceConfig, ConfiguratorMixin):
    """Audit-Logs resource configuration."""

    blueprint_name = "audit_logs"
    url_prefix = "/audit-logs"

    routes = {
        "list": "/",
        "item": "/<id>",
    }

    request_view_args = {
        "id": fields.UUID(),  # TODO: Add direct querying via other search parameters?
    }

    request_search_args = AuditLogSearchRequestArgsSchema

    error_handlers = error_handlers

    response_handlers = {
        "application/vnd.inveniordm.v1+json": RecordResourceConfig.response_handlers[
            "application/json"
        ],
        **RecordResourceConfig.response_handlers,
    }
