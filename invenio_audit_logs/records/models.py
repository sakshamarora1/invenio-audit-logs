# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Base model classes for Audit Logs in Invenio."""

import uuid
from abc import ABC, abstractmethod


class AuditLogModel(ABC):
    """Model class that does not correspond to a database table."""

    # Properties mapped to a ModelField on the Audit Log API class.
    _properties = [
        "timestamp",
        "event",
        "message",
        "user",
        "resource",
        "extra",  # TODO: Update all this to match the actual fields in DB later
    ]
    """Properties of this object that can be accessed."""

    _set_properties = []
    """Properties of this object that can be set."""

    _data = None

    def __init__(self, model_obj=None, **kwargs):
        """Constructor."""
        super().__setattr__("_data", {})
        if model_obj is not None:
            # E.g. when data is loaded from database
            self.from_model(model_obj)
            super().__setattr__("_model_obj", model_obj)
        else:
            # E.g. when data is loaded from the search index
            self.from_kwargs(kwargs)
            super().__setattr__("_model_obj", None)

    @property
    @abstractmethod
    def model_obj(self):
        """The actual model object behind this mock model."""
        return self._model_obj

    def from_kwargs(self, kwargs):
        """Extract information from kwargs."""
        for p in self._properties:
            self._data[p] = kwargs.get(p, None)

    def from_model(self, model_obj):
        """Extract information from an audit log object."""
        for p in self._properties:
            self._data[p] = getattr(model_obj, p, None)

    def __getattr__(self, name):
        """Get an attribute from the model."""
        if name in self._properties:
            return self._data[name]
        else:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        """Set an attribute from the model."""
        if name not in self._set_properties:
            raise AttributeError(name)
        super().__setattr__(name, value)
        setattr(self.model_obj, name, value)

    # Methods required to make it a record.
    @property
    def is_deleted(self):
        """Method needed for the record API."""
        return False

    @property
    def json(self):
        """Method needed for the record API."""
        return {p: getattr(self, p, None) for p in self._properties}

    @property
    def data(self):
        """Method needed for the record API."""
        return {p: getattr(self, p, None) for p in self._properties}

    @classmethod
    def generate_id(cls):
        """Generate an ID for the record."""
        return uuid.uuid4()
