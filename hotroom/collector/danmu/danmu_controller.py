#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017/12/7
# @Author  : wangmengcn
# @Email   : eclipse_sv@163.com
from time import sleep
from threading import Thread

import redis

from danmu_factory import DouyuDM

rooms = ['67373', '71017', '85981']
r = redis.StrictRedis()


def create_danmu_pool():
    newroom_pubsub = r.pubsub()
    newroom_pubsub.subscribe('danmu:createroom')
    delroom_pubsub = r.pubsub()
    delroom_pubsub.subscribe('danmu:destoryroom')
    danmu_pool = dict()
    while True:
        sleep(3)
        create_room_msg = newroom_pubsub.get_message()
        create_room_id = create_room_msg.setdefault('data', None) if create_room_msg else None
        if create_room_id:
            if not danmu_pool.get(create_room_id, None):
                print('新建room:{}'.format(create_room_id))
                danmu = DouyuDM(create_room_id)
                danmu.connect_to_server()
                danmu_thread = Thread(target=danmu.print_danmu)
                danmu_thread.start()
                danmu_pool.setdefault(create_room_id, danmu)
            else:
                print('room:{} 已建立'.format(create_room_id))

        destory_room_msg = delroom_pubsub.get_message()
        destory_room_id = destory_room_msg.setdefault('data', None) if destory_room_msg else None
        if destory_room_id:
            print('销毁room:{}'.format(destory_room_id))
            destory_room = danmu_pool.get(destory_room_id, None)
            if destory_room:
                destory_room.terminate()
                del danmu_pool[destory_room_id]
                print('room:{} 已销毁'.format(destory_room_id))


if __name__ == '__main__':
    create_danmu_pool()
