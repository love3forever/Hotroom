#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017/12/7
# @Author  : wangmengcn
# @Email   : eclipse_sv@163.com
from time import time, sleep
import socket


class DouyuDM:
    HOST = 'openbarrage.douyutv.com'
    PORT = 8601

    def __init__(self, room_id):
        self.room_id = room_id
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False
        self.LOGIN_INFO = "type@=loginreq/username@=qq_aPSMdfM5/password@=12345678/roomid@={}/".format(room_id)
        self.JION_GROUP = "type@=joingroup/rid@={}/gid@=-9999/".format(room_id)
        self.KEEP_ALIVE = "type@=keeplive/tick@={}/"
        self.is_terminated = False

    @staticmethod
    def transform_msg(content):
        length = bytearray([len(content) + 9, 0x00, 0x00, 0x00])
        code = length
        magic = bytearray([0xb1, 0x02, 0x00, 0x00])
        end = bytearray([0x00])
        trscont = bytes(content.encode('utf-8'))
        return bytes(length + code + magic + trscont + end)

    def connect_to_server(self):
        try:
            self.socket.connect((self.HOST, self.PORT))
        except socket.error as e:
            print(str(e))
        else:
            self.is_connected = True
            print('connected to danmu server')

    def send_and_get_msg(self):
        if self.is_connected:
            # 发送登陆信息并加入指定弹幕频道
            self.socket.sendall(self.transform_msg(self.LOGIN_INFO))
            self.socket.sendall(self.transform_msg(self.JION_GROUP))
            keep_aliver = self.keep_connect_alive()
            next(keep_aliver)
            keep_alive_flag = 0
            while not self.is_terminated:
                now = time()
                sleep(1)
                # 更新keepalive
                if keep_alive_flag % 30 == 0:
                    keep_alive_info = self.KEEP_ALIVE.format(now)
                    keep_alive_info = self.transform_msg(keep_alive_info)
                    self.is_terminated = keep_aliver.send(keep_alive_info)
                keep_alive_flag += 1
                try:
                    danmu_msg = self.socket.recv(4000)
                except socket.error as e:
                    print(str(e))
                else:
                    danmu_str = repr(danmu_msg)
                    yield danmu_str

    def keep_connect_alive(self):
        while self.is_connected:
            keep_alive_info = yield False
            if keep_alive_info:
                try:
                    self.socket.sendall(keep_alive_info)
                except socket.error as e:
                    print(str(e))
            print('*' * 10 + 'keepalive' + '*' * 10)
            sleep(1)


if __name__ == '__main__':
    danmu = DouyuDM('85981')
    danmu.connect_to_server()
    msgs = danmu.send_and_get_msg()
    for msg in msgs:
        print(msg)
