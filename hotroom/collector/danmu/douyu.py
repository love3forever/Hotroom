#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-14 16:43:10
# @Author  : eclipse_sv (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

# build communication with douyu danmu server

from requests import Session
from bs4 import BeautifulSoup
from datetime import datetime
from collector.db.db import DB
from collector.danmu.danmuConfig import headers, convert_audience

DOUYU_HOST = 'https://www.douyu.com'
DOUYU_CATALOG = 'https://www.douyu.com/directory'

session = Session()


def get_douyu_catalog():
    with session as s:
        origin_content = s.get(DOUYU_CATALOG, headers=headers)
    if origin_content:
        origin_content = origin_content.content
        soup = BeautifulSoup(origin_content, 'lxml')
        box = soup.select("#live-list-contentbox > li")
        map(get_catalog_info, box)


def get_catalog_info(catalog):
    if catalog:
        a = catalog.select("a")
        p = catalog.select("a > p")
        info = dict()
        info["href"] = DOUYU_HOST + a[0]["href"]
        info["catalog"] = p[0].string
        info["date"] = datetime.now()
        db = get_catalog_db()
        db.save(info)


def get_catalog_db():
    db = DB()
    db.switch_db("Douyudata")
    db.switch_col("Catalog")
    return db


def get_room_db():
    db = DB()
    db.switch_db("Douyudata")
    db.switch_col("Roominfo")
    return db


def get_room_info():
    db = get_catalog_db()
    catalog = db.get_all()
    if catalog:
        for item in catalog:
            save_room_info(item["href"])


def all_rooms():
    db = get_catalog_db()
    catalog = db.get_all()
    if not catalog:
        get_douyu_catalog()
        catalog = db.get_all()
    return [item["href"] for item in catalog]


def save_room_info():
    '''
    # main()
    '''
    catalog_urls = all_rooms()
    if catalog_urls:
        map(parase_room_info, catalog_urls)


def parase_room_info(catalog_url):
    if catalog_url:
        flag = list()
        result = list()
        is_exits = False
        for x in xrange(1, 50):
            if is_exits:
                break
            room_url = catalog_url + "?page={}&isAjax=1".format(x)
            print("current page:{}".format(room_url))
            with session as s:
                room_page = s.get(room_url, headers=headers)
            room_content = room_page.content
            room_soup = BeautifulSoup(room_content, 'lxml')
            rooms = room_soup.select("li")
            if not rooms:
                break
            for item in rooms:
                # 获取每个房间的信息
                room_data = dict()
                room_data["roomid"] = item["data-rid"]
                # 如果已经存在此room则跳出当前循环
                if item["data-rid"] in flag:
                    is_exits = True
                    break
                a = item.select("a")[0]
                img = item.select("img")[0]
                room_data["img"] = img["data-original"]
                room_data["title"] = a["title"]
                catalog = item.find_all(attrs={"class": "tag ellipsis"})[0]
                host = item.find_all(attrs={"class": "dy-name ellipsis fl"})[0]
                audience = item.find_all(attrs={"class": "dy-num fr"})[0]
                room_data["catalog"] = catalog.string
                room_data["host"] = host.string
                room_data["audience"] = convert_audience(audience.string)
                room_data["url"] = item["data-rid"]
                room_data["date"] = datetime.now()
                result.append(room_data)
                flag.append(item["data-rid"])

        # 将获取到的room信息存入数据库
        db = get_room_db()
        db.save_many(result)
