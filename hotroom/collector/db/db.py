#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-14 19:16:06
# @Author  : eclipse_sv (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

from pymongo import MongoClient


class DB(object):
    """docstring for DB"""

    def __init__(self, host='localhost', port=27017):
        self.cli = MongoClient(host=host, port=port)

    def switch_db(self, database):
        if database and isinstance(database, str):
            self.db = self.cli[database]

    def switch_col(self, col):
        if col and isinstance(col, str):
            self.col = self.db[col]

    def save(self, data):
        if self.col:
            self.col.insert_one(data)

    def save_many(self,data):
        if self.col:
            self.col.insert_many(data)

    def get_all(self):
        if self.col:
            return self.col.find()
