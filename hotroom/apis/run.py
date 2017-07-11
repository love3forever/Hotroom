from flask import Flask
from douyu.game_api import bp_douyu_game

api_app = Flask(__name__)

api_app.register_blueprint(bp_douyu_game)

if __name__ == '__main__':
    api_app.run(debug=True)
