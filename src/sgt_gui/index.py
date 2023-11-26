# -*-coding:utf-8 -*-
"""
:创建时间: 2023/11/26 19:33
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

import functools

if False:
    from typing import *
try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
except ImportError:
    try:
        from PySide2.QtGui import *
        from PySide2.QtCore import *
        from PySide2.QtWidgets import *
    except ImportError:
        from PySide.QtGui import *
        from PySide.QtCore import *

try:
    from shiboken2 import *
except ImportError:
    from shiboken import *

from cpgui.pop_ups import confirm, input_text

from cpform.widget.all import *

import simpledb

from sgt_gui.app_api import AppApi
from sgt.core import Model, App
from sgt_gui.utils import *

db = simpledb.new('index')

app_list = []


def create_my_item_widget(app_api, model, refresh_callback=None):
    # type: (AppApi, Model, Callable) -> QWidget
    app = app_api.app
    widget = VBoxLayout(
        childs=[
            Label(
                model.name,
                font_size=16,
            ),
            Label(
                "inpout {} output {}".format(model.in_size, model.out_size),
                font_size=12,
            ),
        ],
    )

    def _create_clone_sgt_model_to_mine_window(*args):
        my_name = input_text(title='your name', text=model.name)
        if my_name is None:
            return
        app.clone_sgt_model_to_mine(model, my_name, callback=refresh_callback)

    widget = HBoxLayout(childs=[
        widget,
        Button(
            icon='play',
            func=lambda *args: app_api.run(model),
            fixed_width=35, fixed_height=35
        ),
        Button(
            icon='upload',
            func=lambda *args: app_api.upload_train_data(model),
            fixed_width=35, fixed_height=35
        ),
        Button(
            icon='delete',
            func=lambda *args: model.delete(callback=lambda: widget.close()) if confirm(message='要删除吗？') else None,
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


def create_public_item_widget(app, model, refresh_callback=None):
    # type: (App, Model, Callable) -> QWidget
    widget = VBoxLayout(
        childs=[
            Label(
                model.name,
                font_size=16,
            ),
            Label(
                "inpout {} output {}".format(model.in_size, model.out_size),
                font_size=12,
            ),
        ],
    )

    def _create_clone_sgt_model_to_mine_window(*args):
        my_name = input_text(title='your name', text=model.name)
        if my_name is None:
            return
        app.clone_sgt_model_to_mine(model, my_name, callback=refresh_callback)

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
def create_public_sgt_model_widget(app_api):
    # type: (AppApi) -> QWidget
    app = app_api.app
    def _make_view():
        model_list = app.read_public_sgt_model()
        return ListViewWidget(
            data_list=model_list,
            create_item_callback=lambda model: create_public_item_widget(app, model, refresh_callback=_refresh_view),
            filter_callback=lambda search_str, model: search_str in model.name,
        )

    def _refresh_view(*args):
        widget.toggle_to(_make_view())

    widget = ToggleWidget(
        widget=_make_view()
    )
    return mydocker(
        name='Hub',
        title='Hub: {}'.format(app_api.app_title),
        form=widget,
    )


def warp_app(app_api):
    # type: (AppApi) -> None
    def _make_view():
        model_list = app_api.app.read_my_sgt_model()
        return ListViewWidget(
            data_list=model_list,
            create_item_callback=lambda model: create_my_item_widget(app_api, model, refresh_callback=_refresh_view),
            filter_callback=lambda search_str, model: search_str in model.name,
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
                func=lambda *args: app_api.create(refresh_view_callback=_refresh_view),
            ),
            Button(
                icon='box',
                func=functools.partial(create_public_sgt_model_widget, app_api),
            ),
            Button(
                icon='refresh-cw',
                func=_refresh_view,
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


# 主要部件的实现
def create_main_widget(secret):
    def _logout():
        if confirm(message='要登出吗？'):
            db.set('secret', None)
            for i in app_list:
                i.logout()
            create_main_window()

    return create_tab_group_widget(
        tab_config=[
            (i.app_title, functools.partial(warp_app, i))
            for i in app_list
        ],
        default='SkinWeights',
        end=VBoxLayout(childs=[Button(icon='log-out', func=lambda *args: _logout())], margins=10, align='bottom'),
    )


# 权限验证部分实现
def create_need_auth_token_widget():
    secret_id_line_edit = LineEdit()
    secret_key_line_edit = LineEdit(is_encrypt=True)

    def _push_auth_token():
        secret = {
            'secret_id': secret_id_line_edit.read_data()[0],
            'secret_key': secret_key_line_edit.read_data()[0],
        }
        db.set('secret', secret)
        for i in app_list:
            i.login(**secret)
        create_main_window()

    return VBoxLayout(
        childs=[
            Label('需要授权密钥'),
            FormLayout(
                childs=[
                    'Secret id', secret_id_line_edit,
                    'Secret key', secret_key_line_edit,
                ],
            ),
            Button('Push', func=_push_auth_token, icon='log-in'),
        ],
        align='center',
    )


def create_need_auth_token_widget_or_main_widget(secret):
    if secret is None:
        return create_need_auth_token_widget()
    for i in app_list:
        i.login(**secret)
    if all(i.app.check_auth_token() for i in app_list):
        return create_main_widget(secret)
    else:
        return VBoxLayout(
            childs=[
                create_need_auth_token_widget(),
                VBoxLayout(
                    childs=[BackgroundWidget(LabelWidget('无效的授权密钥'), color='#c94f4f')],
                    align='bottom',
                    spacing=0,
                    margins=0,
                ),
            ],
            spacing=0,
            margins=0,
        )


def create_main_window():
    secret = db.get('secret', _default=None)

    mydocker(
        name='SGT',
        title='SGT',
        form=create_need_auth_token_widget_or_main_widget(secret),
    )
