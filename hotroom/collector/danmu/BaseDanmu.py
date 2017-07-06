#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-22 13:59:02
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from danmuConfig import headers
from bs4 import BeautifulSoup
from requests import Session
from abc import ABCMeta, abstractmethod


class BaseDanmu():
    """docstring for BaseDanmu"""
    __metaclass__ = ABCMeta

    def __init__(self, mhost='localhost', mport=27017):
        self._mongocli = MongoClient(host=mhost, port=mport, connect=False)
        # 如果数据库启用了密码验证，将此段代码放开进行验证
        # try:
        #     name = os.getenv('mongo_name')
        #     pasw = os.getenv('mongo_pswd')
        #     authdb = self._mongocli['admin']
        #     authdb.authenticate(name=name, password=pasw)
        # except PyMongoError as e:
        #     print("Erro accured during db authenticate:{}".format(str(e)))
        self.session = Session()
        self.soup = BeautifulSoup
        self.headers = headers

    @abstractmethod
    def getCatalogs(self):
        pass

    @abstractmethod
    def getRoomInfos(self):
        pass

    @abstractmethod
    def getCatalogURLs(self):
        pass
