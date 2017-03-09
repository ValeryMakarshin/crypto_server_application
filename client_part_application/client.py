#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import json
import hashlib
from time import sleep
from crypto_fun.diffie_hellman import dhSecondUser
from crypto_fun.rsa1 import User
from crypto_fun.rc4 import EncoderRC4, DecoderRC4
from config import *

# BLOCK_SIZE = 1024
#
# KEY = 'key'
# REGISTRATION_FLAG = 1
# DATA = 'data'
# RSA_FLAG = 4
# REQUEST_AUTHENTICATION_FLAG = 2
# PASSWORD_AUTHENTICATION_FLAG = 3


def client_read(sock):
    data = []
    while True:
        block = sock.recv(BLOCK_SIZE)
        data += block
        if len(block) != BLOCK_SIZE:
            break
    return data


def send_encrypt_json(sock, encoder_rc4, dic):
    bt = bytes(encoder_rc4.encode_text(json.dumps(dic)))
    sock.send(bt)


def get_dic_with_flag(flag, data):
    dic = {}
    dic.setdefault(KEY, flag)
    dic.setdefault(DATA, data)
    return dic

def decode_read_by_connect(decoder_rc4, conn):
    bt = bytes(client_read(conn))
    result = (decoder_rc4.decode_text(bt))
    return json.loads(result)


sock = socket.socket()
sock.connect(('localhost', PORT))

data = client_read(sock)
s = json.loads(bytes.decode(bytes(data)))
print(s)
dh_second_user = dhSecondUser(s['g'], s['p'], s['A'])
sock.send(dh_second_user.to_json().encode())
key = dh_second_user.get_final_key()
print('key_dh ', key)
encoder_rc4 = EncoderRC4(key)
decoder_rc4 = DecoderRC4(key)

data = client_read(sock)
user = User()
print('Передача RSA клиента')
send_encrypt_json(sock, encoder_rc4, user.public_key_to_dic())
# sock.send(user.public_key_to_json().encode())

# send_encrypt_json(sock, encoder_rc4, user.public_key_to_dic())
# sock.send(user.public_key_to_json().encode())
# client_read(sock)
print('Передача завершена')

print('Прием RSA сервера')
rsa_key = decode_read_by_connect(decoder_rc4, sock)
print(rsa_key)
print('Прием завершена')

# Регистрация




SIGNATURE = 'signature'
LOGIN = 'login'
login = '11'
PASSWORD = 'password'
password = '125464'
dic = {}
dic.setdefault(LOGIN, login)
dic.setdefault(PASSWORD, password)

# print('Отправление данных для регистрации')
# main_dic = get_dic_with_flag(REGISTRATION_FLAG, dic)
# print(main_dic)
# # bber = bytes(encoder_rc4.encode_text(json.dumps(main_dic)))
# # sock.send(bytes(bber))
# send_encrypt_json(sock, encoder_rc4, main_dic)
# print('Ожидание ответа о успешности регистрации')
# data = client_read(sock)
# print('Ответ пришел')

print('Запрос слова для авторизации')
main_dic = get_dic_with_flag(REQUEST_AUTHENTICATION_FLAG, '')
print(main_dic)
# sock.send(bytes(encoder_rc4.encode_text(json.dumps(main_dic))))
send_encrypt_json(sock, encoder_rc4, main_dic)
print('Слово получено')
data = decode_read_by_connect(decoder_rc4, sock)
print(data)

dic = {}
dic.setdefault(LOGIN, login)
password_byte = password.encode()
first_password_hash = hashlib.sha256(password_byte).hexdigest()
# print(data[0])
# str().encode()
first_password_hash += data[DATA]
print(first_password_hash)
first_password_hash = first_password_hash.encode()
second_password_hash = hashlib.sha256(first_password_hash).hexdigest()

print(second_password_hash)
dic.setdefault(PASSWORD, second_password_hash)
print('Отправление данных для авторизации')
main_dic = get_dic_with_flag(REGISTRATION_FLAG, dic)

send_encrypt_json(sock, encoder_rc4, main_dic)

result = decode_read_by_connect(decoder_rc4, sock)
print(result)
# sock.send('hello!'.encode())
sock.close()

# print(data)
