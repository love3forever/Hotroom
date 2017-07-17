#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-17 21:03:33
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

from fabric.api import *
from fabric.contrib.console import confirm


env.use_ssh_config = True
env.hosts = ['al', 'al1']
env.roledefs = {
    'al1': ['al'],
    'al2': ['al1'],
}


@roles('al1')
@task
def pre_deploy():
    local('git add -A && git commit')
    local('git push origin master && git push tx master')


@roles('al1')
def deploy_douyu():
    code_dir = '~/git/Hotroom'
    with settings(warn_only=True):
        if run("ls {}".format(code_dir)).failed:
            run("git clone hhttps://github.com/love3forever/Hotroom.git {}".format(code_dir))
    with cd(code_dir):
        run("git pull")
        run("sudo pip install -r ./requirement.txt")
        with cd('./hotroom'):
            pids = run(
                "ps -ef | grep celery | grep -v grep | awk '{print $2}'")
            if pids:
                pid_list = pids.split('\r\n')
                for i in pid_list:
                    run('kill -9 %s' % i)  # 杀掉运行服务进程
            run('pwd')
            run("(nohup celery -A douyu_app worker -B --loglevel=error >& /dev/null < /dev/null &) && sleep 1")
            run('echo deployed')


@roles('al2')
def deploy_other():
    run("uname -a")


@task
def deploy():
    execute(deploy_douyu)
    execute(deploy_other)
