#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-16 15:17:47
# @Author  : eclipse_sv (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$
from douyu_app import app
from collector.danmu.CDouyu import Douyu


@app.task
def SAVE_DOUYU_DATA():
    douyu = Douyu()
    douyu.getRoomInfos()
