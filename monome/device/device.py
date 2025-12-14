import asyncio
import sys

import aiosc

from .event import Event


class Device(aiosc.OSCProtocol):
    """
    Device forms the base class for monome devices such as Arc and Grid.
    """

    def __init__(self):
        super().__init__()

        self.add_handler("/sys/disconnect", self._on_sys_disconnect)
        self.add_handler("/sys/{id,size,host,port,prefix,rotation}", self._on_sys_info)

        self.connected: bool = False
        self.transport: None = None

        self.prefix = "monome"

        self.ready_event = Event()
        self.disconnect_event = Event()

        self._reset_info_properties()

    def _reset_info_properties(self):
        self.id = None
        self.width = None
        self.height = None
        self.rotation = None

    def _info_properties_set(self):
        return all(
            x is not None for x in [self.id, self.width, self.height, self.rotation]
        )

    def _on_sys_disconnect(self, addr, path, *args):
        self.disconnect()

    def _on_sys_info(self, addr, path, *args):
        if path == "/sys/id":
            self.id = args[0]
        elif path == "/sys/size":
            self.width, self.height = (args[0], args[1])
        elif path == "/sys/rotation":
            self.rotation = args[0]

        if self._info_properties_set():
            self.connected = True
            self.ready_event.dispatch()

    def connection_made(self, transport):
        super().connection_made(transport)
        self.host, self.port = transport.get_extra_info("sockname")

        self.send("/sys/host", self.host)
        self.send("/sys/port", self.port)
        self.send("/sys/prefix", self.prefix)
        self.send("/sys/info/id", self.host, self.port)
        self.send("/sys/info/size", self.host, self.port)
        self.send("/sys/info/rotation", self.host, self.port)

    async def connect(self, host, port, loop=None):
        if self.transport is not None and not self.transport.is_closing():
            self.disconnect()

        if loop is None:
            if sys.version_info >= (3, 7):
                loop = asyncio.get_running_loop()
            else:
                loop = asyncio.get_event_loop()

        transport, protocol = await loop.create_datagram_endpoint(
            lambda: self, local_addr=("127.0.0.1", 0), remote_addr=(host, port)
        )

    def disconnect(self):
        self.disconnect_event.dispatch()
        self._reset_info_properties()
        self.transport.close()  # FIXME: Close is not an attribute
        self.connected = False
