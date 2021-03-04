from volumio_vfd.character_display_noritake import CharacterDisplayNoritake
from volumio_vfd.clock_source import ClockSource
from volumio_vfd.volumio_client import VolumioClient


def main() -> None:
    display = CharacterDisplayNoritake()
    clock = ClockSource()
    volumio = VolumioClient()

    display.clear()
    clock.start()
    volumio.start()


if __name__ == "__main__":
    main()
