class Wing:
    def __init__(self, lift, drag, surface, masse, span):
        self.lift = lift
        self.drag = drag
        self.surface = surface
        self.masse = masse
        self.span = span
        self.aspect_ratio = span ** 2 / surface
        # self.surface = surface

    def get_lift(self):
        return self.lift

    def get_drag(self):
        return self.drag

    def get_surface(self):
        return self.surface

    def get_masse(self):
        return self.masse

    def get_span(self):
        return self.span
