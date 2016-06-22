#!/usr/bin/env python
# encoding: utf-8

"""
@version: 0.1
@author: Kouen
@license: Apache Licence
@email: jobkouen@outlook.com
@software: PyCharm Community Edition
@file: dictionary.py
@time: 16/6/20 下午3:13

    存放对应关键字, 相互关系
"""

import datetime

g_eight_60 = dict()


def init_data():
    g = Gan('1')
    z = Zhi('1')
    x = 1
    y = 1
    while 1:
        key_x = str(x)
        if key_x == '10':
            key_x = '0'
        key_y = str(y)
        if key_y == '10':
            key_y = 'A'
        elif key_y == '11':
            key_y = 'B'
        elif key_y == '12':
            key_y = '0'

        c = x-y
        if c < 0:
            c += 12
        cx = c/2
        key = 10*cx+x

        value = g.get_chinese(key_x) + z.get_chinese(key_y)
        g_eight_60[key] = value
        g_eight_60[value] = key
        x += 1
        y += 1

        if x == 11 and y == 13:
            break
        if x == 11:
            x = 1
        if y == 13:
            y = 1


class Base(object):
    _sym = dict()
    _switch = {}

    def set_init(self, d_id, sw):
        sym = self.symbol()
        self._sym[sym] = d_id
        self._switch[sym] = {}
        self._switch[sym].update(sw)

    def __eq__(self, other):
        if isinstance(other, Base):
            return self.symbol() == other.symbol() and self.me_id() == other.me_id()
        else:
            return False

    def __str__(self):
        return self.to_chinese()

    def me_id(self):
        return self._sym[self.symbol()]

    def symbol(self):
        pass

    def to_chinese(self):
        return self._switch[self.symbol()][self._sym[self.symbol()]]

    def to_id(self, chinese):
        q_dict = self._switch[self.symbol()]
        temp_dict = dict()
        for key in q_dict.keys():
            temp_dict[q_dict[key]] = key
        ret = None
        try:
            ret = temp_dict[chinese]
        except (KeyError,):
            raise (KeyError, u"请传入正确的天干地支阴阳五行, 在内部找不到对应的编码:%s" % ret)
        return ret

    def get_chinese(self, d_id):
        return self._switch[self.symbol()][d_id]


class Xing(Base):
    """ 五行 我生为儿,生我为父,我克为妻,克我为敌,同我为兄"""
    def __init__(self, xing):
        switch = {
            1: '金',
            2: '水',
            3: '木',
            4: '火',
            0: '土'
        }
        self.set_init(xing, switch)

    def symbol(self):
        return '@'

    def son(self):
        return self.get_chinese((self.me_id()+1) % 5)

    def father(self):
        return self.get_chinese((self.me_id()+4) % 5)

    def wife(self):
        return self.get_chinese((self.me_id()+2) % 5)

    def enemy(self):
        return self.get_chinese((self.me_id()+3) % 5)

    def brother(self):
        return self.get_chinese(self.me_id())


class YinYang(Base):
    """ 阴阳 """

    def __init__(self, yy):
        switch = {
            1: '阳',
            0: '阴'
        }
        self.set_init(yy, switch)

    def symbol(self):
        return '!'


class Gan(Xing, YinYang):
    """
        天干
    """
    relations = {
        '1': (3, 1),
        '2': (3, 0),
        '3': (4, 1),
        '4': (4, 0),
        '5': (0, 1),
        '6': (0, 0),
        '7': (1, 1),
        '8': (1, 0),
        '9': (2, 1),
        '0': (2, 0),
    }

    def __init__(self, d_id):
        if len(d_id) != 1:
            d_id = self.to_id(d_id)

        Xing.__init__(self, Gan.relations[d_id][0])
        YinYang.__init__(self, Gan.relations[d_id][1])
        switch = {
            '1': '甲',
            '2': '乙',
            '3': '丙',
            '4': '丁',
            '5': '戊',
            '6': '己',
            '7': '庚',
            '8': '辛',
            '9': '壬',
            '0': '葵'
        }
        self.set_init(d_id, switch)

    def symbol(self):
        return '#'


class Zhi(Xing, YinYang):
    """ 12地支 """
    relations = {
        '1': (2, 1),
        '2': (0, 0),
        '3': (3, 1),
        '4': (3, 0),
        '5': (0, 1),
        '6': (4, 0),
        '7': (4, 1),
        '8': (0, 0),
        '9': (1, 1),
        'A': (1, 0),
        'B': (0, 1),
        '0': (2, 0),
    }

    def __init__(self, d_id):
        if len(d_id) != 1:
            d_id = self.to_id(d_id)

        Xing.__init__(self, Zhi.relations[d_id][0])
        YinYang.__init__(self, Zhi.relations[d_id][1])
        switch = {
            '1': '子',
            '2': '丑',
            '3': '寅',
            '4': '卯',
            '5': '辰',
            '6': '巳',
            '7': '午',
            '8': '未',
            '9': '申',
            'A': '酉',
            'B': '戌',
            '0': '亥'
        }
        self.set_init(d_id, switch)

    def symbol(self):
        return '$'


class PillarBase(object):
    gan = None
    zhi = None

    def __init__(self, g, z):
        if isinstance(g, Gan) and isinstance(z, Zhi):
            self.gan = g
            self.zhi = z
        else:
            raise (TypeError, u"PillarBase __init__ need Gan(%s) and Zhi(%s)." % (type(g), type(z)))

    @staticmethod
    def get_year_pillar(d):
        """
            获取年柱
        :param d: 日期 1991010113
        """
        ed = (int(d[:4])-1924) % 60 + 1
        try:
            return g_eight_60[ed][0:3], g_eight_60[ed][3:]
        except KeyError:
            raise (KeyError, u"dictionary must be first run init_data().")

    @staticmethod
    def get_month_pillar(d):
        year_pillar = PillarBase.get_year_pillar(d)
        temp = int(d[4:6])-10
        if temp < 0:
            temp += 12
        month_zhi = str(temp % 12)
        year_pillar_gan = year_pillar[0]
        month_gan = 1
        if year_pillar_gan in ('甲', '己'):
            month_gan = 3
        elif year_pillar_gan in ('乙', '庚'):
            month_gan = 5
        elif year_pillar_gan in ('丙', '辛'):
            month_gan = 7
        elif year_pillar_gan in ('丁', '壬'):
            month_gan = 9

        for i in range(1, int(d[4:6])):
            month_gan += 1
            if month_gan == 11:
                month_gan = 1

        if month_zhi == '10':
            month_zhi = 'A'
        elif month_zhi == '11':
            month_zhi = 'B'
        elif month_zhi == '12':
            month_zhi = '0'
        return Gan(str(month_gan)).to_chinese(), Zhi(month_zhi).to_chinese()

    @staticmethod
    def get_day_pillar(d):
        st = datetime.datetime.strptime("19240111", "%Y%m%d")
        ed = datetime.datetime.strptime(d[:8], "%Y%m%d")
        days = (ed-st).days % 60 + 1
        try:
            return g_eight_60[days][0:3], g_eight_60[days][3:]
        except KeyError:
            raise (KeyError, u"dictionary must be first run init_data().")

    @staticmethod
    def get_hour_pillar(d):
        """
            甲己还加甲，乙庚丙做初。
            丙辛从戊起，丁壬庚子居。
            戊癸何处去？壬子是真途。
            23~1:1 >>>>
        """
        hour = int(d[8:10])
        switch = dict()
        zhi_serial = 1
        for i in range(1, 25):
            if i == 24:
                key = 0
            else:
                key = i

            if key % 2 == 1:
                zhi_serial += 1

            if zhi_serial == 13:
                zhi_serial = 1

            value = str(zhi_serial)
            if zhi_serial == 10:
                value = 'A'
            elif zhi_serial == 11:
                value = 'B'
            elif zhi_serial == 12:
                value = '0'
            switch[key] = value

        day_pillar_gan = PillarBase.get_day_pillar(d)[0]

        gan = 9
        if day_pillar_gan in ('甲', '己'):
            gan = 1
        elif day_pillar_gan in ('乙', '庚'):
            gan = 3
        elif day_pillar_gan in ('丙', '辛'):
            gan = 5
        elif day_pillar_gan in ('丁', '壬'):
            gan = 7

        ed = hour / 2
        if hour % 2 == 1:
            ed += 1
        for i in range(0, ed):
            gan += 1
            if gan == 11:
                gan = 1

        return Gan(str(gan)).to_chinese(), Zhi(switch[hour]).to_chinese()


class YearPillar(PillarBase):
    """
        年柱
    """
    def __init__(self, d):
        g, z = PillarBase.get_year_pillar(d)
        PillarBase.__init__(self, Gan(g), Zhi(g))


class MonthPillar(PillarBase):
    """
        月柱
    """
    def __init__(self, d):
        g, z = PillarBase.get_month_pillar(d)
        PillarBase.__init__(self, Gan(g), Zhi(g))


class DayPillar(PillarBase):
    """
        日柱
    """
    def __init__(self, d):
        g, z = PillarBase.get_day_pillar(d)
        PillarBase.__init__(self, Gan(g), Zhi(g))


class HourPillar(PillarBase):
    """
        时柱
    """
    def __init__(self, d):
        g, z = PillarBase.get_hour_pillar(d)
        PillarBase.__init__(self, Gan(g), Zhi(g))


class People(object):
    def __init__(self, d):
        self._eight = {
            'year': YearPillar(d),
            'month': MonthPillar(d),
            'day': DayPillar(d),
            'hour': HourPillar(d)
        }

if __name__ == '__main__':
    init_data()
