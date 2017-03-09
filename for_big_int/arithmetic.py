
def to_binary(x):
    return list(map(int, '{0:b}'.format(x)))


def fast_mod_pow(a, e, n):
    a %= n
    bin_arr = to_binary(e)
    result = 1
    for i in bin_arr[:-1]:
        if i:
            result *= a
            result %= n
        result *= result
        result %= n
    result *= a ** bin_arr[-1]
    result %= n
    return result


def inv_mod(a, m):
    m1 = m
    a, x, u = a % m, 0, 1
    while a:
        x, u, m, a = u, x - (m // a) * u, a, m % a
    return x % m1


def int_to_byte(n):
    MOD = 255
    STEP_BYTE = 8
    result = []
    while n > 0:
        result.append(n & MOD)
        n >>= STEP_BYTE
    return result[::-1]


def byte_to_int(bytes):
    STEP_BYTE = 8
    result = 0
    for i in bytes:
        result <<= STEP_BYTE
        result |= i
    return result

