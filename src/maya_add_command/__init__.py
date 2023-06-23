# -*-coding:utf-8 -*-
u"""
:创建时间: 2022/1/5 3:28
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:QQ: 2921251087
:爱发电: https://afdian.net/@Phantom_of_the_Cang
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127

"""
from __future__ import unicode_literals, print_function
import os
import sys
import uuid
import maya.cmds as mc

PATH = os.path.dirname(os.path.abspath(__file__))
PLUG_PATH = os.sep.join((PATH, "mel_doit.py"))
PLUG_NAME = u"mel_doit_{}".format(str(hash(PLUG_PATH)).replace(u"-", u"_"))
command_name = u'mel_doit_' + uuid.uuid4().hex
is_init = False


def init_maya_add_command():
    global is_init
    if not is_init:
        sys.mel_doit_command_name = command_name
        try:
            mc.loadPlugin(PLUG_PATH, n=PLUG_NAME)
        except:
            pass
        finally:
            is_init = True
            del sys.mel_doit_command_name


def _write_undo_queue(redo, undo):
    if callable(redo) and callable(undo):
        try:
            getattr(mc, command_name)(doIt=id(redo), undoIt=id(undo))
        except Exception as ex:
            raise RuntimeError(u"Add command error")
        return
    else:
        raise RuntimeError(u"redo or undo are non-executable objects")


class UndoQueueItem(object):
    def __init__(self, redo, undo):
        self._read = redo
        self._undo = undo

    def read(self):
        self._read()

    def undo(self):
        self._undo()


def write_undo_queue(redo, undo):
    if callable(redo) and callable(undo):
        i = UndoQueueItem(redo, undo)
        _write_undo_queue(i.read, i.undo)
    else:
        raise RuntimeError(u"redo or undo are non-executable objects")


def add_command(do, redo, undo):
    if callable(do) and callable(redo) and callable(undo):
        do()
        write_undo_queue(redo, undo)
    else:
        raise RuntimeError(u"redo are non-executable objects")
