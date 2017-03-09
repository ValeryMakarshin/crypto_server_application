import json
from random import getrandbits, randint
from for_big_int.prime import next_prime, fast_mod_pow
from for_big_int.arithmetic import inv_mod

BIT_LENGTH = 512

FERMAT_NUMBERS = [65537, 4294967297, 18446744073709551617]


# FERMAT_NUMBERS = [3, 5, 17]


class User():
    def __init__(self, bit_length=BIT_LENGTH):
        self.p = next_prime(getrandbits(bit_length))
        self.q = next_prime(getrandbits(bit_length))
        self.n = self.p * self.q

        self.f_n = (self.p - 1) * (self.q - 1)
        self.e = FERMAT_NUMBERS[randint(0, len(FERMAT_NUMBERS) - 1)]
        self.d = int(inv_mod(self.e, self.f_n))
        print(self.e * self.d % self.f_n)

    def encode(self, с, key, n):
        return fast_mod_pow(с, key, n)

    def __str__(self):
        return str.format('p = %d, q = %d, n = %d, e = %d, d = %d, fn = %d' %
                          (self.p, self.q, self.n, self.e, self.d, self.f_n))

    def public_key_to_dic(self):
        dic = {}
        dic.setdefault('e', self.e)
        dic.setdefault('n', self.n)
        return dic

    def public_key_to_json(self):
        return json.dumps(self.public_key_to_dic())

if __name__ == '__main__':
    alice = User(128)
    n = 124
    print(alice)

    t = alice.encode(n, alice.e, alice.n)
    print(t)
    t = alice.encode(t, alice.d, alice.n)
    print(t)
