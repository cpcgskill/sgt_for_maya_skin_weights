# -*-coding:utf-8 -*-
"""
:创建时间: 2022/9/12 2:43
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

"""
from __future__ import unicode_literals, print_function, division

import json


def check_data(data, identity=None):
    test_str = json.dumps(data)
    if test_str.find('NaN') != -1:
        raise ValueError('find a NaN in data, data identity = "{}"'.format(identity))
    if test_str.find('Infinity') != -1:
        raise ValueError('find a Infinity in data, data identity = "{}"'.format(identity))


__all__ = ['check_data']

if __name__ == '__main__':
    try:
        check_data(json.loads('[NaN]'), identity='test check Nan of data')
    except ValueError as ex:
        print('check_data works fine, ValueError meg: \n', ex.message)
    try:
        check_data(json.loads('[Infinity]'), identity='test check Infinity of data')
    except ValueError as ex:
        print('check_data works fine, ValueError meg: \n', ex.message)
    try:
        check_data(json.loads('[-Infinity]'), identity='test check -Infinity of data')
    except ValueError as ex:
        print('check_data works fine, ValueError meg: \n', ex.message)
