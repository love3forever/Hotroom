#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-16 15:17:47
# @Author  : eclipse_sv (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$
from douyu_app import app
from collector.basicinfo.CDouyu import Douyu


@app.task
def save_douyu_data():
    douyu = Douyu()
    douyu.get_room_infos()
