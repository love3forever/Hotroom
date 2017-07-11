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
from datetime import datetime, timedelta

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
        test_data = self._col.aggregate(
            [{'$group': {'_id': '$catalog', 'heat': {'$sum': 1}}}])
        self.logger.info('game catalog aggregation completed')
        sorted_catalog = sorted(test_data, key=lambda x: x[
                                'heat'], reverse=True)
        self.logger.info('game catalog data sortting completed')
        return_data = {
            'douyu_game_catalogs': sorted_catalog
        }
        return self.wrapper_response(return_data)


@api_douyu_game.resource('/game/<string:game>')
class Douyu_game_info(Douyu_Api):
    """根据游戏名称获取游戏具体信息"""

    def __init__(self, host='localhost', port=27017):
        super(Douyu_game_info, self).__init__()
        self.logger.info('{} inited'.format(__name__))

    def get(self, game):
        '''
        {$project:{host:'$_id',count:1,earliest:1,latest:1,date:1,audience:1,_id:0}}
        '''
        pipeline = []
        pipeline.append({'$match': {'catalog': game}})
        pipeline.append({'$sort': {'audience': 1}})
        pipeline.append({'$group': {'_id': '$host', 'count': {'$sum': 1}, 'earliest': {'$min': '$date'}, 'latest': {
                        '$max': '$date'}, 'date': {'$push': '$date'}, 'audience': {'$push': '$audience'}}})
        pipeline.append({'$project': {'host': '$_id', 'count': 1,
                                      'earliest': 1, 'latest': 1, 'date': 1, 'audience': 1, '_id': 0}})
        pipeline.append({'$limit': 20})
        try:
            game_data = self._col.aggregate(pipeline)
        except Exception as e:
            self.logger.error(str(e))
            abort(404)
        else:
            return_data = {
                'catalog': game,
                'result': list(game_data)
            }
            self.logger.info('get {} detail data'.format(game.encode('utf-8')))
            return self.wrapper_response(return_data)
