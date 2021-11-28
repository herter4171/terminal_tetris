from abc import ABCMeta, abstractmethod
from shapely.affinity import translate, rotate
from shapely.geometry import Point, Polygon
from shapely.geometry.base import BaseGeometry
from shapely.geometry.multipolygon import MultiPolygon

from utils import percent_diff_abs


class AbstrBaseShape(metaclass=ABCMeta):

    __all_geo = []
    __bound_box = None

    @staticmethod
    def get_all_geo():
        return AbstrBaseShape.__all_geo

    @staticmethod
    def get_active_block():
        ret_block = None

        for curr_block in AbstrBaseShape.__all_geo:
            assert(isinstance(curr_block, AbstrBaseShape))
            if curr_block._active:
                ret_block = curr_block
                break

        return ret_block

    @staticmethod
    def get_inactive_blocks():
        idle_blocks = []

        for curr_block in AbstrBaseShape.__all_geo:
            assert(isinstance(curr_block, AbstrBaseShape))
            if not curr_block._active:
                idle_blocks.append(curr_block)

        return idle_blocks

    @staticmethod
    def set_bound_box(bound_box):
        AbstrBaseShape.__bound_box = bound_box

    @property
    @abstractmethod
    def color(self):
        pass

    @property
    def is_active(self):
        return self._active

    @property
    def _velocity(self):
        return Point(0, 1) if self._active else Point(0, 0)

    @property
    def y_max(self):
        assert(isinstance(self._poly, Polygon))
        x_min, y_min, x_max, y_max = self._poly.bounds
        return y_max

    def __init__(self, partial_poly):
        """Instantiate with list of points."""
        # May be constructed with partial geometry
        if not partial_poly:
            self._poly = self._get_initial_poly()
        else:
            self._poly = partial_poly

        self._center = Point(0, 0)
        self._active = False
        AbstrBaseShape.__all_geo.append(self)

    def __hash__(self):
        return hash(str(self._poly))

    def __eq__(self, other):
        assert(isinstance(other, AbstrBaseShape))
        return self._poly == other._poly

    def toggle_active(self):
        self._active = not self._active

    def translate(self, vec, hard_check=True):
        """Move all points based on given vector coords."""
        assert(isinstance(vec, Point))
        velocity = self._velocity
        delta_x = vec.x + velocity.x
        delta_y = vec.y + velocity.y

        new_poly = translate(self._poly, delta_x, delta_y)
        valid_move = False

        # Want to be able to move pieces for initialization
        should_move = not hard_check

        # If not doing a hard check, ensure move is valid
        if not should_move:
            should_move = self._move_is_valid(new_poly)

        # Perform translation if shape is still in bounds
        if should_move:
            self._poly = new_poly
            self._center = translate(self._center, delta_x, delta_y)
            valid_move = True

        return valid_move

    def clear(self, row_poly):
        """Eliminates row geometry and returns points from area delta."""
        assert(isinstance(row_poly, Polygon))
        assert(isinstance(self._poly, Polygon))
        old_area = self._poly.area
        self._poly = self._poly.difference(row_poly)
        new_area = self._poly.area

        # If area is zero, this shape is fully cleared
        if new_area == 0:
            AbstrBaseShape.__all_geo.remove(self)
        elif type(self._poly) == MultiPolygon:
            self._split_multi_poly()

        return old_area - new_area

    def _split_multi_poly(self):
        """Assign one poly to self plus new instance for other."""
        assert(isinstance(self._poly, MultiPolygon))
        # Split polygons
        for other_poly in self._poly[1:]:
            block_type = type(self)
            block_type(other_poly)

        # Assign first to self
        self._poly = self._poly[0]

    def get_distance(self, other_geo):
        """Returns distance from other geo to internal polygon."""
        assert(isinstance(other_geo, BaseGeometry))
        return other_geo.distance(self._poly)

    def check_overlap(self, check_point, offset=True):
        assert(isinstance(check_point, Point))
        assert(isinstance(self._poly, Polygon))
        mid_point = check_point

        if offset:
            mid_point = translate(check_point, 0.5, 0.5)

        return self._poly.intersects(mid_point)

    def rotate(self, degrees):
        # TODO: Rotate around center better?
        new_poly = rotate(self._poly, degrees, origin=self._center)

        if self._move_is_valid(new_poly):
            self._poly = new_poly

    @abstractmethod
    def _get_initial_poly(self):
        pass

    def _flip_horizontal(self):
        assert(isinstance(self._poly, Polygon))
        coords_x, coords_y = self._poly.exterior.coords.xy

        # Invert x and increment by max x
        max_x = max(coords_x)
        coords_x = [-x_val + max_x for x_val in coords_x]

        # Get tuples for new points and assign polyon
        new_coords = [(coords_x[i], coords_y[i]) for i in range(len(coords_x))]
        self._poly = Polygon(new_coords)

    def _move_is_valid(self, new_poly):
        """Wrapper for checking bounds and overlaps."""
        in_bounds = self._new_poly_in_bounds(new_poly)
        has_overlap = self._new_poly_has_overlap(new_poly)

        return in_bounds and not has_overlap

    def _new_poly_in_bounds(self, new_poly, margin_pct=0.1):
        """Checks if proposed move is within bounds of game box."""
        assert(isinstance(AbstrBaseShape.__bound_box, Polygon))
        intersect_poly = AbstrBaseShape.__bound_box.intersection(new_poly)

        ref_area = self._poly.area
        area_pct_diff = percent_diff_abs(ref_area, intersect_poly.area)

        return area_pct_diff <= margin_pct

    def _new_poly_has_overlap(self, new_poly, margin_pct=0.1):
        """Checks if proposed move overlaps idle blocks."""
        # TODO: Final setting?
        has_overlap = False

        for idle_block in AbstrBaseShape.get_inactive_blocks():
            assert(isinstance(idle_block, AbstrBaseShape))
            diff_poly = new_poly.difference(idle_block._poly)

            ref_area = self._poly.area
            area_pct_diff = percent_diff_abs(ref_area, diff_poly.area)

            if area_pct_diff > margin_pct:
                has_overlap = True
                break

        return has_overlap
