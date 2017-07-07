#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-16 14:34:14
# @Author  : eclipse_sv (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

from celery.schedules import crontab

# BROKER_URL = 'amqp://guest:guest@localhost:5672//'
BROKER_URL = 'redis://127.0.0.1:6379/2'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/3'

CELERY_TIMEZONE = 'Asia/Shanghai'

CELERYBEAT_SCHEDULE = {
    'SAVE_DOUYU_ROOMINFO': {
        'task': 'task_douyu.SAVE_DOUYU_DATA',
        'schedule': crontab(minute=[40]),
    }
}
