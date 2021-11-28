from colorama import Fore
from shapely.geometry import Polygon

from geometry.AbstrBaseShape import AbstrBaseShape


class LBlockR(AbstrBaseShape):

    @property
    def color(self):
        return Fore.WHITE

    def __init__(self, partial_poly=None):
        super().__init__(partial_poly)

    def _get_initial_poly(self):
        return Polygon([
            (0, 0),
            (3, 0),
            (3, 1),
            (1, 1),
            (1, 2),
            (0, 2),
            (0, 0)
        ])


class LBlockL(LBlockR):

    @property
    def color(self):
        return Fore.YELLOW

    def __init__(self, partial_poly=None):
        super().__init__(partial_poly)
        self._flip_horizontal()