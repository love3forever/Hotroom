#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-16 08:50:08
# @Author  : eclipse_sv (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36'
ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
CONNECTION = "close"

headers = {
    'User-Agent': AGENT,
    'Accept': ACCEPT,
    'Connection': CONNECTION,
}


def convert_audience(audience):
    if audience:
        value = 0
        if u"万" in audience:
            number = list(audience)
            number.pop()
            if "." in number:
                value = int(float(''.join(number)) * 10000)
            else:
                value = int(''.join(number)) * 10000
        else:
            value = int(audience)
        return value
