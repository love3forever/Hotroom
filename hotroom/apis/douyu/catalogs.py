from flask.blueprints import Blueprint
from flask import jsonify
from flask_restful import Api, Resource
from pymongo import MongoClient

douyuCatalogs = Blueprint('douyucatalog', __name__)
catalogs = Api(douyuCatalogs)


class DoyuCatalogs(Resource):
    def __init__(self):
        self._mongoCli = MongoClient(host='localhost', port=27017)
        self._db = self._mongoCli['Douyudata']
        self._col = self._db['Catalog']

    def get(self):
        results = self._col.find({}, {"_id": 0})
        return jsonify({'catalogs': list(results)})


catalogs.add_resource(DoyuCatalogs, "/apis/douyu/catalogs",
                      endpoint='douyuCatalog')
