from colorama import Fore
from shapely.geometry import Polygon

from geometry.AbstrBaseShape import AbstrBaseShape


class StepBlockR(AbstrBaseShape):

    @property
    def color(self):
        return Fore.CYAN

    def __init__(self):
        super().__init__()

    def _get_initial_poly(self):
        return Polygon([
            (0, 0),
            (2, 0),
            (2, 1),
            (3, 1),
            (3, 2),
            (1, 2),
            (1, 1),
            (0, 1),
            (0, 0)
        ])


class StepBlockL(StepBlockR):

    @property
    def color(self):
        return Fore.LIGHTGREEN_EX

    def __init__(self):
        super().__init__()
        self._flip_horizontal()