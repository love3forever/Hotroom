#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-14 19:59:08
# @Author  : eclipse_sv (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$
from datetime import datetime
from collector.danmu.douyu import get_douyu_catalog, get_room_info,get_room_db,get_catalog_db

if __name__ == "__main__":
    start = datetime.now()
    get_douyu_catalog()
    get_room_info()
    end = datetime.now()
    print("costs time {}".format((end - start).seconds))
