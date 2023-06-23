# -*-coding:utf-8 -*-
"""
:创建时间: 2022/9/9 7:21
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
import warnings
from array import array
from collections import Iterable

_byte_t = type(b'')
_str_t = type('')


# def expand_data(data):
#     """展开数据"""
#     return array('f', (t for i in data for t in i))
def _expand_data(data):
    for i in data:
        if isinstance(i, Iterable) and (not isinstance(i, (_byte_t, _str_t))):
            for t in i:
                yield t
        else:
            yield i


def expand_data(data, size=1):
    """展开数据"""
    for i in range(size):
        data = list(_expand_data(data))
    return data


def zoom_in_on_data_features(data):
    """放大数据特征"""
    max_data = max(data)
    return array('f', (i * ((i / max_data) ** 2) for i in data))


def merge_vertex_data(*data):
    """合并顶点数据, 也就是vtx[0]数据, vtx[1]数据, ...这样的数据"""
    return zip(*data)


def merge_and_expand_vertex_data(*data):
    """合并并展开顶点数据, 也就是vtx[0]数据, vtx[1]数据, ...这样的数据"""
    data = merge_vertex_data(*data)
    return [expand_data(i) for i in data]


__all__ = ['expand_data', 'zoom_in_on_data_features', 'merge_vertex_data', 'merge_and_expand_vertex_data']

if __name__ == '__main__':
    print('expand_data',
          expand_data([[1, 2, 3], [3, 2, 1], 0, 'aaa']))
    print('zoom_in_on_data_features',
          zoom_in_on_data_features([2, 1, 5, 5, 8, 5, 6, 2, 7, 4, 0, 9, 8, 7, 1, 5, 7, 6, 3, 2, 5, 6, 2, 1]))
    print('merge_vertex_data',
          merge_vertex_data([1, 1, 1, 1], [[1], [1], [1], [1]]))
    print('merge_and_expand_vertex_data',
          merge_and_expand_vertex_data([1, 1, 1, 1], [[1], [1], [1], [1]]))
