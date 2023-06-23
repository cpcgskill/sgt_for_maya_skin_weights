# -*-coding:utf-8 -*-
"""
:创建时间: 2023/3/27 15:45
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:Github: https://github.com/cpcgskill
:QQ: 2921251087
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
:爱发电: https://afdian.net/@Phantom_of_the_Cang

为SGT模型创建了一系列用于窗口API函数。
这些窗口API函数可以创建、更新、运行、上传、删除和克隆SGT模型。
"""
from __future__ import unicode_literals, print_function, division

if False:
    from typing import *

from cpgui.pop_ups import confirm
from cpform.docker import dialog_docker, quit_dialog_docker

from sgtone.utils import *


# 创建网络的窗口的实现
def create_sgt_model(user_unique_id, name,
                     in_size, out_size,
                     client_data=None,
                     is_public=False,
                     callback=None):
    if client_data is None:
        client_data = dict()

    def _success_callback_func(*args):
        quit_dialog_docker()
        if callable(callback):
            callback()
        # return success_label_widget()

    dialog_docker(
        title='creating model: {}'.format(name),
        form=http_json_api_widget(
            url='/public/create_sgt_model',
            json_object={
                'auth_token': user_unique_id,
                'name': name,
                'client_data': client_data,
                'in_size': in_size,
                'out_size': out_size,
                'is_public': is_public,
            },
            success_call=_success_callback_func,
        ),
    )


def update_sgt_model_client_data(user_unique_id, sgt_model_name, client_data, callback=None):
    def _success_call(header, data):
        quit_dialog_docker()
        if callable(callback):
            callback()
        # return success_label_widget()

    dialog_docker(
        title='update sgt model client data',
        form=http_json_api_widget(
            url='/public/update_sgt_model_client_data',
            json_object={
                'auth_token': user_unique_id,
                'name': sgt_model_name,
                'client_data': client_data,
            },
            success_call=_success_call,
        ),
    )


def run_sgt_model(user_unique_id, name, run_data, callback=None):
    """

    :param user_unique_id:
    :param name:
    :param run_data:
    :type callback: (List[Tuple[float]]) -> Any
    :return:
    """

    def _http_end_callback(headers, data):
        quit_dialog_docker()
        if callable(callback):
            callback(data)

    dialog_docker(
        title='running model: {}'.format(name),
        form=http_json_api_widget(
            url='/public/run_sgt_model',
            json_object={
                'auth_token': user_unique_id,
                'name': name,
                'data': run_data,
            },
            success_call=_http_end_callback,
        ),
    )


def upload_sgt_model_train_data(user_unique_id, name, train_data, callback=None):
    def _http_end_callback(headers, data):
        quit_dialog_docker()
        if callable(callback):
            callback()

    dialog_docker(
        title='uploading model data: {}'.format(name),
        form=http_json_api_widget(
            url='/public/upload_sgt_model_train_data',
            json_object={
                'auth_token': user_unique_id,
                'name': name,
                'train_data': train_data,
            },
            success_call=_http_end_callback,
        ),
    )


def delete_sgt_model(
        user_unique_id,
        name,
        need_to_request_confirmation=True,
        callback=None
):
    if need_to_request_confirmation:
        if not confirm('是否删除模型'):
            return

    def _success_call(header, data):
        quit_dialog_docker()
        if callable(callback):
            callback()
        # return success_label_widget()

    dialog_docker(
        title='delete model: {}'.format(name),
        form=http_json_api_widget(
            url='/public/delete_sgt_model',
            json_object={
                'auth_token': user_unique_id,
                'name': name,
            },
            success_call=_success_call,
        ),
    )


def clone_sgt_model_to_mine(user_unique_id, new_name, author_unique_id, name, callback=None):
    def _success_call(header, data):
        quit_dialog_docker()
        if callable(callback):
            callback()
        # return success_label_widget()

    dialog_docker(
        title='clone model: {}'.format(new_name),
        form=http_json_api_widget(
            url='/public/clone_sgt_model_to_mine',
            json_object={
                'auth_token': user_unique_id,
                'new_name': new_name,
                'author_unique_id': author_unique_id,
                'name': name,
            },
            success_call=_success_call,
        ),
    )


def read_my_sgt_model(user_unique_id):
    state = dict()

    def _success_call(headers, body):
        state['data'] = body
        quit_dialog_docker()

    dialog_docker(
        title='read my sgt model',
        form=http_json_api_widget(
            url='/public/read_my_sgt_model',
            json_object={
                "auth_token": user_unique_id,
            },
            success_call=_success_call,
        ),
    )
    return [i for i in state['data']]


def read_public_sgt_model(user_unique_id):
    state = dict()

    def _success_call(headers, body):
        state['data'] = body
        quit_dialog_docker()

    dialog_docker(
        title='read public sgt model',
        form=http_json_api_widget(
            url='/public/read_public_sgt_model',
            json_object={
                "auth_token": user_unique_id,
            },
            success_call=_success_call,
        ),
    )
    return [i for i in state['data']]


def check_auth_token(auth_token):
    state = dict()

    def _success_call(headers, body):
        state['data'] = body
        quit_dialog_docker()

    dialog_docker(
        title='check auth token',
        form=http_json_api_widget(
            url='/public/check_auth_token',
            json_object={
                'auth_token': auth_token,
            },
            success_call=_success_call
        ),
    )
    return state['data']


__all__ = [
    'create_sgt_model',
    'update_sgt_model_client_data',
    'run_sgt_model',
    'upload_sgt_model_train_data',
    'delete_sgt_model',
    'clone_sgt_model_to_mine',
    'read_my_sgt_model',
    'read_public_sgt_model',
    'check_auth_token',
]
