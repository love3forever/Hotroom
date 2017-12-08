#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017/12/7
# @Author  : wangmengcn
# @Email   : eclipse_sv@163.com
import socket
import re
from time import time, sleep
from datetime import datetime
from threading import Thread
from json import dumps
from . import r


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
        self.msg_types = ['@=chatmsg', '@=onlinegift', '@=dgb',
                          '@=uenter', '@=bc_buy_deserve', '@=ssd',
                          '@=spbc', '@=ggbb']
        self.convert_function_map = {
            '@=chatmsg': self.convert_chatmsg,
            '@=onlinegift': self.convert_onlinegift,
            '@=dgb': self.convert_dgb,
            '@=uenter': self.convert_uenter,
            '@=bc_buy_deserve': self.convert_bc_buy_deserve,
            '@=ssd': self.convert_ssd,
            '@=spbc': self.convert_spbc,
            '@=ggbb': self.convert_ggbb
        }

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

    def print_danmu(self):
        msgs = self.send_and_get_msg()
        for msg in msgs:
            self.convert_danmu(msg)

    def publish_danmu(self):
        danmu_channel = 'channel:{}'.format(self.room_id)
        msgs = self.send_and_get_msg()
        for msg in msgs:
            danmu_info = dumps(self.convert_danmu(msg))
            if danmu_info:
                r.publish(danmu_channel, danmu_info)

    def terminate(self):
        self.is_terminated = True

    def send_and_get_msg(self):
        if self.is_connected:
            # 发送登陆信息并加入指定弹幕频道
            self.socket.sendall(self.transform_msg(self.LOGIN_INFO))
            self.socket.sendall(self.transform_msg(self.JION_GROUP))
            keep_aliver = self.keep_connect_alive()
            next(keep_aliver)
            loop_begin = datetime.now()
            while not self.is_terminated:
                now = time()
                sleep(0.1)
                # 更新keepalive
                running_time = datetime.now()
                if (running_time - loop_begin).seconds > 40:
                    keep_alive_info = self.KEEP_ALIVE.format(now)
                    keep_alive_info = self.transform_msg(keep_alive_info)
                    self.is_terminated = keep_aliver.send(keep_alive_info)
                    loop_begin = datetime.now()
                try:
                    danmu_msg = self.socket.recv(1000)
                except socket.error as e:
                    print(str(e))
                else:
                    yield danmu_msg

    def keep_connect_alive(self):
        while self.is_connected:
            keep_alive_info = yield False
            if keep_alive_info:
                try:
                    self.socket.sendall(keep_alive_info)
                except socket.error as e:
                    print('error in keepalive:' + str(e))
            print('*' * 10 + 'keepalive' + '*' * 10)
            sleep(1)

    def convert_danmu(self, danmu_msg):
        for flag in self.msg_types:
            if flag in danmu_msg:
                return self.convert_function_map.get(flag)(danmu_msg)

    def convert_chatmsg(self, chat_msg):
        # 转换普通聊天信息
        chat_dict = dict()
        user_name = re.search("\/nn@=(.+?)\/", chat_msg)
        if user_name:
            chat_dict.setdefault('username', user_name.group(1))
        chat_content = re.search("\/txt@=(.+?)\/", chat_msg)
        if chat_content:
            chat_dict.setdefault('chatcontent', chat_content.group(1))
        user_level = re.search("\/level@=(.+?)\/", chat_msg)
        if user_level:
            chat_dict.setdefault('userlevel', user_level.group(1))
        chat_date = datetime.now()
        chat_dict.setdefault('date', chat_date.isoformat(' '))
        for k, v in chat_dict.items():
            print('{} >>> {}:{}'.format(self.room_id, k, v))
        return chat_dict

    def convert_onlinegift(self, onlinegift):
        # 转换在线礼物信息
        onlinegift_dict = dict()
        username = re.search("\/nn@=(.+?)\/", onlinegift)
        if username:
            onlinegift_dict.setdefault('username', username.group(1))
        sil = re.search("\/sil@=(.+?)\/", onlinegift)
        if sil:
            onlinegift_dict.setdefault('sil', sil.group(1))
        print('{} >>user:{} 获得鱼丸{}个'.format(self.room_id, username, sil))
        return onlinegift_dict

    def convert_dgb(self, dgb):
        # 转换赠送礼物信息
        pass

    def convert_uenter(self, uenter):
        # 转换用户进入直播间信息
        uenter_dict = dict()
        username = re.search("\/nn@=(.+?)\/", uenter)
        if username:
            uenter_dict.setdefault('username', username.group(1))
        print('{} >>>欢迎:{} 进入直播间'.format(self.room_id, uenter_dict.setdefault('username', None)))
        return uenter_dict

    def convert_bc_buy_deserve(self, bc_buy_deserve):
        # 转换酬勤赠送信息
        return None

    def convert_ssd(self, ssd):
        # 转换超级弹幕信息
        return None

    def convert_spbc(self, spbc):
        # 转换房间内赠送礼物信息
        spbc_dict = dict()
        sender_name = re.search("\/sn@=(.+?)\/", spbc)
        if sender_name:
            spbc_dict.setdefault('sender_name', sender_name.group(1))
        reciver_name = re.search("\/dn@=(.+?)\/", spbc)
        if reciver_name:
            spbc_dict.setdefault('reciver_name', reciver_name.group(1))
        gift_num = re.search("\/gc@=(.+?)\/", spbc)
        if gift_num:
            spbc_dict.setdefault('gift_num', gift_num.group(1))
        gift_name = re.search("\/gn@=(.+?)\/", spbc)
        if gift_name:
            spbc_dict.setdefault('gift_name', gift_name.group(1))
        print('{} >>> {}赠送给{} {}个{}'.format(self.room_id, spbc_dict.get('sender_name', None),
                                            spbc_dict.get('reciver_name', None),
                                            spbc_dict.get('gift_num', None),
                                            spbc_dict.get('gift_name', None)))
        return spbc_dict

    def convert_ggbb(self, ggbb):
        # 转换房间用户抢红包信息
        return None


if __name__ == '__main__':
    rooms = ['67373', '71017']
    danmu_client = []
    for room in rooms:
        danmu = DouyuDM(room)
        danmu_client.append(danmu)
        danmu.connect_to_server()
        danmu_thread = Thread(target=danmu.print_danmu)
        danmu_thread.start()
