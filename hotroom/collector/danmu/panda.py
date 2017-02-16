#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-16 08:45:00
# @Author  : eclipse_sv (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

from requests import Session
from bs4 import BeautifulSoup
from datetime import datetime
from collector.db.db import DB
from collector.danmu.danmuConfig import headers


PANDA_CATALOG = 'http://www.panda.tv/cate'
PANDA_ROOM = 'http://www.panda.tv/ajax_sort?token=&pageno={}&pagenum=120&classification={}'
PANDA_SPIDER = 'http://www.panda.tv/ajax_sort?token=&pageno=1&pagenum=120&classification={}'
PAND_HOST = 'http://www.panda.tv/'

session = Session()


def get_catalog_db():
    db = DB()
    db.switch_db("Pandata")
    db.switch_col("Catalog")
    return db


def get_room_db():
    db = DB()
    db.switch_db("Pandata")
    db.switch_col("Roominfo")
    return db


def save_catalog_info():
    with session as s:
        cate_page = s.get(PANDA_CATALOG, headers=headers)
    if cate_page:
        cate_soup = BeautifulSoup(cate_page.content, "lxml")
        cate_lis = cate_soup.select('.video-list-item')
        if cate_lis:
            data = list()
            for li in cate_lis:
                a = li.select('a')[0]
                href = a["href"]
                if "http://" in href:
                    continue
                catelog = href.split('/')[-1]
                href = PAND_HOST + href
                img = li.select('img')[0]
                imgsrc = img['src']
                desc = img['alt']
                liinfo = {
                    'catelog': catelog,
                    'href': href,
                    'img': imgsrc,
                    'desc': desc,
                    'date': datetime.now()
                }
                data.append(liinfo)
            if data:
                get_catalog_db().save_many(data)
        else:
            print("no data received")


def get_catalogs():
    db = get_catalog_db()
    data = db.get_all()
    if data:
        return [item['catelog'] for item in data]
    return None


def get_room_urls():
    catalogs = get_catalogs()
    if not catalogs:
        save_catalog_info()
        catalogs = get_catalogs()
    result = list()
    for item in catalogs:
        catalog = item
        spider = session.get(PANDA_SPIDER.format(
            catalog), headers=headers).json()
        count = int(spider['data']['total'])
        pagenum = count / 120 + 2
        for num in xrange(1, pagenum):
            result.append(PANDA_ROOM.format(num, catalog))
    return result


def save_room_info(url):
    if url:
        print('searching data for {}'.format(url))
        room_info = session.get(url, headers=headers)
        room_info = room_info.json()
        if room_info["data"] is not None:
            result = list()
            items = room_info['data'].get('items')
            if items:
                for item in items:
                    value = {
                        'roomid': item['id'],
                        'title': item['name'],
                        'audience': int(item['person_num']),
                        'url': PAND_HOST + item['id'],
                        'img': item['pictures']['img'],
                        "date": datetime.now(),
                        "catalog": item['classification']['cname'],
                        "host": item['userinfo']['nickName']
                    }
                    result.append(value)
                get_room_db().save_many(result)
                print('{} room data saved'.format(url))
