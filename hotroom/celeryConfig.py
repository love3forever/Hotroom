#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-16 14:34:14
# @Author  : eclipse_sv (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

from celery.schedules import crontab

# BROKER_URL = 'amqp://guest:guest@localhost:5672//'
BROKER_URL = 'redis://127.0.0.1:6379/7'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/6'

CELERY_TIMEZONE = 'Asia/Shanghai'

CELERYBEAT_SCHEDULE = {
    'SAVE_DOUYU_ROOMINFO': {
        'task': 'tasks.SAVE_DOUYU_INFO',
        'schedule': crontab(minute=[10, 30, 50]),
    },
    'SAVE_PANDA_ROOMINFO': {
        'task': 'tasks.SAVE_PANDA_INFO',
        'schedule': crontab(minute=[20, 40, 0]),
    },
    'SAVE_QUANMIN_ROOMINFO': {
        'task': 'tasks.SAVE_QUANMIN_INFO',
        'schedule': crontab(minute=[25, 45, 5]),
    },
    'REFRESH_DOUYU_CATALOG': {
        'task': 'tasks.REFRESH_DOUYU',
        'schedule': crontab(minute=[3], hour=[0]),
    },
    'REFRESH_PANDA_CATALOG': {
        'task': 'tasks.REFRESH_PANDA',
        'schedule': crontab(minute=[3], hour=[0]),
    },
    'REFRESH_QUANMIN_CATALOG': {
        'task': 'tasks.REFRESH_QUANMIN',
        'schedule': crontab(minute=[3], hour=[0]),
    },
}