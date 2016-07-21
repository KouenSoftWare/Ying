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
            u"材": u"金", u"色": u"白",
            u"方": u"西", u"季": u"秋",
            u"时": u"日入", u"节": u"七夕",
            u"星": u"金星", u"声": u"哭",
            u"音": u"商", u"脏": u"肺",
            u"腑": u"大肠", u"体": u"皮",
            u"志": u"悲", u"指": u"无名指",
            u"官": u"鼻", u"觉": u"香",
            u"液": u"涕", u"味": u"辛",
            u"臭": u"腥", u"气": u"气",
            u"荣": u"毛", u"兽": u"白虎",
            u"畜": u"鸡", u"虫": u"哺乳类",
            u"谷": u"粟", u"果": u"桃",
            u"菜": u"葱", u"常": u"义",
            u"经": u"书", u"政": u"力",
            u"恶": u"燥", u"化": u"收",
            u"祀": u"门", u"卦": u"兑",
            u"数": u"9", u"动": u"咳",
            u"病": u"肩背"
        },
        "X2": {
            u"材": u"水", u"色": u"黑",
            u"方": u"北", u"季": u"东",
            u"时": u"夜半", u"节": u"重阳",
            u"星": u"水星", u"声": u"呻",
            u"音": u"羽", u"脏": u"肾",
            u"腑": u"膀胱", u"体": u"骨",
            u"志": u"恐", u"指": u"小指",
            u"官": u"耳", u"觉": u"声",
            u"液": u"唾", u"味": u"咸",
            u"臭": u"朽", u"气": u"骨",
            u"荣": u"发", u"兽": u"玄武",
            u"畜": u"猪", u"虫": u"龟、甲壳类、两栖类",
            u"谷": u"菽", u"果": u"梨",
            u"菜": u"藿", u"常": u"智",
            u"经": u"易", u"政": u"静",
            u"恶": u"寒", u"化": u"藏",
            u"祀": u"井", u"卦": u"坎",
            u"数": u"6", u"动": u"栗",
            u"病": u"腰股"
        },
        "X3": {
            u"材": u"木", u"色": u"青",
            u"方": u"东", u"季": u"春",
            u"时": u"平旦", u"节": u"新年",
            u"星": u"木星", u"声": u"呼",
            u"音": u"角", u"脏": u"肝",
            u"腑": u"胆", u"体": u"筋",
            u"志": u"怒", u"指": u"食指",
            u"官": u"木", u"觉": u"色",
            u"液": u"泣", u"味": u"酸",
            u"臭": u"膻", u"气": u"筋",
            u"荣": u"爪", u"兽": u"青龙",
            u"畜": u"狗", u"虫": u"鱼类、昆虫类、爬虫类",
            u"谷": u"苎麻", u"果": u"李",
            u"菜": u"韭", u"常": u"仁",
            u"经": u"诗", u"政": u"宽",
            u"恶": u"风", u"化": u"生",
            u"祀": u"户", u"卦": u"震",
            u"数": u"8", u"动": u"握",
            u"病": u"颈项"
        },
        "X4": {
            u"材": u"火", u"色": u"赤",
            u"方": u"南", u"季": u"夏",
            u"时": u"日中", u"节": u"上巳",
            u"星": u"火星", u"声": u"笑",
            u"音": u"徵", u"脏": u"心",
            u"腑": u"小肠", u"体": u"脉",
            u"志": u"喜", u"指": u"中指",
            u"官": u"舌", u"觉": u"触",
            u"液": u"汗", u"味": u"苦",
            u"臭": u"焦", u"气": u"血",
            u"荣": u"面", u"兽": u"朱雀",
            u"畜": u"羊", u"虫": u"鸟类",
            u"谷": u"黍", u"果": u"杏",
            u"菜": u"薤", u"常": u"礼",
            u"经": u"礼", u"政": u"明",
            u"恶": u"热", u"化": u"长",
            u"祀": u"灶", u"卦": u"离",
            u"数": u"7", u"动": u"忧",
            u"病": u"胸胁"
        },
        "X0": {
            u"材": u"土", u"色": u"黄",
            u"方": u"中", u"季": u"长夏",
            u"时": u"日西", u"节": u"端午",
            u"星": u"土星", u"声": u"歌",
            u"音": u"宫", u"脏": u"脾",
            u"腑": u"胃", u"体": u"肉",
            u"志": u"思", u"指": u"",
            u"官": u"", u"觉": u"大拇指",
            u"液": u"口", u"味": u"味",
            u"臭": u"香", u"气": u"肉",
            u"荣": u"唇", u"兽": u"勾陈",
            u"畜": u"牛", u"虫": u"人类",
            u"谷": u"稻", u"果": u"枣",
            u"菜": u"葵", u"常": u"信",
            u"经": u"春秋", u"政": u"恭",
            u"恶": u"湿", u"化": u"化",
            u"祀": u"霤", u"卦": u"坤",
            u"数": u"10", u"动": u"哕",
            u"病": u"脊"
        }
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
