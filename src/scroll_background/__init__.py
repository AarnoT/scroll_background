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
    x, y : float
        The X and Y coordinates.

    Attributes
    ----------
    length
    x, y : float
        The X and Y coordinates.

    Examples
    --------
    Adding and substracting vectors.

    >>> vector1 = Vector2(10, 5)
    >>> vector2 = Vector2(-5, 2)
    >>> vector1 + vector2
    <Vector2(5, 7)>
    >>> vector1 - vector2
    <Vector2(15, 3)>

    Converting an instance of `Vector2` to a tuple.

    >>> tuple(Vector2(12, 30))
    (12, 30)

    """

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    @property
    def length(self):
        """The length of the vector.

        Returns
        -------
        length : float

        """
        return math.hypot(self.x, self.y)

    def copy(self):
        """Return a copy of the vector.

        Returns
        -------
        copy : Vector2

        """
        return Vector2(self.x, self.y)

    def __add__(self, other):
        """Return the sum of two vectors.

        Parameters
        ----------
        other : Vector2

        Returns
        -------
        sum  : Vector2

        """
        return Vector2(self.x + other.x, self.y + other.y)

    def __radd__(self, other):
        """Return the sum of two vectors.

        Parameters
        ----------
        other : Vector2

        Returns
        -------
        sum  : Vector2

        """
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Return the difference of two vectors.

        Parameters
        ----------
        other : Vector2

        Returns
        -------
        difference : Vector2

        """
        return Vector2(self.x - other.x, self.y - other.y)

    def __rsub__(self, other):
        """Return the difference of two vectors.

        Parameters
        ----------
        other : Vector2

        Returns
        -------
        difference : Vector2

        """
        return Vector2(other.x - self.x, other.y - self.y)

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
        def wrapper(self, *args, **kwargs):
            arg_list = []
            for arg in args:
                if isinstance(arg, collections.abc.Sequence) and len(arg) == 2:
                    arg_list.append(Vector2(*arg))
                else:
                    arg_list.append(arg)
            if kwargs:
                return method(self, *arg_list, **kwargs)
            else:
                return method(self, *arg_list)
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
    background
    display
    display_pos
    true_pos
    scrolling_area
    zoom

    _original_background : pygame.Surface
        Copy of the original background surface. You need to draw to
        it before creating a `ScrollBackground`, because it's a copy.
    _background : pygame.Surface
        Copy of the background used for zooming.
    _display : pygame.Surface
        The display surface.
    _display_pos : Vector2
        Position of the display relative to the background.
        Only contains integers in float format.
    _true_pos : Vector2
        More precise position.
    _scrolling_area : pygame.Rect
        The area that limits scrolling.
    _zoom : float
        The factor by which the background is zoomed.

    Raises
    ------
    ValueError
        If the background can't contain the display.

    """

    @Vector2.sequence2vector2
    def __init__(self, background, display, display_pos):
        self._original_background = background.copy()
        self._display = display
        self._display_pos = Vector2(*(int(coord) for coord in display_pos))
        self._true_pos = display_pos
        # Setter sets self._scrolling_area and self._background.
        self.background = background.copy()
        self._zoom = 1.0

    @property
    def background(self):
        """Return the background.

        Returns
        -------
        pygame.Surface

        """
        return self._background

    @background.setter
    def background(self, value):
        """Set the background to value.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the background can't contain the display.

        """
        self._scrolling_area = pg.Rect((0, 0), value.get_size())
        if not self._scrolling_area.contains(
                ((0, 0), self._display.get_size())):
            raise ValueError('Background can\'t contain display.')
        self._background = value

    @property
    def display(self):
        """Return the display.

        Returns
        -------
        pygame.Surface

        """
        return self._display

    @display.setter
    def display(self, value):
        """Set the display to value.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the background can't contain the display.

        """
        if not self._scrolling_area.contains(
                ((0, 0), self.value.get_size())):
            raise ValueError('Background can\'t contain display.')
        self._display = value

    @property
    def display_pos(self):
        """Return a copy of _display_pos.

        Returns
        -------
        Vector2

        """
        return self._display_pos.copy()

    @display_pos.setter
    @Vector2.sequence2vector2
    def display_pos(self, value):
        """Set _display_pos and _true_pos to copies of value.

        Parameters
        ----------
        value : Vector2

        Returns
        -------
        None

        """
        self._display_pos = value.copy()
        self._true_pos = value.copy()

    @property
    def true_pos(self):
        """Return a copy of _true_pos.

        Returns
        -------
        Vector2

        """
        return self._true_pos.copy()

    @true_pos.setter
    @Vector2.sequence2vector2
    def true_pos(self, value):
        """Set _display_pos and _true_pos to copies of value.

        Parameters
        ----------
        value : Vector2

        Returns
        -------
        None

        """
        self._display_pos = value.copy()
        self._true_pos = value.copy()

    @property
    def scrolling_area(self):
        """Return a copy of the scrolling area.

        Returns
        -------
        scrolling_area : pygame.Rect

        """
        return self._scrolling_area.copy()

        self._zoom = 1.0

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
        # Using setter.
        self.background = pg.transform.scale(self._original_background, tuple(
            int(size*scale) for size in self._original_background.get_size()))
        self._display_pos = Vector2(
           *(int(coord*scale) for coord in self._true_pos))
        self._true_pos = Vector2(*(coord*scale for coord in self._true_pos))
        self._display.blit(self._background, (0, 0),
                           (tuple(self._display_pos), self._display.get_size()))

    @Vector2.sequence2vector2
    def center(self, point):
        """Center the display on a point.

        Parameters
        ----------
        point : Vector2

        """
        new_display_pos = Vector2(point.x - self.display.get_width()/2,
                                  point.y - self.display.get_height()/2)
        if (new_display_pos - self.true_pos).length >= 1:
            self.scroll(new_display_pos - self.display_pos)

    @Vector2.sequence2vector2
    def scroll(self, position_change):
        """Scroll the display by position_change

        If the display isn't inside `self._scrolling_area`
        after being moved it will be moved back inside.

        Parameters
        ----------
        position_change : Vector2

        Returns
        -------
        None

        """
        prev_pos = self._display_pos
        self._true_pos += position_change
        self._display_pos = Vector2(*(int(coord) for coord in self._true_pos))
        display_rect = pg.Rect(
            tuple(self._display_pos), self.display.get_size())
        if not self.scrolling_area.contains(display_rect):
            # Move display inside scrolling_area
            display_rect.clamp_ip(self.scrolling_area)
            self._display_pos = Vector2(*display_rect.topleft)
            self._true_pos = Vector2(*display_rect.topleft)
        position_change = self.display_pos - prev_pos
        self.display.scroll(int(-position_change.x), int(-position_change.y))
        self.redraw_rects(*self._calculate_redraw_areas(position_change))

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
            scroll_x = (self._display_pos.x +
                        self.display.get_width() - position_change.x)
            pos1 = scroll_x - self._display_pos.x, 0
            area1 = pg.Rect(
                scroll_x,
                self._display_pos.y,
                position_change.x,
                self.display.get_height())
        elif position_change.x < 0:
            pos1 = 0, 0
            area1 = pg.Rect(
                self._display_pos.x,
                self._display_pos.y,
                -position_change.x,
                self.display.get_height())
        if position_change.y > 0:
            scroll_y = (self._display_pos.y +
                        self.display.get_height() - position_change.y)
            pos2 = 0, scroll_y - self.display_pos.y
            area2 = pg.Rect(
                self._display_pos.x,
                scroll_y,
                self.display.get_width(),
                position_change.y)
        elif position_change.y < 0:
            pos2 = 0, 0
            area2 = pg.Rect(
                self._display_pos.x,
                self._display_pos.y,
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
