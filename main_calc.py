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
from src.dictionary import PillarBase, init_data, get_eight_all
import copy


def is_hurt(dictCond, positions):
    """
        位置中的八字,是否有受到刑冲
    :param dictCond: 所有组合
    :param positions: 需要被判断的组合
    :return: Boolean
    """
    setBadPos = set()
    for t in (18, 19):
        for pos in dictCond.get(t, []):
            for i in pos:
                if isinstance(i, int):
                    setBadPos.add(i)
    for pos in positions[:-1]:
        if pos in setBadPos:
            return False
    return True


def cimate_analyze(eight, d_date):
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
    xing_info = [list(), list()]
    for i in range(len(eight)):
        xing_info[0].append(GAN['XING'][DICT["NAME"][eight[i][0]]])
        xing_info[1].append(ZHI['XING'][DICT["NAME"][eight[i][1]]])
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

    # (*)判断条件:距离立秋,立夏,立冬,立春 日期是否符合条件, 判断5X喜忌,

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
        _f = False
        if _cond2 == _cond1 and _container.count(_cond2) > 1:
            _f = True
        elif _cond2 != _cond1:
            _f = True

        if _cond2 and _cond2 in _container and _f:
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
                if len(_p) == 1:
                    _p.add(_container.index(_cond2, _container.index(_cond2)+1))
                _p = list(_p)
                if _x:
                    _p.append(_x)
                combination.add((_type, tuple(_p)))

    for gan in eight[0]:
        _(gan, GAN['CLASH'].get(gan), eight[0], 1)
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
            p.add(eight[1].index(zhi))
            p = list(p)
            p.append(part[-1])
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
            p.add(eight[1].index(zhi))
            p = list(p)
            p.append(part[-1])
            combination.add((12, tuple(p)))

        _(zhi, ZHI['MERGE6'][zhi][0], eight[1], 13, ZHI['MERGE6'][zhi][1])
        _(zhi, ZHI['PUNISHMENT'][zhi][0], eight[1], 18, ZHI['PUNISHMENT'][zhi][1])
        _(zhi, ZHI['DAMAGE'][zhi], eight[1], 16)
        _(zhi, ZHI['HURT'][zhi], eight[1], 17)
        _(zhi, ZHI['CLASH'][zhi], eight[1], 19)
        _(zhi, ZHI['AnMerge'].get(zhi, ''), eight[1], 15)

    return combination


def elements_evolution(eight, five_xing, combination):
    """
        判断组合的有效性, 给出组合后的演化结果
    :param five_xing:原始八字的五行组合,来自cimate_analyze[0]
    :param combination: 所有组合,来自elements_combination
    :return: five_xing->演化后的结果, 总体五行力量比例
    """
    dictCombination = dict()
    listSuccessCombination = list()
    for item_comb in combination:
        if not dictCombination.get(item_comb[0]):
            dictCombination[item_comb[0]] = list()
        dictCombination[item_comb[0]].append(item_comb[1])

    xingRate = {
        'X1': 0.0,
        'X2': 0.0,
        'X3': 0.0,
        'X4': 0.0,
        'X0': 0.0
    }
    xingEvolution = copy.deepcopy(five_xing)
    single = [[0]*len(five_xing[0]), [0]*len(five_xing[0])]
    userPos = single
    badComb = dict()
    setBadCombPos = set()
    for item_comb in combination:
        positions = item_comb[1]

        if item_comb[0] in (11, 12):
            iCond = 0
            for i in range(len(five_xing[0])):
                if five_xing[0][i] == positions[-1]:
                    iCond += 1

            if iCond >= 1 and is_hurt(dictCombination, positions) and \
               not userPos[1][positions[0]] and not userPos[1][positions[1]] and not userPos[1][positions[2]]:
                for i in positions[:-1]:
                    xingEvolution[1][i] = positions[-1]
                    userPos[1][i] = 1
                listSuccessCombination.append(item_comb)
            else:
                for i in positions[:-1]:
                    single[1][i] = 1

        if item_comb[0] == 13:
            if positions[1]-positions[0] == 1:
                if (positions[2] == five_xing[0][positions[0]] or positions[2] == five_xing[0][positions[1]]) and \
                   not userPos[1][positions[0]] and \
                   not userPos[1][positions[1]]:
                    xingEvolution[1][positions[0]] = positions[2]
                    xingEvolution[1][positions[1]] = positions[2]
                    listSuccessCombination.append(item_comb)
                    userPos[1][positions[0]] = 1
                    userPos[1][positions[1]] = 1
                else:
                    single[1][positions[0]] = 1
                    single[1][positions[1]] = 1

        if item_comb[0] == 14:
            if (positions[2] == five_xing[0][positions[0]] or positions[2] == five_xing[0][positions[1]]) and \
               (five_xing[1][1] == positions[2] or five_xing[1][1] == XING['FATHER'][positions[2]]) and \
               is_hurt(dictCombination, positions) and \
               not userPos[1][positions[0]] and \
               not userPos[1][positions[1]]:
                xingEvolution[1][positions[0]] = positions[2]
                xingEvolution[1][positions[1]] = positions[2]
                listSuccessCombination.append(item_comb)
                userPos[1][positions[0]] = 1
                userPos[1][positions[1]] = 1
            else:
                single[1][positions[0]] = 1
                single[1][positions[1]] = 1

        if item_comb[0] in (15, 16, 17, 18, 19):
            if badComb.get(positions[0]) and badComb[positions[0]][0] > positions[1]:
                badComb[positions[0]] = (positions[1], item_comb[0])

            elif not badComb.get(positions[0]):
                badComb[positions[0]] = (positions[1], item_comb[0])

    for i in badComb.keys():
        if i not in setBadCombPos and badComb[i][0] not in setBadCombPos:
            setBadCombPos.add(badComb[i][0])
            setBadCombPos.add(i)
            listSuccessCombination.append([badComb[i][1], [i, badComb[i][0]]])

    total = len(single[0])*2.0

    for i in range(5):
        _k = "X%d" % i
        xingRate[_k] = (xingEvolution[0].count(_k) + xingEvolution[1].count(_k))/total

    quator = list(QUARTER[eight[1][1]]['4J'])

    for key in xingRate.keys():
        xingRate[key] = round(xingRate[key], 3)

    eight_xing_rate = [[0]*len(single[0]), [0]*len(single[0])]
    y = len(single[0])
    for i in range(2):
        for j in range(y):
            xing_total = five_xing[0].count(five_xing[i][j])+five_xing[1].count(five_xing[i][j])
            eight_xing_rate[i][j] = xingRate[five_xing[i][j]]/xing_total
    wait_fen = [0.0, 0.0]

    paichu = dict()
    for i in range(2):
        for j in range(y):
            if single[i][j]:
                if not paichu.get(five_xing[i][j]):
                    paichu[five_xing[i][j]] = 0
                paichu[five_xing[i][j]] += 1

    for i in range(2):
        for j in range(y):
            if not single[i][j]:
                if quator.index(five_xing[i][j]) == 4:
                    eight_xing_rate[i][j] /= 2
                    wait_fen[0] += (eight_xing_rate[i][j]/3*2)
                    wait_fen[1] += (eight_xing_rate[i][j]/3)
                if quator.index(five_xing[i][j]) == 3:
                    eight_xing_rate[i][j] /= 4
                    wait_fen[0] += (eight_xing_rate[i][j]*2)
                    wait_fen[1] += (eight_xing_rate[i][j])

    for i in range(2):
        for j in range(y):
            if not single[i][j]:
                xing_total = five_xing[0].count(five_xing[i][j])+five_xing[1].count(five_xing[i][j])
                xing_total -= paichu.get(five_xing[i][j], 0)
                if quator.index(five_xing[i][j]) == 0:
                    eight_xing_rate[i][j] += (wait_fen[0]/xing_total)
                if quator.index(five_xing[i][j]) == 1:
                    eight_xing_rate[i][j] += (wait_fen[1]/xing_total)

    # 先判断谁是0, 然后把剩下的比例,换个它的FATHER,平均(统计是0的总数)
    is_zero = list()
    for i in xingRate.keys():
        if xingRate[i] == 0.0:
            is_zero.append(i)

    fathers = list()
    for i in is_zero:
        fathers.append(XING['FATHER'][i])

    divisor = 0.0
    for i in range(2):
        for j in range(y):
            if five_xing[i][j] in fathers and not single[i][j]:
                divisor += 1.0

    surplus = (1.0 - sum(eight_xing_rate[0])-sum(eight_xing_rate[1]))
    for i in range(2):
        for j in range(y):
            if five_xing[i][j] in fathers and not single[i][j]:
                eight_xing_rate[i][j] += (surplus/divisor)

    xingRateEvo = {
        'X0': 0.0,
        'X1': 0.0,
        'X2': 0.0,
        'X3': 0.0,
        'X4': 0.0
    }
    for i in range(2):
        for j in range(y):
            xingRateEvo[five_xing[i][j]] += eight_xing_rate[i][j]

    for i in range(2):
        for j in range(y):
            eight_xing_rate[i][j] = round(eight_xing_rate[i][j], 3)

    for i in xingRateEvo.keys():
        xingRateEvo[i] = round(xingRateEvo[i], 3)
    return xingEvolution, eight_xing_rate, single, xingRate, xingRateEvo, listSuccessCombination


def calc_score(xingEvolution, eight_xing_rate, xing_like, successComb):
    score = 0.0
    opera = {
        xing_like[0]: 2,
        XING['FATHER'][xing_like[0]]: 1,
        XING['SON'][xing_like[0]]: -0.5,
        XING['WIFE'][xing_like[0]]: -1,
        XING['HUSBAND'][xing_like[0]]: -2
    }

    otherScore = dict()
    for i in successComb:
        rate = 1
        if i[0] == 16:
            rate = 0.65
        elif i[0] == 17:
            rate = 0.8
        elif i[0] == 18:
            rate = 0.5
        elif i[0] == 19:
            rate = 0.4
        elif i[0] == 11:
            rate = 3
        elif i[0] == 12:
            rate = 2.2
        elif i[0] == 13:
            rate = 1.7
        elif i[0] == 14:
            rate = 1.4

        otherScore[i[1][0]] = rate
        otherScore[i[1][1]] = rate

    xing_power = {
        'X0': 0.0,
        'X1': 0.0,
        'X2': 0.0,
        'X3': 0.0,
        'X4': 0.0
    }
    for i in range(2):
        for j in range(len(xingEvolution[0])):
            xing_power[xingEvolution[i][j]] += (eight_xing_rate[i][j] * otherScore.get(j, 1) * 100)

    for i in xing_power.keys():
        score += (opera[i] * xing_power[i])

    score = round((200 + score), 1)

    return score, xing_power


def explain():
    pass

if __name__ == '__main__':
    init_data()
    t_birth = datetime.datetime.strptime("1992010116", "%Y%m%d%H")
    t_find_date = datetime.datetime.strptime("20120801", "%Y%m%d")
    eight = get_eight_all(t_birth, t_find_date, is_nong=False)
    d = datetime.datetime.strptime("1991112716", '%Y%m%d%H')

    level_1 = cimate_analyze(eight, d)
    level_2 = elements_analyze(level_1[0])

    col_eight = [list(), list()]
    for _i_ in eight:
        col_eight[0].append(DICT['NAME'][_i_[0]])
        col_eight[1].append(DICT['NAME'][_i_[1]])

    level_3 = elements_combination(col_eight)
    level_4 = elements_evolution(col_eight, level_1[0], level_3)
    level_5 = calc_score(level_4[0], level_4[1], level_1[2], level_4[5])

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
    pprint(level_5)
    print