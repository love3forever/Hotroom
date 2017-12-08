#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017/12/8
# @Author  : wangmengcn
# @Email   : eclipse_sv@163.com
from flask import Flask
from .douyu.game_api import bp_douyu_game
from .douyu.streamer_api import bp_douyu_streamer

from .socketio import socketio

api_app = Flask(__name__)


def init_app():
    api_app.register_blueprint(bp_douyu_game)
    api_app.register_blueprint(bp_douyu_streamer)
    return api_app


def init_socketio():
    return socketio
