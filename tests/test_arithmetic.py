import unittest
from random import getrandbits
from for_big_int.arithmetic import *

BIT_LENGTH = 80


class test_arithmetic(unittest.TestCase):
    def test_convert_int(self):
        n = getrandbits(BIT_LENGTH)
        bt = int_to_byte(n)
        self.assertEqual(n, byte_to_int(bt))

    def test_fast_mod_pow(self):
        a = getrandbits(BIT_LENGTH)
        e = getrandbits(BIT_LENGTH)
        n = getrandbits(BIT_LENGTH)
        self.assertEqual(pow(a, e, n), fast_mod_pow(a, e, n))