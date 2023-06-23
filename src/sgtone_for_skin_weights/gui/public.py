# -*-coding:utf-8 -*-
"""
:创建时间: 2023/3/9 16:10
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
from cpform.widget.all import *

from sgtone.core import clone_sgt_model_to_mine, read_public_sgt_model

import sgtone_for_skin_weights.config
from sgtone_for_skin_weights.gui.utils import *


# WeightsNet列表视图部分实现

def create_item_widget(user_unique_id, i, refresh_callback=None):
    client_data = i['client_data']
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
            icon='copy',
            func=_create_clone_sgt_model_to_mine_window,
            fixed_width=35, fixed_height=35
        ),
    ])
    return widget


# 我的WeightsNet部件
def create_public_sgt_model_widget(user_unique_id):
    def _make_view():
        data = read_public_sgt_model(user_unique_id)
        data = [i for i in data if i['client_data']['model_type'] == sgtone_for_skin_weights.config.model_type]
        return ListViewWidget(
            data_list=data,
            create_item_callback=lambda data: create_item_widget(user_unique_id, data, refresh_callback=_refresh_view),
            filter_callback=lambda search_str, data: search_str in data['name'],
        )

    def _refresh_view(*args):
        widget.toggle_to(_make_view())

    widget = ToggleWidget(
        widget=_make_view()
    )
    return widget
