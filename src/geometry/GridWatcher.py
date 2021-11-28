from shapely.geometry import Point, box, Polygon

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

    def clear_lines(self):
        full_line_boxes, full_line_geo = self._get_full_line_geo()
        points = 0

        if full_line_boxes:
            for i in range(len(full_line_boxes)):
                curr_box = full_line_boxes[i]
                overlap_geo = full_line_geo[i]

                points += self._clear_single_line(curr_box, overlap_geo)

        return points

    def _clear_single_line(self, line_box, overlap_geo):
        assert(isinstance(line_box, Polygon))
        points = 0

        for curr_geo in overlap_geo:
            assert(isinstance(curr_geo, AbstrBaseShape))
            points += curr_geo.clear(line_box)

        self._move_geo_above_cleared_line(line_box.centroid.y)

        return points

    def _move_geo_above_cleared_line(self, y_mid):
        idle_blocks = AbstrBaseShape.get_inactive_blocks()
        move_vec = Point(0, 1)

        for curr_block in idle_blocks:
            assert(isinstance(curr_block, AbstrBaseShape))
            if curr_block.y_max < y_mid:
                curr_block.translate(move_vec, hard_check=False)

    def _get_full_line_geo(self):
        full_line_inds = []
        full_line_geo = []

        idle_blocks = AbstrBaseShape.get_inactive_blocks()

        for line_ind in range(len(self._check_cols[0])):
            line_points = [col[line_ind] for col in self._check_cols]

            is_full, overlap_geo = self._check_if_line_full(
                line_points,
                idle_blocks
            )

            if is_full:
                full_line_inds.append(line_ind)
                full_line_geo.append(overlap_geo)

        x_min = 0
        x_max = self._x_max

        full_line_boxes = []

        for line_ind in full_line_inds:
            y_mid = self._check_cols[0][line_ind].y
            offset = GridWatcher.__coord_offset

            y_min, y_max = [y_mid - offset, y_mid + offset]
            full_line_boxes.append(box(x_min, y_min, x_max, y_max))

        return full_line_boxes, full_line_geo

    def _check_if_line_full(self, points, idle_blocks):
        """If each point hits a block, the line is full."""
        num_overlap = 0
        overlap_geo = set()

        for curr_pt in points:
            assert(isinstance(curr_pt, Point))

            for curr_block in idle_blocks:
                assert(isinstance(curr_block, AbstrBaseShape))

                if curr_block.check_overlap(curr_pt, offset=False):
                    num_overlap += 1
                    overlap_geo.add(curr_block)

        return num_overlap == len(points), overlap_geo
