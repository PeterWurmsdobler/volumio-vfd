import abc
import logging
from datetime import datetime, timedelta
from typing import Optional

from volumio_vfd.player_status import PlayerState, PlayerStatus

log = logging.getLogger(__name__)


class CharacterDisplay(metaclass=abc.ABCMeta):
    """Abstract base class to provide character display services.

    The general layout is 4 lines with appropriate font:

                                                   8 characters
    +----------------------------------------------------------+
    | Performer - Performer - Performer - Perf... |  Volume    |
    | Composer - Composer - Composer - Compose... |  duration  |
    | Oeuvre - Oeuvre - Oeuvre - Oeuvre - Oeuvre  |  elapsed   |
    | Part - Part - Part - Part - Part - Part ... |  remaining |
    +----------------------------------------------------------+

    """

    margin: int = 8

    last_status: PlayerStatus = PlayerStatus()
    last_update: datetime = datetime.now()

    @property
    @abc.abstractmethod
    def width(self) -> int:
        """Return width of character display in number of characters per line."""

    @property
    @abc.abstractmethod
    def height(self) -> int:
        """Return height of character display in number of lines."""

    @abc.abstractmethod
    def clear(self) -> None:
        """Clear the entire display"""

    @abc.abstractmethod
    def write(self, text: str, line: int, position: int) -> None:
        """Write text on line and at position, all zero indexed."""

    def _update_item(self, new: str, line: int, position: int = 0) -> None:
        limit = self.width - self.margin - 3
        if len(new) > limit:
            self.write(new[:limit] + "...", line, position)
        else:
            self.write(new, line, position)

    def _update_seconds(self, seconds: float, line: int) -> None:
        timestr = str(timedelta(seconds=int(seconds)))
        self.write(timestr, line, self.width - len(timestr) - 1)

    def _update_volume(self, volume: int, line: int) -> None:
        if self.last_status.volume != volume:
            volume_str = f"{volume}%"
            self.write(volume_str, line, self.width - len(volume_str) - 1)

    def update(self, timestamp: datetime, new_status: Optional[PlayerStatus]) -> None:
        """Update the display with latest player status."""

        if new_status is None:
            # If stopped we simply display the time
            if self.last_status.state == PlayerState.Stopped:
                timestr = timestamp.strftime("%H:%M:%S")
                self.write(timestr, 1, (self.width - len(timestr)) // 2)
            else:
                delta = timestamp - self.last_update
                elapsed: float = self.last_status.elapsed + delta.total_seconds()
                self._update_seconds(elapsed, 2)
                self._update_seconds(self.last_status.duration - elapsed, 3)

        else:
            # Clear screen if there is a change of state
            if new_status.state != self.last_status.state:
                self.last_status = PlayerStatus()
                self.clear()

            # If stopped we simply display the time
            if new_status.state != PlayerState.Stopped:
                if self.last_status.performer != new_status.performer:
                    self._update_item(new_status.performer, 0)
                if self.last_status.composer != new_status.composer:
                    self._update_item(new_status.composer, 1)
                if self.last_status.oeuvre != new_status.oeuvre:
                    self._update_item(new_status.oeuvre, 2)
                if self.last_status.part != new_status.part:
                    self._update_item(new_status.part, 3)

                self._update_volume(new_status.volume, 0)
                self._update_seconds(new_status.duration, 1)
                self._update_seconds(new_status.elapsed, 2)
                self._update_seconds(new_status.duration - new_status.elapsed, 3)

            self.last_status = new_status
            self.last_update = timestamp
