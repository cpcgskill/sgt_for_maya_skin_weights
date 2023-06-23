#!/usr/bin/python
# -*-coding:utf-8 -*-
u"""
:创建时间: 2021/9/20 13:31
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:QQ: 2921251087
:爱发电: https://afdian.net/@Phantom_of_the_Cang
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127

"""
from __future__ import (nested_scopes, generators,
                        division, absolute_import,
                        with_statement, print_function,
                        unicode_literals)
from cpgui.std_imp import *


def get_file_name():
    """
    获得文件路径

    :return: unicode is None
    """
    path = QFileDialog.getOpenFileName()
    if len(path) < 3:
        return None
    return path


def get_directory_name():
    """
    获得文件夹路径

    :return: unicode is None
    """
    path = QFileDialog.getExistingDirectory()
    if len(path) < 3:
        return None
    return path


def input_text(title='输入', message=u'>>>', text=u''):
    """
    创建一个接受字符串输入的输入框

    :param title: 标题
    :param message: 消息
    :param text: 默认参数
    :return: unicode is None
    """
    v, is_ok = QInputDialog.getText(mui, title, message, QLineEdit.Normal, text)
    if is_ok:
        return v
    return None


def input_int(title='输入', message=u'>>>', text=0):
    """
    创建一个接受整数输入的输入框

    :param title: 标题
    :param message: 消息
    :param text: 默认参数
    :return: unicode is None
    """
    v, is_ok = QInputDialog.getInt(mui, title, message, text)
    if is_ok:
        return v
    return None


def input_double(title='输入', message=u'>>>', text=0.0):
    """
    创建一个接受浮点输入的输入框

    :param title: 标题
    :param message: 消息
    :param text: 默认参数
    :return: unicode is None
    """
    v, is_ok = QInputDialog.getDouble(mui, title, message, text)
    if is_ok:
        return v
    return None


def input_float(title='输入', message=u'>>>', text=0.0):
    """
    创建一个接受浮点输入的输入框

    :param title: 标题
    :param message: 消息
    :param text: 默认参数
    :return: unicode is None
    """
    return input_double(title, message, text)


class _InputMultipleText(QDialog):
    def __init__(self, title=u'输入', message=u'>>>', text=u''):
        super(_InputMultipleText, self).__init__(mui)
        self._is_ok = False

        self.setWindowTitle(title)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(QLabel(message))
        self.text = QTextEdit()
        self.text.setPlainText(text)
        self.main_layout.addWidget(self.text)

        self.f_layout = QHBoxLayout()
        self.f_layout.addStretch(0)
        self._ok_bn = QPushButton(u"确认")
        self._close_bn = QPushButton(u"取消")
        self._ok_bn.clicked.connect(lambda *args: self.ok())
        self._close_bn.clicked.connect(lambda *args: self.close())
        self.f_layout.addWidget(self._ok_bn)
        self.f_layout.addWidget(self._close_bn)

        self.main_layout.addLayout(self.f_layout)

    def ok(self):
        self._is_ok = True
        self.close()

    def res(self):
        if self._is_ok:
            return self.text.toPlainText(), True
        else:
            return "", False


def input_multiLine_text(title='输入', message=u'>>>', text=u''):
    """
    创建一个接受字符串输入的多行输入框

    :param title: 标题
    :param message: 消息
    :param text: 默认参数
    :return: unicode is None
    """
    w = _InputMultipleText(title, message, text)
    w.exec_()
    v, ok = w.res()
    if ok:
        return v
    else:
        return None


def confirm(title='确认', message=u''):
    """
    确认对话框

    :param title: 标题
    :param message: 消息
    :return: bool
    """
    reply = QMessageBox.question(mui, title, message, QMessageBox.Yes, QMessageBox.No)
    if reply == QMessageBox.StandardButton.No:
        return False
    else:
        return True
