# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Invenio-Audit-Logs is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

import pytest

from invenio_audit_logs.proxies import current_audit_logs_service


@pytest.fixture
def service(appctx):
    """Fixture for the current service."""
    return current_audit_logs_service


def test_create(authenticated_identity, create_draft_log, service):
    """Test the create method."""
    result = service.create(authenticated_identity, create_draft_log)

    assert result is not None
    assert result.action == "draft.create"
    assert result.resource_type == "record"
