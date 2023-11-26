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

from sgt.utils import *


# 创建网络的窗口的实现
def create_sgt_model(secret,
                     name,
                     app_name,
                     model_type,
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
                'secret_id': secret['secret_id'],
                'secret_key': secret['secret_key'],
                'name': name,
                'app_name': app_name,
                'model_type': model_type,
                'client_data': client_data,
                'in_size': in_size,
                'out_size': out_size,
                'is_public': is_public,
            },
            success_call=_success_callback_func,
        ),
    )


def update_sgt_model_client_data(secret, sgt_model_name, app_name, model_type, client_data, callback=None):
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
                'secret_id': secret['secret_id'],
                'secret_key': secret['secret_key'],
                'name': sgt_model_name,
                'app_name': app_name,
                'model_type': model_type,
                'client_data': client_data,
            },
            success_call=_success_call,
        ),
    )


def run_sgt_model(secret, name, app_name, model_type, run_data, callback=None):
    """

    :param secret:
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
                'secret_id': secret['secret_id'],
                'secret_key': secret['secret_key'],
                'name': name,
                'app_name': app_name,
                'model_type': model_type,
                'data': run_data,
            },
            success_call=_http_end_callback,
        ),
    )


def upload_sgt_model_train_data(secret, name, app_name, model_type, train_data, callback=None):
    def _http_end_callback(headers, data):
        quit_dialog_docker()
        if callable(callback):
            callback()

    dialog_docker(
        title='uploading model data: {}'.format(name),
        form=http_json_api_widget(
            url='/public/upload_sgt_model_train_data',
            json_object={
                'secret_id': secret['secret_id'],
                'secret_key': secret['secret_key'],
                'name': name,
                'app_name': app_name,
                'model_type': model_type,
                'train_data': train_data,
            },
            success_call=_http_end_callback,
        ),
    )


def delete_sgt_model(
        secret,
        name,
        app_name,
        model_type,
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
                'secret_id': secret['secret_id'],
                'secret_key': secret['secret_key'],
                'name': name,
                'app_name': app_name,
                'model_type': model_type,
            },
            success_call=_success_call,
        ),
    )


def clone_sgt_model_to_mine(secret, new_name, author_unique_id, name, app_name, callback=None):
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
                'secret_id': secret['secret_id'],
                'secret_key': secret['secret_key'],
                'new_name': new_name,
                'author_unique_id': author_unique_id,
                'name': name,
                'app_name': app_name,
            },
            success_call=_success_call,
        ),
    )


def read_my_sgt_model(secret, app_name=None):
    state = dict()

    def _success_call(headers, body):
        state['data'] = body
        quit_dialog_docker()

    dialog_docker(
        title='read my sgt model',
        form=http_json_api_widget(
            url='/public/read_my_sgt_model',
            json_object={
                'secret_id': secret['secret_id'],
                'secret_key': secret['secret_key'],
            },
            success_call=_success_call,
        ),
    )
    if app_name is None:
        return [i for i in state['data']]
    else:
        return [i for i in state['data'] if i['app_name'] == app_name]


def read_public_sgt_model(secret, app_name=None):
    state = dict()

    def _success_call(headers, body):
        state['data'] = body
        quit_dialog_docker()

    dialog_docker(
        title='read public sgt model',
        form=http_json_api_widget(
            url='/public/read_public_sgt_model',
            json_object={
                'secret_id': secret['secret_id'],
                'secret_key': secret['secret_key'],
            },
            success_call=_success_call,
        ),
    )
    if app_name is None:
        return [i for i in state['data']]
    else:
        return [i for i in state['data'] if i['app_name'] == app_name]


def check_auth_token(secret):
    state = dict()

    def _success_call(headers, body):
        state['data'] = body
        quit_dialog_docker()

    dialog_docker(
        title='check auth token',
        form=http_json_api_widget(
            url='/public/check_auth_token',
            json_object={
                'secret_id': secret['secret_id'],
                'secret_key': secret['secret_key'],
            },
            success_call=_success_call
        ),
    )
    return state['data']


class Model(object):
    def __init__(self, app, user_unique_id, name, model_type, in_size, out_size, client_data=None, is_public=False):
        self.app = app
        self.user_unique_id = user_unique_id
        self.name = name
        self.model_type = model_type
        self.in_size = in_size
        self.out_size = out_size
        self.client_data = client_data
        self.is_public = is_public

    def update_client_data(self, client_data, callback=None):
        update_sgt_model_client_data(
            secret=self.app.secret,
            sgt_model_name=self.name,
            app_name=self.app.app_name,
            model_type=self.model_type,
            client_data=client_data,
            callback=callback,
        )
        self.client_data = client_data
        return self

    def run(self, data, callback=None):
        run_sgt_model(
            secret=self.app.secret,
            name=self.name,
            app_name=self.app.app_name,
            model_type=self.model_type,
            run_data=data,
            callback=callback,
        )
        return self

    def upload_train_data(self, train_data, callback=None):
        upload_sgt_model_train_data(
            secret=self.app.secret,
            name=self.name,
            app_name=self.app.app_name,
            model_type=self.model_type,
            train_data=train_data,
            callback=callback,
        )
        return self

    def delete(self, callback=None):
        delete_sgt_model(
            secret=self.app.secret,
            name=self.name,
            app_name=self.app.app_name,
            model_type=self.model_type,
            need_to_request_confirmation=False,
            callback=callback,
        )
        return self


class App(object):
    def __init__(self, app_name, secret=None):
        self.secret = secret
        self.app_name = app_name

    def login(self, secret_id, secret_key):
        self.secret = {
            'secret_id': secret_id,
            'secret_key': secret_key,
        }
        return self

    def logout(self):
        self.secret = None
        return self


    def check_auth_token(self):
        return check_auth_token(self.secret)

    def create_sgt_model(self, name, model_type, in_size, out_size, client_data=None, is_public=False, callback=None):
        create_sgt_model(
            secret=self.secret,
            name=name,
            app_name=self.app_name,
            model_type=model_type,
            in_size=in_size,
            out_size=out_size,
            client_data=client_data,
            is_public=is_public,
            callback=callback,
        )
        return Model(self, name, model_type, in_size, out_size, client_data, is_public)

    def read_my_sgt_model(self):
        datas = read_my_sgt_model(self.secret, self.app_name)
        return [
            Model(
                app=self,
                user_unique_id=i['user_unique_id'],
                name=i['name'],
                model_type=i['model_type'],
                in_size=i['in_size'],
                out_size=i['out_size'],
                client_data=i['client_data'],
                is_public=i['is_public'],
            )
            for i in datas
        ]
    def read_public_sgt_model(self):
        datas = read_public_sgt_model(self.secret, self.app_name)
        return [
            Model(
                app=self,
                user_unique_id=i['user_unique_id'],
                name=i['name'],
                model_type=i['model_type'],
                in_size=i['in_size'],
                out_size=i['out_size'],
                client_data=i['client_data'],
                is_public=i['is_public'],
            )
            for i in datas
        ]

    def clone_sgt_model_to_mine(self, public_model, new_name, callback=None):
        clone_sgt_model_to_mine(
            secret=self.secret,
            new_name=new_name,
            author_unique_id=public_model.user_unique_id,
            name=public_model.name,
            app_name=public_model.app.app_name,
            callback=callback,
        )

__all__ = [
    'Model',
    'App'
]
