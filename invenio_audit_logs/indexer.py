# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Invenio-Audit-Logs is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Record modification prior to indexing."""

from __future__ import absolute_import, print_function


def indexer_receiver(sender, json=None, record=None, index=None, **dummy_kwargs):
    """Connect to before_record_index signal to transform record for indexing."""
    if index and index.startswith("auditlog-"):
        # Remove _created and _updated fields added by invenio-indexer _prepare_record API
        json.pop("_created", None)
        json.pop("_updated", None)
        # Add log_id field to the index which is only available after db commit
        json["log_id"] = record.model.log_id
        # Add @timestamp field for datastream compatibility
        json["@timestamp"] = record.model.created
