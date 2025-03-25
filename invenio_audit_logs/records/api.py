# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2025 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""API classes for audit log event."""

from datetime import datetime

from flask import current_app
from invenio_records.dumpers import SearchDumper, SearchDumperExt
from invenio_records.dumpers.indexedat import IndexedAtDumperExt
from invenio_records.systemfields import ModelField
from invenio_records_resources.records.api import Record
from invenio_records_resources.records.systemfields import IndexField
from invenio_search import current_search_client
from invenio_search.utils import prefix_index

from .models import AuditLogModel


class AuditLogEvent(Record):
    """Class to represent a structured audit-log event."""

    model_cls = AuditLogModel
    """The model class for the request."""

    dumper = SearchDumper(
        extensions=[],
        model_fields={
            "log_id": ("uuid", int),
        },
    )
    """Search dumper with configured extensions."""

    index = IndexField("logs-audit", search_alias="logs-audit")
    """The search engine index to use."""

    log_id = ModelField("log_id", dump_type=str)

    timestamp = ModelField("@timestamp", dump_type=datetime)

    event = ModelField("event", dump_type=dict)

    message = ModelField("message", dump_type=str)

    user = ModelField("user", dump_type=dict)

    resource = ModelField("resource", dump_type=dict)

    extra = ModelField("extra", dump_type=dict)

    metadata = None
    """Disabled metadata field from the base class."""

    def __getitem__(self, name):
        """Get a dict key item."""
        try:
            return getattr(self.model, name)
        except AttributeError:
            raise KeyError(name)

    def __repr__(self):
        """Create string representation."""
        return f"<{self.__class__.__name__}: {self.model.data}>"

    def __unicode__(self):
        """Create string representation."""
        return self.__repr__()

    # @classmethod
    # def from_model(cls, sa_model):
    #     """Create an aggregate from an SQL Alchemy model."""
    #     return cls({}, model=cls.model_cls(model_obj=sa_model))

    def _validate(self, *args, **kwargs):
        """Skip the validation."""
        pass

    # @classmethod
    # def get_record(cls, id_):
    #     """Get the user via the specified ID."""
    #     # TODO: Implement the proper model lookup
    #     return cls.from_model(id_)

    @classmethod
    def log(
        cls,
        event={},
        resource={},
        user={},
        extra={},
        timestamp=None,
        message=None,
    ):
        """
        Create a LogEvent instance.

        :param log_type: Type of log event.
        :param event: Dict with `action` (required) and optional `description`.
        :param resource: Dict with `type`, `id`, and optional `metadata`.
        :param user: Dict with `id`, `email`, and optional `roles` (default: empty).
        :param extra: Additional metadata dictionary (default: empty).
        :param timestamp: Optional timestamp (defaults to now).
        :param message: Optional human-readable message.
        """

        log_entry = {
            "log_id": cls.model_cls.generate_id(),
            "event": event,
            "resource": resource,
            "user": user,
            "extra": extra,
            "@timestamp": timestamp or datetime.now().isoformat(),
            "message": message,
        }
        current_search_client.index(
            index=prefix_index(cls.index.search_alias), body=log_entry
        )

    def to_dict(self):
        """Convert the log event to a dictionary matching the schema."""
        return {
            "log_id": self.log_id,
            "@timestamp": self.timestamp,
            "event": self.event,
            "message": self.message,
            "user": self.user,
            "resource": self.resource,
            "extra": self.extra,
        }
