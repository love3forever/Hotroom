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
        self._col = self._db['streamers_View']
        self.logger.info('{} inited'.format(__name__))

    def get(self):
        '''
        获取斗鱼全部主播基本信息
        '''
        try:
            streamer_data = self._col.find({}, {'_id': 0})
        except Exception as e:
            self.logger.error(str(e))
            abort(503)
        else:
            return_data = {
                'streamers': list(streamer_data)
            }
            return self.wrapper_response(return_data)


@api_douyu_streamer.resource('/streamer/<string:nameOrRoomid>')
class Douyu_streamer(Douyu_Api):
    """docstring for Douyu_streamer"""

    def __init__(self, host='localhost', port=27017):
        super(Douyu_streamer, self).__init__()
        self.logger.info('{} inited'.format(__name__))

    def get(self, nameOrRoomid):
        pipline = []
        # 通过nameOrRoomid进行筛选
        pipline.append(
            {
                "$match": {
                    "$or": [
                        {
                            "host": nameOrRoomid
                        },
                        {
                            "roomid": nameOrRoomid
                        }
                    ]
                }
            })
        # 将数据组织成为所需要的形式
        pipline.append(
            {
                "$project": {
                    "host": "$host",
                    "roomid": "$roomid",
                    "catalog": "$catalog",
                    "audience": "$audience",
                    "title": "$title",
                    "date": "$date",
                    "hourOfDay": {
                        "$hour": "$date"
                    },
                    "dayOfWeek": {
                        "$dayOfWeek": "$date"
                    }
                }
            })
        # 将多个数据融合成为一个
        pipline.append(
            {
                "$group": {
                    "_id": 'null',
                    "host": {
                        "$first": "$host"
                    },
                    "roomid": {
                        "$first": "$roomid"
                    },
                    "catalog": {
                        "$addToSet": "$catalog"
                    },
                    "avgAudience": {
                        "$avg": "$audience"
                    },
                    "title": {
                        "$addToSet": "$title"
                    },
                    "hourOfDay": {
                        "$push": "$hourOfDay"
                    },
                    "dayOfWeek": {
                        "$push": "$dayOfWeek"
                    },
                    "earliest": {
                        "$min": "$date"
                    },
                    "latest": {
                        "$max": "$date"
                    }
                }
            })
        # 数据转为最终需要的格式
        pipline.append(
            {
                "$project": {
                    "_id": 0,
                    "host": 1,
                    "roomid": 1,
                    "catalog": 1,
                    "avgAudience": {
                        "$ceil": "$avgAudience"
                    },
                    "title": 1,
                    "hourOfDay": 1,
                    "dayOfWeek": 1,
                    "earliest": 1,
                    "latest": 1
                }
            })
        try:
            streamer_data = self._col.aggregate(pipline)
        except Exception as e:
            self.logger.error(str(e))
            abort(503)
        else:
            return self.wrapper_response(list(streamer_data)[0])
