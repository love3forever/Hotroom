#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-07 17:31:59
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$
from celery.schedules import crontab

# BROKER_URL = 'amqp://guest:guest@localhost:5672//'
BROKER_URL = 'redis://127.0.0.1:6379/7'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/6'

CELERY_TIMEZONE = 'Asia/Shanghai'

CELERYBEAT_SCHEDULE = {
    'SAVE_PANDA_ROOMINFO': {
        'task': 'task_other.SAVE_PANDA_DATA',
        'schedule': crontab(minute=[40]),
    },
    'SAVE_QUANMIN_ROOMINFO': {
        'task': 'task_other.SAVE_QUANMIN_DATA',
        'schedule': crontab(minute=[41]),
    },
}
