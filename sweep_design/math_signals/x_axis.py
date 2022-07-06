
class Xaxis:

    def __init__(self, start: float = None, end: float = None, dx: float = None) -> None:
        self._start = start
        self._end = end
        self._dx = dx

    @property
    def dx(self):
        return self._dx