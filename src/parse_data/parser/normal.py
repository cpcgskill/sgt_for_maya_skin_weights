# -*-coding:utf-8 -*-
"""
:创建时间: 2022/9/11 3:20
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

"""
from __future__ import unicode_literals, print_function, division
import cpapi.all as om
import cpmel.cmds as cc

from parse_data.ctx import Ctx

if False:
    from typing import List, Tuple, AnyStr


def _parse_mesh_vertex_normal_data(mesh):
    mesh_shape = mesh.shape  # type: cc.Mesh
    mfn = mesh_shape.api1_m_fn()

    normal_array = om.MFloatVectorArray()
    mfn.getVertexNormals(True, normal_array, om.MSpace.kWorld)

    return [(i.x, i.y, i.z) for i in normal_array]


def parse_std_mesh_vertex_normal_data(ctx):
    """
    解析顶点法线数据

    :type ctx: Ctx
    :rtype: List[(float, float, float)]
    """
    return _parse_mesh_vertex_normal_data(ctx.std_mesh)


__all__ = ['parse_std_mesh_vertex_normal_data']

if __name__ == '__main__':
    def test():
        from maya_test_tools import open_file, question_open_maya_gui

        cc.eval('''polySphere -r 4 -sx 4 -sy 3 -ax 0 1 0 -cuv 2 -ch 1;''')
        orig_mesh = cc.selected()[0]
        ctx = Ctx(orig_mesh)

        test_data = parse_std_mesh_vertex_normal_data(ctx)
        print('parse_vertex_normal_data', test_data)

        question_open_maya_gui()


    test()
