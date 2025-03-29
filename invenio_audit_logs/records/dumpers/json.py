# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2025 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Relations dumper.

Dumper used to dump/load relations to/from a search engine body.
"""

from invenio_records.dumpers import SearchDumperExt


class AuditLogJsonDumperExt(SearchDumperExt):
    """Dumper for a relations field."""

    def dump(self, record, data):
        """Dump relations."""
        json = getattr(record, "json", None)
        # dump the json fields as the index fields
        data = json
