import asyncio
import sys
from typing import Callable

import aiosc

from .event import Event


class SerialOsc(aiosc.OSCProtocol):
    def __init__(self, loop=None, autoconnect_app=None):
        # TODO: Add parameter and return type hints to Callable type hint (e.g. Callable[[str, str]bool] for a function that takes two strings and returns a bool)
        handlers: dict[str, Callable] = {
            "/serialosc/device": self._on_serialosc_device,
            "/serialosc/add": self._on_serialosc_add,
            "/serialosc/remove": self._on_serialosc_remove,
        }

        super().__init__(handlers)

        self.device_added_event = Event()
        self.device_removed_event = Event()

    def connection_made(self, transport):
        super().connection_made(transport)
        self.host, self.port = transport.get_extra_info("sockname")

        self.send("/serialosc/list", self.host, self.port)
        self.send("/serialosc/notify", self.host, self.port)

    async def connect(self, loop=None):
        if loop is None:
            if sys.version_info >= (3, 7):
                loop = asyncio.get_running_loop()
            else:
                loop = asyncio.get_event_loop()

        transport, protocol = await loop.create_datagram_endpoint(
            lambda: self, local_addr=("127.0.0.1", 0), remote_addr=("127.0.0.1", 12002)
        )

    def _on_serialosc_device(self, addr, path, id, type, port):
        type = type.strip()  # remove trailing spaces for arcs
        self.device_added_event.dispatch(id, type, port)

    def _on_serialosc_add(self, addr, path, id, type, port):
        type = type.strip()  # remove trailing spaces for arcs
        self.device_added_event.dispatch(id, type, port)
        self.send("/serialosc/notify", self.host, self.port)

    def _on_serialosc_remove(self, addr, path, id, type, port):
        type = type.strip()  # remove trailing spaces for arcs
        self.device_removed_event.dispatch(id, type, port)
        self.send("/serialosc/notify", self.host, self.port)
