import random
from for_big_int.arithmetic import fast_mod_pow


def is_prime(n):
    k = len('{0:b}'.format(n))
    t = n - 1
    s = 0
    while not t & 1:
        s += 1
        t >>= 1

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = fast_mod_pow(a, t, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s):
            x = (x * x) % n
            if x == 1:
                return False
            if x == n - 1:
                break
            return False
    return True


def next_prime(n):
    n |= 1
    n += 2
    while not is_prime(n):
        n += 2
    return n

if __name__ == '__main__':
    n = 101

    print(is_prime(n))
    # print(next_prime(n))
