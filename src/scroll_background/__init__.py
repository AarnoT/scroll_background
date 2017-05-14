"""Package for scrolling a surface in Pygame.
"""


class Vector2:
    """A utility class that contains an X, and a Y coordinate.

    Two vectors can be added or substracted together.
    `Vector2` also implements the __iter__ method, which makes
    `Vector2` instances easy to convert to another iterable.

    Parameters
    ----------
    x, y : int
        The X and Y coordinates.

    Attributes
    ----------
    x, y : int
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
        self.x = x
        self.y = y

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

    def __rsub__(self, other):
        """Return the difference of two vectors.

        Parameters
        ----------
        other : Vector2

        Returns
        -------
        difference : Vector2

        """

    def __iter__(self):
        """Iterate a vector.

        Yields
        ------
        x : int
        y : int

        """

    def __repr__(self):
        """Return the string representation of a vector.

        Returns
        -------
        repr : str

        """

    @classmethod
    def sequence2vector2(cls, func, *args, **kwargs):
        """Decorator to convert 2-length sequence arguments to vectors.

        Parameters
        ----------
        func : function or method
            The function that will be wrapped.

        Returns
        -------
        wrapped_func : function
            The wrapped function.

        """


class ScrollBackground:
    """A class for scrolling a Pygame surface.

    Parameters
    ----------
    background : pygame.Surface
    display : pygame.Surface
    display_pos : Vector2

    Attributes
    ----------
    background : pygame.Surface
        The original background surface.
    scaled_background : pygame.Surface
        Scaled version of the background.
    display : pygame.Surface
        The display surface.
    display_pos : Vector2
        Position of the display relative to the background.
    _scrolling_area : pygame.Rect
        The area that limits scrolling.

    Raises
    ------
    ValueError
        If the background can't contain the display.

    """

    @Vector2.sequence2vector2
    def __init__(self, background, display, display_pos):
        pass

    @property
    def scrolling_area(self):
        """Return a copy of the scrolling area.

        Returns
        -------
        scrolling_area : pygame.Rect

        """
        return self._scrolling_area.copy()

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

    @staticmethod
    def redraw_rects(cls, redraw_positions, redraw_areas):
        """Redraw the redraw areas from the background to the display.

        Parameters
        ----------
        redraw_positions : iterable of Vector2
        redraw_areas : iterable of pygame.Rect

        Returns
        -------
        None

        """
