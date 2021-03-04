from noritake.gu600_comms import GU600CommsSPI
from noritake.gu600_config import GU600Models
from noritake.gu600_driver import GU600Driver
from noritake.gu600_enums import ExtendedFontFace, FontProportion, FontSpace

from volumio_vfd.character_display import CharacterDisplay


class CharacterDisplayNoritake(CharacterDisplay):
    """Noritake character display class to provide character display services."""

    def __init__(self) -> None:
        cfg = GU600Models["GU240x64D-K612A8"]
        spi = GU600CommsSPI(0, 0)
        self.vfd = GU600Driver(spi, cfg)
        self.vfd.clear_all()
        self.vfd.select_extended_font(
            ExtendedFontFace.FONTFACE_7x15A,
            FontProportion.FONT_FIXEDSPACE,
            FontSpace.FONTSPACE_1PIXEL,
        )
        self.character_width: int = 8
        self.character_height: int = 16
        self._width: int = self.vfd.config.width / self.character_width
        self._height: int = self.vfd.config.height / self.character_height

    @property
    def width(self) -> int:
        """Return width of character display in number of characters per line."""
        return self._width

    @property
    def height(self) -> int:
        """Return height of character display in number of lines."""
        return self._height

    def clear(self) -> None:
        """Clear the entire display"""
        self.vfd.clear_all()

    def write(self, text: str, line: int, position: int) -> None:
        """Write text on line and at position, all zero indexed."""
        self.vfd.write_text(
            line * self.character_width, position * self.character_width, text
        )
