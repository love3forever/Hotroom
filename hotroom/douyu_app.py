#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-15 20:53:02
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

# celery -A celeryApp worker -B --loglevel=info

from celery import Celery

app = Celery('douyuapp', include=['task_douyu'])
app.config_from_object('celery_douyu_config')

if __name__ == '__main__':
    app.start()
