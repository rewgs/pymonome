from .grid import Grid
from .page import GridPage


class GridApp:
    def __init__(self, grid: Grid | None = None):
        if grid is None:
            grid = Grid()

        self.set_grid(grid)

    def set_grid(self, grid: Grid):
        """set_grid assigns the GridApp to a Grid and initializes it with several handlers."""

        self.grid = grid
        self.grid.ready_event.add_handler(self.on_grid_ready)
        self.grid.disconnect_event.add_handler(self.on_grid_disconnect)
        self.grid.key_event.add_handler(self.on_grid_key)
        self.grid.tilt_event.add_handler(self.on_tilt)

    # NOTE: Considering the examples are (re)defining this method, it seems like
    # maybe GridApp should be an ABC and this method should be an abstractmethod.
    def on_grid_ready(self):
        pass

    # NOTE: Ditto ^
    def on_grid_disconnect(self):
        pass

    # NOTE: Ditto ^ (again)
    def on_grid_key(self, x, y, s):
        pass

    # NOTE: Ditto ^ (cubed)
    def on_tilt(self, n, x, y, z):
        pass


class GridPageManager(GridApp):
    def __init__(self, num_pages=1):
        super().__init__()

        self.pages = [GridPage(self) for i in range(num_pages)]
        self.set_current_page(0)

    def on_grid_ready(self):
        for page in self.pages:
            page.manager_ready()

    def on_grid_key(self, x, y, s):
        self.current_page.key_event.dispatch(x, y, s)

    def on_grid_disconnect(self):
        for page in self.pages:
            page.manager_disconnect()

    def set_current_page(self, index):
        self.current_page = self.pages[index]
        if self.current_page.buffer:
            self.current_page.buffer.render(self.grid)


class GridSplitter(GridApp):
    def __init__(self, sections):
        super().__init__()
        self._sections = sections
        for section in self._sections:
            section.splitter = self

    def on_grid_ready(self):
        for section in self._sections:
            section.splitter_ready()

    def on_grid_disconnect(self):
        for section in self._sections:
            section.splitter_disconnect()

    def on_grid_key(self, x, y, s):
        for section in self._sections:
            if (
                section.x_offset <= x < section.x_offset + section.section_width
                and section.y_offset <= y < section.y_offset + section.section_height
            ):
                section.key_event.dispatch(
                    x - section.x_offset, y - section.y_offset, s
                )
