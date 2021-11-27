from random import randrange

from geometry.AbstrBaseShape import AbstrBaseShape
from geometry.blocks.LBlocks import LBlockR, LBlockL
from geometry.blocks.LongBlock import LongBlock
from geometry.blocks.SquareBlock import SquareBlock
from geometry.blocks.StepBlocks import StepBlockR, StepBlockL
from geometry.blocks.TeeBlock import TeeBlock


class BlockFactory(object):

    __block_types = [
        LBlockR,
        LBlockL,
        LongBlock,
        SquareBlock,
        StepBlockR,
        StepBlockL,
        TeeBlock
    ]

    def __init__(self, bound_box):
        """Instantiate by setting global bound box."""
        AbstrBaseShape.set_bound_box(bound_box)

    def get_next_block(self):
        ind = randrange(len(BlockFactory.__block_types))
        block_type = BlockFactory.__block_types[ind]

        return block_type()