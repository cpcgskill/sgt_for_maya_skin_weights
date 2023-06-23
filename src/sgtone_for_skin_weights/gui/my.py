# -*-coding:utf-8 -*-
"""
:创建时间: 2023/3/9 14:16
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

"""
from __future__ import unicode_literals, print_function, division

if False:
    from typing import *

from cpgui.pop_ups import input_text

import cpmel.cmds as cc

from cpform.widget.all import *

from sgtone.core import *

import sgtone_for_skin_weights.config
from sgtone_for_skin_weights.exc import SgtException
from sgtone_for_skin_weights.core import parse_run_data, parse_train_data, set_skin_weight
from sgtone_for_skin_weights.gui.utils import *


# 创建网络的窗口的实现
def create_arg_widget(key_name, is_multi_line=False):
    if is_multi_line:
        return VBoxLayout(childs=[Label(key_name), TextEditWidget()])
    else:
        return HBoxLayout(childs=[Label(key_name), LineEditWidget()])


def create_create_weights_sgt_model_window(user_unique_id, callback=None):
    def _push_callback_func(name, detail, input_joint_list, output_joint_list, is_public):
        input_joint_list = input_joint_list.splitlines()
        output_joint_list = output_joint_list.splitlines()

        if name == '':
            raise SgtException('名称不可为空')
        if len(input_joint_list) < 1:
            raise SgtException('至少需要一个输入关节')
        if len(output_joint_list) < 1:
            raise SgtException('至少需要一个输出关节')

        create_sgt_model(
            user_unique_id,
            name,
            len(input_joint_list) * 7 * (1 + sgtone_for_skin_weights.config.preconvolution),
            len(output_joint_list),
            client_data={
                'model_type': sgtone_for_skin_weights.config.model_type,
                "input_transform_config": input_joint_list,
                "output_transform_config": output_joint_list,
                "detail": detail,
            },
            is_public=is_public,
            callback=callback,
        )

    w = SubmitWidget(
        form=[
            create_arg_widget('名称'),
            create_arg_widget('详情'),
            create_arg_widget('输入对象列表(每行一个)', is_multi_line=True),
            create_arg_widget('输出关节列表(每行一个)', is_multi_line=True),
            CheckBoxWidget(info='是否公开', default_state=False),
        ],
        doit_text='Push',
        func=_push_callback_func
    )

    mydocker(
        name='create_sgt_model_window',
        title='Create',
        form=w,
    )


# 运行和上传模型的实现

def create_add_template_window(user_unique_id, sgt_model_name, client_data, template):
    name_to_template_table = {i['name']: i for i in client_data.get('templates', [])}
    name_to_template_table[template['name']] = template
    client_data['templates'] = list(name_to_template_table.values())

    update_sgt_model_client_data(user_unique_id, sgt_model_name, client_data)


def create_delete_template_window(user_unique_id, sgt_model_name, client_data, template):
    name_to_template_table = {i['name']: i for i in client_data.get('templates', [])}
    name_to_template_table.pop(template['name'])
    client_data['templates'] = list(name_to_template_table.values())

    update_sgt_model_client_data(user_unique_id, sgt_model_name, client_data)


def create_select_template_dialog(user_unique_id, client_data):
    name_to_template_table = {i['name']: i for i in client_data.get('templates', [])}

    selected = create_select_dialog(name_to_template_table.keys())
    if selected is None:
        return None
    else:
        return name_to_template_table[selected]


def create_sgt_model_input_widget(user_unique_id, sgt_model_name, client_data):
    def _create_sgt_model_input_widget(template=None):
        def _add_template(*args):
            template_name = input_text(title='template name')
            if template_name is None:
                return
            data = {
                'name': template_name,
                'skin_mesh_template': skin_mesh_widget.read_data()[0],
                'input_transform_template': input_transform_widget.read_data()[0],
                'output_transform_template': output_transform_widget.read_data()[0],
            }
            create_add_template_window(user_unique_id, sgt_model_name, client_data, data)

        def _load_template(*args):
            selected = create_select_template_dialog(user_unique_id, client_data)
            if selected is not None:
                widget.toggle_to(_create_sgt_model_input_widget(selected))

        def _delete_template(*args):
            template = create_select_template_dialog(user_unique_id, client_data)
            if template is not None:
                create_delete_template_window(user_unique_id, sgt_model_name, client_data, template)

        head_widget = HBoxLayout(
            childs=[
                ButtonWidget(
                    text='加载模板',
                    icon='more-vertical',
                    func=_load_template,
                ),
                ButtonWidget(
                    text='删除模板',
                    icon='delete',
                    func=_delete_template,
                ),
                ButtonWidget(
                    text='添加为模板',
                    icon='save',
                    func=_add_template,
                ),
            ],
            align='left',
        )

        detail = client_data['detail']

        if template is None:
            skin_mesh_widget = SelectWidget(mobject_type='transform')
        else:
            skin_mesh_widget = SelectWidget(mobject_type='transform', text=template['skin_mesh_template'])
        if template is None:
            input_transform_template = ['' for i in client_data['input_transform_config']]
            output_transform_template = ['' for i in client_data['output_transform_config']]
        else:
            input_transform_template = template['input_transform_template']
            output_transform_template = template['output_transform_template']
        input_transform_widget = VBoxLayout(
            childs=[
                HBoxLayout(
                    childs=[
                        Label(text=i),
                        SelectWidget(
                            mobject_type='transform',
                            text=default_value,
                        )
                    ],
                )
                for i, default_value in zip(client_data['input_transform_config'], input_transform_template)
            ]
        )
        output_transform_widget = VBoxLayout(
            childs=[
                HBoxLayout(
                    childs=[
                        Label(text=i),
                        SelectWidget(
                            mobject_type='transform',
                            text=default_value,
                        )
                    ],
                )
                for i, default_value in zip(client_data['output_transform_config'], output_transform_template)
            ]
        )
        input_transform_widget = DataSetWidget(child=input_transform_widget)
        output_transform_widget = DataSetWidget(child=output_transform_widget)

        return VBoxLayout(
            childs=[
                head_widget,
                Label(text=sgt_model_name, font_size=16),
                Label(text='detail:', font_size=12),
                Label(text=detail, font_size=12),
                Label(text='蒙皮模型:', font_size=12),
                skin_mesh_widget,
                Label(text='输入关节:', font_size=12),
                input_transform_widget,
                Label(text='输出关节:', font_size=12),
                output_transform_widget,
            ],
            align='top'
        )

    widget = ToggleWidget(_create_sgt_model_input_widget())
    return widget


def create_run_weights_sgt_model_window(user_unique_id, name, client_data):
    def _run(mesh, input_transform_list, output_transform_list):
        if mesh == '':
            raise SgtException('模型未指定')
        if not cc.objExists(mesh):
            raise SgtException('输入变换{}不存在'.format(repr(mesh)))
        for i in input_transform_list:
            if i == '':
                raise SgtException('需要指定所有输入变换')
            if not cc.objExists(i):
                raise SgtException('输入变换{}不存在'.format(repr(i)))
        for i in output_transform_list:
            if i == '':
                raise SgtException('需要指定所有输出变换')
            if not cc.objExists(i):
                raise SgtException('输出变换{}不存在'.format(repr(i)))
        run_data = parse_run_data(mesh, input_transform_list)
        run_sgt_model(
            user_unique_id,
            name,
            run_data,
            lambda data: set_skin_weight(mesh, output_transform_list, data)
        )

    w = create_sgt_model_input_widget(user_unique_id, name, client_data)
    w = SubmitWidget(
        form=[
            ScrollAreaWidget(widget=w),
        ],
        doit_text='生成权重',
        func=_run,
    )
    mydocker(
        name='run model: {}'.format(name),
        title='run model: {}'.format(name),
        form=w,
    )


def create_upload_weights_sgt_model_train_data_window(user_unique_id, name, client_data):
    def _run(mesh, input_transform_list, output_transform_list):
        if mesh == '':
            raise SgtException('模型未指定')
        if not cc.objExists(mesh):
            raise SgtException('输入变换{}不存在'.format(repr(mesh)))
        for i in input_transform_list:
            if i == '':
                raise SgtException('需要指定所有输入变换')
            if not cc.objExists(i):
                raise SgtException('输入变换{}不存在'.format(repr(i)))
        for i in output_transform_list:
            if i == '':
                raise SgtException('需要指定所有输出变换')
            if not cc.objExists(i):
                raise SgtException('输出变换{}不存在'.format(repr(i)))
        train_data = parse_train_data(mesh, input_transform_list, output_transform_list)
        upload_sgt_model_train_data(user_unique_id, name, train_data)

    w = create_sgt_model_input_widget(user_unique_id, name, client_data)
    w = SubmitWidget(
        form=[
            ScrollAreaWidget(widget=w),
        ],
        doit_text='上传',
        func=_run,
    )
    mydocker(
        name='upload model data: {}'.format(name),
        title='upload model data: {}'.format(name),
        form=w,
    )


# WeightsNet列表视图部分实现

def create_item_widget(user_unique_id, i, refresh_callback=None):
    widget = VBoxLayout(
        childs=[
            Label(
                i['name'],
                font_size=16,
            ),
            Label(
                "inpout {} output {}".format(i['in_size'], i['out_size']),
                font_size=12,
            ),
        ],
    )

    def _create_clone_sgt_model_to_mine_window(*args):
        my_name = input_text(title='your name', text=i['name'])
        if my_name is None:
            return
        clone_sgt_model_to_mine(
            user_unique_id, my_name, i['user_unique_id'], i['name'],
            callback=refresh_callback
        )

    widget = HBoxLayout(childs=[
        widget,
        Button(
            icon='play',
            func=lambda *args: create_run_weights_sgt_model_window(
                user_unique_id,
                i['name'],
                i['client_data'],
            ),
            fixed_width=35, fixed_height=35
        ),
        Button(
            icon='upload',
            func=lambda *args: create_upload_weights_sgt_model_train_data_window(
                user_unique_id,
                i['name'],
                i['client_data'],
            ),
            fixed_width=35, fixed_height=35
        ),
        Button(
            icon='delete',
            func=lambda *args: delete_sgt_model(
                user_unique_id,
                i['name'],
                callback=lambda: widget.close(),
            ),
            fixed_width=35, fixed_height=35
        ),
        Button(
            icon='copy',
            func=_create_clone_sgt_model_to_mine_window,
            fixed_width=35, fixed_height=35
        ),
    ])
    widget = Background(widget, color='#303030')
    return widget


# 我的WeightsNet部件
def create_my_sgt_model_widget(user_unique_id):
    def _make_view():
        data = read_my_sgt_model(user_unique_id)
        data = [i for i in data if i['client_data']['model_type'] == sgtone_for_skin_weights.config.model_type]
        return ListViewWidget(
            data_list=data,
            create_item_callback=lambda data: create_item_widget(user_unique_id, data, refresh_callback=_refresh_view),
            filter_callback=lambda search_str, data: search_str in data['name'],
        )

    def _refresh_view(*args):
        left_widget.toggle_to(_make_view())

    left_widget = ToggleWidget(
        widget=_make_view()
    )
    right_widget = VBoxLayout(
        childs=[
            Button(
                icon='plus',
                func=lambda *args: create_create_weights_sgt_model_window(
                    user_unique_id,
                    _refresh_view,
                ),
            ),
        ],
        margins=2,
        spacing=2,
        align='top'
    )
    w = HBoxLayout(
        childs=[
            left_widget,
            right_widget,
        ],
        margins=2,
        spacing=2,
    )

    return w
