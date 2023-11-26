# -*-coding:utf-8 -*-
"""
:创建时间: 2022/9/9 4:22
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

"""
from __future__ import unicode_literals, print_function, division

import functools
import logging
import os
import time
import contextlib

import cpmel.cmds as cc


from skinkit.weights import WeightEditor, edit_weights_block
from parse_data.all import *
from parse_data.check import check_data

PATH = os.path.dirname(os.path.abspath(__file__))
NET_PATH = os.sep.join([PATH, "net.pt"])
DEBUG = True


def show_message(*message):
    logging.warning(' '.join(message))
    cc.refresh()


@contextlib.contextmanager
def timing(work_name):
    # if IS_PRINT:
    show_message("正在执行 {}".format(work_name))
    # else:
    #     cc.warning("正在执行 {}".format(work_name))
    #     cc.refresh()
    start = time.clock()
    yield
    end = time.clock()
    # if IS_PRINT:
    show_message("执行 {} 耗时 {}".format(work_name, end - start))
    # else:
    #     cc.warning("执行 {} 耗时 {}".format(work_name, end - start))
    #     cc.refresh()


def parse_source_data(ctx, source_object_list, preconvolution):
    # with timing('扫描焦点视图'):
    #     view_data = expand_data(parse_focus_view_data(ctx, 10, 10, 10), size=4)
    # if DEBUG:
    #     check_data(view_data)
    point_data_list = []
    with timing('解析顶点数据'):
        for i in source_object_list:
            with timing('解析顶点point数据'):
                data = parse_vertex_point_data_from_transform_node_translation(ctx, cc.new_object(i))
                if DEBUG:
                    check_data(data)
                point_data_list.append(data)
            with timing('解析顶点distance数据'):
                data = parse_vertex_distance_data_from_transform_node_translation(ctx, cc.new_object(i))
                if DEBUG:
                    check_data(data)
                point_data_list.append(data)
            with timing('解析顶点normal数据'):
                data = parse_std_mesh_vertex_normal_data(ctx)
                if DEBUG:
                    check_data(data)
                point_data_list.append(data)

    with timing('合并数据'):
        point_data_list = merge_and_expand_vertex_data(*point_data_list)
    with timing('卷积数据'):
        this_point_data_list = point_data_list
        point_data_list = [this_point_data_list]

        for i in range(preconvolution):
            this_point_data_list = parse_smoothed_data_by_mesh(ctx, this_point_data_list)
            point_data_list.append(this_point_data_list)
        # print('point_data_list:', point_data_list)
        point_data_list = merge_and_expand_vertex_data(*point_data_list)
    return point_data_list


def parse_label_data(ctx, skin_joint_list):
    with timing('生成标签数据'):
        data = parse_vertex_skin_weight_data_from_joint_list(ctx, skin_joint_list)
    if DEBUG:
        check_data(data)
    return data


def keep_select_list_wrapper(fn):
    @functools.wraps(fn)
    def _(*args, **kwargs):
        sel = cc.selected()
        try:
            return fn(*args, **kwargs)
        finally:
            cc.select(sel, r=True)

    return _


@contextlib.contextmanager
def with_parse_data_ctx(mesh, source_object_list):
    print('with_parse_data_ctx args', (mesh, source_object_list))
    std_center_and_scale = None
    if len(source_object_list) > 1:
        bounding_box_min, bounding_box_max = object_bounding_box_from_point_object(*source_object_list)
        std_center_and_scale = bounding_box_to_center_and_std_scale(bounding_box_min, bounding_box_max)
        print('with_parse_data_ctx std_center_and_scale', std_center_and_scale)

        # center, scale = std_center_and_scale
        # cc.polyCube(n='debug_box')[0].set_translation(center).set_scale((scale, scale, scale))

    with Ctx(mesh, std_center_and_scale) as ctx:
        yield ctx


@keep_select_list_wrapper
def parse_run_data(mesh, source_object_list, preconvolution):
    print('parse_run_data args', (mesh, source_object_list))
    with with_parse_data_ctx(mesh, source_object_list) as ctx:
        source_data = parse_source_data(ctx, source_object_list, preconvolution)
        print('source_data size', len(source_data[0]))
        print('source_data item', source_data[0])
    return list(source_data)
    # print('parse_run_data args', (mesh, head_box_object, source_object_list))
    # with Ctx(mesh, None if head_box_object is None else object_center_and_std_scale(head_box_object)) as ctx:
    #     source_data = parse_source_data(ctx, source_object_list)
    #     print('source_data size', len(source_data[0]))
    #     print('source_data item', source_data[0])
    # return list(source_data)
    # data = net_run_callback(data)


@keep_select_list_wrapper
def set_skin_weight(mesh, skin_joint_list, data):
    print('set_skin_weight args', (mesh, skin_joint_list, data[:100]))
    with edit_weights_block(mesh):
        w = WeightEditor(mesh)
        data = [[t if t > 0.03 else 0 for t in i] for i in data]
        w.set_joint_list_weights(data, skin_joint_list)
        w.save_weights()


@keep_select_list_wrapper
def parse_train_data(mesh, source_object_list, skin_joint_list, preconvolution):
    print('parse_train_data args', (mesh, source_object_list, skin_joint_list))
    with with_parse_data_ctx(mesh, source_object_list) as ctx:
        source_data = parse_source_data(ctx, source_object_list, preconvolution)
        label_data = parse_label_data(ctx, skin_joint_list)
        print('source_data size', len(source_data[0]))
        print('label_data size', len(label_data[0]))
        print('source_data item', source_data[0])
        print('label_data item', label_data[0])
        return list(merge_vertex_data(source_data, label_data))


__all__ = ['parse_run_data', 'set_skin_weight', 'parse_train_data']
