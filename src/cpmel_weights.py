# -*-coding:utf-8 -*-
u"""
:创建时间: 2022/5/4 14:38
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:QQ: 2921251087
:爱发电: https://afdian.net/@Phantom_of_the_Cang
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127

"""
from __future__ import unicode_literals, print_function
import contextlib

import maya.cmds as mc
import cpmel.cmds as cc
import maya_add_command

maya_add_command.init_maya_add_command()


def skin_cluster_node(mesh):
    # 广度优先遍历搜索得到所有蒙皮节点
    skin = [i for i in mc.listHistory(mesh, bf=True) if mc.objectType(i) == "skinCluster"]
    return skin[0]


class WeightsEditor(object):
    def __init__(self, mesh):
        self.mesh = cc.new_object(mesh)
        skin = skin_cluster_node(self.mesh.name())
        self.skin = cc.new_object(skin)
        # self.old_weights = skin.get_weights(mesh.vtx, [i for i in range(len(cc.skinCluster(skin, q=True, inf=True)))])

    def _joint_to_inf(self, joint):
        joint = cc.new_object(joint)
        return [hash(i) for i in cc.skinCluster(self.skin, q=True, inf=True)].index(hash(joint))

    def get_joint_weights(self, joint):
        inf = self._joint_to_inf(joint)
        return self.skin.get_weights(self.mesh.vtx, [inf])

    def set_joint_weights(self, joint, weights):
        inf = self._joint_to_inf(joint)
        self.skin.unsafe_set_weights(self.mesh.vtx, [inf], weights)

    # def set_joint_list_weights(self, joint_list, weights):
    #     for j, w in zip(joint_list, zip(*weights)):
    #         self.set_joint_weights(j, w)

    def set_joint_list_weights(self, joint_list, weights):
        infs = [self._joint_to_inf(i) for i in joint_list]
        self.skin.unsafe_set_weights(self.mesh.vtx, infs, [t for i in weights for t in i])


@contextlib.contextmanager
def weights_editor_ctx(mesh):
    mesh = cc.new_object(mesh)
    skin = skin_cluster_node(mesh.name())
    skin = cc.new_object(skin)
    un_weights = skin.get_weights(mesh.vtx, [i for i in range(len(cc.skinCluster(skin, q=True, inf=True)))])
    yield WeightsEditor(mesh)
    mesh = cc.new_object(mesh)
    skin = skin_cluster_node(mesh.name())
    skin = cc.new_object(skin)
    new_weights = skin.get_weights(mesh.vtx, [i for i in range(len(cc.skinCluster(skin, q=True, inf=True)))])
    skin.unsafe_set_weights(mesh.vtx, [i for i in range(len(cc.skinCluster(skin, q=True, inf=True)))], new_weights)

    def read():
        skin.unsafe_set_weights(mesh.vtx, [i for i in range(len(cc.skinCluster(skin, q=True, inf=True)))], un_weights)

    def undo():
        skin.unsafe_set_weights(mesh.vtx, [i for i in range(len(cc.skinCluster(skin, q=True, inf=True)))], new_weights)

    maya_add_command.write_undo_queue(read, undo)


if __name__ == "__main__":
    with weights_editor_ctx(cc.selected()[0]) as w_ctx:
        w_ctx.get_joint_weights('Head_M')
