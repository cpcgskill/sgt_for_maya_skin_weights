# -*-coding:utf-8 -*-
"""
:创建时间: 2022/9/9 7:05
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
import maya.api.OpenMaya as om2
import cpmel.cmds as cc
from parse_data.ctx import Ctx

if False:
    from typing import List, Tuple, AnyStr


# def _parse_mesh_vertex_point_data(mesh):
#     """
#     :type mesh: cc.Transform
#     :rtype: List[om2.MPoint]
#     """
#     mesh_shape = mesh.shape  # type: cc.Mesh
#     mfn = mesh_shape.api1_m_fn()
#     pts = om.MPointArray()
#     mfn.getPoints(pts, om.MSpace.kWorld)
#
#     return [i for i in pts]

def _parse_mesh_vertex_point_data(mesh):
    """
    :type mesh: cc.Transform
    :rtype: List[om2.MPoint]
    """
    mesh_shape = mesh.shape  # type: cc.Mesh
    mfn = mesh_shape.api2_m_fn()
    # pts = om.MPointArray()
    # mfn.getPoints(pts, om2.MSpace.kWorld)
    # pts = om.MPointArray()

    # pts = mfn.getPoints(om2.MSpace.kWorld)
    for i in range(mfn.numVertices):
        yield mfn.getPoint(i)

    # return [i for i in pts]

def parse_vertex_distance_data_from_origin_point(ctx, origin_point=(0, 0, 0)):
    """
    从原点获得顶点的点数据， 获得的点数据是相对与输入原点的标准模型顶点数据

    :type ctx: Ctx
    :type origin_point: (float, float, float)
    :rtype: List[float]
    """
    origin_point = ctx.standardization_point(origin_point)
    origin_point = om2.MPoint(origin_point[0], origin_point[1], origin_point[2])

    pts = _parse_mesh_vertex_point_data(ctx.std_mesh)

    pts = [
        origin_point.distanceTo(i)
        for i in pts
    ]
    return pts


def parse_vertex_distance_data_from_transform_node_translation(ctx, transform):
    """

    :type ctx: Ctx
    :type transform: cc.Transform
    :rtype: List[float]
    """
    transform = cc.new_object(transform)
    return parse_vertex_distance_data_from_origin_point(ctx, transform.get_translation(ws=True))


__all__ = ['parse_vertex_distance_data_from_origin_point', 'parse_vertex_distance_data_from_transform_node_translation']

if __name__ == '__main__':
    def test():
        from maya_test_tools import open_file, question_open_maya_gui

        cc.eval('''polySphere -r 4 -sx 4 -sy 3 -ax 0 1 0 -cuv 2 -ch 1;''')
        orig_mesh = cc.selected()[0]
        ctx = Ctx(orig_mesh)

        test_data_1 = parse_vertex_distance_data_from_origin_point(ctx, (0, 0, 0))
        print('parse_vertex_distance_data_from_origin_point 1', test_data_1)
        # 0.48513047892189287, 0.48513047892189104, 0.48513047892188993, 0.4851304789218896, 0.5163347572834751
        test_data_2 = parse_vertex_distance_data_from_origin_point(ctx, (0, -0.25, 0))
        print('parse_vertex_distance_data_from_origin_point 2', test_data_2)
        test_loc_3 = cc.spaceLocator(n='test_data_3_origin_point_loc')[0].set_translation((3.464, 2, 0), ws=True)
        test_data_3 = parse_vertex_distance_data_from_transform_node_translation(ctx, test_loc_3)
        print('parse_vertex_distance_data_from_transform_node_translation', test_data_2)

        # for i in test_data_1:
        #     cc.spaceLocator(p=i, n='test_data_1_loc')
        # for i in test_data_2:
        #     cc.spaceLocator(p=i, n='test_data_2_loc')
        # for i in test_data_3:
        #     cc.spaceLocator(p=i, n='test_data_3_loc')

        question_open_maya_gui()


    test()
