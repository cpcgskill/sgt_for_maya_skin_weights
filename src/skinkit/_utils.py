# -*-coding:utf-8 -*-
"""
:创建时间: 2022/9/20 11:18
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

"""
from __future__ import unicode_literals, print_function, division
from array import array
import cpmel.cmds as cc
from cpapi.all import *
import maya.cmds as mc


def new_float_array(source):
    return array('f', source)


def find_skin_cluster_node_list(mesh):
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
            yield i


def find_skin_cluster_node(mesh):
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


def find_skin_joint_list(skin_node):
    skin_node = cc.new_object(skin_node)
    return mc.skinCluster(skin_node.name(), q=True, inf=True)


__all__ = [
    'new_float_array',
    'find_skin_cluster_node_list',
    'find_skin_cluster_node',
    'find_skin_joint_list',
]
