#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-16 15:17:47
# @Author  : eclipse_sv (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$
from celeryApp import app
from collector.danmu.CDouyu import Douyu
from collector.danmu.CPanda import Panda
from collector.danmu.CQuanmin import Quanmin


douyu = Douyu()
panda = Panda()
quanmin = Quanmin()


@app.task
def SAVE_DOUYU_DATA():
    douyu.getRoomInfos()


@app.task
def SAVE_PANDA_DATA():
    panda.getRoomInfos()


@app.task
def SAVE_QUANMIN_DATA():
    quanmin.getRoomInfos()
