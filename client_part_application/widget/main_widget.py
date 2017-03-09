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

import sys
import PyQt5.QtWidgets as p_widget

LABEL_HEIGHT = 50
LABEL_WEIGHT = 50

TEXT_EDIT_HEIGHT = 50
TEXT_EDIT_WEIGHT = 200


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


class widget(p_widget.QWidget):
    def __init__(self):
        self.flag_connection = 0
        self.flag_authentication = 0
        super().__init__()
        self.ip_address_text_edit = p_widget.QTextEdit(self)
        self.login_text_edit = p_widget.QTextEdit(self)
        self.password_text_edit = p_widget.QTextEdit(self)
        self.data_text_edit = p_widget.QTextEdit(self)

        self.button_connect = p_widget.QPushButton('Connect', self)
        self.button_registration = p_widget.QPushButton('Registration', self)
        self.button_authentication = p_widget.QPushButton('Authentication', self)
        self.button_request = p_widget.QPushButton('Request', self)

        self.init_ui()

    def init_ui(self):
        main_vertical_box = p_widget.QVBoxLayout()
        hbox = p_widget.QHBoxLayout()
        ip_label = p_widget.QLabel(self)
        ip_label.setText('ip: ')
        ip_label.setFixedSize(LABEL_WEIGHT, LABEL_HEIGHT)
        self.ip_address_text_edit.setFixedSize(TEXT_EDIT_WEIGHT, TEXT_EDIT_HEIGHT)

        hbox.addWidget(ip_label)
        hbox.addWidget(self.ip_address_text_edit)
        hbox.addWidget(self.button_connect)
        main_vertical_box.addLayout(hbox)

        hbox = p_widget.QHBoxLayout()
        login_label = p_widget.QLabel(self)
        login_label.setText('login: ')
        login_label.setFixedSize(LABEL_WEIGHT, LABEL_HEIGHT)
        self.login_text_edit.setFixedSize(TEXT_EDIT_WEIGHT, TEXT_EDIT_HEIGHT)

        vbox = p_widget.QVBoxLayout()
        hbox.addWidget(login_label)
        hbox.addWidget(self.login_text_edit)
        vbox.addLayout(hbox)

        hbox = p_widget.QHBoxLayout()
        password_label = p_widget.QLabel(self)
        password_label.setText('password: ')
        password_label.setFixedSize(LABEL_WEIGHT, LABEL_HEIGHT)
        self.password_text_edit.setFixedSize(TEXT_EDIT_WEIGHT, TEXT_EDIT_HEIGHT)

        hbox.addWidget(password_label)
        hbox.addWidget(self.password_text_edit)
        vbox.addLayout(hbox)

        hbox = p_widget.QHBoxLayout()
        hbox.addWidget(self.button_registration)
        hbox.addWidget(self.button_authentication)
        vbox.addLayout(hbox)
        main_vertical_box.addLayout(vbox)

        hbox_request = p_widget.QHBoxLayout()
        request_label = p_widget.QLabel(self)
        request_label.setText('request: ')
        request_label.setFixedSize(LABEL_WEIGHT, LABEL_HEIGHT)
        self.data_text_edit.setFixedSize(TEXT_EDIT_WEIGHT, TEXT_EDIT_HEIGHT)

        hbox_request.addWidget(request_label)
        hbox_request.addWidget(self.data_text_edit)
        hbox_request.addWidget(self.button_request)
        main_vertical_box.addLayout(hbox_request)

        self.setLayout(main_vertical_box)
        self.button_connect.clicked.connect(self.button_connect_click)
        self.button_registration.clicked.connect(self.button_registration_click)
        self.button_authentication.clicked.connect(self.button_authentication_click)
        self.button_request.clicked.connect(self.button_request_click)
        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle('Quadratic sieve')
        self.show()
        self.defualt_value()

    def defualt_value(self):
        self.button_registration.setEnabled(False)
        self.button_authentication.setEnabled(False)
        self.button_request.setEnabled(False)

    def button_connect_click(self):
        self.sock = socket.socket()
        self.sock.connect(('localhost', PORT))

        data = client_read(self.sock)
        s = json.loads(bytes.decode(bytes(data)))
        print(s)
        dh_second_user = dhSecondUser(s['g'], s['p'], s['A'])
        self.sock.send(dh_second_user.to_json().encode())
        key_dh = dh_second_user.get_final_key()
        print('key_dh ', key_dh)
        self.encoder_rc4 = EncoderRC4(key_dh)
        self.decoder_rc4 = DecoderRC4(key_dh)

        data = client_read(self.sock)
        self.user = User()
        print('Передача RSA клиента')
        send_encrypt_json(self.sock, self.encoder_rc4, self.user.public_key_to_dic())
        print('Передача завершена')

        print('Прием RSA сервера')
        self.rsa_key = decode_read_by_connect(self.decoder_rc4, self.sock)
        print(self.rsa_key)
        print('Прием завершена')

        self.button_registration.setEnabled(True)
        self.button_authentication.setEnabled(True)
        print('con')

    def button_registration_click(self):

        print(self.login_text_edit.toPlainText())

        dic = {}
        dic.setdefault(LOGIN, self.login_text_edit.toPlainText())
        dic.setdefault(PASSWORD, self.password_text_edit.toPlainText())

        print('Отправление данных для регистрации')
        main_dic = get_dic_with_flag(REGISTRATION_FLAG, dic)
        print(main_dic)
        send_encrypt_json(self.sock, self.encoder_rc4, main_dic)
        print('Ожидание ответа о успешности регистрации')
        data = client_read(self.sock)
        print('Ответ пришел')
        print('reg')

    def button_authentication_click(self):
        login = self.login_text_edit.toPlainText()
        password = self.password_text_edit.toPlainText()

        print('Запрос слова для авторизации')
        main_dic = get_dic_with_flag(REQUEST_AUTHENTICATION_FLAG, '')
        print(main_dic)
        # sock.send(bytes(encoder_rc4.encode_text(json.dumps(main_dic))))
        send_encrypt_json(self.sock, self.encoder_rc4, main_dic)
        print('Слово получено')
        data = decode_read_by_connect(self.decoder_rc4, self.sock)
        print(data)

        dic = {}
        dic.setdefault(LOGIN, login)
        password_byte = password.encode()
        first_password_hash = hashlib.sha256(password_byte).hexdigest()
        first_password_hash += data[DATA]
        print(first_password_hash)
        first_password_hash = first_password_hash.encode()
        second_password_hash = hashlib.sha256(first_password_hash).hexdigest()

        print(second_password_hash)
        dic.setdefault(PASSWORD, second_password_hash)
        print('Отправление данных для авторизации')
        main_dic = get_dic_with_flag(REGISTRATION_FLAG, dic)

        send_encrypt_json(self.sock, self.encoder_rc4, main_dic)

        result = decode_read_by_connect(self.decoder_rc4, self.sock)
        print(result)
        if result[KEY] == SUCCESSFUL_AUTHENTICATION_FLAG:
            self.button_request.setEnabled(True)
            print('successful_authentication')
        else:
            print('fail_authentication')

    def button_request_click(self):
        main_dic = get_dic_with_flag(DATA_FLAG, self.data_text_edit.toPlainText())
        send_encrypt_json(self.sock, self.encoder_rc4, main_dic)

        result = decode_read_by_connect(self.decoder_rc4, self.sock)
        self.data_text_edit.setText(result[DATA])
        print(result[DATA])


        print('req')


if __name__ == '__main__':
    app = p_widget.QApplication(sys.argv)
    ex = widget()
    sys.exit(app.exec_())
