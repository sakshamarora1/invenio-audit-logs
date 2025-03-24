# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2025 CERN.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Audit Logs Service API."""

from flask import current_app
from invenio_logging.proxies import current_datastream_logging_manager

from invenio_records_resources.services.base import LinksTemplate
from invenio_records_resources.services.base.utils import map_search_params
from invenio_records_resources.services.records import RecordService


class AuditLogService(RecordService):
    """Audit log service layer."""

    def search(self, identity, params, **kwargs):
        """Search for app logs."""
        self.require_permission(identity, "search")
        search_params = map_search_params(self.config.search, params)
        query_param = search_params["q"]
        results = current_datastream_logging_manager.search("audit", query_param)

        return self.result_list(
            self,
            identity,
            results,
            search_params,
            links_tpl=LinksTemplate(self.config.links_search, context={"args": params}),
            links_item_tpl=self.links_item_tpl,
            expandable_fields=self.expandable_fields,
            expand=kwargs.get("expand", False),
        )
