import itertools
import re

from .device import Device, Event


def pack_row(row):
    return (
        row[7] << 7
        | row[6] << 6
        | row[5] << 5
        | row[4] << 4
        | row[3] << 3
        | row[2] << 2
        | row[1] << 1
        | row[0]
    )


class Grid(Device):
    def __init__(self):
        super().__init__()

        self.add_handler("/*/grid/key", self._on_grid_key)
        self.add_handler("/*/tilt", self._on_tilt)

        self.key_event: Event = Event()
        self.tilt_event: Event = Event()

        self.varibright: bool = True

        self.ready_event.add_handler(self._set_varibright)

    def _set_varibright(self):
        if not re.match(r"^m\d+$", self.id, flags=re.IGNORECASE):
            self.varibright = False

    def _on_grid_key(self, addr, path, x, y, s):
        self.key_event.dispatch(x, y, s)

    def _on_tilt(self, addr, path, n, x, y, z):
        self.tilt_event.dispatch(n, x, y, z)

    def led_set(self, x, y, s):
        self.send("/{}/grid/led/set".format(self.prefix), x, y, s)

    def led_all(self, s):
        self.send("/{}/grid/led/all".format(self.prefix), s)

    def led_map(self, x_offset, y_offset, data):
        args = [pack_row(data[i]) for i in range(8)]
        self.send("/{}/grid/led/map".format(self.prefix), x_offset, y_offset, *args)

    def led_row(self, x_offset, y, data):
        args = [pack_row(data[i * 8 : (i + 1) * 8]) for i in range(len(data) // 8)]
        self.send("/{}/grid/led/row".format(self.prefix), x_offset, y, *args)

    def led_col(self, x, y_offset, data):
        args = [pack_row(data[i * 8 : (i + 1) * 8]) for i in range(len(data) // 8)]
        self.send("/{}/grid/led/col".format(self.prefix), x, y_offset, *args)

    def led_intensity(self, i):
        self.send("/{}/grid/led/intensity".format(self.prefix), i)

    def led_level_set(self, x, y, l):
        if self.varibright:
            self.send("/{}/grid/led/level/set".format(self.prefix), x, y, l)
        else:
            self.led_set(x, y, l >> 3 & 1)

    def led_level_all(self, l):
        if self.varibright:
            self.send("/{}/grid/led/level/all".format(self.prefix), l)
        else:
            self.led_all(l >> 3 & 1)

    def led_level_map(self, x_offset, y_offset, data):
        if self.varibright:
            args = itertools.chain(*data)
            self.send(
                "/{}/grid/led/level/map".format(self.prefix), x_offset, y_offset, *args
            )
        else:
            self.led_map(
                x_offset, y_offset, [[l >> 3 & 1 for l in row] for row in data]
            )

    def led_level_row(self, x_offset, y, data):
        if self.varibright:
            self.send("/{}/grid/led/level/row".format(self.prefix), x_offset, y, *data)
        else:
            self.led_row(x_offset, y, [l >> 3 & 1 for l in data])

    def led_level_col(self, x, y_offset, data):
        if self.varibright:
            self.send("/{}/grid/led/level/col".format(self.prefix), x, y_offset, *data)
        else:
            self.led_col(x, y_offset, [l >> 3 & 1 for l in data])

    def tilt_set(self, n, s):
        self.send("/{}/tilt/set".format(self.prefix), n, s)
