from shapely.geometry import Point

from geometry.AbstrBaseShape import AbstrBaseShape


class GridWatcher(object):

    __coord_offset = 0.5

    @staticmethod
    def _get_check_coords(coord_max):
        raw_coords = list(range(coord_max))
        return [crd + GridWatcher.__coord_offset for crd in raw_coords]

    def __init__(self, x_max, y_max):
        self._x_max = x_max
        self._y_max = y_max
        self._check_cols = self._get_check_columns()

    def get_all_bin_height_pts(self):
        idle_blocks = AbstrBaseShape.get_inactive_blocks()
        height_pts = []

        for curr_bin in self._check_cols:
            curr_height_pt = self._get_single_bin_height_pt(curr_bin, idle_blocks)
            height_pts.append(curr_height_pt)

        return height_pts

    def _get_single_bin_height_pt(self, curr_bin, idle_blocks):
        height = self._y_max
        height_pt = None

        for curr_pt in curr_bin:
            assert(isinstance(curr_pt, Point))

            for curr_block in idle_blocks:
                assert(isinstance(curr_block, AbstrBaseShape))
                if curr_block.check_overlap(curr_pt, offset=False):
                    height = curr_pt.y - GridWatcher.__coord_offset
                    height_pt = Point(curr_pt.x, height)
                    break

            if height_pt:
                break

        if not height_pt:
            height_pt = Point(curr_bin[0].x, self._y_max)

        return height_pt

    def _get_check_columns(self):
        # Get center-point coord lists
        coords_x = GridWatcher._get_check_coords(self._x_max)
        coords_y = GridWatcher._get_check_coords(self._y_max)
        #coords_y.reverse()

        columns = []

        for curr_x in coords_x:
            curr_col = [Point(curr_x, curr_y) for curr_y in coords_y]
            columns.append(curr_col)

        return columns


