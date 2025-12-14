from .device import Event


class GridPage:
    def __init__(self, manager):
        self.manager = manager
        self.buffer = None

        self.ready_event: Event = Event()
        self.disconnect_event: Event = Event()
        self.key_event: Event = Event()
        self.tilt_event: Event = Event()

    def manager_ready(self):
        self.id = "grid_page"
        self.width = self.manager.grid.width
        self.height = self.manager.grid.height
        self.rotation = self.manager.grid.rotation

        self.buffer = GridBuffer(self.width, self.height)
        self.ready_event.dispatch()

    def manager_disconnect(self):
        self.disconnect_event.dispatch()

    @property
    def active(self):
        return self is self.manager.current_page

    def led_set(self, x, y, s):
        self.buffer.led_set(x, y, s)
        if self.active:
            self.manager.grid.led_set(x, y, s)

    def led_all(self, s):
        self.buffer.led_all(s)
        if self.active:
            self.manager.grid.led_all(s)

    def led_map(self, x_offset, y_offset, data):
        self.buffer.led_map(x_offset, y_offset, data)
        if self.active:
            self.manager.grid.led_map(x_offset, y_offset, data)

    def led_row(self, x_offset, y, data):
        self.buffer.led_row(x_offset, y, data)
        if self.active:
            self.manager.grid.led_row(x_offset, y, data)

    def led_col(self, x, y_offset, data):
        self.buffer.led_col(x, y_offset, data)
        if self.active:
            self.manager.grid.led_col(x, y_offset, data)

    def led_intensity(self, i):
        self.manager.grid.led_intensity(i)

    def led_level_set(self, x, y, l):
        self.buffer.led_level_set(x, y, l)
        if self.active:
            self.manager.grid.led_level_set(x, y, l)

    def led_level_all(self, l):
        self.buffer.led_level_all(l)
        if self.active:
            self.manager.grid.led_level_all(l)

    def led_level_map(self, x_offset, y_offset, data):
        self.buffer.led_level_map(x_offset, y_offset, data)
        if self.active:
            self.manager.grid.led_level_map(x_offset, y_offset, data)

    def led_level_row(self, x_offset, y, data):
        self.buffer.led_level_row(x_offset, y, data)
        if self.active:
            self.manager.grid.led_level_row(x_offset, y, data)

    def led_level_col(self, x, y_offset, data):
        self.buffer.led_level_col(x, y_offset, data)
        if self.active:
            self.manager.grid.led_level_col(x, y_offset, data)


class SeqGridPageManager(GridPageManager):
    def __init__(self, num_pages=1, switch_button=(-1, -1)):
        super().__init__(num_pages)
        self._switch_button = switch_button

    def on_grid_ready(self):
        super().on_grid_ready()
        switch_x, switch_y = self._switch_button

        self._switch_x = self.grid.width + switch_x if switch_x < 0 else switch_x
        self._switch_y = self.grid.height + switch_y if switch_y < 0 else switch_y

    def on_grid_key(self, x, y, s):
        # TODO: bring back presses from pymonome 0.8
        if x == self._switch_x and y == self._switch_y and s == 1:
            self.set_current_page(
                (self.pages.index(self.current_page) + 1) % len(self.pages)
            )
        else:
            super().on_grid_key(x, y, s)


class SumGridPageManager(GridPageManager):
    def __init__(self, num_pages=1, switch_button=(-1, -1), **kwargs):
        super().__init__(num_pages)
        self._switch_button = switch_button
        self._selected_page_index = -1
        self._presses = set()

    def on_grid_ready(self):
        super().on_grid_ready()
        switch_x, switch_y = self._switch_button

        self._switch_x = self.grid.width + switch_x if switch_x < 0 else switch_x
        self._switch_y = self.grid.height + switch_y if switch_y < 0 else switch_y

    def on_grid_key(self, x, y, s):
        if not self._presses and x == self._switch_x and y == self._switch_y:
            if s == 1:
                self._selected_page_index = self.pages.index(self.current_page)
                # TODO: implement proper setter for this case
                self.current_page = None
                self.display_chooser()
            else:
                self.set_current_page(self._selected_page_index)
            return
        # handle regular buttons
        if self.current_page is None:
            if x < len(self.pages):
                self._selected_page_index = x
                self.display_chooser()
            return

        if s == 1:
            self._presses.add((x, y))
        else:
            self._presses.discard((x, y))

        super().on_grid_key(x, y, s)

    def display_chooser(self):
        self.grid.led_all(0)
        page_row = [1 if i < len(self.pages) else 0 for i in range(self.grid.width)]
        self.grid.led_row(0, self.grid.height - 1, page_row)
        self.grid.led_col(self._selected_page_index, 0, [1] * self.grid.height)
