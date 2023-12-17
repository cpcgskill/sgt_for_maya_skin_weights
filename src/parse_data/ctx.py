# -*-coding:utf-8 -*-
"""
:创建时间: 2022/9/7 7:16
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
from parse_data.std_func import create_std_mesh_from_std_center_and_scale, object_center_and_std_scale


class Ctx(object):
    def __init__(self, source_mesh, std_center_and_scale=None):
        self.orig_mesh = cc.new_object(source_mesh)
        if std_center_and_scale is None:
            self.std_center_and_scale = object_center_and_std_scale(source_mesh)
        else:
            self.std_center_and_scale = std_center_and_scale
        self.std_center, self.std_scale = self.std_center_and_scale
        self.std_mesh = create_std_mesh_from_std_center_and_scale(source_mesh, self.std_center_and_scale)

    def standardization_point(self, point):
        """
        标准化点信息

        :type point: (float, float, float)
        :rtype: List[(float, float, float)]
        """
        point = (
            point[0] - self.std_center[0],
            point[1] - self.std_center[1],
            point[2] - self.std_center[2],
        )
        point = (
            point[0] / self.std_scale,
            point[1] / self.std_scale,
            point[2] / self.std_scale,
        )
        return point

    def unstandardization_point(self, point):
        """
        反标准化点信息

        :type point: (float, float, float)
        :rtype: List[(float, float, float)]
        """
        point = (
            point[0] * self.std_scale,
            point[1] * self.std_scale,
            point[2] * self.std_scale,
        )
        point = (
            point[0] + self.std_center[0],
            point[1] + self.std_center[1],
            point[2] + self.std_center[2],
        )
        return point

    def clear(self):
        return cc.delete(self.std_mesh)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clear()


__all__ = ['Ctx']

if __name__ == '__main__':
    def test():
        from maya_test_tools import open_file, question_open_maya_gui

        cc.eval('''polySphere -r 4 -sx 4 -sy 3 -ax 0 1 0 -cuv 2 -ch 1;''')
        orig_mesh = cc.selected()[0]
        print('new Ctx', Ctx(orig_mesh, ((0, 1, 0), 1.5)))
        print('auto new Ctx', Ctx(orig_mesh))

        question_open_maya_gui()


    test()
