class ArcBuffer:
    def __init__(self, rings):
        self.rings = rings
        self.levels = [[0 for i in range(64)] for ring in range(rings)]

    def __and__(self, other):
        rings = len(self.levels)
        result = ArcBuffer(rings)
        for ring in range(rings):
            for x in range(64):
                result.levels[ring][x] = self.levels[ring][x] & other.levels[ring][x]
        return result

    def __xor__(self, other):
        result = GridBuffer(self.width, self.height)
        for row in range(self.height):
            for col in range(self.width):
                result.levels[row][col] = self.levels[row][col] ^ other.levels[row][col]
        return result

    def __or__(self, other):
        result = GridBuffer(self.width, self.height)
        for row in range(self.height):
            for col in range(self.width):
                result.levels[row][col] = self.levels[row][col] | other.levels[row][col]
        return result

    def ring_set(self, n, x, l):
        self.levels[n][x] = l

    def ring_all(self, n, l):
        self.levels[n] = [l] * 64

    def ring_map(self, n, data):
        self.levels[n] = data

    def ring_range(self, n, x1, x2, l):
        for i in range(x1, x2 + 1):
            self.levels[n][i] = l

    def render(self, arc):
        for i in range(self.rings):
            arc.ring_map(i, self.levels[i])
