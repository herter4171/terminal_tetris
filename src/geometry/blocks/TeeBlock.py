from colorama import Fore
from shapely.geometry import Polygon

from geometry.AbstrBaseShape import AbstrBaseShape


class TeeBlock(AbstrBaseShape):

    @property
    def color(self):
        return Fore.RED

    def __init__(self, partial_poly=None):
        super().__init__(partial_poly)

    def _get_initial_poly(self):
        return Polygon([
            (0, 0),
            (3, 0),
            (3, 1),
            (2, 1),
            (2, 2),
            (1, 2),
            (1, 1),
            (0, 1),
            (0, 0)
        ])