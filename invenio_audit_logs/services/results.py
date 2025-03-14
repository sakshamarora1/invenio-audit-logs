# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Audit Logs Service Results."""

from invenio_records_resources.services.records.results import RecordItem, RecordList


class AuditLogItem(RecordItem):
    """Single item result."""

    @property
    def id(self):
        """Get the result id."""
        return str(self.id)


class AuditLogList(RecordList):
    """List result."""

    @property
    def hits(self):
        """Iterator over the hits."""
        for hit in self.items:
            # Project the hit
            projection = self._schema.dump(
                hit,
                context=dict(identity=self._identity),
            )
            if self._links_item_tpl:
                projection["links"] = self._links_item_tpl.expand(self._identity, hit)
            if self._nested_links_item:
                for link in self._nested_links_item:
                    link.expand(self._identity, hit, projection)

            yield projection
