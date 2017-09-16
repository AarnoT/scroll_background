"""Package for scrolling a surface in Pygame.
"""

import math
import functools
import collections.abc

import pygame as pg

pg.init()


class Vector2:
    """A utility class that contains an X, and a Y coordinate.

    Two vectors can be added or substracted together. `Vector2` also
    implements the __iter__ method, which makes `Vector2` instances
    easy to convert to another iterable.

    Parameters
    ----------
    pos : iterable of float
        The X and Y coordinates.

    Attributes
    ----------
    length
    x, y : float
        The X and Y coordinates.

    Examples
    --------
    Adding and substracting vectors.

    >>> vector1 = Vector2((10, 5))
    >>> vector2 = Vector2((-5, 2))
    >>> vector1 + vector2
    <Vector2(5.0, 7.0)>
    >>> vector1 - vector2
    <Vector2(15.0, 3.0)>

    Converting an instance of `Vector2` to a `tuple`.

    >>> tuple(Vector2((12, 30)))
    (12.0, 30.0)

    """

    def __init__(self, pos):
        self.x, self.y = (float(coord) for coord in pos)

    @property
    def length(self):
        """The length of the vector.

        Returns
        -------
        length : float

        """
        return math.hypot(self.x, self.y)

    def scale(self, scale):
        """Multiply vector by scale.

        Parameters
        ----------
        scale : float

        Returns
        -------
        self : Vector2

        """
        self.x *= scale
        self.y *= scale
        return self

    def copy(self):
        """Return a copy of the vector.

        Returns
        -------
        copy : Vector2

        """
        return Vector2((self.x, self.y))

    def asint(self):
        """Return a tuple with the x and y values as integers.

        Returns
        -------
        tuple of int

        """
        return (int(self.x), int(self.y))

    def __eq__(self, other):
        """Test if two vectors are equal.

        Parameters
        ----------
        other : Vector2

        Returns
        -------
        bool

        """
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        """Return the sum of two vectors.

        Parameters
        ----------
        other : Vector2

        Returns
        -------
        sum  : Vector2

        """
        return Vector2((self.x + other.x, self.y + other.y))

    def __radd__(self, other):
        """Return the sum of two vectors.

        Parameters
        ----------
        other : Vector2

        Returns
        -------
        sum  : Vector2

        """
        return Vector2((self.x + other.x, self.y + other.y))

    def __sub__(self, other):
        """Return the difference of two vectors.

        Parameters
        ----------
        other : Vector2

        Returns
        -------
        difference : Vector2

        """
        return Vector2((self.x - other.x, self.y - other.y))

    def __rsub__(self, other):
        """Return the difference of two vectors.

        Parameters
        ----------
        other : Vector2

        Returns
        -------
        difference : Vector2

        """
        return Vector2((other.x - self.x, other.y - self.y))

    def __iter__(self):
        """Iterate a vector.

        Yields
        ------
        x : float
        y : float

        """
        yield self.x
        yield self.y

    def __repr__(self):
        """Return the string representation of a vector.

        Returns
        -------
        repr : str

        """
        return '<Vector2({}, {})>'.format(self.x, self.y)

    @classmethod
    def sequence2vector2(cls, method):
        """Decorator to convert 2-length sequence arguments to vectors.

        Parameters
        ----------
        func : method
            The method that will be wrapped.

        Returns
        -------
        wrapper : function
            The wrapper function.

        """
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            arg_list = []
            for arg in args:
                if isinstance(arg, collections.abc.Sequence) and len(arg) == 2:
                    arg_list.append(Vector2(arg))
                else:
                    arg_list.append(arg)
            if kwargs:
                return method(*arg_list, **kwargs)
            else:
                return method(*arg_list)
        return wrapper


class ScrollBackground:
    """A class for scrolling a Pygame surface.

    Parameters
    ----------
    background : pygame.Surface
    display : pygame.Surface
    display_pos : Vector2

    Attributes
    ----------
    display_pos
    scrolling_area
    zoom

    _original_background : pygame.Surface
        Copy of the original background surface.
    background : pygame.Surface
        Copy of the original background used for zooming.
    display : pygame.Surface
        The display surface.
    true_pos : Vector2
        Accurate display position.
    clear_rects : list of pygame.Rect
        Rects used to clear sprites from the background.
    _zoom : float
        The factor by which the background is zoomed.

    """

    @Vector2.sequence2vector2
    def __init__(self, background, display, display_pos):
        self._original_background = background.copy()
        self.background = background.copy()
        self.display = display
        self.true_pos = display_pos
        self.clear_rects = []
        self._zoom = 1.0

    def blit(self, source, dest, area=None, special_flags=0):
        """Scale arguments and blit them to the display surface.

        Returns
        -------
        pygame.Rect

        """
        # Scale arguments based on zoom factor.
        source_size = Vector2(source.get_size()).scale(self.zoom).asint()
        source = pg.transform.scale(source, tuple(source_size))
        dest = Vector2(dest).scale(self.zoom).asint()
        if area is not None:
            area.topleft = Vector2(area.topleft).scale(self.zoom).asint()
            area.size = Vector2(area.size).scale(self.zoom).asint()
            area.topleft = (Vector2(area.topleft) - self.display_pos).asint()

        draw_pos = (Vector2(dest) - self.display_pos).asint()
        draw_rect = self.display.blit(source, draw_pos, area, special_flags)
        return draw_rect

    @property
    def display_pos(self):
        """Return true_pos mapped to integer values.

        Returns
        -------
        Vector2

        """
        return Vector2(round(num, 0) for num in self.true_pos)

    @display_pos.setter
    @Vector2.sequence2vector2
    def display_pos(self, value):
        """Set true_pos to value.

        Parameters
        ----------
        value : Vector2

        Returns
        -------
        None

        """
        self.true_pos = value

    @property
    def scrolling_area(self):
        """The area inside which the display can be scrolled.

        The top left corner is always at (0, 0).

        Returns
        -------
        scrolling_area : pygame.Rect

        """
        return pg.Rect((0, 0), self.background.get_size())

    @property
    def zoom(self):
        """Return the zoom factor.

        Returns
        -------
        zoom : float

        """
        return self._zoom

    @zoom.setter
    def zoom(self, scale):
        """Create a new zoomed background and scale variables.

        Parameters
        ----------
        scale : float

        Returns
        -------
        None

        """
        original_bg_size = self._original_background.get_size()
        new_width, new_height = (int(size*scale) for size in original_bg_size)
        self.background = pg.transform.scale(self._original_background,
                                             (new_width, new_height))
        self.true_pos.scale(scale)
        self.move_or_center_display()
        self.redraw_display()
        self._zoom = scale

    @Vector2.sequence2vector2
    def centered_pos(self, point):
        """Return the position where the display is centered on a point.

        Parameters
        ----------
        point : Vector2

        Returns
        -------
        centered_pos : Vector2

        """
        return point - Vector2((self.display.get_width()/2,
                                self.display.get_height()/2))

    @Vector2.sequence2vector2
    def center(self, point):
        """Scroll the display so that it is centered on a point.

        Parameters
        ----------
        point : Vector2

        Returns
        -------
        None

        """
        centered_pos = self.centered_pos(point)
        if (centered_pos - self.true_pos).length >= 1:
            self.scroll(centered_pos - self.true_pos)

    @Vector2.sequence2vector2
    def scroll(self, position_change):
        """Scroll the display by position_change.

        Parameters
        ----------
        position_change : Vector2

        Returns
        -------
        None

        Examples
        --------
        Scrolling the display 100 pixels to the right and down.

        >>> background = ScrollBackground(pg.Surface((600, 600)),
        ...                               pg.Surface((200, 200)), (200, 200))
        >>> background.scroll((100, 100))
        >>> tuple(background.display_pos)
        (300.0, 300.0)

        """
        prev_pos = self.display_pos
        self.true_pos += position_change
        self.move_or_center_display()
        position_change = self.display_pos - prev_pos

        self.display.scroll(int(-position_change.x), int(-position_change.y))
        self.redraw_rects(*self._calculate_redraw_areas(position_change))

    def move_or_center_display(self):
        """Move the display onto the background or center it.

        Returns
        -------
        None

        Examples
        --------
        Centering the display.

        >>> background = ScrollBackground(pg.Surface((600, 600)),
        ...                               pg.Surface((800, 800)), (200, 200))
        >>> background.move_or_center_display()
        >>> tuple(background.display_pos)
        (-100.0, -100.0)

        """
        display_rect = pg.Rect(tuple(self.true_pos), self.display.get_size())
        display_rect.clamp_ip(self.scrolling_area)
        if int(self.true_pos.x) != display_rect.x:
            self.true_pos.x = display_rect.x
        if int(self.true_pos.y) != display_rect.y:
            self.true_pos.y = display_rect.y

    @Vector2.sequence2vector2
    def _calculate_redraw_areas(self, position_change):
        """Calculate which areas need to be redrawn.

        Up to two redraw positions and areas will be returned.

        Parameters
        ----------
        position_change : Vector2

        Returns
        -------
        redraw_positions : tuple of Vector2
        redraw_areas : tuple of pygame.Rect

        """
        area1 = None
        area2 = None
        if position_change.x > 0:
            scroll_x = (self.display_pos.x +
                        self.display.get_width() - position_change.x)
            pos1 = scroll_x - self.display_pos.x, 0
            area1 = pg.Rect(
                scroll_x,
                self.display_pos.y,
                position_change.x,
                self.display.get_height())
        elif position_change.x < 0:
            pos1 = 0, 0
            area1 = pg.Rect(
                self.display_pos.x,
                self.display_pos.y,
                -position_change.x,
                self.display.get_height())
        if position_change.y > 0:
            scroll_y = (self.display_pos.y +
                        self.display.get_height() - position_change.y)
            pos2 = 0, scroll_y - self.display_pos.y
            area2 = pg.Rect(
                self.display_pos.x,
                scroll_y,
                self.display.get_width(),
                position_change.y)
        elif position_change.y < 0:
            pos2 = 0, 0
            area2 = pg.Rect(
                self.display_pos.x,
                self.display_pos.y,
                self.display.get_width(),
                -position_change.y)
        if area1 and area2:
            return (pos1, pos2), (area1, area2)
        elif area1:
            return (pos1,), (area1,)
        elif area2:
            return (pos2,), (area2,)
        else:
            return (), ()

    def redraw_rects(self, redraw_positions, redraw_areas):
        """Redraw the redraw areas from the background to the display.

        Parameters
        ----------
        redraw_positions : iterable of Vector2
        redraw_areas : iterable of pygame.Rect

        Returns
        -------
        None

        """
        for pos, rect in zip(redraw_positions, redraw_areas):
            self.display.blit(self.background, tuple(pos), rect)

    def redraw_display(self):
        """Draw the background to the display.

        Returns
        -------
        None

        """
        self.display.fill((0, 0, 0))
        self.display.blit(self.background, (0, 0),
                          (tuple(self.display_pos), self.display.get_size()))

    def draw_sprites(self, sprites):
        """Clear previously drawn sprites and draw new ones.

        Sprites can be any objects with pygame.Rect as the .rect
        attribute and a pygame.Surface as the .image attribute. The
        position of the sprites should be relative to the background.

        Parameters
        ----------
        sprites : iterable of sprites

        Returns
        -------
        draw_rects : list of pygame.Rect

        """
        draw_rects = []
        for rect in self.clear_rects:
            clear_pos = Vector2(rect.topleft) - self.display_pos
            draw_rects.append(
                self.display.blit(self.background, tuple(clear_pos), rect))
        self.clear_rects.clear()

        for sprite in sprites:
            draw_pos = Vector2(sprite.rect.topleft) - self.display_pos
            draw_rect = self.display.blit(sprite.image, tuple(draw_pos))
            self.clear_rects.append(sprite.rect)
            draw_rects.append(draw_rect)
        return draw_rects


class MultiSurfaceBackground(ScrollBackground):
    """Subclass of ScrollBackground that can use more than one surface.

    You should use this if your background is large or you want a
    background that repeats infinitely.

    Parameters
    ----------
    background_surfaces : nested list of pygame.Surface
        All of the surfaces should be the same size so that they can
        be combined into a square shape.
    display : pygame.Surface
    display_pos : Vector2
    repeating : bool
        Boolean that determines whether the background should
        repeat infinitely.

    Attributes
    ----------
    _original_background_surfaces : nested list of pygame.Surface
    background_surfaces : nested list of pygame.Surface
    repeating : bool

    """

    def __init__(self, background_surfaces, display, display_pos,
                 repeating=False):
        super().__init__(pg.Surface((1, 1)), display, display_pos)
        self._original_background_surfaces = [
            surf.copy() for surf in background_surfaces]
        self.background_surfaces = [
            surf.copy() for surf in background_surfaces]
        self.combine_surfaces()
        self.repeating = repeating

    @property
    def scrolling_area(self):
        """The area inside which the display can be scrolled.

        The top left corner is always at (0, 0).

        Returns
        -------
        scrolling_area : pygame.Rect

        """
        background_width = len(self.background_surfaces[0]) * (
            self.background_surfaces[0][0].get_width())
        background_height = len(self.background_surfaces) * (
            self.background_surfaces[0][0].get_height())
        return pg.Rect((0, 0), (background_width, background_height))

    def check_visible_surfaces(self):
        """Return a rect that represents each visible surface.

        Returns
        -------
        pygame.Rect

        """
        surf_width, surf_height = self.background_surfaces[0][0].get_size()

        left = math.floor(self.display_pos.x/surf_width)
        top = math.floor(self.display_pos.y/surf_height)
        right = math.floor(
            (self.display_pos.x + self.display.get_width())/surf_width)
        bottom = math.floor(
            (self.display_pos.y + self.display.get_height())/surf_height)
        return pg.Rect(left, top, right - left, bottom - top)

    def combine_surfaces(self, surface_rect=None):
        """Combine visible surfaces and set them as the background.

        Arguments
        ---------
        surface_rect : pg.Rect
            Rectangle that represents the surfaces.

        Returns
        -------
        None

        """
        surface_rect = surface_rect or self.check_visible_surfaces()
        surf_width, surf_height = self.background_surfaces[0][0].get_size()
        x_surfs = len(self.background_surfaces[0])
        y_surfs = len(self.background_surfaces)

        self.background = pg.Surface((
            (surface_rect.width + 1) * surf_width,
            (surface_rect.height + 1) * surf_height))

        for j in range(surface_rect.top, surface_rect.bottom + 1):
            for i in range(surface_rect.left, surface_rect.right + 1):
                pos = Vector2((i - surface_rect.left, j - surface_rect.top))
                surf_x = abs(i % (x_surfs * (int(i / (abs(i) or 1)) or 1)))
                surf_y = abs(j % (y_surfs * (int(j / (abs(j) or 1)) or 1)))
                self.background.blit(
                    self.background_surfaces[surf_y][surf_x],
                    (pos.x * surf_width, pos.y * surf_height))

    @Vector2.sequence2vector2
    def offset_position(self, pos):
        """Make a position relative to the currently visible surfaces.

        Arguments
        ---------
        pos : Vector2

        Returns
        -------
        offset_pos : Vector2

        """
        surf_width, surf_height = self.background_surfaces[0][0].get_size()
        left = math.floor(self.display_pos.x / surf_width) * surf_width
        top = math.floor(self.display_pos.y / surf_height) * surf_height
        return Vector2((pos.x - left, pos.y - top))

    @ScrollBackground.zoom.setter
    def zoom(self, scale):
        """Create a new zoomed background and scale variables.

        Parameters
        ----------
        scale : float

        Returns
        -------
        None

        """
        original_size = self._original_background_surfaces[0][0].get_size()
        new_width, new_height = (int(size*scale) for size in original_size)
        for j in range(len(self.background_surfaces)):
            for i in range(len(self.background_surfaces[0])):
                self.background_surfaces[j][i] = pg.transform.scale(
                    self._original_background_surfaces[j][i],
                    (new_width, new_height))
        self.true_pos.scale(scale)
        self.move_or_center_display()
        new_center = self.display_pos.copy() + Vector2(self.display.get_size())
        new_center.scale(0.5)
        self.center(new_center)
        self.redraw_display()
        self._zoom = scale

    @Vector2.sequence2vector2
    def scroll(self, position_change):
        """Scroll the display by position_change.

        Parameters
        ----------
        position_change : Vector2

        Returns
        -------
        None

        """
        prev_surf_rect = self.check_visible_surfaces()
        prev_pos = self.display_pos
        self.true_pos += position_change
        if not self.repeating:
            self.move_or_center_display()
        position_change = self.display_pos - prev_pos
        curr_surf_rect = self.check_visible_surfaces()
        if prev_surf_rect != curr_surf_rect:
            self.combine_surfaces(surface_rect=curr_surf_rect)

        self.display.scroll(int(-position_change.x), int(-position_change.y))
        self.redraw_rects(*self._calculate_redraw_areas(position_change))

    def redraw_rects(self, redraw_positions, redraw_areas):
        """Redraw the redraw areas from the background to the display.

        Parameters
        ----------
        redraw_positions : iterable of Vector2
        redraw_areas : iterable of pygame.Rect

        Returns
        -------
        None

        """
        for pos, rect in zip(redraw_positions, redraw_areas):
            rect.topleft = tuple(self.offset_position(rect.topleft))
            self.display.blit(self.background, tuple(pos), rect)

    def redraw_display(self):
        """Draw the background to the display.

        Returns
        -------
        None

        """
        surf_width, surf_height = self.background_surfaces[0][0].get_size()
        pos = self.offset_position(self.display_pos)
        self.display.fill((0, 0, 0))
        self.display.blit(self.background, (0, 0),
                          (tuple(pos), self.display.get_size()))

    def draw_sprites(self, sprites):
        """Clear previously drawn sprites and draw new ones.

        Sprites can be any objects with pygame.Rect as the .rect
        attribute and a pygame.Surface as the .image attribute. The
        position of the sprites should be relative to the background.

        Parameters
        ----------
        sprites : iterable of sprites

        Returns
        -------
        draw_rects : list of pygame.Rect

        """
        draw_rects = []
        for rect in self.clear_rects:
            clear_pos = Vector2(rect.topleft) - self.display_pos
            rect.topleft = tuple(self.offset_position(rect.topleft))
            draw_rects.append(
                self.display.blit(self.background, tuple(clear_pos), rect))
        self.clear_rects.clear()

        for sprite in sprites:
            draw_pos = Vector2(sprite.rect.topleft) - self.display_pos
            draw_rect = self.display.blit(sprite.image, tuple(draw_pos))
            self.clear_rects.append(sprite.rect)
            draw_rects.append(draw_rect)
        return draw_rects


if __name__ == "__main__":
    import doctest
    doctest.testmod()
