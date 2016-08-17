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
import copy
from DateConversion import *
import JieQi
import infomations

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
            '1': u'甲',
            '2': u'乙',
            '3': u'丙',
            '4': u'丁',
            '5': u'戊',
            '6': u'己',
            '7': u'庚',
            '8': u'辛',
            '9': u'壬',
            '0': u'癸'
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
            '1': u'子',
            '2': u'丑',
            '3': u'寅',
            '4': u'卯',
            '5': u'辰',
            '6': u'巳',
            '7': u'午',
            '8': u'未',
            '9': u'申',
            'A': u'酉',
            'B': u'戌',
            '0': u'亥'
        }
        self.set_init(d_id, switch)

    def symbol(self):
        return '$'


class PillarBase(object):
    @staticmethod
    def get_year_pillar(d):
        """
            获取年柱
        :param d: 日期 1991010113
        """
        ed = (int(d[:4])-1924) % 60 + 1
        try:
            return g_eight_60[ed][0:1], g_eight_60[ed][1:]
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
        converter = LunarSolarConverter()

        d_date = datetime.datetime.strptime(d[:8], "%Y%m%d")
        f_data = Lunar(d_date.year, d_date.month, d_date.day, False)
        solar_date = converter.LunarToSolar(f_data)
        solar_date = vars(solar_date)
        solar_date = "%d%02d%02d" % (solar_date['solarYear'], solar_date['solarMonth'], solar_date['solarDay'])
        st = datetime.datetime(
            year=int(solar_date[0:4]),
            month=1,
            day=1
        )
        ed = datetime.datetime.strptime(solar_date, "%Y%m%d")
        seq = 0
        year_num = int(solar_date[2:4])
        if year_num == 0:
            year_num = 100
        if 1901 <= int(d[0:4]) <= 2000:
            seq = 5*(year_num-1) + ((year_num-1)/4) + 15 + (ed-st).days + 1
        elif 2001 <= int(d[0:4]) <= 2100:
            seq = 5*(year_num-1) + ((year_num-1)/4) + (ed-st).days + 1
        seq %= 60
        if not seq:
            seq = 60

        return g_eight_60[seq][0], g_eight_60[seq][1]

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

    @staticmethod
    def get_yun_pillar(birth, f_data, man=True):
        """
            获取大运或者小运的柱,根据f_data
        :param birth: 生日
        :param f_data: 查找的日期
        :param man:是否是男的
        :return: 天干, 地支
        """
        calc_order = 1
        gan, zhi = PillarBase.get_year_pillar(birth)
        if man and gan not in (u'甲', u'丙', u'戊', u'庚', u'壬'):
            calc_order = -1
        elif not man and gan in (u'甲', u'丙', u'戊', u'庚', u'壬'):
            calc_order = -1

        st_jz = g_eight_60[u"".join(PillarBase.get_month_pillar(birth))]
        count_day = 0
        birth_date = datetime.datetime.strptime(birth, "%Y%m%d")
        converter = LunarSolarConverter()
        if calc_order == 1:
            while 1:
                ln_birth = vars(converter.LunarToSolar(
                    Lunar(birth_date.year, birth_date.month, birth_date.day, False)
                ))
                ln_birth = "%d%02d%02d" % (ln_birth['solarYear'], ln_birth['solarMonth'], ln_birth['solarDay'])
                ln = datetime.datetime.strptime(ln_birth, "%Y%m%d")
                if JieQi.Lunar(ln).ln_jie() and infomations.JIEQI[JieQi.Lunar(ln).ln_jie()] % 2:
                    break
                count_day += 1
                birth_date += datetime.timedelta(days=1)
        else:
            while 1:
                ln_birth = vars(converter.LunarToSolar(
                    Lunar(birth_date.year, birth_date.month, birth_date.day, False)
                ))
                ln_birth = "%d%02d%02d" % (ln_birth['solarYear'], ln_birth['solarMonth'], ln_birth['solarDay'])
                ln = datetime.datetime.strptime(ln_birth, "%Y%m%d")
                if JieQi.Lunar(ln).ln_jie() and infomations.JIEQI[JieQi.Lunar(ln).ln_jie()] % 2:
                    break
                count_day += 1
                birth_date -= datetime.timedelta(days=1)

        st_big_yun = count_day / 3
        if count_day % 3 != 0 and st_big_yun != 10:
            st_big_yun += 1

        if f_data - int(birth[0:4]) < st_big_yun:
            pass
        else:
            for i in range((f_data - int(birth[0:4]) - st_big_yun)/10+1):
                st_jz -= 1
                if st_jz == 0:
                    st_jz = 60
        return g_eight_60[st_jz][0], g_eight_60[st_jz][1]


def get_jieqi_seq(seq, year):
    """
        获取节气
    :param seq:节气编号,从1开始
    :param year:指定年份,新历
    :return: YYYYMMDD  新历
    """
    st_d = datetime.datetime.strptime("%s%02d01" % (year, (seq+1)/2+1), "%Y%m%d")
    curr_d = st_d
    while curr_d.month == st_d.month:
        ln = JieQi.Lunar(curr_d)
        if ln.ln_jie() and infomations.JIEQI[ln.ln_jie()] == seq:
            return ln.localtime.strftime("%Y%m%d")
        curr_d += datetime.timedelta(days=1)
    raise Exception(u"居然找不到节气?")


def get_jieqi_name(name, year):
    return get_jieqi_seq(infomations.JIEQI[unicode(name)], year)


def get_eight_all(birth, find_data, is_nong=False, man=True):
    """
        输出八字大运流年流月
    :param birth: 生日
    :param find_data: 日期
    :param is_nong: 是否是农历
    :return:
    """
    assert isinstance(birth, datetime.datetime)
    assert isinstance(find_data, datetime.datetime)
    eight = list()
    converter = LunarSolarConverter()
    if not is_nong:
        nongli = converter.SolarToLunar(Solar(birth.year, birth.month, birth.day))
        f_data = converter.SolarToLunar(Solar(find_data.year, find_data.month, find_data.day))
        solar_date = Solar(find_data.year, find_data.month, find_data.day)
    else:
        nongli = Lunar(birth.year, birth.month, birth.day, False)
        f_data = Lunar(find_data.year, find_data.month, find_data.day, False)
        solar_date = converter.LunarToSolar(f_data)

    nongli = vars(nongli)  # lunarDay,lunarMonth, lunarYear
    f_data = vars(f_data)  # lunarDay,lunarMonth, lunarYear
    solar_date = vars(solar_date)
    nongli = "%d%02d%02d" % (nongli['lunarYear'], nongli['lunarMonth'], nongli['lunarDay'])
    f_data = "%d%02d%02d" % (f_data['lunarYear'], f_data['lunarMonth'], f_data['lunarDay'])
    solar_date = "%d%02d%02d" % (solar_date['solarYear'], solar_date['solarMonth'], solar_date['solarDay'])
    eight.append(PillarBase.get_year_pillar(nongli))
    eight.append(PillarBase.get_month_pillar(nongli))
    eight.append(PillarBase.get_day_pillar(nongli))
    eight.append(PillarBase.get_hour_pillar(nongli+str(birth.hour)))
    eight.append(PillarBase.get_yun_pillar(nongli, int(solar_date[0:4]), man))
    eight.append(PillarBase.get_year_pillar(f_data))
    eight.append(PillarBase.get_month_pillar(f_data))
    eight.append(PillarBase.get_day_pillar(f_data))
    return eight

if __name__ == '__main__':
    init_data()
    # print get_jieqi_seq(7, 1988)
    # print get_jieqi_name(u"立春", 1988)
    # a = PillarBase.get_yun_pillar('19911127', 2078)
    # print a[0], a[1]

    t_birth = datetime.datetime.strptime("1992010116", "%Y%m%d%H")
    t_find_date = datetime.datetime.strptime("20050101", "%Y%m%d")
    for i in get_eight_all(t_birth, t_find_date, is_nong=False):
        for j in i:
            print j,
        print
