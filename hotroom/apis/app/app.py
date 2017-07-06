from flask import Flask
from sys import path
path.append("..")
from douyu.catalogs import douyuCatalogs
from douyu.roominfo import roominfo

app = Flask(__name__)

app.register_blueprint(douyuCatalogs)
app.register_blueprint(roominfo)

if __name__ == '__main__':
    app.run(debug=True)
