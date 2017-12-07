#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-22 18:18:44
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$
import time
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

    def get_catalogs(self):
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

    def get_room_infos(self):
        self.get_catalogs()
        catalog_urls = self.get_catalog_urls()
        if catalog_urls:
            map(self.save_room_info, catalog_urls)
            return 0

    def save_room_info(self, url):
        self.logger.info('saving data of page:{}'.format(url))
        room_data = None
        with self.session as s:
            try:
                room_data = s.get(url, headers=self.headers,
                                  stream=True, timeout=5)
                time.sleep(0.2)
            except Exception as e:
                self.logger.error(str(e))

        if room_data:
            room_info = room_data.json()
            result = list()
            datas = room_info['data']
            for item in datas:
                data = dict()
                data['img'] = item['thumb']
                data['title'] = item['title']
                data['url'] = Quanmin.QUANMIN_HOST.format(item['no'])
                data['audience'] = int(item['view'])
                data['date'] = datetime.now()
                data['uid'] = data['date'].strftime("%Y-%m-%d %H")
                data['catalog'] = item['category_name']
                data['host'] = item['nick']
                data['roomid'] = item['no']
                result.append(data)
            if result:
                self.logger.info(
                    'Inserting {} quanmin data'.format(len(result)))
                self._roomCol.insert_many(result)

    def get_catalog_urls(self):
        catalogs = self._cataCol.find()
        room_urls = list()
        for catalog in catalogs:
            url = Quanmin.QUANMIN_TEST.format(catalog['href'])
            with self.session as s:
                test_data = s.get(url, headers=self.headers).json()
            if len(test_data) != 0:
                if test_data['pageCount'] != 1:
                    for x in xrange(2, test_data['pageCount'] + 1):
                        room_urls.append(
                            Quanmin.QUANMIN_ROOM.format(catalog['href'], x))
                room_urls.append(url)
        return room_urls
