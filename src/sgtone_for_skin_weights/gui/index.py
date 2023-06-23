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

import json
import os
import sys

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

from cpgui.pop_ups import confirm

import cpmel.cmds as cc

from cpform.docker import default_docker
from cpform.widget.all import *

import simpledb

from sgtone.core import *

from sgtone_for_skin_weights.gui.utils import *
from sgtone_for_skin_weights.gui.my import create_my_sgt_model_widget
from sgtone_for_skin_weights.gui.public import create_public_sgt_model_widget

db = simpledb.new('index')


# 主要部件的实现
def create_main_widget(user_unique_id):
    def _logout():
        if confirm(message='要登出吗？'):
            db.set('auth_token', None)
            create_main_window()

    return create_tab_group_widget(
        tab_config=[
            ('My', lambda: create_my_sgt_model_widget(user_unique_id)),
            ('Public', lambda: create_public_sgt_model_widget(user_unique_id)),
        ],
        default='My',
        end=VBoxLayout(childs=[Button(icon='log-out', func=lambda *args: _logout())], margins=10, align='bottom'),
    )


# 权限验证部分实现
def create_need_auth_token_widget():
    line_edit = LineEdit(is_encrypt=True)

    def _push_auth_token():
        db.set('auth_token', line_edit.read_data()[0])
        create_main_window()

    return VBoxLayout(
        childs=[
            Label('需要授权密钥'),
            line_edit,
            Button('Push', func=_push_auth_token, icon='log-in'),
        ],
        align='top',
    )


def create_need_auth_token_widget_or_main_widget(auth_token):
    if auth_token is None:
        return create_need_auth_token_widget()
    if check_auth_token(auth_token):
        return create_main_widget(auth_token)
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
    auth_token = db.get('auth_token', _default=None)

    mydocker(
        name='SgtoneForSkinWeights',
        title='SgtoneForSkinWeights',
        form=create_need_auth_token_widget_or_main_widget(auth_token),
    )
