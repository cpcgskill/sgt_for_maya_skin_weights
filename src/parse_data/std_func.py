# -*-coding:utf-8 -*-
"""
:创建时间: 2022/9/7 6:48
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
from cpmel.cmds import select, duplicate, parent, createNode, xform, delete, ls


def _freeze_all_object_transforms(obj):
    "makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1;"
    cc.makeIdentity(obj, apply=True, t=True, r=True, s=True, n=True, pn=True)
    return obj


def object_bounding_box(*obj):
    """

    :type obj: cc.Transform
    :rtype: ((float, float, float), (float, float, float))
    """
    bounding_box = []
    for i in obj:
        xmin, ymin, zmin, xmax, ymax, zmax = cc.xform(i, q=True, ws=True, bb=True)
        xmax += 1
        xmin -= 1
        ymax += 1
        ymin -= 1
        zmax += 1
        zmin -= 1
        bounding_box.append((xmin, ymin, zmin, xmax, ymax, zmax))
    xmin, ymin, zmin, xmax, ymax, zmax = zip(*bounding_box)
    # xmin, ymin, zmin, xmax, ymax, zmax = cc.xform(*obj, q=True, ws=True, bb=True)

    return (
        (sorted(xmin)[0], sorted(ymin)[0], sorted(zmin)[0]),
        (sorted(xmax)[-1], sorted(ymax)[-1], sorted(zmax)[-1]),
    )


def object_bounding_box_from_point_object(*obj):
    """

    :type obj: cc.Transform
    :rtype: ((float, float, float), (float, float, float))
    """
    bounding_box = []
    for i in obj:
        x, y, z = cc.xform(i, q=True, ws=True, t=True)
        xmax = x + 1
        xmin = x - 1
        ymax = y + 1
        ymin = y - 1
        zmax = z + 1
        zmin = z - 1
        bounding_box.append((xmin, ymin, zmin, xmax, ymax, zmax))
    xmin, ymin, zmin, xmax, ymax, zmax = zip(*bounding_box)
    # xmin, ymin, zmin, xmax, ymax, zmax = cc.xform(*obj, q=True, ws=True, bb=True)

    return (
        (sorted(xmin)[0], sorted(ymin)[0], sorted(zmin)[0]),
        (sorted(xmax)[-1], sorted(ymax)[-1], sorted(zmax)[-1]),
    )


def bounding_box_to_std_scale(bounding_box_min, bounding_box_max):
    """

    :type bounding_box_min: (float, float, float)
    :type bounding_box_max: (float, float, float)
    :rtype: float
    """
    return max((
        bounding_box_max[0] - bounding_box_min[0],
        bounding_box_max[1] - bounding_box_min[1],
        bounding_box_max[2] - bounding_box_min[2]
    ))


def bounding_box_to_center(bounding_box_min, bounding_box_max):
    """

    :type bounding_box_min: (float, float, float)
    :type bounding_box_max: (float, float, float)
    :rtype:  (float, float, float)
    """
    return ((bounding_box_min[0] + bounding_box_max[0]) / 2,
            (bounding_box_min[1] + bounding_box_max[1]) / 2,
            (bounding_box_min[2] + bounding_box_max[2]) / 2)


def bounding_box_to_center_and_std_scale(bounding_box_min, bounding_box_max):
    # 中心
    center = bounding_box_to_center(bounding_box_min, bounding_box_max)
    # 获得标准缩放
    std_scale = bounding_box_to_std_scale(bounding_box_min, bounding_box_max)
    return center, std_scale


def object_std_scale(*obj):
    boundingBoxMin, boundingBoxMax = object_bounding_box(*obj)
    return bounding_box_to_std_scale(boundingBoxMin, boundingBoxMax)


def object_center(*obj):
    boundingBoxMin, boundingBoxMax = object_bounding_box(*obj)
    return bounding_box_to_center(boundingBoxMin, boundingBoxMax)


def object_center_and_std_scale(*obj):
    # 边界框
    bounding_box_min, bounding_box_max = object_bounding_box(*obj)
    # 中心
    center = bounding_box_to_center(bounding_box_min, bounding_box_max)
    # 获得标准缩放
    std_scale = bounding_box_to_std_scale(bounding_box_min, bounding_box_max)
    return center, std_scale


def create_std_mesh_from_std_center_and_scale(poly, std_center_and_scale):
    """

    :type poly: cc.Transform
    :type std_center_and_scale: ((float, float, float), float)
    :rtype: cc.Transform
    """
    select(poly, r=True)
    # 新的多边形
    new_poly = duplicate(rr=True)[0]
    try:
        if new_poly.parent is not None:
            new_poly = parent(new_poly, w=True)[0]
    except RuntimeError:
        pass
    unlock_attrs = [
        'tx', 'ty', 'tz',
        'rx', 'ry', 'rz',
        'sx', 'sy', 'sz',
        'visibility',
    ]
    for i in unlock_attrs:
        # unlock_attr = new_poly.attr(i)
        # if unlock_attr.is_lock():
        new_poly.attr(i).unlock()
    # 获得中心与标准缩放
    center, std_scale = std_center_and_scale
    # 按中心缩放并将中心位置归零
    test_transform = createNode("transform", p=None)
    xform(test_transform, ws=True, t=center)
    parent(new_poly, test_transform)
    xform(test_transform, ws=True, s=(1 / std_scale, 1 / std_scale, 1 / std_scale))
    xform(test_transform, ws=True, t=(0, 0, 0))
    # 清除临时变换节点
    new_poly = parent(new_poly, w=True)[0]
    delete(test_transform)
    # 清空变换
    _freeze_all_object_transforms(new_poly)
    # 将枢轴点设置为对象边界框的中心
    xform(new_poly, cp=True)

    return new_poly


def auto_create_std_mesh(poly):
    """
    使用原始模型计算标准中心和标准缩放然后以计算结果创建标准模型

    :type poly: cc.Transform
    :rtype: cc.Transform
    """
    return create_std_mesh_from_std_center_and_scale(poly, object_center_and_std_scale(poly))


__all__ = [
    'object_bounding_box', 'object_bounding_box_from_point_object',
    'bounding_box_to_std_scale', 'bounding_box_to_center','bounding_box_to_center_and_std_scale',
    'object_std_scale', 'object_center', 'object_center_and_std_scale',
    'create_std_mesh_from_std_center_and_scale', 'auto_create_std_mesh'
]
if __name__ == '__main__':
    def test():
        from maya_test_tools import open_file, question_open_maya_gui

        cc.eval('''
polySphere -r 3 -sx 20 -sy 20 -ax 0 1 0 -cuv 2 -ch 1;
select -cl  ;
joint -p 5 0 0 ;
joint -p -5 0 0 ;
''')
        print('object_bounding_box_from_point_object ',
              object_bounding_box_from_point_object(cc.new_object('joint1'), cc.new_object('joint2')))



        print('object_std_scale ', object_std_scale(cc.new_object('pSphere1'), cc.new_object('joint1')))
        print('object_center ', object_center(cc.new_object('pSphere1'), cc.new_object('joint1')))
        print('auto_create_std_mesh of pSphere1 :', auto_create_std_mesh(cc.new_object('pSphere1')))
        print('object_center_and_std_scale ',
              object_center_and_std_scale(cc.new_object('joint1'), cc.new_object('joint2')))
        print(
            'create_std_mesh_from_std_center_and_scale ',
            create_std_mesh_from_std_center_and_scale(
                cc.new_object('pSphere1'),
                object_center_and_std_scale(cc.new_object('pSphere1'), cc.new_object('joint1'))
            )
        )

        question_open_maya_gui()


    test()
