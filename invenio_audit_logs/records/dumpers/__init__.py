# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2024 CERN.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Search dumper transofrming data for indexing."""


from .json import AuditLogJsonDumperExt

__all__ = ("AuditLogJsonDumperExt",)
