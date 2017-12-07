#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-22 17:42:49
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$
import time
from BaseDanmu import BaseDanmu
from datetime import datetime


class Panda(BaseDanmu):
    """docstring for Panda"""
    PANDA_CATALOG = 'http://www.panda.tv/cate'
    PANDA_ROOM = 'http://www.panda.tv/ajax_sort?token=&pageno={}&pagenum=120&classification={}'
    PANDA_SPIDER = 'http://www.panda.tv/ajax_sort?token=&pageno=1&pagenum=120&classification={}'
    PAND_HOST = 'http://www.panda.tv'

    def __init__(self, mhost='localhost', mport=27017):
        super(Panda, self).__init__(mhost=mhost, mport=mport)
        self._db = self._mongocli['Pandata']
        self._cataCol = self._mongocli['Pandata']['Catalog']
        self._roomCol = self._mongocli['Pandata']['Roominfo']

    def get_catalogs(self):
        with self.session as s:
            cate_page = s.get(Panda.PANDA_CATALOG, headers=self.headers)
        if cate_page:
            cate_soup = self.soup(cate_page.content, "lxml")
            cate_lis = cate_soup.select('.video-list-item')
            if cate_lis:
                data = list()
                for li in cate_lis:
                    a = li.select('a')[0]
                    href = a["href"]
                    if "http://" in href or '?' in href:
                        continue
                    catelog = href.split('/')[-1]
                    href = Panda.PAND_HOST + href
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
                    self._cataCol.drop()
                    self._cataCol.insert_many(data)
            else:
                print("no data received")

    def get_catalog_urls(self):
        all_catalogs = self._cataCol.find()
        catalogs = [item['catelog'] for item in all_catalogs]
        urls = list()
        for href in catalogs:
            catalog = href
            spider = dict()
            with self.session as s:
                try:
                    spider = s.get(Panda.PANDA_SPIDER.format(
                        catalog), headers=self.headers).json()
                    time.sleep(0.2)
                except Exception as e:
                    self.logger.error(str(e))

            count = int(spider['data']['total'])
            pagenum = count / 120 + 2
            for num in xrange(1, pagenum):
                urls.append(Panda.PANDA_ROOM.format(num, catalog))
        return urls

    def get_room_infos(self):
        self.get_catalogs()
        catalog_urls = self.get_catalog_urls()
        map(self.save_panda_rooms, catalog_urls)
        return 0

    def save_panda_rooms(self, url):
        if url:
            self.logger.info('searching data for {}'.format(url))
            room_info = None
            with self.session as s:
                try:
                    room_info = s.get(url, headers=self.headers,
                                      stream=True, timeout=5)
                    time.sleep(0.01)
                except Exception as e:
                    self.logger.error(str(e))

            room_info = room_info.json()
            if room_info["data"] is not None:
                result = list()
                items = room_info['data'].get('items')
                if items:
                    for item in items:
                        try:
                            value = {
                                'roomid': item['id'],
                                'title': item['name'],
                                'audience': int(item['person_num']),
                                'url': Panda.PAND_HOST + item['id'],
                                'img': item['pictures']['img'],
                                "date": datetime.now(),
                                "uid": datetime.now().strftime("%Y-%m-%d %H"),
                                "catalog": item['classification']['cname'],
                                "host": item['userinfo']['nickName']
                            }
                            result.append(value)
                        except Exception as e:
                            print(item['person_num'])
                            self.logger.error('Erro accure :{}'.format(str(e)))
                self.logger.info('{} records inserting into pandata with url:{}'.format(
                    len(result), url))
                if result:
                    self._roomCol.insert_many(result)
