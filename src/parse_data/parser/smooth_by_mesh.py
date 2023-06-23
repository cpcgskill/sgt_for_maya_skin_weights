# -*-coding:utf-8 -*-
"""
:创建时间: 2023/4/23 20:13
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

"""
from __future__ import unicode_literals, print_function, division

if False:
    from typing import *

from cpapi.all import *

from parse_data.ctx import Ctx


def parse_smoothed_data_by_mesh(ctx, data_list):
    """
    从原点获得顶点的点数据， 获得的点数据是相对与输入原点的标准模型顶点数据

    :type ctx: Ctx
    :type data_list: List[Tuple]
    :rtype: List[(float, float, float)]
    """
    vtx_it = MItMeshVertex(ctx.std_mesh.api1_m_dag_path())
    _test_int_ptr = MScriptUtil().asIntPtr()
    out_list = []
    for _, data_index in zip(vtx_it, range(len(data_list))):
        vtx_it.setIndex(data_index, _test_int_ptr)
        data_indexs = MIntArray()
        vtx_it.getConnectedVertices(data_indexs)
        data_indexs.append(data_index)
        out_list.append([sum(i) / data_indexs.length() for i in zip(*[data_list[i] for i in data_indexs])])
    return out_list


__all__ = ['parse_smoothed_data_by_mesh']
