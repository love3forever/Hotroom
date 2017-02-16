#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-14 19:59:08
# @Author  : eclipse_sv (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$
from datetime import datetime
from celery import group
from celeryTask import getCatalogInfo, saveRoomInfo
from collector.danmu.douyu import all_rooms
from collector.danmu.panda import save_catalog_info

if __name__ == "__main__":
    save_catalog_info()
