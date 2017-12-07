#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-22 13:59:02
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

import logging
from abc import ABCMeta, abstractmethod

from bs4 import BeautifulSoup
from pymongo import MongoClient
from requests import Session

from danmuConfig import headers


class BaseDanmu:
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
        # 配置logging
        logger_name = __name__
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.ERROR)

        # create file handler
        log_path = "./Data_collector_log.log"
        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.ERROR)

        # create formatter
        fmt = "%(asctime)-15s %(levelname)s %(filename)s\
         %(lineno)d %(process)d %(message)s"
        datefmt = "%a %d %b %Y %H:%M:%S"
        formatter = logging.Formatter(fmt, datefmt)

        # add handler and formatter to logger
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    @abstractmethod
    def get_catalogs(self):
        pass

    @abstractmethod
    def get_room_infos(self):
        pass

    @abstractmethod
    def get_catalog_urls(self):
        pass
