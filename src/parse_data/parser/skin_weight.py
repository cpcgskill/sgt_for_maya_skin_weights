# -*-coding:utf-8 -*-
"""
:创建时间: 2022/9/9 0:56
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
from cpapi.all import *
from parse_data.ctx import Ctx

if False:
    from typing import List


def _find_skin_cluster_node(mesh):
    """

    :type mesh: cc.Transform
    :rtype: cc.SkinClusterFilter
    """
    mesh = cc.new_object(mesh)
    if isinstance(mesh, cc.Transform):
        mesh = mesh.shape
    # 广度优先遍历搜索得到所有蒙皮节点
    skin_node = [i for i in cc.listHistory(mesh, bf=True) if cc.objectType(i) == "skinCluster"]
    for i in skin_node:
        output_geometry_array = MObjectArray()
        i.api1_m_fn().getOutputGeometry(output_geometry_array)
        output_geometry_set = {cc.new_object(MFnDagNode(j).fullPathName()) for j in output_geometry_array}
        if mesh in output_geometry_set or mesh.parent in output_geometry_set:
            return i
    raise ValueError('The skin node cannot be found')
    # if len(skin_node) < 1:
    #     raise ValueError('The skin node cannot be found')
    # return skin_node[0]


def _calculate_joint_inf(skin_node, joint):
    joint = cc.new_object(joint)
    return [i for i in cc.skinCluster(skin_node, q=True, inf=True)].index(joint)


def parse_vertex_skin_weight_data_from_joint_list(ctx, joint_list, skin_node=None):
    """

    :type ctx: Ctx
    :type joint_list: List[cc.Joint]
    :rtype: List[List[float]]
    """
    if skin_node is None:
        skin_node = _find_skin_cluster_node(ctx.orig_mesh)
    infs = [_calculate_joint_inf(skin_node, i) for i in joint_list]
    weights = skin_node.get_weights(ctx.orig_mesh.vtx, infs)
    return [list(weights[i * len(infs): i * len(infs) + len(infs)]) for i, _ in enumerate(ctx.orig_mesh.vtx)]


__all__ = ['parse_vertex_skin_weight_data_from_joint_list']

if __name__ == '__main__':
    def test():
        from maya_test_tools import open_file, question_open_maya_gui

        cc.eval('''
polySphere -r 1 -sx 20 -sy 20 -ax 0 1 0 -cuv 2 -ch 1;
select -cl  ;
joint -p 0 1 0 ;
select -cl  ;
joint -p 0 -1 0 ;
select -cl  ;
select -r pSphere1 ;
select -r pSphere1 joint1 joint2 ;
SmoothBindSkin;
''')
        orig_mesh = cc.new_object('pSphere1')

        ctx = Ctx(orig_mesh)

        test_data = parse_vertex_skin_weight_data_from_joint_list(ctx, ['joint1', 'joint2'])
        print('parse_vertex_skin_weight_data_from_joint_list', test_data)

        question_open_maya_gui()


    test()
