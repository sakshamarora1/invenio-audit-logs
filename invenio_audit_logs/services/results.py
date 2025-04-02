# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Invenio-Audit-Logs is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Audit Logs Service Results."""

from collections.abc import Iterable, Sized

from invenio_records_resources.services.records.results import (
    RecordItem,
    RecordList,
)


class AuditLogItem(RecordItem):
    """Single item result."""

    def __init__(
        self,
        service,
        identity,
        audit_log,
        errors=None,
        links_tpl=None,
        schema=None,
    ):
        """Constructor."""
        self._data = None
        self._errors = errors
        self._identity = identity
        self._audit_log = audit_log
        self._service = service
        self._links_tpl = links_tpl
        self._schema = schema or service.schema

    @property
    def id(self):
        """Get the result id."""
        return str(self.id)

    def __getitem__(self, key):
        """Key a key from the data."""
        return self.data[key]

    @property
    def links(self):
        """Get links for this result item."""
        return self._links_tpl.expand(self._identity, self._audit_log)

    @property
    def _obj(self):
        """Return the object to dump."""
        return self._audit_log

    @property
    def data(self):
        """Property to get the log."""
        if self._data:
            return self._data

        self._data = self._schema.dump(
            self._obj,
            context={
                "identity": self._identity,
                "record": self._audit_log,
            },
        )

        if self._links_tpl:
            self._data["links"] = self.links

        return self._data

    @property
    def errors(self):
        """Get the errors."""
        return self._errors

    def to_dict(self):
        """Get a dictionary for the log."""
        res = self.data
        if self._errors:
            res["errors"] = self._errors
        return res


class AuditLogList(RecordList):
    """List result."""

    @property
    def items(self):
        """Iterator over the items."""
        if isinstance(self._results, Iterable):
            return self._results
        return self._results

    @property
    def total(self):
        """Get total number of hits."""
        if hasattr(self._results, "hits"):
            return self._results.hits.total["value"]
        elif isinstance(self._results, Sized):
            return len(self._results)
        else:
            return None

    @property
    def hits(self):
        """Iterator over the hits."""
        for hit in self.items:
            # Project the hit
            projection = self._schema.dump(
                hit,
                context=dict(identity=self._identity, record=hit),
            )

            if self._links_item_tpl:
                projection["links"] = self._links_item_tpl.expand(self._identity, hit)

            yield projection

    def to_dict(self):
        """Return result as a dictionary."""
        res = {
            "hits": {
                "hits": list(self.hits),
                "total": self.total,
            }
        }

        if self.aggregations:
            res["aggregations"] = self.aggregations

        if self._params:
            res["sortBy"] = self._params["sort"]
            if self._links_tpl:
                res["links"] = self._links_tpl.expand(self._identity, self.pagination)

        return res
