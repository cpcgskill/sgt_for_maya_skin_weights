# -*-coding:utf-8 -*-
"""
:创建时间: 2023/11/26 19:37
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

from sgt.core import App


class AppApi(object):
    def __init__(self, app_title, app_name):
        self.app_title = app_title
        self.app = App(app_name)

    def login(self, secret_id, secret_key):
        self.app.login(secret_id, secret_key)

    def logout(self):
        self.app.logout()

    def create(self, refresh_view_callback=None):
        pass

    def run(self, model):
        pass

    def upload_train_data(self, model):
        pass


__all__ = ["AppApi"]