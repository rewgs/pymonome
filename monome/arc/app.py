from .arc import Arc


class ArcApp:
    def __init__(self, arc=None):
        if arc is None:
            arc = Arc()

        self.set_arc(arc)

    def set_arc(self, arc):
        self.arc = arc
        self.arc.ready_event.add_handler(self.on_arc_ready)
        self.arc.disconnect_event.add_handler(self.on_arc_disconnect)
        self.arc.delta_event.add_handler(self.on_arc_delta)
        self.arc.key_event.add_handler(self.on_arc_key)

    def on_arc_ready(self):
        pass

    def on_arc_disconnect(self):
        pass

    def on_arc_delta(self, ring, delta):
        pass

    def on_arc_key(self, ring, s):
        pass
