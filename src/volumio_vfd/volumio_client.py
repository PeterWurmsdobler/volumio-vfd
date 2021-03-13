from __future__ import unicode_literals

import logging
import queue
import threading
from typing import Any, Optional

from socketIO_client import SocketIO

from volumio_vfd.player_status import PlayerState, PlayerStatus

log = logging.getLogger(__name__)


def on_GetState_response(*args: Any) -> None:
    log.debug("********* Got Response **************")


class VolumioClient(threading.Thread):
    """The Client to Volumio to get music meta data and put them into a queue.

    Theis client uses a socket IO client to listen to the Volumio music data
    updates through a callback function. The latter produces a new music data
    item to be put into a threadsafe queue provided by the application.
    """

    def __init__(
        self, status_queue: queue.Queue, server: str = "localhost", port: int = 3000
    ) -> None:
        """Create instances with mandatory queue, and optional server and port."""

        super(VolumioClient, self).__init__(target=self._run, daemon=True)
        self._stop_event = threading.Event()
        self._status_queue = status_queue
        self._server = server
        self._port = port

    def join(self, timeout: Optional[float] = None) -> None:
        """Set stop event and join within a given time period."""
        log.debug("Ask client to stop ...")
        self._stop_event.set()
        super().join(timeout)

    def _run(self) -> None:
        """private thread runner to consume data and produce music data objects."""

        log.debug("Volumio 2 Web Service client starting ...")
        log.debug(f"Connecting to Volumio 2 Web Service on {self._server}:{self._port}")

        with SocketIO(self._server, self._port) as socketIO:
            log.debug("Connected to Volumio 2 Web Service")
            socketIO.on("pushState", self._on_state_response)
            socketIO.emit("GetState", on_GetState_response)

            # Request initial values
            socketIO.emit("getState", "")

            while not self._stop_event.is_set():
                socketIO.wait_for_callbacks(seconds=0.5)
                socketIO.emit("getState", "")

    def _on_state_response(self, *args: Any) -> None:

        response = args[0]

        status = PlayerStatus()

        state = response.get("status").lower()
        if state == "stop":
            status.state = PlayerState.Stopped
        elif state == "pause":
            status.state = PlayerState.Paused
        elif state == "play":
            status.state = PlayerState.Playing
        else:
            status.state = PlayerState.Stopped

        # String values
        status.performer = response["artist"] if "artist" in response else ""
        status.composer = response["artist"] if "artist" in response else ""
        status.oeuvre = response["album"] if "album" in response else ""
        status.part = response["title"] if "title" in response else ""

        # Numeric values
        status.elapsed = int(response["seek"]) if "seek" in response else 0
        status.duration = int(response["duration"]) if "duration" in response else 0
        status.volume = int(response["volume"]) if "volume" in response else 0

        # put PLayer Status on queue.
        self._status_queue.put(status, block=False)
