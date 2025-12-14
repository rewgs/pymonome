class Arc(Device):
    def __init__(self, prefix="monome"):
        super().__init__(prefix)

        self.add_handler("/*/enc/delta", self._on_enc_delta)
        self.add_handler("/*/enc/key", self._on_enc_key)

        self.delta_event = Event()
        self.key_event = Event()

    def _on_enc_delta(self, addr, path, ring, delta):
        self.delta_event.dispatch(ring, delta)

    def _on_enc_key(self, addr, path, n, s):
        self.key_event.dispatch(n, s)

    def ring_set(self, n, x, l):
        self.send("/{}/ring/set".format(self.prefix), n, x, l)

    def ring_all(self, n, l):
        self.send("/{}/ring/all".format(self.prefix), n, l)

    def ring_map(self, n, data):
        self.send("/{}/ring/map".format(self.prefix), n, *data)

    def ring_range(self, n, x1, x2, l):
        self.send("/{}/ring/range".format(self.prefix), n, x1, x2, l)
