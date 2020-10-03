import struct
import xxhash
from random import *

SEED = getrandbits(32)


class Hasher:

    def __init__(self):
        self.fn = xxhash.xxh32(seed=SEED)
        self.range = 2**32 -1

    def hasher(self, num):
        """Input: an integer (index for vector).  Output: a random integer."""
        self.fn.reset()
        # self.fn.update(bytes([num]))
        byte_form = struct.pack(">I", num)
        self.fn.update(byte_form)
        return self.fn.intdigest()

    def hashes_to_bucket(self, num: int,  probability: float) -> bool:
        return self.hasher(num) < (self.range * probability)

