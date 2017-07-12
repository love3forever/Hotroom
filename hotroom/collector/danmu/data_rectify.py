#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-12 10:27:53
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$
import argparse

from pymongo import MongoClient
from datetime import datetime


def rectify(db_name):
    mongo = MongoClient()
    db = mongo[db_name]
    col = db['Roominfo']
    data_without_stamp = col.find({'uid': {'$eq': None}})
    print(data_without_stamp.count())
    for data in data_without_stamp:
        iso_time = data['date']
        host = data['host']
        rectify_date = iso_time.strftime("%Y-%m-%d %H")
        print(rectify_date)
        col.update_one({'host': host, 'date': iso_time},
                       {'$set': {'uid': rectify_date}})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', dest='db_name', type=str,
                        help='the database name')
    options = parser.parse_args()
    rectify(**vars(options))
