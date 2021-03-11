from __future__ import unicode_literals

import logging
import queue
import threading
from typing import Any, Optional

from socketIO_client import SocketIO

from volumio_vfd.player_status import PlayerState, PlayerStatus


class VolumioClient(object):
    """The Client to Volumio to get music meta data and put them into a queue.

    Theis client uses a socket IO client to listen to the Volumio music data
    updates through a callback function. The latter produces a new music data
    item to be put into a threadsafe queue provided by the application.
    """

    def __init__(
        self, dataqueue: queue.Queue, server: str = "localhost", port: int = 3000
    ):
        """Create instances with mandatory queue, and optional server and port."""
        self.dataqueue = dataqueue
        self.server = server
        self.port = port

        self._running_lock = threading.Lock()
        self._running = False

        self.client_thread: Optional[threading.Thread] = None

    def start(self) -> None:
        """Start Volumio client thread."""

        if self.client_thread is None:
            self.client_thread = threading.Thread(target=self._run)
            self.client_thread.daemon = True
            self.client_thread.start()
        else:
            logging.debug("Thread already runnning.")

    def stop(self) -> None:
        """Stop Volumio client thread."""

        if self.client_thread is not None:

            with self._running_lock:
                self._running = False

            self.client_thread.join()
            self.client_thread = None

    def _run(self) -> None:
        """Thread runner to consume data and produce music data objects."""

        with self._running_lock:
            self._running = True

        logging.debug("Volumio 2 musicdata service starting ...")
        logging.debug(
            "Connecting to Volumio Web Service on {0}:{1}".format(
                self.server, self.port
            )
        )

        with SocketIO(self.server, self.port) as socketIO:
            logging.debug("Connected to Volumio Web Service")
            socketIO.on("pushState", self._on_state_response)

            # Request initial values
            socketIO.emit("getState", "")

            while self._running:
                socketIO.wait_for_callbacks(seconds=20)
                socketIO.emit("getState", "")

    def _on_state_response(self, *args: Any) -> None:
        # Read musicplayer status and update musicdata

        volumio_status = args[0]

        player_status = PlayerStatus()

        state = volumio_status.get("status").lower()
        if state == "stop":
            player_status.state = PlayerState.Stopped
        elif state == "pause":
            player_status.state = PlayerState.Paused
        elif state == "play":
            player_status.state = PlayerState.Playing
        else:
            player_status.state = PlayerState.Stopped

        # String values
        player_status.performer = (
            volumio_status["artist"] if "artist" in volumio_status else ""
        )
        player_status.composer = (
            volumio_status["artist"] if "artist" in volumio_status else ""
        )
        player_status.oeuvre = (
            volumio_status["album"] if "album" in volumio_status else ""
        )
        player_status.part = (
            volumio_status["title"] if "title" in volumio_status else ""
        )

        # Numeric values
        player_status.elapsed = (
            int(volumio_status["seek"]) if "seek" in volumio_status else 0
        )
        player_status.duration = (
            int(volumio_status["duration"]) if "duration" in volumio_status else 0
        )
        player_status.remaining = (
            int(volumio_status["volume"]) if "volume" in volumio_status else 0
        )

        # put music data item on queue.
        self.dataqueue.put(player_status, block=False)
