from .event import Event


class GridSection:
    def __init__(self, size, offset):
        self.splitter = None

        self.section_width = size[0]
        self.section_height = size[1]
        self.x_offset = offset[0]
        self.y_offset = offset[1]

        self.ready_event = Event()
        self.disconnect_event = Event()
        self.key_event = Event()
        self.tilt_event = Event()

    def splitter_ready(self):
        self.width = self.section_width
        self.height = self.section_height
        self.rotation = 0
        self.ready_event.dispatch()

    def splitter_disconnect(self):
        self.disconnect_event.dispatch()

    def led_set(self, x, y, s):
        if x < self.section_width and y < self.section_height:
            self.splitter.grid.led_set(x + self.x_offset, y + self.y_offset, s)

    def led_all(self, s):
        # TODO: fix map
        data = [[s for col in range(8)] for row in range(8)]
        self.splitter.grid.led_map(self.x_offset, self.y_offset, data)

    def led_map(self, x_offset, y_offset, data):
        self.splitter.grid.led_map(
            self.x_offset + x_offset, self.y_offset + y_offset, data
        )

    def led_row(self, x_offset, y, data):
        data = data[: self.section_width]
        self.splitter.grid.led_row(self.x_offset + x_offset, self.y_offset + y, data)

    def led_col(self, x, y_offset, data):
        data = data[: self.section_height]
        self.splitter.grid.led_col(self.x_offset + x, self.y_offset + y_offset, data)

    def led_intensity(self, i):
        self.splitter.grid.led_intensity(i)

    def led_level_set(self, x, y, l):
        if x < self.section_width and y < self.section_height:
            self.splitter.grid.led_level_set(self.x_offset + x, self.y_offset + y, l)

    def led_level_all(self, l):
        data = [[l for col in range(8)] for row in range(8)]
        self.splitter.grid.led_map(self.x_offset, self.y_offset, data)

    def led_level_map(self, x_offset, y_offset, data):
        self.splitter.grid.led_level_map(
            self.x_offset + x_offset, self.y_offset + y_offset, data
        )

    def led_level_row(self, x_offset, y, data):
        data = data[: self.section_width]
        self.splitter.grid.led_level_row(
            self.x_offset + x_offset, self.y_offset + y, data
        )

    def led_level_col(self, x, y_offset, data):
        data = data[: self.section_height]
        self.splitter.grid.led_level_col(
            self.x_offset + x, self.y_offset + y_offset, data
        )
