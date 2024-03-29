from os import system, name
import shutil
from colorama import Style
from shapely.geometry import Point, box
from time import sleep

from KeyboardInput import KeyBoardInput
from geometry.blocks.BlockFactory import BlockFactory
from geometry.AbstrBaseShape import AbstrBaseShape
from geometry.GridWatcher import GridWatcher


class GameGrid(object):

    # Character for blocks
    __fill = '█'

    __num_x = 20
    __num_y = 30

    # Spawn at top middle
    __start_point = Point(int(__num_x/2), 2)

    # Boundaries of the game box
    __bound_box = box(0, 0, __num_x, __num_y)

    # TODO: Make variable
    __sleep_interval = 0.15

    @property
    def game_over(self):
        return self._game_over

    def __init__(self):
        self._block_gen = BlockFactory(GameGrid.__bound_box)
        self._keyboard = KeyBoardInput()
        self._grid_watch = GridWatcher(GameGrid.__num_x, GameGrid.__num_y)
        self._points = 0
        self._game_over = False
        cols, self._line_height = shutil.get_terminal_size()

    def __str__(self):
        sleep(GameGrid.__sleep_interval)
        #self._clear_frame()
        self._points += self._grid_watch.clear_lines()
        self._check_active_block_placement()
        self._adjust_active_block()

        lines = []
        curr_ln = ''

        # Iterate by row then column
        for curr_y in range(GameGrid.__num_y):
            for curr_x in range(GameGrid.__num_x):
                curr_point = Point(curr_x, curr_y)
                next_char = ' '

                overlap_geo = self._get_overlap_geo(curr_point)

                if overlap_geo:
                    next_char = self._get_pixel(overlap_geo)

                curr_ln += next_char

                if curr_x + 1 == GameGrid.__num_x:
                    lines.append(curr_ln + '|')
                    curr_ln = ''

        lines.append('-'*GameGrid.__num_x)
        lines[-1] += '  Points: {}'.format(self._points)

        while len(lines) < self._line_height:
            lines.append('')

        return '\n'.join(lines)

    def _get_next_block(self):
        """Creates next block at starting point with it set to active."""
        next_block = self._block_gen.get_next_block()
        valid_move = next_block.translate(GameGrid.__start_point)
        next_block.toggle_active()

        if not valid_move:
            self._game_over = True

        return next_block

    def _get_overlap_geo(self, check_point):
        # TODO: Move to different type
        overlap_geo = None

        for curr_geo in AbstrBaseShape.get_all_geo():
            assert(isinstance(curr_geo, AbstrBaseShape))
            if curr_geo.check_overlap(check_point):
                overlap_geo = curr_geo
                break

        return overlap_geo

    def _get_pixel(self, src_geo):
        assert(isinstance(src_geo, AbstrBaseShape))
        return src_geo.color + GameGrid.__fill + Style.RESET_ALL

    def _clear_frame(self):
        """Removes characters from prior frame."""
        cmd = 'cls' if name == 'nt' else 'clear'
        system(cmd)

    def _adjust_active_block(self):
        # Want to operate on active block
        active_block = AbstrBaseShape.get_active_block()

        if active_block is None:
            active_block = self._get_next_block()

        assert(isinstance(active_block, AbstrBaseShape))

        # Get translate vector and rotate angle
        translate_vec = self._keyboard.translate_vec
        rotate_angle = self._keyboard.rotate_angle

        # Perform translation
        active_block.translate(translate_vec)

        # Rotate if non-zero
        if rotate_angle:
            active_block.rotate(rotate_angle)

    def _check_active_block_placement(self, threshold=0.1):
        active_block = AbstrBaseShape.get_active_block()

        if active_block:
            height_pts = self._grid_watch.get_all_bin_height_pts()

            for curr_ht_pt in height_pts:
                if active_block.get_distance(curr_ht_pt) < threshold:
                    active_block.toggle_active()
                    break

