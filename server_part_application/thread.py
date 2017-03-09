import json
import sqlite3
import hashlib

from config import *
from crypto_fun.diffie_hellman import dhFirstUser
from crypto_fun.rc4 import EncoderRC4, DecoderRC4
from server_part_application.db import DbAdapter
from crypto_fun.rsa1 import User

# Регистрация



def get_dic_with_flag(flag, data):
    dic = {}
    dic.setdefault(KEY, flag)
    dic.setdefault(DATA, data)
    return dic


def add_user(login, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(str.format("INSERT INTO users_table VALUES ('%s','%s')" % (login, password)))
    conn.commit()


def read_users(login):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    request = str.format("SELECT * FROM users_table WHERE login_user='%s'" % login)
    c.execute(request)
    result = c.fetchone()
    if result != None:
        result = str(result[1])
        return result
    else:
        return 'None User'


def thread_read(conn):
    data = []
    while True:
        block = conn.recv(BLOCK_SIZE)
        data += block
        if len(block) != BLOCK_SIZE:
            break
    return data


def send_encrypt_json(sock, encoder_rc4, dic):
    sock.send(bytes(encoder_rc4.encode_text(json.dumps(dic))))


def decode_read_by_connect(decoder_rc4, conn):
    bt = bytes(thread_read(conn))
    result = (decoder_rc4.decode_text(bt))
    return json.loads(result)


def thread_def(conn, addr):
    print('connected:', addr)
    dh_first_user = dhFirstUser()
    result_dh = dh_first_user.to_json()
    conn.send(result_dh.encode())

    data = json.loads(bytes.decode(bytes(thread_read(conn))))
    print(data)
    key = dh_first_user.get_final_key(data['B'])
    print('dh = ', key)
    encoder_rc4 = EncoderRC4(key)
    decoder_rc4 = DecoderRC4(key)
    conn.send('flag1'.encode())
    print('Получение ключей RSA')
    rsa_keys = decode_read_by_connect(decoder_rc4, conn)
    print('rsa ', rsa_keys)
    user_rsa = User()
    print('Передача ключей RSA')
    send_encrypt_json(conn, encoder_rc4, user_rsa.public_key_to_dic())

    while True:
        print('Ожидание действий')
        global_data = decode_read_by_connect(decoder_rc4, conn)
        print(data)
        if global_data[KEY] == REGISTRATION_FLAG:
            print('Регистрация пользователя')
            data = global_data[DATA]
            password_byte = data[PASSWORD].encode()
            first_password_hash = hashlib.sha256(password_byte).hexdigest()
            add_user(login=data[LOGIN], password=first_password_hash)
            conn.send('flag1'.encode())
            continue

        if global_data[KEY] == REQUEST_AUTHENTICATION_FLAG:
            print('Запрос на авторизацию пользователя')
            secret_word = '123'
            main_dic = get_dic_with_flag(PASSWORD_AUTHENTICATION_FLAG, secret_word)
            send_encrypt_json(conn, encoder_rc4, main_dic)
            data = decode_read_by_connect(decoder_rc4, conn)
            print(data)
            data = data[DATA]
            user_password = read_users(data[LOGIN])
            user_password += secret_word
            user_password_bytes = user_password.encode()
            hash_result = hashlib.sha256(user_password_bytes).hexdigest()
            print('test b')
            print(hash_result)
            print(data[PASSWORD])
            print('test f')

            if hash_result == data[PASSWORD]:
                main_dic = get_dic_with_flag(SUCCESSFUL_AUTHENTICATION_FLAG, '')
                send_encrypt_json(conn, encoder_rc4, main_dic)
            else:
                main_dic = get_dic_with_flag(FAIL_AUTHENTICATION_FLAG, '')
                send_encrypt_json(conn, encoder_rc4, main_dic)
            continue

        if global_data[KEY] == DATA_FLAG:
            print('Обычный вывод')
            data = str(global_data[DATA])
            main_dic = get_dic_with_flag(DATA_FLAG, data.upper())
            send_encrypt_json(conn, encoder_rc4, main_dic)
            data = decode_read_by_connect(decoder_rc4, conn)
            print(data)
            continue


                # print(se)
            # conn.send(se)

    conn.close()
