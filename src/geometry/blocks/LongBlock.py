from colorama import Fore
from shapely.geometry import Polygon

from geometry.AbstrBaseShape import AbstrBaseShape


class LongBlock(AbstrBaseShape):

    @property
    def color(self):
        return Fore.BLUE

    def __init__(self, partial_poly=None):
        super().__init__(partial_poly)

    def _get_initial_poly(self):
        return Polygon([
            (0, 0),
            (4, 0),
            (4, 1),
            (0, 1),
            (0, 0)
        ])
