#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-11 10:46:56
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$
import logging

from pymongo import MongoClient
from flask_restful import Resource
from flask import jsonify, make_response


class Douyu_Api(Resource):
    """douyu相关api基类，初始化数据库连接，配置logging，提供response包装器"""

    def __init__(self, host='localhost', port=27017):
        super(Douyu_Api, self).__init__()
        # 创建logger
        self.logger = Douyu_logger().logger

        # 创建数据库连接
        self.host = host
        self.port = port
        try:
            self._mongo = Mongo_instance(self.host, self.port).mongo_instance
            self.logger.info('get mongo instance')
        except Exception as e:
            self.logger.error(str(e))
        else:
            # 第一次使用else搭配try使用
            self._db = self._mongo['Douyudata']
            self._col = self._db['Roominfo']

    def wrapper_response(self, response_data):
        try:
            response = make_response(jsonify(response_data))
        except Exception as e:
            self.logger.error(str(e))
        else:
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'POST'
            response.headers[
                'Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
            return response


def singleton(cls):
    instances = {}
    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


@singleton
class Mongo_instance(object):
    '''
    使用单例模式，避免重复创建数据库连接
    '''

    def __init__(self, host, port):
        logger = Douyu_logger().logger
        try:
            self.mongo_instance = MongoClient(host, port)
        except Exception as e:
            logger.error(str(e))
        else:
            logger.info('new mongo instance created')


@singleton
class Douyu_logger(object):
    """docstring for Douyu_logger"""

    def __init__(self):
        # 配置logging
        logger_name = __name__
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.ERROR)

        # create file handler
        log_path = "./douyu_api.log"
        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.DEBUG)

        # create formatter
        fmt = "%(asctime)-15s %(levelname)s %(filename)s\
        %(lineno)d %(process)d %(message)s"
        datefmt = "%a %d %b %Y %H:%M:%S"
        formatter = logging.Formatter(fmt, datefmt)

        # add handler and formatter to logger
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.info('Logger configuration completed')
