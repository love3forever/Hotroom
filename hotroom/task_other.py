#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-07 17:14:53
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

from celeryApp import app
from collector.danmu.CPanda import Panda
from collector.danmu.CQuanmin import Quanmin


@app.task
def SAVE_PANDA_DATA():
    panda = Panda()
    panda.getRoomInfos()


@app.task
def SAVE_QUANMIN_DATA():
    quanmin = Quanmin()
    quanmin.getRoomInfos()
