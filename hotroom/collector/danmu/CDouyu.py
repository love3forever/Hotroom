#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-22 14:21:01
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$
import time
from BaseDanmu import BaseDanmu
from datetime import datetime
from multiprocessing.dummy import Pool


class Douyu(BaseDanmu):
    """docstring for Douyu"""

    def __init__(self, mhost='localhost', mport=27017):
        super(Douyu, self).__init__(mhost=mhost, mport=mport)
        self._db = self._mongocli['Douyudata']
        self._cataCol = self._db['Catalog']
        self._roomCol = self._db['Roominfo']
        self.DOUYU_HTTPS_HOST = 'https://www.douyu.com'
        self.DOUYU_HTTP_HOST = 'http://www.douyu.com'
        self.DOUYU_CATALOG = 'https://www.douyu.com/directory'

    def getCatalogs(self):
        with self.session as s:
            origin_content = s.get(
                self.DOUYU_CATALOG, headers=self.headers, stream=True, timeout=5)
        if origin_content:
            origin_content = origin_content.content
        soup = self.soup(origin_content, 'lxml')
        box = soup.select("#live-list-contentbox > li")
        self._cataCol.drop()
        if box:
            catalogs = Douyu.parseCatalogContent(box)
            self._cataCol.insert_many(catalogs)

    @staticmethod
    def parseCatalogContent(box):
        '''
        将parseCatalogContent的返回值从list改为生成器，减少内存开销
        '''
        for catalog in box:
            try:
                a = catalog.select("a")
                p = catalog.select("a > p")
                info = dict()
                info["href"] = 'https://www.douyu.com{}'.format(a[0]["href"])
                info["catalog"] = p[0].string
                info["date"] = datetime.now()
                yield info
            except Exception as e:
                print("Error accurs when parsing html for\
                 catalogs: {}".format(e))
                yield None

    @staticmethod
    def convertAudience(audience):
        if audience:
            value = 0
            if u"万" in audience:
                number = list(audience)
                number.pop()
                if "." in number:
                    value = int(float(''.join(number)) * 10000)
                else:
                    value = int(''.join(number)) * 10000
            else:
                value = int(audience)
            return value

    def getRoomInfos(self):
        self.getCatalogs()
        catalogURLs = self.getCatalogURLs()
        if not catalogURLs:
            return
        roomContents = map(self.paraseDouyuRoomInfo, catalogURLs)
        roomContents = filter(lambda x: len(x) != 0, roomContents)
        pool = Pool()
        pool.map(lambda x: self._roomCol.insert_many(x), roomContents)
        return 0

    def paraseDouyuRoomInfo(self, catalog_url):
        if catalog_url:
            flag = list()
            result = list()
            is_exits = False
            for x in xrange(1, 50):
                if is_exits:
                    break
                room_url = catalog_url + "?page={}&isAjax=1".format(x)
                print("current page:{}".format(room_url))
                with self.session as s:
                    room_page = s.get(
                        room_url, headers=self.headers, timeout=5, stream=True)
                    time.sleep(0.02)
                room_content = room_page.content
                room_soup = self.soup(room_content, 'lxml')
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
                    host = item.find_all(
                        attrs={"class": "dy-name ellipsis fl"})[0]
                    audience = item.find_all(attrs={"class": "dy-num fr"})[0]
                    room_data["catalog"] = catalog.string
                    room_data["host"] = host.string
                    room_data["audience"] = Douyu.convertAudience(
                        audience.string)
                    room_data["url"] = item["data-rid"]
                    room_data["date"] = datetime.now()
                    result.append(room_data)
                    flag.append(item["data-rid"])

            # 以list的形式返回roominfo
            return result

    def getCatalogURLs(self):
        if self._cataCol:
            catalogCursor = self._cataCol.find()
            if catalogCursor.count() != 0:
                return [item["href"] for item in catalogCursor]
            else:
                return None
