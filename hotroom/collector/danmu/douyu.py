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

DOUYU_HOST = 'http://www.douyu.com'
DOUYU_CATALOG = 'https://www.douyu.com/directory'

session = Session()


def get_douyu_catalog():
    with session as s:
        origin_content = s.get(DOUYU_CATALOG)
        start = datetime.now()
    if origin_content:
        origin_content = origin_content.content
        soup = BeautifulSoup(origin_content, 'lxml')
        box = soup.select("#live-list-contentbox > li")
        for item in box:
            get_catalog_info(item)
        end = datetime.now()
        print("costs time for {} seconds".format((end - start).seconds))


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
    db.switch_db("Douyu")
    db.switch_col("Catalog")
    return db


def get_room_info(catalog_url):
    if catalog_url:
        pass
        flag = []
        for x in xrange(50):
            room_url = catalogURL + "?page={}&isAjax=1".format(x)
            with session as s:
                room_page = s.get(roomURL)
            room_content = room_page.content
            room_soup = BeautifulSoup(room_content)
            rooms = room_soup.select("li")
            
