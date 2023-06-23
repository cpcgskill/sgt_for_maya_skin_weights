# -*-coding:utf-8 -*-
"""
:创建时间: 2023/3/9 12:35
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
import json
import os

from cpgui.std_imp import *

from cpform.widget.all import *

# default_url_root = r'http://127.0.0.1:8000/sgtone'
default_url_root = r'https://self-growth-toolchain.api.cpcgskill.com/sgtone'

loading_gif = os.path.dirname(os.path.abspath(__file__))
loading_gif = os.sep.join([loading_gif, 'loading.gif'])


def error_label_widget(title, msg):
    """错误标签"""

    def _copy_msg():
        QApplication.clipboard().setText(msg)

    return VBoxLayout(
        childs=[
            Label('{}: <p style="color: red">{}</p>'.format(title, msg), word_wrap=True),
            Button('复制错误信息', func=_copy_msg)
        ],
        margins=30,
        align='center',
    )


def success_label_widget():
    return VBoxLayout(childs=[Label('Success')], align='center')


class DoingWidget(Warp):
    def __init__(self):
        self.loading_label = QLabel()
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setFixedSize(QSize(120, 120))

        self.movie = QMovie(self.loading_label)
        self.movie.setFileName(loading_gif)
        self.movie.setScaledSize(QSize(120, 120))
        self.movie.start()
        self.loading_label.setMovie(self.movie)
        super(DoingWidget, self).__init__(VBoxLayout(
            childs=[self.loading_label],
            margins=60,
            align='center',
        ))

    def read_data(self):
        return []


def http_json_api_widget(url, headers=None, json_object=None, success_call=None, ):
    """

    :type url: AnyStr
    :type headers: Dict[AnyStr, AnyStr]
    :type json_object: object
    :type success_call: (Dict[AnyStr, AnyStr], bytes) -> Widget or None
    :rtype: Widget
    """
    if headers is None:
        headers = {'Content-Type': 'application/json'}
    else:
        new_headers = {'Content-Type': 'application/json'}
        for k, v in headers.items():
            new_headers[k] = v
    if json_object is None:
        json_object = dict()

    def _success_call(status_code, headers, body):
        if status_code == 200:
            widget.toggle_to(success_label_widget())
            if callable(success_call):
                success_widget = success_call(headers, json.loads(body))
                if isinstance(success_widget, Widget):
                    widget.toggle_to(success_widget)
        elif status_code == 400:
            error = json.loads(body)
            widget.toggle_to(error_label_widget(
                '异常',
                "{}({})".format(error['exception'], repr(error['message']))
            ))
        else:
            widget.toggle_to(error_label_widget('未知的异常', repr(body)))

    def _fail_call(error):
        widget.toggle_to(error_label_widget('失败', error.__name__))

    widget = ToggleWidget(
        widget=HttpPost(
            child=DoingWidget(),
            url=os.getenv('sgtone_url_root', default_url_root) + url,
            headers=headers,
            body=json.dumps(json_object),
            success_call=_success_call,
            fail_call=_fail_call,
        )
    )
    return widget


__all__ = [
    'error_label_widget',
    'success_label_widget',
    'DoingWidget',
    'http_json_api_widget',
]
