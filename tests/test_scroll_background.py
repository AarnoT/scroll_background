"""Tests for the ScrollBackground class
"""

import pytest
import pygame as pg

from scroll_background import Vector2, ScrollBackground

pg.init()


@pytest.fixture
def background():
    """Fixture that returns a ScrollBackground instance.
    """
    background = pg.Surface((800, 800))
    surf = pg.Surface((200, 200))
    return ScrollBackground(background, surf, (300, 300))


def test_limit_scrolling(background):
    """Test that display_area stays inside scrolling_area.
    """
    background.scroll((500, 0))
    assert tuple(background.display_pos) == (600, 300)
    background.scroll((-800, -800))
    assert tuple(background.display_pos) == (0, 0)


def test_scroll(background):
    """Test that display_area is moved correctly.
    """
    background.scroll((50, 50))
    assert tuple(background.display_pos) == (350, 350)
    background.scroll((-50, -50))
    assert tuple(background.display_pos) == (300, 300)


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


def test_scroll_output(background):
    """Test that the scroll surface looks correct after scrolling.
    """
    # Draw a grid.
    for x in range(0, 800, 50):
        for y in range(0, 800, 50):
            pg.draw.rect(
                background.background, (0, 255, 0), (x, y, 50, 50))
    for x in range(0, 800, 100):
        for y in range(50, 800, 100):
            pg.draw.rect(
                background.background, (0, 0, 255), (x, y, 50, 50))
    for x in range(50, 800, 100):
        for y in range(0, 800, 100):
            pg.draw.rect(
                background.background, (0, 0, 255), (x, y, 50, 50))
    background.display.blit(
            background.background,
            (0, 0),
            pg.Rect(tuple(background.display_pos),
                    background.display.get_size()))

    background.scroll((50, 50))
    display_area = pg.Rect(tuple(background.display_pos),
                           background.display.get_size())
    correct_surf = background.background.subsurface(display_area)
    assert compare_surfaces(correct_surf, background.display)


def test_scroll_output2(background):
    """Test scroll output with a small background surface.
    """
    background.display = pg.Surface((1000, 200))
    background.display_pos = (-100, 0)
    # Draw a grid.
    for x in range(0, 800, 50):
        for y in range(0, 800, 50):
            pg.draw.rect(
                background.background, (0, 255, 0), (x, y, 50, 50))
    for x in range(0, 800, 100):
        for y in range(50, 800, 100):
            pg.draw.rect(
                background.background, (0, 0, 255), (x, y, 50, 50))
    for x in range(50, 800, 100):
        for y in range(0, 800, 100):
            pg.draw.rect(
                background.background, (0, 0, 255), (x, y, 50, 50))
    background.display.blit(
            background.background,
            (0, 0),
            pg.Rect(tuple(background.display_pos),
                    background.display.get_size()))

    display_area = pg.Rect(tuple(background.display_pos),
                           background.display.get_size())
    correct_surf = pg.Surface((1000, 200))
    correct_surf.blit(background.background, (0, 0), display_area)
    background.scroll((0, 600))
    background.scroll((0, -600))
    assert compare_surfaces(correct_surf, background.display)


def test_redraw_areas(background):
    """Redraw areas should be inside scrolling_area.
    """
    redraw_positions, _ = background._calculate_redraw_areas(
        Vector2((50, 50)))
    assert redraw_positions[0] == (150, 0)
    assert redraw_positions[1] == (0, 150)
    redraw_positions, _ = background._calculate_redraw_areas(
        Vector2((-50, -50)))
    assert redraw_positions[0] == (0, 0)
    assert redraw_positions[1] == (0, 0)


def test_redraw_area_size(background):
    """Test that redraw areas are the correct size.
    """
    _, redraw_areas = background._calculate_redraw_areas(
        Vector2((50, 50)))
    assert redraw_areas[0].size == (50, 200)
    assert redraw_areas[1].size == (200, 50)
    _, redraw_areas = background._calculate_redraw_areas(
        Vector2((-50, -50)))
    assert redraw_areas[0].size == (50, 200)
    assert redraw_areas[1].size == (200, 50)


def test_no_drift(background):
    """Test that background doesn't drift when centered.
    """
    center_pos = 123.5649437027, 182.2849278591
    background.center(center_pos)
    pos1 = tuple(background.display_pos)
    for n in range(30):
        background.center(center_pos)
    assert pos1 == tuple(background.display_pos)


def test_draw_sprites(background):
    """Test that sprites are cleared properly.
    """
    background.background.fill((232, 32, 3))
    background.redraw_display()
    sprite = pg.sprite.Sprite()
    sprite.image = pg.Surface((50, 50))
    sprite.rect = pg.Rect(375, 375, 50, 50)
    background.draw_sprites((sprite,))
    background.scroll((30, 30))
    background.draw_sprites(())
    assert len(background.clear_rects) == 0
    correct_surf = background.background.subsurface(
        (tuple(background.display_pos), background.display.get_size()))
    assert compare_surfaces(correct_surf, background.display)
