"""Tests for the ScrollBackground class
"""

import pytest
import pygame as pg

from scroll_background import ScrollBackground

pg.init()


@pytest.fixture
def scroll_bg_limited():
    """Fixture that returns a ScrollBackground instance
    with limited_scrolling as True.
    """
    background = pg.Surface((800, 800))
    surf = pg.Surface((200, 200))
    scrolling_area = (0, 0, 800, 800)
    return ScrollBackground(background, surf, (300, 300),
                            scrolling_area=scrolling_area,
                            limited_scrolling=True)


@pytest.fixture
def scroll_bg():
    """Fixture that returns a ScrollBackground instance
    with limited_scrolling as True.
    """
    background = pg.Surface((800, 800))
    surf = pg.Surface((200, 200))
    scrolling_area = pg.Rect(0, 0, 800, 800)
    return ScrollBackground(background, surf, (300, 300),
                            scrolling_area=scrolling_area,
                            limited_scrolling=False)


def test_too_small_scrolling_area():
    """A ValueError should be raised if scrolling_area us too small.
    """
    background = pg.Surface((400, 400))
    surf = pg.Surface((800, 800))
    with pytest.raises(ValueError):
        ScrollBackground(background, surf, (0, 0),
                         scrolling_area=(0, 0, 400, 400),
                         limited_scrolling=True)


def test_limit_scrolling(scroll_bg_limited):
    """
    Test that limit_scrolling keeps display_area inside scrolling_area.
    """
    scroll_bg_limited.scroll((500, 0))
    assert scroll_bg_limited.display_pos == (600, 300)
    scroll_bg_limited.scroll((-800, -800))
    assert scroll_bg_limited.display_pos == (0, 0)


def test_not_limited_scrolling(scroll_bg):
    """Test that scrolling isn't limited
    """
    scroll_bg.scroll((800, 800))
    assert scroll_bg.display_pos == (1000, 1000)
    scroll_bg.scroll((-1200, -1200))
    assert scroll_bg.display_pos == (-200, -200)


def test_scroll(scroll_bg_limited):
    """Test that display_area is moved correctly.
    """
    scroll_bg_limited.scroll((50, 50))
    assert scroll_bg_limited.scrolling_pos == (350, 350)
    scroll_bg_limited.scroll((-50, -50))
    assert scroll_bg_limited.scrolling_pos == (300, 300)


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


def test_scroll_output(scroll_bg_limited):
    """Test that the scroll surface looks correct after scrolling.
    """
    correct_surf = scroll_bg_limited.background.subsurface(
        scroll_bg_limited.scrolling_rect)
    scroll_bg_limited.scroll((50, 50))
    assert compare_surfaces(correct_surf, scroll_bg_limited.display)
