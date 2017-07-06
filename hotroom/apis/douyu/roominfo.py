from flask.blueprints import Blueprint
from flask_restful import Resource, Api
from pymongo import MongoClient
from flask import jsonify, make_response

roominfo = Blueprint('douyuroominfo', __name__)
roominfoApi = Api(roominfo)


class DouyuRooms(Resource):
    def __init__(self):
        self._mongoCli = MongoClient(host='localhost', port=27017)
        self._db = self._mongoCli['Douyudata']
        self._col = self._db['Roominfo']

    def get(self):
        results = self._col.find({}, {"_id": 0}).limit(50)
        response = make_response(jsonify({'roominfos': list(results)}))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers[
            'Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
        return response


roominfoApi.add_resource(DouyuRooms, "/apis/douyu/roominfos",
                         endpoint='douyuRoominfos')
