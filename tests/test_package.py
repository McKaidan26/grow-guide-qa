"""Smoke test: proves the package installs and the test toolchain runs.

Real tests arrive with real code; pytest exits with an error when it collects
no tests at all, so this keeps CI green on the empty skeleton.
"""

import grow_guide_qa


def test_package_exposes_version():
    assert isinstance(grow_guide_qa.__version__, str)
    assert grow_guide_qa.__version__.count(".") == 2
