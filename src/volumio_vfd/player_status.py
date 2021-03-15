from dataclasses import dataclass
from enum import Enum


class PlayerState(Enum):
    Stopped = 1
    Playing = 2
    Paused = 3


@dataclass()
class PlayerStatus:
    state: PlayerState = PlayerState.Stopped
    performer: str = ""  # The artist carrying out the performer
    composer: str = ""  # the artist having composed the oeuvre
    oeuvre: str = ""  # the oeuvre, concert or album
    part: str = ""  # the part, movement or song
    duration: float = 0.0  # duration in seconds
    elapsed: float = 0.0  # elapsed time in seconds
    volume: int = 0  # volume as percentage
