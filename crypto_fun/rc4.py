#!/usr/bin/env python
from for_big_int.arithmetic import int_to_byte

def KSA(key):
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S


def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]

        K = S[(S[i] + S[j]) % 256]
        yield K


def RC4(key):
    S = KSA(key)
    return PRGA(S)


def string_to_bit(text):
    return list(map(int, text.encode()))


class EncoderRC4():
    def __init__(self, key):
        # self.key_stream = RC4(string_to_bit(key))
        self.key_stream = RC4(int_to_byte(key))

    def encode_text(self, text):
        text_bits = string_to_bit(text)

        result = []
        for i in text_bits:
            result.append(i ^ self.key_stream.__next__())
        return result


class DecoderRC4():
    def __init__(self, key):
        # self.key_stream = RC4(string_to_bit(key))
        self.key_stream = RC4(int_to_byte(key))

    def decode_text(self, text):
        text_bits = text
        print(text_bits)
        result = []
        for i in text_bits:
            result.append(i ^ self.key_stream.__next__())
        return bytes(result).decode()


if __name__ == '__main__':
    key = 'Key'
    plaintext = 'Plaintext'

    print(plaintext)
    encode1 = encode_text(key, plaintext)
    print(encode1)
    decode1 = decode_text(key, encode1)
    print(decode1)
