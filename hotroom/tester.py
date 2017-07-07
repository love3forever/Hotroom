#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-06 14:06:47
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

from unittest import TestCase, main
from collector.danmu import CDouyu, CPanda, CQuanmin


class Test_Collector(TestCase):
    """docstring for Test_Douyu"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_douyu(self):
        douyu = CDouyu.Douyu(mport=27018)
        assert 0 == douyu.getRoomInfos()

    def test_quanmin(self):
        quanmin = CQuanmin.Quanmin(mport=27018)
        assert 0 == quanmin.getRoomInfos()

    def test_panda(self):
        panda = CPanda.Panda(mport=27018)
        assert 0 == panda.getRoomInfos()


if __name__ == '__main__':
    main()
