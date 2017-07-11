#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-11 11:37:24
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$
from douyu_api_abc import Douyu_Api
from flask import Blueprint
from flask_restful import Api, abort
from pymongo import DESCENDING, ASCENDING

bp_douyu_game = Blueprint('douyu_games_api', __name__,
                          url_prefix='/api/v1/douyu')
api_douyu_game = Api(bp_douyu_game)


@api_douyu_game.resource('/games')
class Douyu_games(Douyu_Api):
    """获取斗鱼曾经直播过的所有游戏类型"""

    def __init__(self, host='localhost', port=27017):
        super(Douyu_games, self).__init__()
        self.logger.info('{} inited'.format(__name__))

    def get(self):
        test_data = self._col.find({}, {'_id': 0}).sort(
            'date', DESCENDING).limit(5)
        return_data = {
            'recent_records': list(test_data)
        }
        return self.wrapper_response(return_data)
