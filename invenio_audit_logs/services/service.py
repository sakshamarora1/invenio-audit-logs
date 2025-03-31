# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2025 CERN.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Audit Logs Service API."""

from datetime import datetime
from invenio_records_resources.services.records import (
    RecordService,
    ServiceSchemaWrapper,
)
from invenio_records_resources.services.uow import (
    unit_of_work,
)
from .uow import AuditLogOp


class AuditLogService(RecordService):
    """Audit log service layer."""

    def _wrap_schema(self, schema):
        """Wrap schema."""
        return ServiceSchemaWrapper(self, schema)

    @unit_of_work()
    def create(self, identity, data, raise_errors=True, uow=None, expand=False):
        """Create a record.

        :param identity: Identity of user creating the record.
        :param dict data: Input data according to the data schema.
        :param bool raise_errors: raise schema ValidationError or not.
        """
        self.require_permission(identity, "create")

        data["@timestamp"] = datetime.now().isoformat()

        # Validate data and create record with pid
        schema_data, errors = self.schema.load(
            data,
            context={"identity": identity},
            raise_errors=raise_errors,
        )

        log = self.record_cls.create(
            {},
            **schema_data,
        )

        json_dump = self.schema.dump(
            data,
            context={"identity": identity},
        )
        log.update(json_dump)

        # Persist record (DB and index)
        uow.register(AuditLogOp(log, self.indexer))

        return self.result_item(
            self,
            identity,
            log,
            links_tpl=self.links_item_tpl,
            errors=errors,
        )
