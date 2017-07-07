#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-07 17:28:30
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

from celery import Celery
import celery_other_config


app = Celery('otherapp', include=['task_other'])
app.config_from_object('celery_other_config')

if __name__ == '__main__':
    app.start()
