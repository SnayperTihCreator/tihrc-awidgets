import pytest


def test_import():
    from tihrc.awidgets import ColorButton, ValueSlider
    assert ColorButton is not None
    assert ValueSlider is not None
