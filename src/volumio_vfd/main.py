import logging
import queue
import time
from datetime import datetime

from volumio_vfd.character_display_noritake import CharacterDisplayNoritake
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
    log.info("Starting ...")

    display = CharacterDisplayNoritake()

    status_queue: queue.Queue = queue.Queue()

    server = u"localhost"
    port = 3000
    volumio_client = VolumioClient(status_queue, server, port)

    try:
        volumio_client.start()
        log.info("Started")
        while True:
            timsteap = datetime.now()
            player_status = None
            try:
                player_status = status_queue.get(timeout=0.1)
                status_queue.task_done()

            except queue.Empty:
                pass
            finally:
                display.update(timsteap, player_status)

            # Delay for 0.5 second
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("")
        pass

    finally:
        log.info("Exiting...")
        volumio_client.join()
        status_queue.join()

    log.info("Done.")


if __name__ == "__main__":
    setup_logging(False)
    main()
