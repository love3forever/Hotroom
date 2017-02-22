#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-22 18:18:44
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

from BaseDanmu import BaseDanmu
from datetime import datetime


class Quanmin(BaseDanmu):
    """docstring for Quanmin"""
    QUANMIN_CATALOG = 'http://www.quanmin.tv/json/categories/list.json'
    QUANMIN_ROOM = 'http://www.quanmin.tv/json/categories/{}/list_{}.json'
    QUANMIN_TEST = 'http://www.quanmin.tv/json/categories/{}/list.json'
    QUANMIN_HOST = 'http://www.quanmin.tv/{}'

    def __init__(self, mhost='localhost', mport=27017):
        super(Quanmin, self).__init__(mhost=mhost, mport=mport)
        self._db = self._mongocli['Quanmin']
        self._cataCol = self._db['Catalog']
        self._roomCol = self._db['Roominfo']

    def getCatalogs(self):
        with self.session as s:
            qm_catalogs = s.get(Quanmin.QUANMIN_CATALOG, headers=self.headers)
        if qm_catalogs:
            result = list()
            qm_catalogs = qm_catalogs.json()
            for item in qm_catalogs:
                data = dict()
                data['date'] = datetime.now()
                data['catalog'] = item['name']
                data['href'] = item['slug']
                result.append(data)
        self._cataCol.drop()
        self._cataCol.insert_many(result)

    def getRoomInfos(self):
        catalogURLs = self.getCatalogURLs()
        if catalogURLs:
            map(self.saveRoomInfo, catalogURLs)

    def saveRoomInfo(self, url):
        self.getCatalogs()
        print('saving data of page:{}'.format(url))
        with self.session as s:
            room_info = s.get(url, headers=self.headers).json()
        if len(room_info):
            result = list()
            datas = room_info['data']
            for item in datas:
                data = dict()
                data['img'] = item['thumb']
                data['title'] = item['title']
                data['url'] = Quanmin.QUANMIN_HOST.format(item['no'])
                data['audience'] = int(item['view'])
                data['date'] = datetime.now()
                data['catalog'] = item['category_name']
                data['host'] = item['nick']
                data['roomid'] = item['no']
                result.append(data)
            if result:
                self._roomCol.insert_many(result)

    def getCatalogURLs(self):
        catalogs = self._cataCol.find()
        room_urls = list()
        for catalog in catalogs:
            url = Quanmin.QUANMIN_TEST.format(catalog['href'])
            with self.session as s:
                test_data = s.get(url, headers=self.headers).json()
            if len(test_data) != 0:
                if test_data['pageCount'] != 1:
                    for x in xrange(1, test_data['pageCount']):
                        room_urls.append(
                            Quanmin.QUANMIN_ROOM.format(catalog['href'], x))
                room_urls.append(url)
        return room_urls
