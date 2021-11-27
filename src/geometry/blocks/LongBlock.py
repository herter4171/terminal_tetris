from colorama import Fore
from shapely.geometry import Polygon

from geometry.AbstrBaseShape import AbstrBaseShape


class LongBlock(AbstrBaseShape):

    @property
    def color(self):
        return Fore.BLUE

    def __init__(self):
        super().__init__()

    def _get_initial_poly(self):
        return Polygon([
            (0, 0),
            (4, 0),
            (4, 1),
            (0, 1),
            (0, 0)
        ])
