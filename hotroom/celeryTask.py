#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-15 20:53:02
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

# celery -A celeryTask worker  --loglevel=info

from celery import Celery
from collector.danmu.douyu import get_douyu_catalog, get_room_info, all_rooms, save_room_info


broker = 'redis://127.0.0.1:6379/5'
backend = 'redis://127.0.0.1:6379/6'


app = Celery('celeryTask', broker=broker, backend=backend)


@app.task
def getCatalogInfo():
    get_douyu_catalog()
    return "catalog info saved"


@app.task
def getRoomInfo():
    get_room_info()
    return "room info"


@app.task
def saveRoomInfo(url):
    save_room_info(url)
