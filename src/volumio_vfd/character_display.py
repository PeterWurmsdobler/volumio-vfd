import abc
import datetime

from volumio_vfd.player_status import PlayerState, PlayerStatus


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

    current_status: PlayerStatus = PlayerStatus()

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

    def _update_item(self, old: str, new: str, line: int, position: int = 0) -> None:
        if old != new:
            limit = self.width - self.margin - 3
            if len(new) > limit:
                self.write(new[:limit] + "...", line, position)
            else:
                self.write(new + "...", line, position)

    def _update_seconds(self, seconds: int, line: int) -> None:
        timestr = str(datetime.timedelta(seconds=seconds))
        self.write(timestr, line, self.width - len(timestr) - 1)

    def _update_volume(self, volume: int, line: int) -> None:
        if self.current_status.volume != volume:
            volume_str = f"{volume}%"
            self.write(volume_str, line, self.width - len(volume_str) - 1)

    def update(self, timestamp: datetime.datetime, new_status: PlayerStatus) -> None:
        """Update the display with latest player status."""

        # Clear screen if there is a change of state
        if new_status.state != self.current_status.state:
            self.clear()

        # If stopped we simply display the time
        if new_status.state == PlayerState.Stopped:
            timestr = timestamp.strftime("%H:%M:%S")
            self.write(timestr, 1, (self.width - len(timestr)) // 2)
        else:
            self._update_item(new_status.performer, self.current_status.performer, 0)
            self._update_item(new_status.composer, self.current_status.composer, 1)
            self._update_item(new_status.oeuvre, self.current_status.oeuvre, 2)
            self._update_item(new_status.part, self.current_status.part, 3)
            self._update_volume(new_status.volume, 0)
            self._update_seconds(new_status.duration, 1)
            self._update_seconds(new_status.elapsed, 2)
            self._update_seconds(new_status.remaining, 3)

        self.current_status = new_status
