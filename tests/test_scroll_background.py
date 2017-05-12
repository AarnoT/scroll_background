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


@pytest.fixture
def scroll_surf(scroll_bg):
    """Fixture that returns a pygame Surface.
    """
    return pg.Surface(scroll_bg.display_area.size)


def test_limit_scrolling(scroll_bg, scroll_surf):
    """
    Test that limit_scrolling keeps display_area inside scrolling_area.
    """
    scroll_bg.scroll(scroll_surf, (500, 0))
    assert scroll_bg.scrolling_area.contains(scroll_bg.display_area)

def test_scroll(scroll_bg, scroll_surf):
    """Test that display_area is moved correctly.
    """
    scroll_bg.scroll(scroll_surf, (50, 50))
    assert scroll_bg.topleft == (350, 350)
