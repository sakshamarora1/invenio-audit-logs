# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2025 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Unit of work operations for audit logs."""

from invenio_records_resources.services.uow import Operation
from invenio_db.uow import Operation


class AuditLogOp(Operation):
    """Audit logging operation."""

    def __init__(self, record, indexer, index_refresh=False):
        """Initialize the record commit operation."""
        self._record = record
        self._indexer = indexer
        self._index_refresh = index_refresh

    def on_register(self, uow):
        """Commit record (will flush to the database)."""
        self._record.commit()

    def on_commit(self, uow):
        """Run the operation."""
        arguments = {"refresh": True} if self._index_refresh else {}
        index = self._indexer.record_to_index(self._record)
        body = self._indexer._prepare_record(self._record, index, arguments)
        index = self._indexer._prepare_index(index)

        # We don't want to pass the identity to the indexer because datastreams creation doesn't allow it as it is append only
        return self._indexer.client.index(index=index, body=body, **arguments)
