#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: Kouen
@license: Apache Licence
@email: jobkouen@outlook.com
@software: PyCharm Community Edition
@file: main_calc.py
@time: 16/8/11 上午10:03
@简介:
    4个阶段的计算任务:
        1.调候分析->分析五行喜忌
        2.五行力量分析->分析局势,根据喜忌输出初步报告
        3.五行推演->根据干支冲合会破,演化新的五行力量,根据喜忌输出报告(计算某年,某月,某日得分)
        4.诠释结果->根据干支组合进行分析。

"""

import datetime
from pprint import pprint
from src.infomations import QUARTER, DICT, ZHI, GAN, XING
from src.dictionary import PillarBase, init_data


def cimate_analyze(eight):
    """
        调候分析
    :param eight: 八字
        [
            (年柱),(月柱),(日柱),(时柱)
        ]

    :return:五行喜忌
        {
            'like':()
            'not' :()
        }
    """
    birthday_month = DICT["NAME"][eight[1][1]]
    quater_info = QUARTER[birthday_month]
    xing_info = [
        [
            GAN['XING'][DICT["NAME"][eight[0][0]]],
            GAN['XING'][DICT["NAME"][eight[1][0]]],
            GAN['XING'][DICT["NAME"][eight[2][0]]],
            GAN['XING'][DICT["NAME"][eight[3][0]]]
        ],
        [
            ZHI['XING'][DICT["NAME"][eight[0][1]]],
            ZHI['XING'][DICT["NAME"][eight[1][1]]],
            ZHI['XING'][DICT["NAME"][eight[2][1]]],
            ZHI['XING'][DICT["NAME"][eight[3][1]]]
        ]
    ]
    price_total = 0
    xing_influences = dict()
    like = []
    n_like = []
    for q_xing, q_price in quater_info['5X']:
        xing_influences[q_xing] = q_price
        if q_price > 0:
            like.append(q_xing)
        elif q_price < 0:
            n_like.append(q_xing)

    if (d.month == 2 and d.day <= 4) or (d.month == 1 and d.day <= 21):
        xing_influences['X0'] = -1
    elif (d.month == 2 and d.day <= 4) or (d.month == 1 and d.day <= 21):
        xing_influences['X0'] = -1

    for q_xing, q_price in quater_info['5X']:
        if q_price != 0:
            for eight_xing in xing_info[0]+xing_info[1]:
                if q_xing == eight_xing:
                    price_total += q_price
        else:
            for index in [0, 1]:
                r_index = int(not index)
                if q_xing in xing_info[index]:
                    nearby_xings = []
                    for pos in xrange(0, len(xing_info[index])):
                        if xing_info[index][pos] == q_xing:
                            if pos > 0:
                                nearby_xings.append((index, pos-1))
                            if pos < 3:
                                nearby_xings.append((index, pos+1))
                            nearby_xings.append((r_index, pos))
                    influences_price = 0
                    for _index, _nearby in nearby_xings:
                        _x = xing_info[_index][_nearby]
                        if _x not in xing_influences:
                            continue
                        if _index == index:
                            influences_price += (xing_influences[_x]/2)
                        else:
                            influences_price += xing_influences[_x]/2
                    if influences_price > 2:
                        price_total += 2
                    elif influences_price > 0:
                        price_total += 1
                    elif influences_price < -2:
                        price_total -= 2
                    elif influences_price < 0:
                        price_total -= 1

    return xing_info, price_total, like, n_like


def elements_analyze(xing_info):
    master = xing_info[0][2]
    master_son = XING['FATHER'][master]
    power = 0
    r_power = 0
    xing_power = {
        'X1': 0,
        'X2': 0,
        'X3': 0,
        'X4': 0,
        'X0': 0
    }
    for i in xing_info[0] + xing_info[1]:
        if i == master or i == master_son:
            power += 1
        else:
            r_power += 1
        xing_power[i] += 1

    return xing_power, power, r_power


def elements_combination(eight):
    """

    :param eight: 八字(任意数量)
    [
        [天干],
        [地支]
    ]
    :return:五行力量比对

        组合:
            干支      类型      代码
            天干      冲破      1
            天干      合        2
            地支      三会      11
            地支      三合      12
            地支      六合      13
            地支      半合      14
            地支      暗合      15
            地支      六破      16
            地支      六害      17
            地支      四刑      18
            地支      六冲      19
    """
    combination = set()

    def _(_cond1, _cond2, _container, _type, _x=None):
        if _cond2 and _cond2 in _container:
            if _container.count(_cond2) > 1:
                _cond2_pos = [-1]
                for _i in range(_container.count(_cond2)):
                    _cond2_pos.append(_container.index(_cond2, _cond2_pos[-1]+1))
                for _i in _cond2_pos[1:]:
                    _p = set()
                    _p.add(_container.index(_cond1))
                    _p.add(_i)
                    _p = list(_p)
                    if _x:
                        _p.append(_x)
                    combination.add((_type, tuple(_p)))
            else:
                _p = set()
                _p.add(_container.index(_cond2))
                _p.add(_container.index(_cond1))
                _p = list(_p)
                if _x:
                    _p.append(_x)
                combination.add((_type, tuple(_p)))

    for gan in eight[0]:
        _(gan, GAN['CLASH'][gan], eight[0], 1)
        _(gan, GAN['MERGE'][gan][0], eight[0], 2, GAN['MERGE'][gan][1])

    for zhi in eight[1]:
        part = ZHI['MEET'][zhi]
        conds = list()
        for i in range(0, len(part)-1):
            if part[i] in eight[1]:
                conds.append(True)
            else:
                conds.append(False)
        if sum(conds) == len(conds):
            p = set()
            for i in part[:-1]:
               p.add(eight[1].index(i))
            p.add(0, eight[1].index(zhi))
            combination.add((11, tuple(p)))

        part = ZHI['MERGE3'][zhi]
        conds = list()
        for i in range(0, len(part)-1):
            if part[i] in eight[1]:
                conds.append(True)
                p = set()
                p.add(eight[1].index(part[i]))
                p.add(eight[1].index(zhi))
                p = list(p)
                p.append(part[-1])
                combination.add((14, tuple(p)))
            else:
                conds.append(False)

        if sum(conds) == len(conds):
            p = set()
            for i in part[:-1]:
               p.add(eight[1].index(i))
            p.add(0, eight[1].index(zhi))
            combination.add((12, tuple(p)))

        _(zhi, ZHI['MERGE6'][zhi][0], eight[1], 13, ZHI['MERGE6'][zhi][1])
        _(zhi, ZHI['PUNISHMENT'][zhi][0], eight[1], 18, ZHI['PUNISHMENT'][zhi][1])
        _(zhi, ZHI['DAMAGE'][zhi], eight[1], 16)
        _(zhi, ZHI['HURT'][zhi], eight[1], 17)
        _(zhi, ZHI['CLASH'][zhi], eight[1], 19)
        _(zhi, ZHI['AnMerge'].get(zhi, ''), eight[1], 15)

    return combination


def elements_evolution(five_xing, combination):
    """
        判断组合的有效性, 给出组合后的演化结果
    :param five_xing:原始八字的五行组合,来自cimate_analyze[0]
    :param combination: 所有组合,来自elements_combination
    :return: five_xing->演化后的结果, 总体五行力量比例
    """
    for item_comb in combination:
        if item_comb[0] > 10:  # Y:地支 N:天干
            pass
        else:
            pass
    return ""


def explain():
    pass

if __name__ == '__main__':
    init_data()
    eight = list()
    birth = '1991112716'
    eight.append(PillarBase.get_year_pillar(birth))
    eight.append(PillarBase.get_month_pillar(birth))
    eight.append(PillarBase.get_day_pillar(birth))
    eight.append(PillarBase.get_hour_pillar(birth))
    d = datetime.datetime.strptime(birth, '%Y%m%d%H')
    level_1 = cimate_analyze(eight)
    level_2 = elements_analyze(level_1[0])

    col_eight = [list(), list()]
    for _i_ in eight:
        col_eight[0].append(DICT['NAME'][_i_[0]])
        col_eight[1].append(DICT['NAME'][_i_[1]])

    level_3 = elements_combination(col_eight)
    level_4 = elements_evolution(level_1[0], level_3)

    pprint(col_eight)
    print
    pprint(level_1)
    print
    pprint(level_2)
    print
    pprint(level_3)
    print
    pprint(level_4)
    print
