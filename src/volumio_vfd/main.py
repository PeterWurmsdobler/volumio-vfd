import logging
import queue
import time
from datetime import datetime

from volumio_vfd.character_display_noritake import CharacterDisplayNoritake
from volumio_vfd.player_status import PlayerStatus
from volumio_vfd.volumio_client import VolumioClient

log = logging.getLogger(__name__)


def setup_logging(debug_stdout: bool = False) -> None:
    stdout_level = logging.DEBUG if debug_stdout else logging.INFO
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(logging.Formatter("%(asctime)s: %(message)s"))
    stdout_handler.setLevel(stdout_level)
    root_logger = logging.getLogger()
    root_logger.addHandler(stdout_handler)
    root_logger.setLevel(logging.DEBUG)


def main() -> None:
    display = CharacterDisplayNoritake()

    status_queue: queue.Queue = queue.Queue()

    server = u"localhost"
    port = 3000
    volumio_client = VolumioClient(status_queue, server, port)

    try:
        volumio_client.start()
        while True:
            log.debug("Main thread tick.")
            time.sleep(1)  # Delay for 1 second
        # while True:
        #     try:
        #         player_status = player_status_queue.get(timeout=1000)
        #         player_status_queue.task_done()
        #         assert isinstance(player_status, PlayerStatus)
        #
        #         display.update(datetime.now(), player_status)
        #
        #     except queue.Empty:
        #         pass

    except KeyboardInterrupt:
        print("")
        pass

    finally:
        volumio_client.join()
        # status_queue.join()

    print("Exiting...")


if __name__ == "__main__":
    setup_logging(True)
    main()
