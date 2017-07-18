#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-13 13:41:53
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

from flask import Blueprint
from flask_restful import Api, abort

from douyu_api_abc import Douyu_Api

bp_douyu_streamer = Blueprint(
    'douyu_streamers', __name__, url_prefix='/api/v1/douyu')
api_douyu_streamer = Api(bp_douyu_streamer)


@api_douyu_streamer.resource('/streamers')
class Douyu_streamers(Douyu_Api):
    """docstring for Douyu_streamers"""

    def __init__(self, host='localhost', port=27017):
        super(Douyu_streamers, self).__init__()
        self.logger.info('{} inited'.format(__name__))

    def get(self):
        '''
        获取斗鱼全部主播基本信息
        '''
        pipline = []
        pipline.append(
            {
                "$group": {
                    "_id": "$host",
                    "catalogs": {
                        "$addToSet": "$catalog"
                    },
                    "count": {
                        "$sum": 1
                    },
                    "roomid": {
                        "$first": "$roomid"
                    }
                }
            })
        pipline.append(
            {
                "$project": {
                    "_id": 0,
                    "count": 1,
                    "streamer": "$_id",
                    'catalogs': "$catalogs",
                    'roomid': '$roomid'
                }
            })
        try:
            streamer_data = self._col.aggregate(pipline)
        except Exception as e:
            self.logger.error(str(e))
            return abort(503)
        else:
            return_data = {
                'streamers': list(streamer_data)
            }
            return self.wrapper_response(return_data)
