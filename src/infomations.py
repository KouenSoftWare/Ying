#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: Kouen
@license: Apache Licence
@email: jobkouen@outlook.com
@software: PyCharm Community Edition
@file: relations.py
@time: 16/7/21 上午11:06
@简介:
    所有内部关系
            u"金": 1, u"水": 2, u"木": 3, u"火": 4, u"土": 0
"""

XING = {
    'MEAN': {
        "X1": {
            u"五材": u""
        },
        "X2": {},
        "X3": {},
        "X4": {},
        "X0": {}
    },
    'SON': {
        "X1": "X2", "X2": "X3", "X3": "X4", "X4": "X0", "X0": "X1"
    },
    "WIFE": {
        "X1": "X3", "X2": "X4", "X3": "X0", "X4": "X1", "X0": "X2"
    },
    "HUSBAND": {
        "X1": "X4", "X2": "X0", "X3": "X1", "X4": "X2", "X0": "X3"
    },
    "FATHER": {
        "X1": "X0", "X2": "X1", "X3": "X2", "X4": "X3", "X0": "X4"
    }
}

GAN = {}

ZHI = {}

GOD10 = {}

QUARTER = {}

DICT = {
    "ID": {
        'X1': u"金",
        'X2': u"水",
        'X3': u"木",
        'X4': u"火",
        'X0': u"土",
    },
    "NAME": {
        u"金": 'X1',
        u"水": 'X2',
        u"木": 'X3',
        u"火": 'X4',
        u"土": 'X0',
    }
}
