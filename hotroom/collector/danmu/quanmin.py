#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-17 14:51:20
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$
from datetime import datetime
from requests import Session
from collector.db.db import DB
from collector.danmu.danmuConfig import headers

QUANMIN_CATALOG = 'http://www.quanmin.tv/json/categories/list.json'
QUANMIN_ROOM = 'http://www.quanmin.tv/json/categories/{}/list_{}.json'
QUANMIN_TEST = 'http://www.quanmin.tv/json/categories/{}/list.json'
QUANMIN_HOST = 'http://www.quanmin.tv/{}'

session = Session()


def get_qm_catalogs():
    '''
    通过QUANMIN_CATALOG获取所有的分类页面
    '''
    with session as s:
        qm_catalogs = s.get(QUANMIN_CATALOG, headers=headers)
    if qm_catalogs:
        result = list()
        qm_catalogs = qm_catalogs.json()
        for item in qm_catalogs:
            data = dict()
            data['date'] = datetime.now()
            data['catalog'] = item['name']
            data['href'] = item['slug']
            result.append(data)
    db = DB()
    db.switch_db('Quanmin')
    db.switch_col('Catalog')
    db.save_many(result)


def generate_qm_room_urls():
    '''
    获取所有可用的获取房间新的的url
    '''
    db = DB()
    db.switch_db('Quanmin')
    db.switch_col('Catalog')
    catalogs = db.get_all()
    if catalogs.count() == 0:
        get_qm_catalogs()
        catalogs = db.get_all()
    room_urls = list()
    for catalog in catalogs:
        url = QUANMIN_TEST.format(catalog['href'])
        with session as s:
            test_data = s.get(url, headers=headers).json()
        if len(test_data) != 0:
            if test_data['pageCount'] != 1:
                for x in xrange(1, test_data['pageCount']):
                    room_urls.append(QUANMIN_ROOM.format(catalog['href'], x))
            room_urls.append(url)
    return room_urls


def save_qm_roominfo(url):
    with session as s:
        room_info = s.get(url, headers=headers).json()
    if len(room_info):
        result = list()
        datas = room_info['data']
        for item in datas:
            data = dict()
            data['img'] = item['thumb']
            data['title'] = item['title']
            data['url'] = QUANMIN_HOST.format(item['no'])
            data['audience'] = int(item['view'])
            data['date'] = datetime.now()
            data['catalog'] = item['category_name']
            data['host'] = item['nick']
            data['roomid'] = item['no']
            result.append(data)
        db = DB()
        db.switch_db('Quanmin')
        db.switch_col('Roominfo')
        db.save_many(result)
