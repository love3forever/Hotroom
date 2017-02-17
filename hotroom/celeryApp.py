#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-15 20:53:02
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

# celery -A celeryTask worker  --loglevel=info

from celery import Celery
import celeryConfig


app = Celery('celeryApp', include=['tasks'])
app.config_from_object('celeryConfig')

if __name__ == '__main__':
    app.start()
