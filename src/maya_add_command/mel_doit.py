#!/usr/bin/python
# -*-coding:utf-8 -*-
u"""
:创建时间: 2020/5/18 23:57
:作者: 苍之幻灵
:我的主页: https://cpcgskill.com
:QQ: 2921251087
:爱发电: https://afdian.net/@Phantom_of_the_Cang
:aboutcg: https://www.aboutcg.org/teacher/54335
:bilibili: https://space.bilibili.com/351598127
"""
from __future__ import unicode_literals, print_function

import maya.api.OpenMaya as om
import sys
import uuid
import ctypes

maya_useNewAPI = True


def to_int(i):
    if sys.version_info.major >= 3:
        return int(i)
    else:
        return long(i)


class MeldoIt(om.MPxCommand):
    doIt_label = "d"
    undoIt_label = "ud"
    doIt_label_long = "doIt"
    undoIt_label_long = "undoIt"
    # is_copy = True

    doIt_def = False
    undoIt_def = False

    def __init__(self):
        om.MPxCommand.__init__(self)

    def doIt(self, args):
        arg_data = om.MArgDatabase(syntax_creator(), args)
        if arg_data.isFlagSet(self.doIt_label_long) and arg_data.isFlagSet(self.undoIt_label_long):
            doIt_id = to_int(arg_data.flagArgumentString(self.doIt_label_long, 0))
            undoIt_id = to_int(arg_data.flagArgumentString(self.undoIt_label_long, 0))
            self.doIt_def = ctypes.cast(doIt_id, ctypes.py_object).value
            self.undoIt_def = ctypes.cast(undoIt_id, ctypes.py_object).value
        else:
            om.MGlobal.displayError('No doItComm and undoItComm')
            return

    def redoIt(self):
        if self.doIt_def and self.undoIt_def:
            self.doIt_def()
        else:
            om.MGlobal.displayError('No doItComm and undoItComm')
            return

    def undoIt(self):
        if self.doIt_def and self.undoIt_def:
            self.undoIt_def()
        else:
            om.MGlobal.displayError('No doItComm and undoItComm')
            return

    def isUndoable(self):
        return True


def cmd_creator():
    return MeldoIt()


def syntax_creator():
    syntax = om.MSyntax()
    syntax.addFlag(MeldoIt.doIt_label, MeldoIt.doIt_label_long, syntax.kString)
    syntax.addFlag(MeldoIt.undoIt_label, MeldoIt.undoIt_label_long, syntax.kString)
    return syntax


command_name = None


def initializePlugin(mobject):
    global command_name
    if not hasattr(sys, "mel_doit_command_name"):
        raise RuntimeError("Cannot find command name context")
    command_name = sys.mel_doit_command_name
    mplugin = om.MFnPlugin(mobject, "Phantom of the Cang", "0.1")
    try:
        mplugin.registerCommand(command_name, cmd_creator, syntax_creator)
    except:
        raise RuntimeError("Failed to register command")


def uninitializePlugin(mobject):
    global command_name
    mplugin = om.MFnPlugin(mobject)
    try:
        if command_name is not None:
            mplugin.deregisterCommand(command_name)
    except:
        raise RuntimeError("Failed to unregister command")
