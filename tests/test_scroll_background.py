"""Tests for the ScrollBackground class
"""

import pytest
import pygame as pg

from scroll_background import ScrollBackground

pg.init()


@pytest.fixture
def scroll_bg():
    """Fixture that returns a ScrollBackground instance.
    """
    background = pg.Surface((800, 800))
    display_area = pg.Rect(300, 300, 200, 200)
    return ScrollBackground(background, display_area, limit_scrolling=True)


def test_limit_scrolling(scroll_bg):
    """
    Test that limit_scrolling keeps display_area inside scrolling_area.
    """
    surf = pg.Surface(scroll_bg.display_area.size)
    scroll_bg.scroll(surf, (500, 0))
    assert scroll_bg.scrolling_area.contains(scroll_bg.display_area)
