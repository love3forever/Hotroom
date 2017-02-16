#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-16 09:32:20
# @Author  : eclipse_sv (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

from collector.danmu.panda import save_catalog_info,get_room_urls,save_room_info

if __name__ == "__main__":
    urls = get_room_urls()
    for url in urls:
    	save_room_info(url)
