# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Invenio-Audit-Logs is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Logs resource."""

from flask import g
from flask_resources import Resource, resource_requestctx, response_handler, route
from invenio_records_resources.resources.records.resource import (
    request_extra_args,
    request_search_args,
    request_view_args,
)
from invenio_records_resources.resources.records.utils import search_preference


#
# Resource
#
class AuditLogsResource(Resource):
    """Resource layer for audit-logs."""

    def __init__(self, config, service):
        """Constructor."""
        super(AuditLogsResource, self).__init__(config)
        self.service = service

    def create_blueprint(self, **options):
        """Create the blueprint."""
        # We avoid passing url_prefix to the blueprint because we need to
        # install URLs under both /audit-logs and /api/audit-logs. Instead we
        # add the prefix manually to each route (which is anyway what Flask
        # does in the end)
        options["url_prefix"] = ""
        return super().create_blueprint(**options)

    def create_url_rules(self):
        """Create the URL rules for the log resource."""
        routes = self.config.routes

        def p(route):
            """Prefix a route with the URL prefix."""
            return f"{self.config.url_prefix}{route}"

        return [
            route("GET", p(routes["list"]), self.search),
            route("GET", p(routes["item"]), self.read),
        ]

    @request_extra_args
    @request_search_args
    @request_view_args
    @response_handler(many=True)
    def search(self):
        """Perform a search over the logs."""
        hits = self.service.search(
            identity=g.identity,
            params=resource_requestctx.args,
            search_preference=search_preference(),
        )
        return hits.to_dict(), 200

    @request_extra_args
    @request_view_args
    @response_handler()
    def read(self):
        """Read a specific log entry."""
        item = self.service.read(
            id_=resource_requestctx.view_args["id"],
            identity=g.identity,
        )
        return item.to_dict(), 200
