#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-11 11:37:24
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$
from douyu_api_abc import DouyuApi
from flask import Blueprint
from flask_restful import Api, abort

from datetime import datetime, timedelta

bp_douyu_game = Blueprint('douyu_games_api', __name__,
                          url_prefix='/api/v1/douyu')
api_douyu_game = Api(bp_douyu_game)


# noinspection PyUnusedLocal,PyUnusedLocal
@api_douyu_game.resource('/games')
class DouyuGames(DouyuApi):
    """获取斗鱼曾经直播过的所有游戏类型"""

    def __init__(self, host='localhost', port=27017):
        super(DouyuGames, self).__init__()
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


# noinspection PyUnusedLocal,PyUnusedLocal
@api_douyu_game.resource('/game/<string:game>')
class DouyuGameInfo(DouyuApi):
    """根据游戏名称获取游戏具体信息"""

    def __init__(self, host='localhost', port=27017):
        super(DouyuGameInfo, self).__init__()
        self.logger.info('{} inited'.format(__name__))

    def get(self, game):
        """
        根据游戏名称获取游戏相关细节数据
        """
        pipeline = [{'$match': {'catalog': game}}, {'$sort': {'audience': 1}}, {
            "$group": {
                "_id": "$host",
                "audience": {
                    "$push": "$audience"
                },
                "count": {
                    "$sum": 1
                },
                "date": {
                    "$push": "$date"
                },
                "earliest": {
                    "$min": "$date"
                },
                "latest": {
                    "$max": "$date"
                }
            }
        }, {
                        "$project": {
                            "_id": 0,
                            "audience": 1,
                            "count": 1,
                            "date": 1,
                            "earliest": 1,
                            "host": "$_id",
                            "latest": 1
                        }
                    }, {'$limit': 20}]
        try:
            game_data = self._col.aggregate(pipeline)
        except Exception as e:
            self.logger.error(str(e))
            abort(503)
        else:
            return_data = {
                'catalog': game,
                'result': list(game_data)
            }
            self.logger.info('get {} detail data'.format(game.encode('utf-8')))
            return self.wrapper_response(return_data)


# noinspection PyUnusedLocal,PyUnusedLocal
@api_douyu_game.resource('/game/<string:game>/timeline')
class DouyuGameTimeline(DouyuApi):
    """根据游戏名称，获取游戏人气随时间变化情况"""
    '''使用mongodb操作符来进行聚合，避免使用uid'''

    def __init__(self, host='localhost', port=27017):
        super(DouyuGameTimeline, self).__init__()
        self.logger.info('{} inited'.format(__name__))

    def get(self, game):
        """
        根据游戏名称，获取游戏直播随时间人气变化情况
        """
        pipeline = list()
        pipeline.append({'$match': {'catalog': game}})
        pipeline.append(
            {'$group': {'_id': '$uid', 'count': {'$avg': '$audience'}}})
        pipeline.append(
            {'$project': {'time': '$_id', 'count': {'$ceil': '$count'}, '_id': 0}})
        pipeline.append({'$sort': {'time': 1}})
        try:
            timeline_data = self._col.aggregate(pipeline)
        except Exception as e:
            self.logger.error(str(e))
            abort(503)
        else:
            return_data = {
                'catalog': game,
                'timeline': list(timeline_data)
            }
            self.logger.info(
                'get {} timeline data'.format(game.encode('utf-8')))
            return self.wrapper_response(return_data)


# noinspection PyUnusedLocal,PyUnusedLocal
@api_douyu_game.resource('/game/<string:game>/streamers')
class DouyuGameStreamers(DouyuApi):
    """根据游戏名称，获取直播过该游戏的主播列表,直播时长前100"""

    def __init__(self, host='localhost', port=27017):
        super(DouyuGameStreamers, self).__init__()
        self.logger.info('{} inited'.format(__name__))

    def get(self, game):
        pipeline = list()
        pipeline.append({'$match': {'catalog': game}})
        pipeline.append(
            {
                "$group": {
                    "_id": "$host",
                    "audience": {
                        "$push": "$audience"
                    },
                    "count": {
                        "$sum": 1
                    },
                    "date": {
                        "$push": "$date"
                    }
                }
            })
        pipeline.append(
            {
                "$project": {
                    "_id": 0,
                    "audience": 1,
                    "count": 1,
                    "date": 1,
                    "host": "$_id"
                }
            })
        pipeline.append({'$sort': {'count': -1}})
        pipeline.append({'$limit': 100})
        try:
            streamers_data = self._col.aggregate(pipeline)
        except Exception as e:
            self.logger.error(str(e))
            abort(503)
        else:
            return_data = {
                'catalog': game,
                'streamers': list(streamers_data)
            }
            return self.wrapper_response(return_data)


# noinspection PyUnusedLocal,PyUnusedLocal
@api_douyu_game.resource('/game/top5/<string:param>')
class Top5GameofWeek(DouyuApi):
    """docstring for Top5_game_week"""

    def __init__(self, host='localhost', port=27017):
        super(Top5GameofWeek, self).__init__()
        self.logger.info('{} inited'.format(__name__))

    def get(self, param):
        now = datetime.now()
        begin = ''
        if param == 'week':
            begin = now - timedelta(days=7)
        elif param == 'now':
            begin = now - timedelta(hours=1)
        else:
            abort(404)
        pipline = list()
        pipline.append({
            '$match': {
                'date': {'$gt': begin}
            }
        })
        pipline.append({
            '$group': {
                '_id': '$catalog',
                'heat': {'$avg': '$audience'}
            }
        })
        pipline.append({
            '$project': {
                'catalog': '$_id',
                'heat': {'$ceil': '$heat'},
                '_id': 0
            }
        })
        pipline.append({
            '$sort': {
                'heat': -1
            }
        })
        pipline.append({
            '$limit': 20
        })
        data = self._col.aggregate(pipline)
        if data:
            return self.wrapper_response({
                'code': 200,
                'lastweek': list(data)
            })
        else:
            abort(404)
