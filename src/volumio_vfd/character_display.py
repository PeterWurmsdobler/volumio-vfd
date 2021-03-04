class CharacterDisplay(object):
    """Abstract base class to provide character display services."""

    @property
    def width(self) -> int:
        """Return width of character display in number of characters per line."""
        return 0

    @property
    def height(self) -> int:
        """Return height of character display in number of lines."""
        return 0

    def clear(self) -> None:
        """Clear the entire display"""
        pass

    def write(self, text: str, line: int, position: int) -> None:
        """Write text on line and at position, all zero indexed."""
        pass
