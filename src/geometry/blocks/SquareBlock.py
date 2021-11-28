from colorama import Fore
from shapely.geometry import Polygon

from geometry.AbstrBaseShape import AbstrBaseShape


class SquareBlock(AbstrBaseShape):

    @property
    def color(self):
        return Fore.GREEN

    def __init__(self, partial_poly=None):
        super().__init__(partial_poly)

    def _get_initial_poly(self):
        return Polygon([
            (0, 0),
            (2, 0),
            (2, 2),
            (0, 2),
            (0, 0)
        ])

    def rotate(self, clockwise):
        pass