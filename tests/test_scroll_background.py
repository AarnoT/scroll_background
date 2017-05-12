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


def compare_surfaces(surface1, surface2):
    """Return True if surfaces are identical, otherwise return false.
    """
    surface1_copy = surface1.copy()
    surface1_copy.blit(surface2, (0, 0), special_flags=pg.BLEND_SUB)
    surface2.blit(surface1, (0, 0), special_flags=pg.BLEND_SUB)
    mask1 = pg.mask.from_threshold(surface1_copy, (0, 0, 0, 0), (1, 1, 1, 255))
    mask2 = pg.mask.from_threshold(surface2, (0, 0, 0, 0), (1, 1, 1, 255))
    mask1.invert()
    mask2.invert()
    return mask1.count() == mask2.count() == 0


def test_scroll_output(scroll_bg, scroll_surf):
    """Test that the scroll surface looks correct after scrolling.
    """
    correct_surf = scroll_bg.background.subsurface(scroll_bg.scrolling_rect)
    scroll_bg.scroll(scroll_surf, (50, 50))
    assert compare_surfaces(correct_surf, scroll_surf)
