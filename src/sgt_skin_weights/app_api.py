# -*-coding:utf-8 -*-
"""
:创建时间: 2023/11/26 19:49
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

from sgt_gui.app_api import AppApi
from sgt_skin_weights.gui import create_create_weights_sgt_model_window
from sgt_skin_weights.gui import create_run_weights_sgt_model_window, create_upload_weights_sgt_model_train_data_window


class SkinWeights(AppApi):
    def __init__(self):
        self.preconvolution = 3
        super(SkinWeights, self).__init__(
            app_title='SkinWeights',
            app_name='sgtone_for_skin_weights_v1_preconvolution_{}'.format(self.preconvolution),
        )

    def create(self, refresh_view_callback=None):
        create_create_weights_sgt_model_window(self.app, self.preconvolution, callback=refresh_view_callback)

    def run(self, model):
        create_run_weights_sgt_model_window(self.app, model, self.preconvolution)

    def upload_train_data(self, model):
        create_upload_weights_sgt_model_train_data_window(self.app, model, self.preconvolution)


app = SkinWeights()