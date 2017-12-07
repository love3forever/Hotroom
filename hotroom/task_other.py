#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-07 17:14:53
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

from other_app import app
from collector.basicinfo.CPanda import Panda
from collector.basicinfo.CQuanmin import Quanmin


@app.task
def save_panda_data():
    panda = Panda()
    panda.get_room_infos()


@app.task
def save_quanmin_data():
    quanmin = Quanmin()
    quanmin.get_room_infos()
