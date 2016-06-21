#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: Kouen
@license: Apache Licence
@email: jobkouen@outlook.com
@software: PyCharm Community Edition
@file: rules.py
@time: 16/6/20 下午3:04

    根据输入, 生成规则
"""

import datetime


def create_rules(d_date):
    """
        生成对应规则文件
    :param d_date: 年月日时分秒的数据
    :return: 创建的规则文件
    """
    pass

if __name__ == '__main__':
    d = datetime.datetime.strptime(
        "19920101150000",
        "%Y%m%d%H%M%S"
    )

    print d
