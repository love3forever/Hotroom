#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017/12/8
# @Author  : wangmengcn
# @Email   : eclipse_sv@163.com
from flask_socketio import SocketIO
from eventlet import monkey_patch

monkey_patch()

# socketio相关
socketio = SocketIO(message_queue='redis://localhost:6379/10',
                    async_mode='eventlet')

from . import chat_channel
