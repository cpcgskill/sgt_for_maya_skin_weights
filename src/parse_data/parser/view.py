# -*-coding:utf-8 -*-
"""
:创建时间: 2022/9/7 10:01
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

"""
from __future__ import unicode_literals, print_function, division
import cpmel.cmds as cc
from maya.api.OpenMaya import MPoint, MMeshIntersector, MPointOnMesh
from parse_data.ctx import Ctx

if False:
    from typing import List, Tuple


def parse_focus_view_data(ctx, x_count, y_count, z_count, is_normal=False, debug=False):
    """
    在焦点视图（也就是标准盒子）中进行扫描 （x_count, y_count, z_count）次

    :type ctx: Ctx
    :type x_count: int
    :type y_count: int
    :type z_count: int
    :param is_normal: 是否读取最近点的法线信息
    :type is_normal: bool
    :param debug: debug参数如果为True则返回对应的点
    :type debug: bool
    :rtype: List[List[List[float]]] or List[List[List[Tuple[float, float, float, float]]]]
    :return: List[List[List[扫描点与对应最近点的距离]]] or
             List[List[List[(扫描点与对应最近点的距离, 扫描点与对应最近点的法线x, 扫描点与对应最近点的法线y, 扫描点与对应最近点的法线z)]]]
    """
    mfn = ctx.std_mesh.shape.api2_m_fn()
    mm_intersector = MMeshIntersector().create(mfn.object())
    x_list = []
    for x_id in range(x_count):
        y_list = []
        for y_id in range(y_count):
            z_list = []
            for z_id in range(z_count):
                p = MPoint(-0.5 + (x_id / (x_count - 1)), -0.5 + (y_id / (y_count - 1)), -0.5 + (z_id / (z_count - 1)))
                point_on_mesh = mm_intersector.getClosestPoint(p)
                dis = p.distanceTo(MPoint(point_on_mesh.point))
                if is_normal:
                    data = (dis, point_on_mesh.normal.x, point_on_mesh.normal.z, point_on_mesh.normal.z)
                else:
                    data = dis
                if debug:
                    z_list.append((p, data))
                else:
                    z_list.append(data)
            y_list.append(z_list)
        x_list.append(y_list)
    return x_list


__all__ = ['parse_focus_view_data']

if __name__ == '__main__':
    def test():
        from maya_test_tools import open_file, question_open_maya_gui

        cc.eval('''polySphere -r 4 -sx 4 -sy 3 -ax 0 1 0 -cuv 2 -ch 1;''')
        orig_mesh = cc.selected()[0]
        ctx = Ctx(orig_mesh)

        test_data = parse_focus_view_data(ctx, 10, 10, 10, debug=True)
        print('parse_focus_view_data', test_data)

        for yd in test_data:
            for zd in yd:
                for p, dis in zd:
                    loc = cc.spaceLocator(n='parse_focus_view_data_loc')[0]
                    loc.set_translation((p.x, p.y, p.z), ws=True)
                    loc.set_scale([max(0.1 - dis, 0)]*3, ws=True)

        question_open_maya_gui()


    test()
