# Test utility functions

from datetime import datetime

import pytest

from rpyscope import utils as ut


def test_time_units():
    """Test the TimeUnits enum."""
    assert ut.TimeUnits.sec == 1
    assert ut.TimeUnits.min == 60


@pytest.mark.parametrize("date_prefix", [True, False])
def test_filename_increment(tmp_path, date_prefix):
    """Test a given filename without any files being present."""
    fname = "test"
    ext = "jpg"
    if date_prefix:
        prefix = f"{datetime.now().strftime('%Y-%m-%d')}-"
    else:
        prefix = ""

    expected = tmp_path.joinpath(f"{prefix}{fname}-000.{ext}")

    assert (
        ut.filename_increment(tmp_path, fname, ext, date_prefix=date_prefix) == expected
    )


def test_filename_increment_existing(tmp_path):
    """Test a given filename with files being present."""
    fname = "test"
    ext = "jpg"
    tmp_path.joinpath(f"{fname}-000.{ext}").touch()
    tmp_path.joinpath(f"{fname}-001.{ext}").touch()
    expected = tmp_path.joinpath(f"{fname}-002.{ext}")

    assert ut.filename_increment(tmp_path, fname, ext, date_prefix=False) == expected
