import queue
from datetime import datetime

from volumio_vfd.character_display_noritake import CharacterDisplayNoritake
from volumio_vfd.player_status import PlayerStatus
from volumio_vfd.volumio_client import VolumioClient


def main() -> None:
    display = CharacterDisplayNoritake()

    q: queue.Queue = queue.Queue()

    server = u"localhost"
    port = 3000
    volumio_client = VolumioClient(q, server, port)

    try:
        volumio_client.start()
        while True:
            try:
                player_status = q.get(timeout=1000)
                q.task_done()
                assert isinstance(player_status, PlayerStatus)

                display.update(datetime.now(), player_status)

            except queue.Empty:
                pass

    except KeyboardInterrupt:
        print("")
        pass

    finally:
        volumio_client.stop()

    print("Exiting...")


if __name__ == "__main__":
    main()
