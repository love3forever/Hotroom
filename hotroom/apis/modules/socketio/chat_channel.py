#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017/12/8
# @Author  : wangmengcn
# @Email   : eclipse_sv@163.com
from flask_socketio import emit
from . import socketio


@socketio.on('connect')
def test_connect():
    print('some one connected')
    emit('message', 'connected')


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
