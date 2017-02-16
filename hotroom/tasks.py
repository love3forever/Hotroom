#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-16 15:17:47
# @Author  : eclipse_sv (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$
from celeryApp import app
from collector.danmu.douyu import parase_room_info, all_rooms
from collector.danmu.panda import get_room_urls, save_room_info


@app.task
def SAVE_DOUYU_ROOM_DELAY(url):
    parase_room_info(url)


@app.task
def SAVE_PANDA_ROOM_DELAY(url):
    save_room_info(url)


@app.task
def SAVE_DOUYU_INFO():
    for item in all_rooms():
        SAVE_DOUYU_ROOM_DELAY.delay(item)


@app.task
def SAVE_PANDA_INFO():
    for item in get_room_urls():
        SAVE_PANDA_ROOM_DELAY.delay(item)
