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
        None

        """
        self.x *= scale
        self.y *= scale

    def copy(self):
        """Return a copy of the vector.

        Returns
        -------
        copy : Vector2

        """
        return Vector2((self.x, self.y))

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

    def blit(self, *args, **kwargs):
        """Blit to _original_background and update background.

        This makes it easier to change the background.

        Returns
        -------
        pygame.Rect

        """
        blit_rect = self._original_background.blit(*args, **kwargs)
        # Update background.
        self.zoom = self._zoom
        return blit_rect

    @property
    def display_pos(self):
        """Return true_pos mapped to integer values.

        Returns
        -------
        Vector2

        """
        return Vector2(map(int, self.true_pos))

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
        self.true_pos = Vector2(display_rect.topleft)

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


if __name__ == "__main__":
    import doctest
    doctest.testmod()
