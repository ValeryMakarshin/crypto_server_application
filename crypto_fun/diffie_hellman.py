from json import dumps
from random import getrandbits, randint
from for_big_int.prime import next_prime
from for_big_int.arithmetic import fast_mod_pow

BIT_LENGTH = 256


class dhFirstUser():
    def __init__(self, bit_length=BIT_LENGTH):
        self.p = next_prime(getrandbits(bit_length))
        self.a = randint(2, self.p)
        self.g = next_prime(randint(2, self.p))
        self.A = fast_mod_pow(self.g, self.a, self.p)

    def get_keys(self):
        return self.g, self.p, self.A

    def get_final_key(self, B):
        self.K = fast_mod_pow(B, self.a, self.p)
        return self.K

    def __str__(self):
        return str.format('p = %d; a = %d; g = %d; A = %d; K = %d' % (self.p, self.a, self.g, self.A, self.K))

    def get_dict(self):
        data = {}
        data.setdefault('g', self.g)
        data.setdefault('p', self.p)
        data.setdefault('A', self.A)
        return data

    def to_json(self):
        return dumps(self.get_dict())


class dhSecondUser():
    def __init__(self, g, p, A):
        self.b = randint(2, p)
        self.B = fast_mod_pow(g, self.b, p)
        self.K = fast_mod_pow(A, self.b, p)

    def get_B(self):
        return self.B

    def get_final_key(self):
        return self.K

    def __str__(self):
        return str.format('b = %d; B = %d; K = %d' % (self.b, self.B, self.K))

    def get_dict(self):
        data = {}
        data.setdefault('B', self.B)
        return data

    def to_json(self):
        return dumps(self.get_dict())


if __name__ == '__main__':
    f = dhFirstUser()
    t = dhSecondUser(f.g, f.p, f.A)
    f.get_final_key(t.get_B())
    print(f)
