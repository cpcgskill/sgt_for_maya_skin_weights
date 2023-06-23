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

import contextlib

import cpmel.cmds as cc

from skinkit._utils import *
import skinkit.maya_add_command as maya_add_command

maya_add_command.init_maya_add_command()


class WeightEditor(object):
    def __init__(self, mesh):
        self.mesh = cc.new_object(mesh)
        self.vtx_count = len(list(self.mesh.vtx))
        self.skin_node = find_skin_cluster_node(self.mesh)
        self.skin_joint_list = find_skin_joint_list(self.skin_node)
        self.skin_joint_count = len(self.skin_joint_list)
        self.all_joint_index = range(self.skin_joint_count)

        self.weights = self.skin_node.get_weights(self.mesh.vtx, self.all_joint_index)
        self.weights = [
            self.weights[i * self.skin_joint_count: i * self.skin_joint_count + self.skin_joint_count]
            for i in range(self.vtx_count)
        ]
        self.weights_shape = (len(self.weights), len(self.weights[0]))

    def save_weights(self):
        weights = [t for i in self.weights for t in i]
        self.skin_node.unsafe_set_weights(self.mesh.vtx, self.all_joint_index, weights)
        return self

    def parse_joint_index(self, joint):
        try:
            return self.skin_joint_list.index(joint)
        except ValueError:
            raise ValueError('解析关节索引失败')

    def set_vtx_weights(self, vtx_index, in_weights, joint_list=None):
        if joint_list is None:
            index_list = self.all_joint_index
        else:
            index_list = [self.parse_joint_index(i) for i in joint_list]
        outer_index_list = list(set(self.all_joint_index) - set(index_list))

        main_weights = self.weights[vtx_index]
        item_weights_sum = sum(main_weights)
        if item_weights_sum > 0.000001:
            main_weights = new_float_array((i / item_weights_sum for i in main_weights))

            # 如果有小于0的权重便将它修改为零
            in_weights = [0 if i < 0 else i for i in in_weights]
            # 如果输入的权重之和大于1则规格化权重
            in_weights_sum = sum(in_weights)
            if in_weights_sum > 1:
                in_weights = new_float_array((i / in_weights_sum for i in in_weights))
                in_weights_sum = 1

            # 将要被设置的权重的旧值
            old_weights = [main_weights[i] for i in index_list]
            old_weights_sum = sum(old_weights)

            outer_weights = [main_weights[i] for i in outer_index_list]
            outer_weights_sum = sum(outer_weights)
            if outer_weights_sum > 0.000001:
                scaling_parameter_for_outer_weights = [i / outer_weights_sum for i in outer_weights]
            else:
                scaling_parameter_for_outer_weights = [1 / len(outer_weights) for i in outer_weights]

            outer_weights = [
                w - ((in_weights_sum - old_weights_sum) * sp_w)
                for w, sp_w in zip(outer_weights, scaling_parameter_for_outer_weights)
            ]

            for i, w in zip(index_list, in_weights):
                main_weights[i] = w
            for i, w in zip(outer_index_list, outer_weights):
                main_weights[i] = w
            self.weights[vtx_index] = main_weights
            return self
        else:
            in_weights_sum = sum(in_weights)
            if in_weights_sum > 0.000001:
                in_weights = new_float_array((i / in_weights_sum for i in in_weights))
                for i, w in zip(index_list, in_weights):
                    main_weights[i] = w
                self.weights[vtx_index] = main_weights
                return self
            else:
                return self

    def get_vtx_weights(self, vtx_index, joint_list=None):
        if joint_list is None:
            index_list = self.all_joint_index
        else:
            index_list = [self.parse_joint_index(i) for i in joint_list]
        weights = self.weights[vtx_index]
        return new_float_array((weights[i] for i in index_list))

    def set_joint_list_weights(self, in_weights, joint_list=None):
        for id_, w in enumerate(in_weights):
            self.set_vtx_weights(id_, w, joint_list)
        return self

    def _get_joint_list_weights(self, joint_list=None):
        for id_, _ in enumerate(self.mesh.vtx):
            yield self.get_vtx_weights(id_, joint_list)

    def get_joint_list_weights(self, joint_list):
        return list(self._get_joint_list_weights(joint_list))

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        print_weights = self.weights[:10] if len(self.weights) > 10 else self.weights
        print_weights = [[t for t in i] for i in print_weights]
        print_weights_str = ', '.join([str(i) for i in print_weights])
        print_weights_str = '[{}, ...]'.format(print_weights_str) if len(self.weights) > 10 else '[{}]'.format(
            print_weights_str)
        return "WeightsEditor(shape={}, weights={})".format(
            self.weights_shape,
            print_weights_str,
        )


@contextlib.contextmanager
def edit_weights_block(mesh):
    mesh = cc.new_object(mesh)
    skin = find_skin_cluster_node(mesh)
    old_weights = skin.get_weights(mesh.vtx, [i for i in range(len(cc.skinCluster(skin, q=True, inf=True)))])
    yield
    mesh = cc.new_object(mesh)
    skin = find_skin_cluster_node(mesh)
    new_weights = skin.get_weights(mesh.vtx, [i for i in range(len(cc.skinCluster(skin, q=True, inf=True)))])

    def read():
        skin.unsafe_set_weights(mesh.vtx, [i for i in range(len(cc.skinCluster(skin, q=True, inf=True)))], new_weights)

    def undo():
        skin.unsafe_set_weights(mesh.vtx, [i for i in range(len(cc.skinCluster(skin, q=True, inf=True)))], old_weights)

    maya_add_command.add_command(read, read, undo)


__all__ = ['WeightEditor', 'edit_weights_block']
