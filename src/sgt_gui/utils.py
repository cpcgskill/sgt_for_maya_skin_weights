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

import json
import os
import sys
from collections import namedtuple

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

from cpform.docker import default_docker, dialog_docker, close_docker, quit_dialog_docker
from cpform.widget.all import *


def mydocker(name='CPWindow', title=None, form=None):
    default_docker(
        name=name,
        title=title,
        form=Background(child=form, color='#444444'),
        size=(800, 600),
    )


class SelectButton(QAbstractButton):
    color = QColor(0, 0, 0, 0)

    def __init__(self, text, callback=None):
        super(SelectButton, self).__init__()
        self.setText(text)
        self.setAutoExclusive(True)
        self.setCheckable(True)
        self.setMinimumWidth(140)
        self.setMinimumHeight(40)
        if callback is not None:
            self.clicked.connect(lambda *args: callback() if self.isChecked() else None)

    def enterEvent(self, *args, **kwargs):
        super(SelectButton, self).enterEvent(*args, **kwargs)
        self.color = QColor(0, 0, 0, 15)
        self.update()

    def leaveEvent(self, *args, **kwargs):
        super(SelectButton, self).leaveEvent(*args, **kwargs)
        self.color = QColor(0, 0, 0, 0)
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setPen(Qt.NoPen)
        color = self.color
        if self.isDown():
            color = QColor(0, 0, 0, 25)
        if self.isChecked():
            color = QColor(0, 0, 0, 50)
        p.setBrush(QBrush(color))
        p.drawRect(self.rect())

        p.setPen(QPen(QColor("#fff"), 2))
        if self.isDown():
            font = p.font()
            if font.pixelSize() > 0:
                font.setPixelSize(font.pixelSize() * 0.95)
                p.setFont(font)
        if self.isChecked():
            font = p.font()
            if font.pixelSize() > 0:
                font.setPixelSize(font.pixelSize() * 1.15)
                p.setFont(font)
            p.setPen(QPen(QColor("#00aaff"), 2))

        p.drawText(self.rect(), Qt.AlignCenter, self.text())

        if self.isChecked():
            p.setPen(QPen(QColor("#00aaff"), 4))
            p.drawLine(QPoint(2, 0), QPoint(2, self.height()))

        p.end()


def create_tab_group_widget(tab_config, default, head=None, end=None):
    """

    :type tab_config: List[Tuple[AnyStr, ()->Widget]]
    :type default: AnyStr
    :type head: Widget
    :type end: Widget
    :return:
    """
    view = ToggleWidget(Widget())

    def create_button(k, f):
        bn = SelectButton(k, lambda: view.toggle_to(f()))
        if k == default:
            bn.click()
        return bn

    v_childs = []
    if head is not None:
        v_childs.append(head)
    v_childs.append(VBoxLayout(
        childs=[create_button(k, f) for k, f in tab_config],
        align='top',
        margins=0,
        spacing=0,
    ))
    if end is not None:
        v_childs.append(end)

    return HBoxLayout(
        childs=[
            VBoxLayout(
                childs=v_childs,
                margins=0,
                spacing=0,
            ),
            view,
        ],
        margins=0,
        spacing=0,
    )


class ListViewWidget(WarpWidget):
    def __init__(self, data_list, create_item_callback, filter_callback=None):
        """

        :type data_list: Iterable[Any]
        :type create_item_callback: (Any)->Widget
        :type filter_callback: (AnyStr, Any)->bool
        """
        self.data_list = list(data_list)
        self.create_item_callback = create_item_callback
        self.filter_callback = lambda search_str, data: True if filter_callback is None else filter_callback(search_str, data)

        self._search_widget = LineEditWidget(
            return_pressed_callback=self._update_view,
            placeholder_text='输入关键字回车',
        )
        self._view = ToggleWidget()

        widget = VBoxLayout(childs=[self._search_widget, self._view], margins=0, spacing=0)
        super(ListViewWidget, self).__init__(child=widget)

        self._update_view()

    def set_data_list(self, data_list):
        self.data_list = data_list
        self._update_view()

    def _update_view(self):
        search_str = self._search_widget.get_text()
        widget = VBoxLayout(
            childs=[
                Background(self.create_item_callback(data), color='#303030')
                for data in self.data_list
                if self.filter_callback(search_str, data)
            ],
            margins=2,
            spacing=2,
            align='top',
        )
        widget = ScrollAreaWidget(widget=widget)
        widget = BackgroundWidget(child=widget, color='#323232')
        self._view.toggle_to(widget)


class ComboBoxWidget(ListViewWidget):
    def __init__(self, *actions):
        """

        :type actions: Tuple[AnyStr, AnyStr, Any]
        """
        super(ComboBoxWidget, self).__init__(data_list=actions, create_item_callback=lambda data: LabelWidget(data[0]))


class _SelectDialogCtx(object):
    is_select = False
    this_data = None


def create_select_dialog(option_list):
    """

    :type option_list: Iterable[AnyStr]
    :return:
    """

    ctx = _SelectDialogCtx()

    def _create_item_callback(data):
        def _callback():
            ctx.this_data = data
            ctx.is_select = True
            quit_dialog_docker()

        return ButtonWidget(data, func=_callback)

    dialog_docker(
        title='select',
        form=ListViewWidget(
            data_list=option_list,
            create_item_callback=_create_item_callback,
            filter_callback=lambda search_str, data: search_str in data,
        ),
    )
    if ctx.is_select:
        return ctx.this_data
    else:
        return None



def create_add_template_window(model, template):
    # type: (App, Dict)->None
    client_data = model.client_data
    name_to_template_table = {i['name']: i for i in client_data.get('templates', [])}
    name_to_template_table[template['name']] = template
    client_data['templates'] = list(name_to_template_table.values())
    model.update_client_data(client_data)


def create_delete_template_window(model, template):
    # type: (App, Dict)->None
    client_data = model.client_data
    name_to_template_table = {i['name']: i for i in client_data.get('templates', [])}
    name_to_template_table.pop(template['name'])
    client_data['templates'] = list(name_to_template_table.values())

    model.update_client_data(client_data)


def create_select_template_dialog(model):
    # type: (App)->Dict
    client_data = model.client_data

    name_to_template_table = {i['name']: i for i in client_data.get('templates', [])}

    selected = create_select_dialog(name_to_template_table.keys())
    if selected is None:
        return None
    else:
        return name_to_template_table[selected]

__all__ = [
    'mydocker',
    'create_tab_group_widget',
    'ListViewWidget',
    'ComboBoxWidget',
    'create_select_dialog',
    'create_add_template_window',
    'create_delete_template_window',
    'create_select_template_dialog',
]
