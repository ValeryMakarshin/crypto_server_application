# import threading
# import rsa
# import hashlib
# from time import sleep
# from for_big_int.prime import is_prime
#
# def test_def(i):
#     print('test1 = ', i)
#
#
# threading.Thread(target=test_def, args=(10,)).start()
# print(threading.active_count())
# sleep(1)
# print(threading.active_count())
# print(123)
#
# s = 'qwerty'.encode()
# print(hashlib.sha512(s).hexdigest())
#
#
# import binascii
# dk = hashlib.pbkdf2_hmac('sha512', b'password', b'salt', 100000)
# print(binascii.hexlify(dk))
#

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


n = 1435
bt = int_to_byte(n)
print(bt)
print(byte_to_int(bt))

print(bytes(1))

print('dsfa134'.upper())

